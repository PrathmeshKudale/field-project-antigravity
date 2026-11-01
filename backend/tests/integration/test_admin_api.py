import pytest
from app.api.v1.admin_sources import list_sources
from app.api.v1.admin_rules import review_queue
from app.api.v1.admin_audit import verify_audit_chain


def test_sources_list():
    data = list_sources()
    assert len(data) >= 1
    assert data[0]["status"] == "current"


def test_rule_queue():
    data = review_queue()
    assert len(data) >= 1
    assert data[0]["schema_valid"] is True


def test_audit_verify():
    data = verify_audit_chain()
    assert data["is_valid"] is True
