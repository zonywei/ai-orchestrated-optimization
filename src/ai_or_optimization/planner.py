"""Rule-first planning utilities."""

from __future__ import annotations

from .contracts import RuleFirstPlan, RuleSpec


def build_rule_first_plan(rules: tuple[RuleSpec, ...]) -> RuleFirstPlan:
    """Order rules so feasibility and higher-priority policy are evaluated first."""

    ordered = sorted(
        rules,
        key=lambda rule: (
            0 if rule.kind == "hard" else 1,
            -rule.priority,
            rule.rule_id,
        ),
    )
    return RuleFirstPlan(tuple(ordered))
