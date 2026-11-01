import pytest
from app.rules.engine import evaluate_rule, Status, EligibilityStatus


TEST_RULE = {
    "rule_id": "TEST-DSE-001",
    "route": "ITI_TO_DIPLOMA_DSE",
    "title": "Direct Second Year Diploma Test",
    "caveats": ["Subject to seat availability"],
    "conditions": {
        "all": [
            {"attr": "ssc.passed", "op": "eq", "value": True, "quote": "A candidate who has passed the Class X examination"},
            {"attr": "qualification.type", "op": "in", "value": ["ITI"], "quote": "and holds a Two-Year Craft Certificate"},
            {"attr": "marks.percent", "op": "gte", "value": 50.0, "quote": "shall be eligible for Direct Second Year admission"}
        ]
    }
}


def test_evaluate_rule_pass():
    facts = {"ssc.passed": True, "qualification.type": "ITI", "marks.percent": 65.5}
    res = evaluate_rule(TEST_RULE, facts)
    assert res["status"] == "PASS"
    assert res["eligibility"] == "MEETS_CHECKED_CONDITIONS"
    assert len(res["trace"]) == 3
    assert all(t["status"] == "PASS" for t in res["trace"])


def test_evaluate_rule_fail_marks():
    facts = {"ssc.passed": True, "qualification.type": "ITI", "marks.percent": 45.0}
    res = evaluate_rule(TEST_RULE, facts)
    assert res["status"] == "FAIL"
    assert res["eligibility"] == "NOT_ELIGIBLE_UNDER_THIS_RULE"
    assert res["trace"][2]["status"] == "FAIL"


def test_evaluate_rule_unknown_missing_field():
    facts = {"ssc.passed": True, "qualification.type": "ITI"}
    res = evaluate_rule(TEST_RULE, facts)
    assert res["status"] == "UNKNOWN"
    assert res["eligibility"] == "NEEDS_MORE_INFORMATION"
    assert res["trace"][2]["status"] == "UNKNOWN"


def test_evaluate_rule_wrong_qualification():
    facts = {"ssc.passed": True, "qualification.type": "Degree", "marks.percent": 75.0}
    res = evaluate_rule(TEST_RULE, facts)
    assert res["status"] == "FAIL"
    assert res["eligibility"] == "NOT_ELIGIBLE_UNDER_THIS_RULE"
