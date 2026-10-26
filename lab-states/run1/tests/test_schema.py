"""Hand-written outputs checked against the output schema. No model is called."""
import json
import pathlib

import jsonschema
import pytest

SCHEMA = json.loads((pathlib.Path(__file__).resolve().parents[1] / "schema" / "output.schema.json").read_text())

NOTE_0147 = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below information returns",
             "amount_in_question": 18400, "next_action": "Follow up on records request in 30 days"}


def test_note_0147_output_passes():
    jsonschema.validate(NOTE_0147, SCHEMA)


def test_null_amount_passes():
    jsonschema.validate({**NOTE_0147, "amount_in_question": None}, SCHEMA)


def test_missing_amount_fails():
    output = {k: v for k, v in NOTE_0147.items() if k != "amount_in_question"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(output, SCHEMA)


def test_amount_as_text_fails():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**NOTE_0147, "amount_in_question": "18,400"}, SCHEMA)


def test_extra_field_fails():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({**NOTE_0147, "taxpayer_name": "Synthetic filer"}, SCHEMA)
