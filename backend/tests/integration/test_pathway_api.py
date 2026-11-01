import pytest
from app.api.v1.pathway import check_pathway, facts_dictionary
from app.schemas.pathway import PathwayCheckRequest


def test_facts_dictionary_api():
    dict_data = facts_dictionary()
    assert "attributes" in dict_data
    assert len(dict_data["attributes"]) >= 5


def test_pathway_check_with_facts():
    payload = PathwayCheckRequest(
        facts={
            "ssc.passed": True,
            "qualification.type": "ITI",
            "qualification.trade": "Electrician",
            "craft_certificate.mapped_trade": True,
            "marks.percent": 68.0,
        }
    )
    res = check_pathway(payload)
    assert len(res.routes) >= 1
    assert any(r.status == "PASS" for r in res.routes)
    assert any(r.eligibility == "MEETS_CHECKED_CONDITIONS" for r in res.routes)
    assert "ITI_TO_DIPLOMA_DSE" in res.eligible_targets
