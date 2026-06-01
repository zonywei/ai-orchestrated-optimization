"""Objective contribution analysis for public solve reports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .contracts import ObjectiveSense, OptimizationProblem, SolveReport


ContributionDirection = Literal[
    "increases_objective",
    "reduces_objective",
    "neutral",
]


@dataclass(frozen=True)
class ObjectiveContribution:
    """One variable's contribution to the linear objective."""

    variable_name: str
    coefficient: int | float
    value: int | float
    contribution: int | float
    direction: ContributionDirection


@dataclass(frozen=True)
class ObjectiveContributionReport:
    """A traceable decomposition of objective value by variable."""

    rule_id: str
    sense: ObjectiveSense
    items: tuple[ObjectiveContribution, ...]
    missing_variables: tuple[str, ...] = ()
    invalid_variables: tuple[str, ...] = ()

    @property
    def total_contribution(self) -> int | float:
        return sum(item.contribution for item in self.items)

    @property
    def is_complete(self) -> bool:
        return not self.missing_variables and not self.invalid_variables


def analyze_objective_contributions(
    problem: OptimizationProblem,
    report: SolveReport,
) -> ObjectiveContributionReport:
    """Break a solve report's linear objective into variable-level terms."""

    items: list[ObjectiveContribution] = []
    missing_variables: list[str] = []
    invalid_variables: list[str] = []
    for variable_name, coefficient in problem.objective.coefficients.items():
        if variable_name not in report.assignments:
            missing_variables.append(variable_name)
            continue
        value = report.assignments[variable_name]
        if not isinstance(value, int | float):
            invalid_variables.append(variable_name)
            continue
        contribution = coefficient * value
        items.append(
            ObjectiveContribution(
                variable_name=variable_name,
                coefficient=coefficient,
                value=value,
                contribution=contribution,
                direction=_classify_direction(contribution),
            )
        )
    return ObjectiveContributionReport(
        rule_id=problem.objective.rule_id,
        sense=problem.objective.sense,
        items=tuple(items),
        missing_variables=tuple(missing_variables),
        invalid_variables=tuple(invalid_variables),
    )


def _classify_direction(contribution: int | float) -> ContributionDirection:
    if contribution > 0:
        return "increases_objective"
    if contribution < 0:
        return "reduces_objective"
    return "neutral"
