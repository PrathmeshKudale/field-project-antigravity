from enum import Enum
from typing import Any
from app.rules.dsl import RuleNode, ConditionLeaf, AllGroup, AnyGroup, parse_conditions


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class EligibilityStatus(str, Enum):
    MEETS_CHECKED_CONDITIONS = "MEETS_CHECKED_CONDITIONS"
    NOT_ELIGIBLE_UNDER_THIS_RULE = "NOT_ELIGIBLE_UNDER_THIS_RULE"
    NEEDS_MORE_INFORMATION = "NEEDS_MORE_INFORMATION"
    NEEDS_LOCAL_RULE_CHECK = "NEEDS_LOCAL_RULE_CHECK"
    RULE_STALE_NEEDS_REVIEW = "RULE_STALE_NEEDS_REVIEW"
    BRANCH_OR_TRADE_REVIEW_REQUIRED = "BRANCH_OR_TRADE_REVIEW_REQUIRED"


def _eval_leaf(leaf: ConditionLeaf, facts: dict[str, Any]) -> Status:
    """Evaluate a single condition leaf using Kleene 3-valued logic."""
    if leaf.attr not in facts or facts[leaf.attr] is None or facts[leaf.attr] == "":
        return Status.UNKNOWN

    val = facts[leaf.attr]
    expected = leaf.value

    try:
        match leaf.op:
            case "eq":
                return Status.PASS if val == expected else Status.FAIL
            case "ne":
                return Status.PASS if val != expected else Status.FAIL
            case "gte":
                return Status.PASS if float(val) >= float(expected) else Status.FAIL
            case "lte":
                return Status.PASS if float(val) <= float(expected) else Status.FAIL
            case "gt":
                return Status.PASS if float(val) > float(expected) else Status.FAIL
            case "lt":
                return Status.PASS if float(val) < float(expected) else Status.FAIL
            case "in":
                return Status.PASS if val in expected else Status.FAIL
            case "not_in":
                return Status.PASS if val not in expected else Status.FAIL
            case _:
                return Status.UNKNOWN
    except (ValueError, TypeError):
        return Status.FAIL


def _eval_node(node: RuleNode, facts: dict[str, Any]) -> tuple[Status, list[dict]]:
    """Evaluate a node tree with trace."""
    trace = []
    if isinstance(node, ConditionLeaf):
        status = _eval_leaf(node, facts)
        trace.append({
            "attr": node.attr,
            "op": node.op,
            "value": node.value,
            "status": status.value,
            "quote": node.quote,
        })
        return status, trace

    child_statuses = []
    for child in node.conditions:
        child_status, child_trace = _eval_node(child, facts)
        child_statuses.append(child_status)
        trace.extend(child_trace)

    if isinstance(node, AllGroup):
        # Kleene AND:
        # If any FAIL -> FAIL
        # Else if any UNKNOWN -> UNKNOWN
        # Else -> PASS
        if Status.FAIL in child_statuses:
            return Status.FAIL, trace
        if Status.UNKNOWN in child_statuses:
            return Status.UNKNOWN, trace
        return Status.PASS, trace
    else:  # AnyGroup
        # Kleene OR:
        # If any PASS -> PASS
        # Else if any UNKNOWN -> UNKNOWN
        # Else -> FAIL
        if Status.PASS in child_statuses:
            return Status.PASS, trace
        if Status.UNKNOWN in child_statuses:
            return Status.UNKNOWN, trace
        return Status.FAIL, trace


def evaluate_rule(rule: dict, facts: dict[str, Any]) -> dict:
    """Evaluate a rule against user facts. Deterministic pure function."""
    node = parse_conditions(rule["conditions"])
    status, trace = _eval_node(node, facts)

    if status == Status.PASS:
        eligibility = EligibilityStatus.MEETS_CHECKED_CONDITIONS
    elif status == Status.FAIL:
        eligibility = EligibilityStatus.NOT_ELIGIBLE_UNDER_THIS_RULE
    else:
        eligibility = EligibilityStatus.NEEDS_MORE_INFORMATION

    return {
        "rule_id": rule.get("rule_id", rule.get("rule_key", "")),
        "route": rule.get("route", ""),
        "title": rule.get("title", ""),
        "status": status.value,
        "eligibility": eligibility.value,
        "trace": trace,
        "caveats": rule.get("caveats", []),
    }
