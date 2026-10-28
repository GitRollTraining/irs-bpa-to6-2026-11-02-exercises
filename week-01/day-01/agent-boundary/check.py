"""The done check for this exercise. From lab/, run: python3 ../check.py

It reads the coding agents' configuration files in lab/ (Claude Code's .claude/settings.json and
.mcp.json, Codex's .codex/config.toml). It starts no agent, calls no model and needs no network.

Until a change of yours to one of those files is committed after the tag pilot-draft, it shows
nothing else, so that you decide first. Then, for each coding agent whose files you changed, it
says what they still let the agent reach or do that docs/pilot.md and the week 1 chapter's section
1.3 rule out, reading each setting as its tool's documentation describes it (read on 2026-10-28).
Last it looks for the sign-off at the end of docs/pilot.md, which it does not judge, and for
everything committed.
"""
import json
import pathlib
import re
import subprocess
import sys

try:
    import tomllib
except ImportError:  # Python 3.10, which has no tomllib: mini_toml below reads these files
    tomllib = None

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE / "lab"
DRAFT = "pilot-draft"
CLAUDE = (".claude/settings.json", ".mcp.json")
CODEX = (".codex/config.toml",)
FACTS = "docs/pilot.md"
SIGN_OFF = "Who must agree before the agent runs here:"
CASE_SYSTEM = ("case-files", "case-system")
READS_AND_TESTS = ("python3 -m pytest", "python -m pytest", "pytest", "git status", "git diff", "git log",
                   "git show", "ls", "cat", "head", "tail", "wc", "grep", "rg", "pwd")
EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
CC = "https://code.claude.com/docs/en/"
CX = "https://learn.chatgpt.com/docs/"


# --- Reading the files -------------------------------------------------------------------------

def mini_toml(text):
    """A small TOML reader for Pythons without tomllib: tables, dotted and quoted keys, strings,
    booleans, numbers, arrays and inline tables, which is all these configuration files need."""
    pos = 0
    root = {}
    bare = re.compile(r"[A-Za-z0-9_-]+")
    scalar = re.compile(r"(true|false)(?![A-Za-z0-9_])|[+-]?\d[\d_]*(\.\d+)?")

    def error(message):
        raise ValueError(f"line {text.count(chr(10), 0, pos) + 1}: {message}")

    def at(chars):
        return pos < len(text) and text[pos] in chars

    def skip(newlines):
        nonlocal pos
        while pos < len(text):
            if text[pos] in " \t" or (newlines and text[pos] in "\r\n"):
                pos += 1
            elif text[pos] == "#":
                while pos < len(text) and text[pos] != "\n":
                    pos += 1
            else:
                return

    def string():
        nonlocal pos
        quote = text[pos]
        if text.startswith(quote * 3, pos):
            error("a multi-line string is not read here")
        pos += 1
        out = []
        while pos < len(text) and text[pos] != quote:
            if text[pos] == "\n":
                error("a string must end on its own line")
            if quote == '"' and text[pos] == "\\":
                pos += 1
                out.append({"n": "\n", "t": "\t"}.get(text[pos:pos + 1], text[pos:pos + 1]))
            else:
                out.append(text[pos])
            pos += 1
        if pos >= len(text):
            error("a string is not closed")
        pos += 1
        return "".join(out)

    def key():
        nonlocal pos
        parts = []
        while True:
            skip(False)
            if at("\"'"):
                parts.append(string())
            else:
                found = bare.match(text, pos)
                if not found:
                    error("a key was expected")
                parts.append(found.group())
                pos = found.end()
            skip(False)
            if not at("."):
                return parts
            pos += 1

    def put(table, parts, value):
        for part in parts[:-1]:
            table = table.setdefault(part, {})
            if not isinstance(table, dict):
                error(f"{part} is not a table")
        if parts[-1] in table:
            error(f"{'.'.join(parts)} is set twice")
        table[parts[-1]] = value

    def value():
        nonlocal pos
        skip(False)
        if at("\"'"):
            return string()
        if at("["):
            pos += 1
            items = []
            while True:
                skip(True)
                if at("]"):
                    pos += 1
                    return items
                items.append(value())
                skip(True)
                if at(","):
                    pos += 1
                elif not at("]"):
                    error("an array must close with ]")
        if at("{"):
            pos += 1
            table = {}
            skip(False)
            if at("}"):
                pos += 1
                return table
            while True:
                parts = key()
                if not at("="):
                    error("= was expected")
                pos += 1
                put(table, parts, value())
                skip(False)
                if at(","):
                    pos += 1
                elif at("}"):
                    pos += 1
                    return table
                else:
                    error("an inline table must close with }")
        found = scalar.match(text, pos)
        if not found:
            error("a value was expected")
        pos = found.end()
        word = found.group().replace("_", "")
        if word in ("true", "false"):
            return word == "true"
        return float(word) if "." in word else int(word)

    current = root
    while True:
        skip(True)
        if pos >= len(text):
            return root
        if at("["):
            if text.startswith("[[", pos):
                error("an array of tables is not read here")
            pos += 1
            parts = key()
            if not at("]"):
                error("] was expected")
            pos += 1
            current = root
            for part in parts:
                current = current.setdefault(part, {})
                if not isinstance(current, dict):
                    error(f"{part} is not a table")
        else:
            parts = key()
            if not at("="):
                error("= was expected")
            pos += 1
            put(current, parts, value())
        skip(False)
        if pos < len(text) and not at("\r\n"):
            error("one key and its value to a line")


def read_toml(text):
    return tomllib.loads(text) if tomllib else mini_toml(text)


# --- What each coding agent's files let the agent reach or do ----------------------------------

def reaches_case_system(name, server):
    return any(part in name + " " + json.dumps(server) for part in CASE_SYSTEM)


def tool_of(rule):
    return rule.split("(", 1)[0].strip()


def specifier(rule):
    found = re.fullmatch(r"\s*[\w-]+\((.*)\)\s*", rule, re.S)
    return found.group(1).strip() if found else None


def rules(found, one, many):
    """The rules named, and the verb that agrees with how many there are."""
    return ", ".join(found) + (one if len(found) == 1 else many)


def read_or_test(rule):
    command = specifier(rule)
    if command is None:
        return False  # the whole Bash tool
    command = command[:-2] if command.endswith(":*") else command
    command = command.rstrip("*").strip()
    if any(operator in command for operator in ("&", "|", ";", ">", "<", "`", "$(")):
        return False
    return any(command == start or command.startswith(start + " ") for start in READS_AND_TESTS)


def table(value):
    return value if isinstance(value, dict) else {}


def strings(value):
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def claude_findings(settings_text, mcp_text):
    """For Claude Code's two files: each requirement, with what still breaks it (empty: it holds)."""
    found = {"tools": [], "edits": [], "commands": [], "network": []}
    try:
        settings = json.loads(settings_text) if settings_text is not None else {}
        mcp = json.loads(mcp_text) if mcp_text is not None else {}
        if not isinstance(settings, dict) or not isinstance(mcp, dict):
            raise ValueError("the file is not a JSON object")
    except ValueError as failure:
        return {name: [f"its files are not valid JSON ({failure})"] for name in found}
    permissions = table(settings.get("permissions"))
    allow, deny = strings(permissions.get("allow")), strings(permissions.get("deny"))
    sandbox = table(settings.get("sandbox"))

    for name, server in table(mcp.get("mcpServers")).items():
        if not reaches_case_system(name, server):
            continue
        if name in strings(settings.get("disabledMcpjsonServers")) or \
                any(rule.strip() in (f"mcp__{name}", f"mcp__{name}__*", "mcp__*") for rule in deny):
            continue
        found["tools"].append(
            f'.mcp.json still gives the agent the "{name}" server, which reads real notes. What the agent reads '
            "goes to its model's provider, so it may not reach a real note at all, with or without a yes "
            f"(section 1.1; {CC}mcp)")

    mode = permissions.get("defaultMode")
    if mode is None:
        found["edits"].append("there is no defaultMode, so a session started in a terminal begins in the built-in "
                              f"auto mode, where a classifier approves instead of a person ({CC}permission-modes)")
    elif mode != "default":
        found["edits"].append(f'defaultMode is "{mode}": a person says yes before each edit only in Manual mode, '
                              f'"default" ({CC}permission-modes)')
    edits = [rule for rule in allow if tool_of(rule) in EDIT_TOOLS]
    if edits:
        found["edits"].append(rules(edits, " in allow lets", " in allow let") + " the agent edit without asking, "
                              f"in any mode ({CC}permissions)")

    commands = [rule for rule in allow if tool_of(rule) == "Bash" and not read_or_test(rule)]
    if commands:
        found["commands"].append(rules(commands, " in allow runs", " in allow run") + " without a person's yes, "
                                 "and is neither a read nor a test run (section 1.3, the approvals row)")
    if sandbox.get("enabled") is True and sandbox.get("autoAllowBashIfSandboxed", True) is not False:
        found["commands"].append("with the sandbox on and autoAllowBashIfSandboxed not false, every sandboxed "
                                 f"command runs without asking, writes through the shell included ({CC}sandboxing)")

    if sandbox.get("enabled") is not True:
        found["network"].append("nothing the operating system enforces keeps the agent's commands off the network: a "
                                "deny rule matches a command as it is written, so python3, git or a test the agent "
                                f"wrote can still reach a host ({CC}security; {CC}sandboxing)")
    else:
        if sandbox.get("allowUnsandboxedCommands", True) is not False:
            found["network"].append("a command that fails in the sandbox can be retried outside it after one yes; "
                                    "section 1.3 removes such a choice rather than leaving it to a prompt "
                                    f"({CC}sandboxing)")
        if sandbox.get("excludedCommands"):
            found["network"].append(rules([str(c) for c in sandbox["excludedCommands"]], " in excludedCommands runs",
                                          " in excludedCommands run") + " outside the sandbox, with no network "
                                    f"proxy ({CC}sandboxing)")
        if table(sandbox.get("filesystem")).get("disabled") is True:
            found["network"].append(f"the sandbox's filesystem isolation is off ({CC}sandboxing)")
        domains = strings(table(sandbox.get("network")).get("allowedDomains"))
        domains += [specifier(rule)[len("domain:"):] for rule in allow
                    if tool_of(rule) == "WebFetch" and (specifier(rule) or "").startswith("domain:")]
        if domains:
            found["network"].append("sandboxed commands can reach " + ", ".join(domains) + "; the pilot downloads "
                                    f"nothing ({CC}sandboxing)")
    if not any(rule.strip() in ("WebFetch", "WebFetch(domain:*)") for rule in deny):
        found["network"].append("the web fetch tool runs outside the sandbox and is not denied "
                                f"({CC}permissions)")
    if "WebSearch" not in [rule.strip() for rule in deny]:
        found["network"].append(f"the web search tool runs outside the sandbox and is not denied ({CC}permissions)")
    return found


def codex_findings(config_text):
    """For Codex's file: each requirement, with what still breaks it (empty: it holds)."""
    found = {"tools": [], "approvals": [], "network": [], "record": []}
    try:
        config = read_toml(config_text) if config_text is not None else {}
    except ValueError as failure:
        return {name: [f"its file is not valid TOML ({failure})"] for name in found}
    unset = "is not set in this file, so each developer's own ~/.codex/config.toml decides it"

    for name, server in table(config.get("mcp_servers")).items():
        if not isinstance(server, dict) or not reaches_case_system(name, server):
            continue
        if server.get("enabled", True) is False or server.get("enabled_tools") == []:
            continue
        found["tools"].append(
            f"[mcp_servers.{name}] still gives the agent a server that reads real notes. What the agent reads goes "
            "to its model's provider, so it may not reach a real note at all, with or without a yes "
            f"(section 1.1; {CX}config-file/config-reference)")

    mode, profile = config.get("sandbox_mode"), config.get("default_permissions")
    if mode is None and profile is not None:
        if profile != ":read-only":
            found["approvals"].append(f'default_permissions is "{profile}": this check accepts sandbox_mode = '
                                      f'"read-only", or the built-in ":read-only" profile ({CX}permissions)')
    elif mode is None:
        found["approvals"].append(f"sandbox_mode {unset} ({CX}config-file/config-basic)")
    elif mode == "workspace-write":
        found["approvals"].append('sandbox_mode = "workspace-write" lets the agent edit files and run commands in the '
                                  f"repository without asking ({CX}agent-approvals-security)")
    elif mode != "read-only":
        found["approvals"].append(f'sandbox_mode = "{mode}" takes the sandbox away ({CX}agent-approvals-security)')
    policy = config.get("approval_policy")
    if policy is None:
        found["approvals"].append(f"approval_policy {unset} ({CX}config-file/config-basic)")
    elif policy == "untrusted":
        found["approvals"].append('approval_policy = "untrusted" is no longer supported, and Codex may not start '
                                  f"with it ({CX}agent-approvals-security)")
    elif policy == "never":
        found["approvals"].append('approval_policy = "never" never asks, so the agent cannot edit or run a command '
                                  f"even with your yes ({CX}agent-approvals-security)")
    elif isinstance(policy, dict):
        granular = policy.get("granular")
        if not (isinstance(granular, dict) and granular.get("sandbox_approval") is True):
            found["approvals"].append("approval_policy's granular form without sandbox_approval = true rejects the "
                                      f"agent's requests to edit before you see them ({CX}config-file/config-reference)")
    elif policy != "on-request":
        found["approvals"].append(f'approval_policy = "{policy}" is not one this check accepts; on-request asks '
                                  f"before anything the sandbox does not allow ({CX}config-file/config-reference)")

    search = config.get("web_search")
    if search is None:
        found["network"].append(f"web_search {unset} ({CX}config-file/config-reference)")
    elif search not in ("disabled", "cached"):
        found["network"].append(f'web_search = "{search}": the agent\'s searches reach the web, whatever the '
                                f"sandbox's network setting says ({CX}config-file/config-reference)")
    if mode == "workspace-write" and table(config.get("sandbox_workspace_write")).get("network_access") is True:
        found["network"].append("network_access = true lets the agent's commands reach the network "
                                f"({CX}config-file/config-reference)")

    persistence = table(config.get("history")).get("persistence")
    if persistence is None:
        found["record"].append(f"[history] persistence {unset} ({CX}config-file/config-sample)")
    elif persistence != "save-all":
        found["record"].append(f'[history] persistence = "{persistence}" keeps no transcript of the agent\'s '
                               "sessions, which the pilot keeps as evidence (section 1.3, the record row; "
                               f"{CX}config-file/config-reference)")
    return found


AGENTS = {"Claude Code": (CLAUDE, claude_findings), "Codex": (CODEX, codex_findings)}


# --- The check ---------------------------------------------------------------------------------

def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def at_commit(path, commit):
    shown = git("show", f"{commit}:{path}")
    return shown.stdout if shown.returncode == 0 else None


def now(path):
    return (REPO / path).read_text() if (REPO / path).is_file() else None


def stop(message):
    print("Not yet: " + message)
    sys.exit(1)


def main():
    if not (REPO / ".git").is_dir() or git("rev-parse", "-q", "--verify", f"refs/tags/{DRAFT}").returncode:
        stop("there is no repository lab/ with the tag pilot-draft; run python3 ~/practice/reset.py agent-boundary")
    configuration = CLAUDE + CODEX
    yours = git("rev-list", "--reverse", f"{DRAFT}..HEAD").stdout.split()
    touched = {commit: set(git("diff-tree", "--no-commit-id", "--name-only", "-r", commit).stdout.split())
               for commit in yours}
    if not any(names & set(configuration) for names in touched.values()):
        stop("commit your change to your coding agent's configuration first. This check shows what the "
             "configuration lets the agent reach or do only after your own change is committed, so that you "
             "decide first.")

    changed = set(git("diff", "--name-only", DRAFT, "--", *configuration).stdout.split())
    changed |= set().union(*touched.values()) & set(configuration)
    problems, firsts, judged = [], [], []
    for agent, (paths, findings) in AGENTS.items():
        if not changed & set(paths):
            continue
        judged.append(agent)
        lines = [line for found in findings(*(now(path) for path in paths)).values() for line in found]
        problems.extend(f"{agent}: {line}" for line in dict.fromkeys(lines))
        first = next((commit for commit in yours if touched[commit] & set(paths)), None)
        if first is not None:
            before = findings(*(at_commit(path, first) for path in paths))
            firsts.append(f"{sum(1 for found in before.values() if not found)} of the {len(before)} for {agent}")

    facts = now(FACTS) or ""
    line = next((line for line in facts.splitlines() if line.startswith(SIGN_OFF)), None)
    if line is None:
        problems.append(f'{FACTS} has lost its line "{SIGN_OFF}"')
    elif "TODO" in line or len(re.findall(r"[A-Za-z]+", line[len(SIGN_OFF):])) < 2:
        problems.append(f"{FACTS} does not yet name who must agree before the agent runs there")
    pending = [entry[3:] for entry in git("status", "--porcelain", "--", *configuration, FACTS).stdout.splitlines()]
    if pending:
        problems.append(", ".join(pending) + " not committed yet, as it stands now")

    if problems:
        print(f"Not yet: {len(problems)} left.")
        print("\n".join(f"- {problem}" for problem in problems))
        sys.exit(1)
    whose = " and ".join(f"{agent}'s" for agent in judged)
    holds = "configuration holds" if len(judged) == 1 else "configurations hold"
    record = ", and Codex keeps each session" if "Codex" in judged else ""
    print(f"Done: {whose} {holds} for the pilot: no tool of the agent reaches a real note, nothing but a read or a "
          "test run happens without a person's yes, and the agent's commands and web tools stay off the network"
          f"{record}. The sign-off is named, and all of it is committed. Before this check showed anything, your "
          "first commit met " + " and ".join(firsts) + ".")


if __name__ == "__main__":
    main()
