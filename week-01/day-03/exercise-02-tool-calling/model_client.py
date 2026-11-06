"""Plumbing for the tool-calling exercise: how a request with tools reaches a model, and what comes back.

The notebook holds what the exercise teaches: the case notes, the tools, and the loop that runs them.
This file holds the plumbing every tool-calling program needs, documented so you can reuse it.

How a model is called with tools
--------------------------------
Most providers, Databricks included, accept the OpenAI "chat completions" format. One request
carries three things:

- ``messages``: the conversation so far. A system message, the user's message, then any earlier
  replies and tool results. The model keeps no memory between requests, so every request resends
  the whole conversation.
- ``tools``: the tool definitions on offer, each wrapped as ``{"type": "function", "function":
  {"name", "description", "parameters"}}``. ``parameters`` is a JSON Schema. The model sees these
  definitions, never your Python.
- ``tool_choice``: ``"auto"`` (the model decides), ``"none"`` (no tool) or ``"required"`` (some tool).

The reply is one assistant message. It holds either text in ``content``, or one or more requests in
``tool_calls``. Each request names a tool and carries its arguments as JSON *text*, not a
dictionary: the model wrote characters, and your code must parse them (``json.loads``) and check
them before trusting them. To continue, your code appends that assistant message unchanged, then one
``{"role": "tool", "tool_call_id": ..., "content": ...}`` message per request, and calls the model
again.

What Databricks adds
--------------------
- The address: ``POST /serving-endpoints/<endpoint>/invocations`` on your workspace. In a Databricks
  notebook, the Databricks SDK finds the workspace and signs the request with your own identity, so
  there is no key in this code. Elsewhere it reads DATABRICKS_HOST and DATABRICKS_TOKEN.
- No strict mode for tools: nothing forces a request to match the schema. check_arguments() below
  does that check in your code.
- Reasoning and tools do not mix on every endpoint. On the chat-completions route,
  ``databricks-gpt-6-luna`` refused requests that offered tools with a reasoning effort other than
  ``"none"``. So model_spec.json sets ``"none"``, and _ask_databricks() retries once with ``"none"``
  if an endpoint refuses for that reason. Databricks also serves OpenAI's newer Responses API
  (``/serving-endpoints/responses``), a different request format; this exercise stays with chat
  completions, the format most providers share. The lesson: a provider's documentation lists what
  each model accepts, and an error message usually names the parameter it refused.
- The whole previous assistant message goes back on the next request, including any
  ``reasoning_content``: Databricks asks for it after a tool call.

The stand-in
------------
Outside Databricks, a scripted stand-in plays the model, so the notebook still runs and the course's
setup check calls no model. It answers the exercise's case notes the way a model typically does. It
can ask only for tools on the list it is given, so your changes still show their effect. Every reply
it writes starts with ``[stand-in]``.

Needs Python 3.12 or later, as the course and Databricks' serverless notebooks use.
"""
import json
import os
import pathlib
import re
from typing import Literal, Required, TypedDict

HERE = pathlib.Path( __file__ ).resolve().parent
SPEC_FILE = HERE / "model_spec.json"


class FunctionCall( TypedDict ):
    """The model's request for one tool: its name, and its arguments as JSON text."""
    name: str
    arguments: str


class ToolCall( TypedDict ):
    """One entry of an assistant message's ``tool_calls``. Your tool result answers it by ``id``."""
    id: str
    type: Literal[ "function" ]
    function: FunctionCall


class Message( TypedDict, total = False ):
    """One message of the conversation, in chat-completions format.

    ``role`` is always present. A system or user message has ``content``. An assistant message has
    ``content``, ``tool_calls``, or both, and sometimes ``reasoning_content``. A tool message has
    ``content`` (the result, as text) and ``tool_call_id`` (the request it answers).
    """
    role: Required[ Literal[ "system", "user", "assistant", "tool" ] ]
    content: str
    tool_calls: list[ ToolCall ]
    tool_call_id: str
    reasoning_content: str


class ToolDefinition( TypedDict ):
    """What the model sees of a tool: a name, a description, and a JSON Schema for its arguments."""
    name: str
    description: str
    parameters: dict[ str, object ]


type ToolChoice = Literal[ "auto", "none", "required" ]
type Spec = dict[ str, str | int | None ]


def load_spec( path: pathlib.Path = SPEC_FILE ) -> Spec:
    """Read model_spec.json and decide where the model runs.

    Args:
        path: the spec file. Defaults to model_spec.json beside this file.

    Returns:
        The spec, with "provider" resolved from "auto" to "databricks" (in a Databricks notebook, or
        with DATABRICKS_HOST set) or "stand-in" (anywhere else).
    """
    spec = json.loads( pathlib.Path( path ).read_text() )
    if spec.get( "provider", "auto" ) == "auto":
        in_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ or "DATABRICKS_HOST" in os.environ
        spec[ "provider" ] = "databricks" if in_databricks else "stand-in"
    return spec


def describe( spec: Spec ) -> str:
    """Say in one line where the model runs, for the notebook's first cell.

    Args:
        spec: the spec from load_spec().

    Returns:
        The line.
    """
    if spec[ "provider" ] == "databricks":
        return f"Model: {spec[ 'endpoint' ]} on Databricks, reasoning effort {spec.get( 'reasoning_effort' )}."
    return ( "Model: the scripted stand-in. No model is called; every reply is scripted. "
             "Run this notebook in Databricks to call a real model." )


def ask_model( messages: list[ Message ], tools: list[ ToolDefinition ], tool_choice: ToolChoice = "auto",
               spec: Spec | None = None ) -> Message:
    """Send the conversation so far, and the tools on offer, to the model, and return its reply.

    Args:
        messages: the conversation so far.
        tools: the definitions of the tools on offer. An empty list offers none.
        tool_choice: "auto" (the model decides), "none" (no tool) or "required" (some tool).
        spec: the spec from load_spec(). Defaults to model_spec.json.

    Returns:
        The model's reply: an assistant message with text in "content", requests in "tool_calls",
        or both.
    """
    spec = spec or load_spec()
    wrapped = [ { "type": "function", "function": tool } for tool in tools ]
    if spec[ "provider" ] == "databricks":
        return _ask_databricks( messages, wrapped, tool_choice, spec )
    return _ask_stand_in( messages, wrapped, tool_choice )


_WORKSPACE = None


def _ask_databricks( messages: list[ Message ], tools: list[ dict ], tool_choice: ToolChoice, spec: Spec ) -> Message:
    """Send one chat-completions request to a Databricks Foundation Model API endpoint.

    Args:
        messages: the conversation so far.
        tools: the tool definitions, already wrapped as {"type": "function", "function": ...}.
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
    path = f"/serving-endpoints/{spec[ 'endpoint' ]}/invocations"
    try:
        try:
            reply = _WORKSPACE.api_client.do( "POST", path, body = body )
        except Exception as failure:
            # Some endpoints (e.g. gpt-6-luna on chat completions) reject function tools combined
            # with a reasoning effort other than "none". Retry once with "none" and keep it.
            if tools and "reasoning_effort" in str( failure ) and body.get( "reasoning_effort" ) != "none":
                body[ "reasoning_effort" ] = "none"
                spec[ "reasoning_effort" ] = "none"
                reply = _WORKSPACE.api_client.do( "POST", path, body = body )
            else:
                raise
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


def check_arguments( schema: dict[ str, object ], arguments: dict[ str, object ] ) -> list[ str ]:
    """Check a tool's arguments against its parameter schema: the check strict mode would do.

    Databricks has no strict mode for tools, so the notebook's code checks every request itself.
    This covers the parts of JSON Schema the exercise uses: required properties, unknown
    properties, the types string, integer, number and boolean, and enum. It checks shape only: a
    made-up value of the right type passes.

    Args:
        schema: the tool's "parameters" schema.
        arguments: the arguments the model sent, parsed from JSON.

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
# the way a model typically answers the exercise's notes. It can ask only for a tool on the list.

_ASK_WORDS = ( "guess", "make up", "made up", "invent", "assume", "not in the note", "not stated", "not given",
               "missing", "say so", "ask for", "ask the caseworker", "does not give", "doesn't give" )


def _ask_stand_in( messages: list[ Message ], tools: list[ dict ], tool_choice: ToolChoice ) -> Message:
    """Write the stand-in's reply to the conversation so far.

    Args:
        messages: the conversation so far.
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

    def fill( tool: ToolDefinition, values: dict[ str, object ] ) -> dict[ str, object ]:
        """Build arguments for one tool: the given values where the schema has them, a short text elsewhere.

        Args:
            tool: the tool's definition.
            values: the values the stand-in has, by parameter name.

        Returns:
            The arguments, by parameter name.
        """
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
    return _say( "No tool is needed for this note." )


def _say( text: str ) -> Message:
    """Build a stand-in reply that holds text and no tool request.

    Args:
        text: what the stand-in writes.

    Returns:
        The assistant message.
    """
    return { "role": "assistant", "content": "[stand-in] " + text }


def _call( tool: ToolDefinition, arguments: dict[ str, object ], number: int ) -> Message:
    """Build a stand-in reply that asks for one tool, as a real model's reply does.

    Args:
        tool: the definition of the tool asked for.
        arguments: its arguments; they are sent as JSON text, as a real model sends them.
        number: how many requests came before, to give this one a unique id.

    Returns:
        The assistant message.
    """
    return { "role": "assistant", "content": "",
             "tool_calls": [ { "id": f"call_{number + 1}", "type": "function",
                               "function": { "name": tool[ "name" ], "arguments": json.dumps( arguments ) } } ] }
