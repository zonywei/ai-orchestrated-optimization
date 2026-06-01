"""Constraint audit utilities for rule-first optimization problems."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .contracts import LinearConstraint, OptimizationProblem


ConstraintAuditStatus = Literal[
    "always_satisfied",
    "always_violated",
    "binding_candidate",
    "invalid_reference",
]


@dataclass(frozen=True)
class ConstraintAuditItem:
    """A deterministic pre-solve audit result for one linear constraint."""

    constraint_index: int
    rule_id: str
    status: ConstraintAuditStatus
    activity_min: int | float | None
    activity_max: int | float | None
    rhs: int | float
    operator: str
    unknown_variables: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConstraintAuditReport:
    """A compact pre-solve audit report for public optimization contracts."""

    items: tuple[ConstraintAuditItem, ...]

    @property
    def summary_by_status(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for item in self.items:
            summary[item.status] = summary.get(item.status, 0) + 1
        return summary

    @property
    def violated_items(self) -> tuple[ConstraintAuditItem, ...]:
        return tuple(item for item in self.items if item.status == "always_violated")


def audit_constraints(problem: OptimizationProblem) -> ConstraintAuditReport:
    """Audit linear constraints against declared variable bounds before solving."""

    bounds_by_variable = {
        variable.name: (variable.lower_bound, variable.upper_bound)
        for variable in problem.variables
    }
    items = tuple(
        _audit_constraint(index, constraint, bounds_by_variable)
        for index, constraint in enumerate(problem.constraints)
    )
    return ConstraintAuditReport(items)


def _audit_constraint(
    index: int,
    constraint: LinearConstraint,
    bounds_by_variable: dict[str, tuple[int | float, int | float]],
) -> ConstraintAuditItem:
    unknown_variables = tuple(
        variable_name
        for variable_name in constraint.expression
        if variable_name not in bounds_by_variable
    )
    if unknown_variables:
        return ConstraintAuditItem(
            constraint_index=index,
            rule_id=constraint.rule_id,
            status="invalid_reference",
            activity_min=None,
            activity_max=None,
            rhs=constraint.rhs,
            operator=constraint.operator,
            unknown_variables=unknown_variables,
        )

    activity_min = 0
    activity_max = 0
    for variable_name, coefficient in constraint.expression.items():
        lower_bound, upper_bound = bounds_by_variable[variable_name]
        term_min, term_max = _term_range(coefficient, lower_bound, upper_bound)
        activity_min += term_min
        activity_max += term_max

    return ConstraintAuditItem(
        constraint_index=index,
        rule_id=constraint.rule_id,
        status=_classify_constraint(constraint, activity_min, activity_max),
        activity_min=activity_min,
        activity_max=activity_max,
        rhs=constraint.rhs,
        operator=constraint.operator,
    )


def _term_range(
    coefficient: int | float,
    lower_bound: int | float,
    upper_bound: int | float,
) -> tuple[int | float, int | float]:
    values = (coefficient * lower_bound, coefficient * upper_bound)
    return min(values), max(values)


def _classify_constraint(
    constraint: LinearConstraint,
    activity_min: int | float,
    activity_max: int | float,
) -> ConstraintAuditStatus:
    if constraint.operator == "<=":
        if activity_max <= constraint.rhs:
            return "always_satisfied"
        if activity_min > constraint.rhs:
            return "always_violated"
    elif constraint.operator == ">=":
        if activity_min >= constraint.rhs:
            return "always_satisfied"
        if activity_max < constraint.rhs:
            return "always_violated"
    elif constraint.operator == "==":
        if activity_min == activity_max == constraint.rhs:
            return "always_satisfied"
        if constraint.rhs < activity_min or constraint.rhs > activity_max:
            return "always_violated"
    return "binding_candidate"
