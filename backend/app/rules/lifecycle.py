from datetime import date


def is_rule_stale(rule: dict) -> bool:
    effective_until = rule.get("effective_until")
    if not effective_until:
        return False
    if isinstance(effective_until, str):
        effective_until = date.fromisoformat(effective_until)
    return date.today() > effective_until
