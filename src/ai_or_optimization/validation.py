"""Validation utilities for public AI OR contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import OptimizationProblem, SolveReport


VALID_RULE_KINDS = {"hard", "soft"}
VALID_VARIABLE_KINDS = {"binary", "integer", "continuous"}
VALID_CONSTRAINT_OPERATORS = {"<=", "==", ">="}
VALID_OBJECTIVE_SENSES = {"minimize", "maximize"}


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

    for index, rule in enumerate(problem.rules):
        if rule.kind not in VALID_RULE_KINDS:
            issues.append(
                ValidationIssue(
                    "invalid_rule_kind",
                    f"Rule {rule.rule_id!r} has invalid kind {rule.kind!r}.",
                    f"rules[{index}].kind",
                )
            )

    for index, variable in enumerate(problem.variables):
        if variable.kind not in VALID_VARIABLE_KINDS:
            issues.append(
                ValidationIssue(
                    "invalid_variable_kind",
                    f"Variable {variable.name!r} has invalid kind {variable.kind!r}.",
                    f"variables[{index}].kind",
                )
            )
        if variable.lower_bound > variable.upper_bound:
            issues.append(
                ValidationIssue(
                    "invalid_variable_bounds",
                    f"Variable {variable.name!r} has lower_bound greater than upper_bound.",
                    f"variables[{index}]",
                )
            )
        if variable.kind == "binary" and not _valid_binary_bounds(
            variable.lower_bound,
            variable.upper_bound,
        ):
            issues.append(
                ValidationIssue(
                    "invalid_binary_bounds",
                    (
                        f"Binary variable {variable.name!r} must have integer bounds "
                        "inside 0..1."
                    ),
                    f"variables[{index}]",
                )
            )
        if variable.kind == "integer" and not (
            _is_integer_value(variable.lower_bound)
            and _is_integer_value(variable.upper_bound)
        ):
            issues.append(
                ValidationIssue(
                    "invalid_integer_bounds",
                    f"Integer variable {variable.name!r} must have integer bounds.",
                    f"variables[{index}]",
                )
            )

    for constraint_index, constraint in enumerate(problem.constraints):
        if constraint.operator not in VALID_CONSTRAINT_OPERATORS:
            issues.append(
                ValidationIssue(
                    "invalid_constraint_operator",
                    (
                        f"Constraint {constraint_index} has invalid operator "
                        f"{constraint.operator!r}."
                    ),
                    f"constraints[{constraint_index}].operator",
                )
            )
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

    if problem.objective.sense not in VALID_OBJECTIVE_SENSES:
        issues.append(
            ValidationIssue(
                "invalid_objective_sense",
                f"Objective has invalid sense {problem.objective.sense!r}.",
                "objective.sense",
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
    *,
    validate_assignments: bool = False,
) -> tuple[ValidationIssue, ...]:
    """Validate that a solve report can be traced back to the problem rules."""

    issues: list[ValidationIssue] = []
    known_rule_ids = {rule.rule_id for rule in problem.rules}
    known_variable_names = {variable.name for variable in problem.variables}
    for index, rule_id in enumerate(report.rule_trace):
        if rule_id not in known_rule_ids:
            issues.append(
                ValidationIssue(
                    "unknown_report_rule",
                    f"Solve report references unknown rule_id {rule_id!r}.",
                    f"rule_trace[{index}]",
                )
            )

    if validate_assignments and report.status in {"optimal", "feasible"}:
        issues.extend(_validate_assignment_keys(report, known_variable_names))
        issues.extend(_validate_assignment_completeness(problem, report))
        issues.extend(_validate_assignment_values(problem, report))
        issues.extend(_validate_constraint_activity(problem, report))
    return tuple(issues)


def _validate_assignment_keys(
    report: SolveReport,
    known_variable_names: set[str],
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for variable_name in report.assignments:
        if variable_name not in known_variable_names:
            issues.append(
                ValidationIssue(
                    "unknown_assignment_variable",
                    f"Solve report assigns unknown variable {variable_name!r}.",
                    "assignments",
                )
            )
    return tuple(issues)


def _validate_assignment_completeness(
    problem: OptimizationProblem,
    report: SolveReport,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for variable in problem.variables:
        if variable.name not in report.assignments:
            issues.append(
                ValidationIssue(
                    "missing_assignment_value",
                    f"Solve report is missing assignment for variable {variable.name!r}.",
                    f"assignments[{variable.name}]",
                )
            )
    return tuple(issues)


def _validate_assignment_values(
    problem: OptimizationProblem,
    report: SolveReport,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    variables_by_name = {variable.name: variable for variable in problem.variables}
    for variable_name, value in report.assignments.items():
        variable = variables_by_name.get(variable_name)
        if variable is None:
            continue
        if not _is_numeric(value):
            issues.append(
                ValidationIssue(
                    "invalid_assignment_value",
                    f"Assignment for {variable_name!r} must be numeric.",
                    f"assignments[{variable_name}]",
                )
            )
            continue
        if value < variable.lower_bound or value > variable.upper_bound:
            issues.append(
                ValidationIssue(
                    "assignment_out_of_bounds",
                    (
                        f"Assignment {value!r} for {variable_name!r} is outside "
                        f"{variable.lower_bound!r}..{variable.upper_bound!r}."
                    ),
                    f"assignments[{variable_name}]",
                )
            )
        if variable.kind == "binary" and value not in {0, 1}:
            issues.append(
                ValidationIssue(
                    "invalid_binary_assignment",
                    f"Binary assignment for {variable_name!r} must be 0 or 1.",
                    f"assignments[{variable_name}]",
                )
            )
        if variable.kind == "integer" and not _is_integer_value(value):
            issues.append(
                ValidationIssue(
                    "invalid_integer_assignment",
                    f"Integer assignment for {variable_name!r} must be integral.",
                    f"assignments[{variable_name}]",
                )
            )
    return tuple(issues)


def _validate_constraint_activity(
    problem: OptimizationProblem,
    report: SolveReport,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for index, constraint in enumerate(problem.constraints):
        missing_variables = tuple(
            variable_name
            for variable_name in constraint.expression
            if variable_name not in report.assignments
        )
        if missing_variables:
            continue
        invalid_variables = tuple(
            variable_name
            for variable_name in constraint.expression
            if not _is_numeric(report.assignments[variable_name])
        )
        if invalid_variables:
            continue

        activity = sum(
            coefficient * report.assignments[variable_name]
            for variable_name, coefficient in constraint.expression.items()
        )
        if not _constraint_satisfied(activity, constraint.operator, constraint.rhs):
            issues.append(
                ValidationIssue(
                    "violated_constraint",
                    (
                        f"Solve report activity {activity!r} violates constraint "
                        f"{constraint.operator} {constraint.rhs!r}."
                    ),
                    f"constraints[{index}]",
                )
            )
    return tuple(issues)


def _valid_binary_bounds(
    lower_bound: int | float,
    upper_bound: int | float,
) -> bool:
    return (
        _is_integer_value(lower_bound)
        and _is_integer_value(upper_bound)
        and 0 <= lower_bound <= upper_bound <= 1
    )


def _is_numeric(value: object) -> bool:
    return isinstance(value, int | float)


def _is_integer_value(value: int | float) -> bool:
    return isinstance(value, int) or float(value).is_integer()


def _constraint_satisfied(
    activity: int | float,
    operator: str,
    rhs: int | float,
) -> bool:
    if operator == "<=":
        return activity <= rhs
    if operator == "==":
        return activity == rhs
    if operator == ">=":
        return activity >= rhs
    return False


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
