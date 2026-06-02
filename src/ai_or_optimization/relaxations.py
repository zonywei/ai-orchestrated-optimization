"""Deterministic relaxation suggestions for structural infeasibility."""

from __future__ import annotations

from dataclasses import dataclass

from .audit import ConstraintAuditItem, audit_constraints
from .contracts import OptimizationProblem


@dataclass(frozen=True)
class ConstraintRelaxationSuggestion:
    """A small public suggestion for relaxing an impossible linear constraint."""

    rule_id: str
    constraint_index: int
    operator: str
    current_rhs: int | float
    suggested_rhs: int | float
    delta: int | float
    reason: str

    @property
    def suggested_action(self) -> str:
        return (
            f"Move RHS from {self.current_rhs!r} to nearest reachable bound "
            f"{self.suggested_rhs!r} (delta {self.delta!r})."
        )


@dataclass(frozen=True)
class RelaxationReport:
    """A compact set of deterministic relaxation suggestions."""

    suggestions: tuple[ConstraintRelaxationSuggestion, ...] = ()

    @property
    def has_suggestions(self) -> bool:
        return bool(self.suggestions)


def suggest_constraint_relaxations(problem: OptimizationProblem) -> RelaxationReport:
    """Suggest RHS changes for constraints that are impossible from bounds alone."""

    suggestions = tuple(
        suggestion
        for item in audit_constraints(problem).violated_items
        if (suggestion := _suggest_rhs_relaxation(item)) is not None
    )
    return RelaxationReport(suggestions)


def _suggest_rhs_relaxation(
    item: ConstraintAuditItem,
) -> ConstraintRelaxationSuggestion | None:
    if item.activity_min is None or item.activity_max is None:
        return None

    if item.operator == "<=":
        suggested_rhs = item.activity_min
    elif item.operator == ">=":
        suggested_rhs = item.activity_max
    elif item.operator == "==":
        suggested_rhs = _nearest_reachable_rhs(item)
    else:
        return None

    delta = suggested_rhs - item.rhs
    return ConstraintRelaxationSuggestion(
        rule_id=item.rule_id,
        constraint_index=item.constraint_index,
        operator=item.operator,
        current_rhs=item.rhs,
        suggested_rhs=suggested_rhs,
        delta=delta,
        reason=(
            "The declared variable bounds make the original RHS unreachable; "
            "the suggestion moves the RHS to the nearest reachable activity bound."
        ),
    )


def _nearest_reachable_rhs(item: ConstraintAuditItem) -> int | float:
    if item.activity_min is None or item.activity_max is None:
        return item.rhs
    if item.rhs < item.activity_min:
        return item.activity_min
    if item.rhs > item.activity_max:
        return item.activity_max
    return item.rhs
