"""Plumbing for the tool-calling exercise: send one request to a model, and check a tool's arguments.

The notebook holds everything the exercise is about: the case notes, the tools, the loop that runs
them. This file holds only what the exercise is not about:

- ask_model() sends the conversation and the tool definitions to a model and returns its reply.
  Where the request goes is set in model_spec.json, beside this file.
- check_arguments() checks a tool's arguments against the tool's parameter schema.

Two providers:

- "databricks": a Databricks Foundation Model API endpoint, such as databricks-gpt-6-luna. The
  request body is the standard OpenAI chat-completions format, with "tools" and "tool_choice". In a
  Databricks notebook, the Databricks SDK signs the request with your own identity; elsewhere it
  reads DATABRICKS_HOST and DATABRICKS_TOKEN.
- "stand-in": a scripted stand-in for the model, for running the notebook outside Databricks and
  for the course's setup check. It never calls a model. It answers the three case notes the way a
  model typically does, and it only asks for tools that are on the list it is given, so the
  exercise's changes still show their effect. Every reply it makes is marked as scripted.
"""
import json
import os
import pathlib
import re

HERE = pathlib.Path( __file__ ).resolve().parent
SPEC_FILE = HERE / "model_spec.json"


def load_spec( path = SPEC_FILE ) -> dict:
    """Read model_spec.json.

    Args:
        path: the spec file. Defaults to model_spec.json beside this file.

    Returns:
        The spec, with "provider" resolved to "databricks" or "stand-in".
    """
    spec = json.loads( pathlib.Path( path ).read_text() )
    if spec.get( "provider", "auto" ) == "auto":
        in_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ or "DATABRICKS_HOST" in os.environ
        spec[ "provider" ] = "databricks" if in_databricks else "stand-in"
    return spec


def describe( spec: dict ) -> str:
    """One line saying where the model runs, for the notebook's first cell.

    Args:
        spec: the spec from load_spec().

    Returns:
        The line.
    """
    if spec[ "provider" ] == "databricks":
        effort = spec.get( "reasoning_effort" ) or "the endpoint's default"
        return f"Model: {spec[ 'endpoint' ]} on Databricks, reasoning effort {effort}."
    return ( "Model: the scripted stand-in. No model is called; every reply is scripted. "
             "Run this notebook in Databricks to call a real model." )


def ask_model( messages: list, tools: list, tool_choice: str = "auto", spec: dict | None = None ) -> dict:
    """Send the conversation so far, and the tools on offer, to the model.

    Args:
        messages: the conversation, in OpenAI chat format: system, user, assistant and tool messages.
        tools: the tool definitions on offer, each {"name", "description", "parameters"}.
        tool_choice: "auto" (the model decides), "none" (no tool) or "required" (some tool).
        spec: the spec from load_spec(). Defaults to model_spec.json.

    Returns:
        The model's reply, as an assistant message: {"role": "assistant", "content": text,
        "tool_calls": [...]}, where each tool call is {"id", "type": "function",
        "function": {"name", "arguments"}} and "arguments" is JSON text.
    """
    spec = spec or load_spec()
    wrapped = [ { "type": "function", "function": tool } for tool in tools ]
    if spec[ "provider" ] == "databricks":
        return _ask_databricks( messages, wrapped, tool_choice, spec )
    return _ask_stand_in( messages, wrapped, tool_choice )


_WORKSPACE = None


def _ask_databricks( messages: list, tools: list, tool_choice: str, spec: dict ) -> dict:
    """One chat-completions request to a Databricks Foundation Model API endpoint.

    Args:
        messages: the conversation, in OpenAI chat format.
        tools: the tool definitions, wrapped as {"type": "function", "function": ...}.
        tool_choice: "auto", "none" or "required".
        spec: the spec, naming the endpoint, the reasoning effort and the token limit.

    Returns:
        The model's reply, as an assistant message.

    Raises:
        RuntimeError: the Databricks SDK is missing, or the endpoint refused the request.
    """
    global _WORKSPACE
    try:
        from databricks.sdk import WorkspaceClient
    except ImportError:
        raise RuntimeError( "the Databricks SDK is not installed here. Run this notebook in Databricks, "
                            "or set provider to stand-in in model_spec.json." ) from None
    if _WORKSPACE is None:
        _WORKSPACE = WorkspaceClient()
    body = { "messages": messages, "max_tokens": spec.get( "max_tokens", 1500 ) }
    if tools:
        body[ "tools" ] = tools
        body[ "tool_choice" ] = tool_choice
    if spec.get( "reasoning_effort" ):
        body[ "reasoning_effort" ] = spec[ "reasoning_effort" ]
    try:
        reply = _WORKSPACE.api_client.do( "POST", f"/serving-endpoints/{spec[ 'endpoint' ]}/invocations",
                                          body = body )
    except Exception as failure:
        raise RuntimeError( f"the endpoint {spec[ 'endpoint' ]} refused the request: {failure}. Check the "
                            "endpoint name in model_spec.json against Serving in your workspace." ) from None
    message = reply[ "choices" ][ 0 ][ "message" ]
    # Keep the whole message, reasoning included: Databricks asks for the complete previous
    # assistant message in the next request when the conversation continues after a tool call.
    message = { key: value for key, value in message.items() if value is not None }
    message[ "role" ] = "assistant"
    message.setdefault( "content", "" )
    return message


def check_arguments( schema: dict, arguments: dict ) -> list:
    """Check a tool's arguments against its parameter schema: the checking strict mode would do.

    Databricks has no strict mode for tools, so the notebook's code checks every request itself.
    This covers the parts of JSON Schema the exercise uses: required properties, unknown
    properties, the types string, integer, number and boolean, and enum.

    Args:
        schema: the tool's "parameters" schema.
        arguments: the arguments the model sent.

    Returns:
        One line per problem; empty when the arguments fit the schema.
    """
    problems = []
    properties = schema.get( "properties", {} )
    for name in schema.get( "required", [] ):
        if name not in arguments:
            problems.append( f"missing {name}" )
    types = { "string": str, "integer": int, "number": ( int, float ), "boolean": bool }
    for name, value in arguments.items():
        rule = properties.get( name )
        if rule is None:
            problems.append( f"{name} is not one of this tool's parameters" )
            continue
        wanted = types.get( rule.get( "type" ) )
        if wanted and ( not isinstance( value, wanted ) or ( wanted is int and isinstance( value, bool ) ) ):
            problems.append( f"{name} should be a {rule[ 'type' ]}, not {value!r}" )
        if "enum" in rule and value not in rule[ "enum" ]:
            problems.append( f"{name} must be one of {rule[ 'enum' ]}, not {value!r}" )
    return problems


# The scripted stand-in. It reads the note, the system prompt and the tools on offer, and answers
# the way a model typically answers these three notes. It can ask only for a tool on the list.

_ASK_WORDS = ( "guess", "make up", "made up", "invent", "assume", "not in the note", "not stated", "not given",
               "missing", "say so", "ask for", "ask the caseworker", "does not give", "doesn't give" )


def _ask_stand_in( messages: list, tools: list, tool_choice: str ) -> dict:
    """The stand-in's reply to the conversation so far.

    Args:
        messages: the conversation, in OpenAI chat format.
        tools: the tool definitions, wrapped as {"type": "function", "function": ...}.
        tool_choice: "auto", "none" or "required".

    Returns:
        An assistant message, as ask_model() describes.
    """
    system = messages[ 0 ][ "content" ].lower()
    note = next( m[ "content" ] for m in messages if m[ "role" ] == "user" )
    offered = { t[ "function" ][ "name" ]: t[ "function" ] for t in tools } if tool_choice != "none" else {}
    asked = [ call[ "function" ][ "name" ] for m in messages if m[ "role" ] == "assistant"
              for call in m.get( "tool_calls" ) or [] ]
    results = [ json.loads( m[ "content" ] ) for m in messages if m[ "role" ] == "tool" ]
    year = re.search( r"[Tt]ax year (\d{4})", note )
    case = re.search( r"Case (\d{2}-\d{4})", note )
    form = re.search( r"1099-(NEC|K|MISC)", note )
    receipts = re.search( r"gross receipts reported: ([\d,]+)", note )

    def fill( tool: dict, values: dict ) -> dict:
        """Arguments for one tool: the given values where the schema has them, a short text elsewhere."""
        params = tool.get( "parameters", {} )
        arguments = {}
        for name, rule in params.get( "properties", {} ).items():
            if name in values:
                arguments[ name ] = values[ name ]
            elif name in params.get( "required", [] ):
                arguments[ name ] = ( "Information returns on file exceed the receipts reported; a "
                                      "caseworker should decide the next step." if rule.get( "type" ) == "string"
                                      else values.get( "amount", 0 ) )
        return arguments

    known = { "case_id": case.group( 1 ) if case else "unknown" }

    # First: look up the information returns the note mentions.
    lookup = offered.get( "get_information_returns" )
    if lookup and form and "get_information_returns" not in asked:
        if not year and any( word in system for word in _ASK_WORDS ):
            return _say( "The note does not say which tax year the Form 1099-" + form.group( 1 ) + " is for, "
                         "so I have not looked anything up. Please confirm the tax year with the filer." )
        values = dict( known, tax_year = int( year.group( 1 ) ) if year else 2025,
                       form_type = "1099-" + form.group( 1 ) )
        return _call( lookup, fill( lookup, values ), len( asked ) )

    # Then: act on a gap between the receipts reported and the forms on file.
    found = next( ( r for r in results if isinstance( r, dict ) and "total" in r ), None )
    gap = ( found[ "total" ] - int( receipts.group( 1 ).replace( ",", "" ) ) ) if found and receipts else 0
    if gap > 0:
        for name, tool in offered.items():
            if name != "get_information_returns" and name not in asked:
                values = dict( known, tax_year = found.get( "tax_year" ), amount = gap,
                               proposed_additional_income = gap )
                return _call( tool, fill( tool, values ), len( asked ) )
        return _say( f"The Forms 1099 on file total {found[ 'total' ]:,}, which is {gap:,} more than the "
                     f"{receipts.group( 1 )} of gross receipts reported. "
                     + ( f"For the next step, I used {asked[ -1 ]}." if asked[ 1 : ] else
                         "A caseworker should decide the next step." ) )

    if tool_choice == "required" and offered and not asked:
        name, tool = next( iter( offered.items() ) )
        return _call( tool, fill( tool, dict( known, tax_year = 2025, form_type = "1099-NEC" ) ), 0 )

    if found is not None:
        if found.get( "forms" ):
            return _say( f"The Forms {found.get( 'form_type' )} on file for {found.get( 'tax_year' )} total "
                         f"{found[ 'total' ]:,}. The note gives no receipts to compare them with." )
        return _say( f"No Form {found.get( 'form_type' )} is on file for tax year {found.get( 'tax_year' )}." )
    if results:
        return _say( "The tool reported: " + json.dumps( results[ -1 ] ) )
    return _say( "No tool needed: the note records a change of address and raises no question about "
                 "the return." )


def _say( text: str ) -> dict:
    """A stand-in reply with text and no tool call."""
    return { "role": "assistant", "content": "[stand-in] " + text }


def _call( tool: dict, arguments: dict, number: int ) -> dict:
    """A stand-in reply that asks for one tool."""
    return { "role": "assistant", "content": "",
             "tool_calls": [ { "id": f"call_{number + 1}", "type": "function",
                               "function": { "name": tool[ "name" ], "arguments": json.dumps( arguments ) } } ] }
