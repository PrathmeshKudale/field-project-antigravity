import pytest
from app.rules.engine import evaluate_rule, Status


DEMO_RULE = {
    "rule_id": "PROP-001",
    "route": "TEST_ROUTE",
    "conditions": {
        "all": [
            {"attr": "marks.percent", "op": "gte", "value": 50.0, "quote": "at least 50% marks in qualifying exam"},
            {"attr": "ssc.passed", "op": "eq", "value": True, "quote": "passed Class X board exam"}
        ]
    }
}


@pytest.mark.parametrize("marks,ssc,expected_status", [
    (60.0, True, "PASS"),
    (40.0, True, "FAIL"),
    (60.0, False, "FAIL"),
    (40.0, False, "FAIL"),
    (None, True, "UNKNOWN"),
    (60.0, None, "UNKNOWN"),
    (None, None, "UNKNOWN"),
    (50.0, True, "PASS"),
])
def test_rule_engine_truth_table(marks, ssc, expected_status):
    facts = {}
    if marks is not None:
        facts["marks.percent"] = marks
    if ssc is not None:
        facts["ssc.passed"] = ssc
    res = evaluate_rule(DEMO_RULE, facts)
    assert res["status"] == expected_status
