"""The done check for the tool-calling exercise.

It lives here, not in the notebook, because it is not what the exercise teaches. The notebook's
last cell calls check_work( globals() ): it hands over the notebook's variables, and this file
reads the ones the steps change.
"""
from collections.abc import Callable
from typing import Any

DONE = "Done: the model cannot mail a notice, your code supplies the case number, and the prompt says not to guess."


def check_work( notebook: dict[ str, Any ] ) -> str:
    """Check the three steps, and the last run of each case note.

    Args:
        notebook: the notebook's variables, from globals().

    Returns:
        DONE, or "Not yet:" followed by one line per step still to do.
    """
    try:
        problems = _problems( notebook )
    except KeyError as missing:
        problems = [ f"run every cell from the top, in order ({missing} is not defined yet)." ]
    if not problems:
        return DONE
    return "Not yet:\n" + "\n".join( "- " + problem for problem in problems )


def _problems( notebook: dict[ str, Any ] ) -> list[ str ]:
    """List what is still to do.

    Args:
        notebook: the notebook's variables.

    Returns:
        One line per problem, each naming its step; empty when every step is done.

    Raises:
        KeyError: a variable the steps define is missing, because a cell has not been run.
    """
    problems = []
    offered: list[ str ] = notebook[ "OFFERED" ]
    tools: dict[ str, dict ] = notebook[ "TOOLS" ]
    cases: dict[ str, dict ] = notebook[ "CASES" ]

    # Step 2: the mailing tool is gone, and refer_to_caseworker is described and offered.
    if "send_cp2000_notice" in offered:
        problems.append( "Step 2: send_cp2000_notice is still in OFFERED." )
    if "refer_to_caseworker" not in offered:
        problems.append( "Step 2: refer_to_caseworker is not in OFFERED." )
    refer = notebook[ "REFER_DEFINITION" ]
    descriptions = [ refer.get( "description", "" ),
                     refer.get( "parameters", {} ).get( "properties", {} ).get( "reason", {} ).get( "description", "" ) ]
    if any( "TODO" in text or len( text ) < 30 for text in descriptions ):
        problems.append( "Step 2: write both descriptions in REFER_DEFINITION, for a colleague who sees nothing else." )

    # Step 3: the model cannot send case_id, and your code adds it.
    lookup = tools[ "get_information_returns" ][ "definition" ][ "parameters" ]
    if "case_id" in lookup.get( "properties", {} ) or "case_id" in lookup.get( "required", [] ):
        problems.append( "Step 3: the model can still send case_id. Do TODO 3a." )
    add_values: Callable[ [ str, dict, dict ], dict ] = notebook[ "add_values_your_code_knows" ]
    supplied = add_values( "get_information_returns", { "tax_year": 2023, "form_type": "1099-NEC" },
                           cases[ "24-0147" ] )
    if supplied.get( "case_id" ) != "24-0147":
        problems.append( "Step 3: your code does not add the case number yet. Do TODO 3b." )

    # Step 4: the system prompt says what to do when a value is missing.
    if notebook[ "SYSTEM_PROMPT" ] == notebook[ "SYSTEM_PROMPT_START" ]:
        problems.append( "Step 4: the system prompt is unchanged." )

    # The last run of each note used today's list, and mailed nothing.
    results: dict[ str, dict ] = notebook[ "RESULTS" ]
    for case_id in cases:
        run = results.get( case_id )
        if run is None or run[ "offered" ] != offered:
            problems.append( f"Run case {case_id} again with your changes: its step's cell runs it." )
        elif run[ "mailed" ]:
            problems.append( f"Case {case_id}: a notice was still mailed in its last run." )
    return problems
