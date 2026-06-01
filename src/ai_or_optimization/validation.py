"""Validation utilities for public AI OR contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import OptimizationProblem, SolveReport


@dataclass(frozen=True)
class ValidationIssue:
    """A contract-level issue that should be resolved before execution."""

    code: str
    message: str
    location: str


def validate_problem(problem: OptimizationProblem) -> tuple[ValidationIssue, ...]:
    """Validate rule traceability and variable references in a public problem."""

    issues: list[ValidationIssue] = []
    rule_ids = tuple(rule.rule_id for rule in problem.rules)
    variable_names = tuple(variable.name for variable in problem.variables)
    known_rule_ids = set(rule_ids)
    known_variable_names = set(variable_names)

    issues.extend(
        _duplicate_issues(
            rule_ids,
            code="duplicate_rule_id",
            message_prefix="Duplicate rule_id",
            location_prefix="rules",
            field_name="rule_id",
        )
    )
    issues.extend(
        _duplicate_issues(
            variable_names,
            code="duplicate_variable_name",
            message_prefix="Duplicate variable name",
            location_prefix="variables",
            field_name="name",
        )
    )

    for index, variable in enumerate(problem.variables):
        if variable.lower_bound > variable.upper_bound:
            issues.append(
                ValidationIssue(
                    "invalid_variable_bounds",
                    f"Variable {variable.name!r} has lower_bound greater than upper_bound.",
                    f"variables[{index}]",
                )
            )

    for constraint_index, constraint in enumerate(problem.constraints):
        if constraint.rule_id not in known_rule_ids:
            issues.append(
                ValidationIssue(
                    "unknown_constraint_rule",
                    f"Constraint references unknown rule_id {constraint.rule_id!r}.",
                    f"constraints[{constraint_index}].rule_id",
                )
            )
        for variable_name in constraint.expression:
            if variable_name not in known_variable_names:
                issues.append(
                    ValidationIssue(
                        "unknown_constraint_variable",
                        f"Constraint references unknown variable {variable_name!r}.",
                        f"constraints[{constraint_index}].expression",
                    )
                )

    if problem.objective.rule_id not in known_rule_ids:
        issues.append(
            ValidationIssue(
                "unknown_objective_rule",
                f"Objective references unknown rule_id {problem.objective.rule_id!r}.",
                "objective.rule_id",
            )
        )
    for variable_name in problem.objective.coefficients:
        if variable_name not in known_variable_names:
            issues.append(
                ValidationIssue(
                    "unknown_objective_variable",
                    f"Objective references unknown variable {variable_name!r}.",
                    "objective.coefficients",
                )
            )

    return tuple(issues)


def validate_solve_report(
    problem: OptimizationProblem,
    report: SolveReport,
) -> tuple[ValidationIssue, ...]:
    """Validate that a solve report can be traced back to the problem rules."""

    issues: list[ValidationIssue] = []
    known_rule_ids = {rule.rule_id for rule in problem.rules}
    for index, rule_id in enumerate(report.rule_trace):
        if rule_id not in known_rule_ids:
            issues.append(
                ValidationIssue(
                    "unknown_report_rule",
                    f"Solve report references unknown rule_id {rule_id!r}.",
                    f"rule_trace[{index}]",
                )
            )
    return tuple(issues)


def _duplicate_issues(
    values: tuple[str, ...],
    *,
    code: str,
    message_prefix: str,
    location_prefix: str,
    field_name: str,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    reported: set[str] = set()
    for index, value in enumerate(values):
        if value in seen and value not in reported:
            issues.append(
                ValidationIssue(
                    code,
                    f"{message_prefix} {value!r}.",
                    f"{location_prefix}[{index}].{field_name}",
                )
            )
            reported.add(value)
        seen.add(value)
    return tuple(issues)
