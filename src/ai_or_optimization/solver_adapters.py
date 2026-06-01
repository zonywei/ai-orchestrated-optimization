"""Solver adapter interface for public AI OR workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .audit import audit_constraints
from .contracts import OptimizationProblem, SolveReport
from .demo_solver import solve_assignment_problem
from .planner import build_rule_first_plan
from .validation import ValidationIssue, validate_problem, validate_solve_report


@dataclass(frozen=True)
class SolverOptions:
    """Portable options that adapter implementations may honor."""

    time_limit_seconds: float | None = None
    random_seed: int | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class SolverAdapter(Protocol):
    """Minimal protocol for plugging a solver behind the public contracts."""

    name: str
    capabilities: tuple[str, ...]

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        """Solve a validated optimization problem."""


def run_solver(
    problem: OptimizationProblem,
    adapter: SolverAdapter,
    options: SolverOptions | None = None,
) -> SolveReport:
    """Validate a problem and delegate execution to a solver adapter."""

    validation_issues = validate_problem(problem)
    if validation_issues:
        return _not_run_from_issues(validation_issues)

    audit_report = audit_constraints(problem)
    if audit_report.violated_items:
        return SolveReport(
            status="infeasible",
            objective_value=None,
            rule_trace=tuple(item.rule_id for item in audit_report.violated_items),
            diagnostics=tuple(
                (
                    "structural_infeasible: "
                    f"constraint {item.constraint_index} has activity range "
                    f"{item.activity_min}..{item.activity_max} {item.operator} {item.rhs}"
                )
                for item in audit_report.violated_items
            ),
        )

    report = adapter.solve(problem, options)
    report_issues = validate_solve_report(problem, report, validate_assignments=True)
    if report_issues:
        return _not_run_from_issues(report_issues)
    return report


@dataclass(frozen=True)
class ExhaustiveAssignmentAdapter:
    """Public demo adapter that wraps the tiny exhaustive assignment solver."""

    cost_by_item_and_slot: dict[str, dict[str, int]]
    name: str = "public.exhaustive_assignment"
    capabilities: tuple[str, ...] = ("assignment", "exhaustive", "demo")

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        missing_variables = self._missing_assignment_variables(problem)
        if missing_variables:
            return SolveReport(
                status="not_run",
                objective_value=None,
                diagnostics=tuple(
                    f"missing_assignment_variable: {variable_name}"
                    for variable_name in missing_variables
                ),
            )

        plan = build_rule_first_plan(problem.rules)
        report = solve_assignment_problem(self.cost_by_item_and_slot, rule_trace=plan.rule_ids)
        if report.status not in {"optimal", "feasible"}:
            return report
        return SolveReport(
            status=report.status,
            objective_value=report.objective_value,
            assignments=self._to_variable_assignments(report.assignments),
            rule_trace=report.rule_trace,
            diagnostics=report.diagnostics,
        )

    def _missing_assignment_variables(self, problem: OptimizationProblem) -> tuple[str, ...]:
        declared_variables = {variable.name for variable in problem.variables}
        return tuple(
            variable_name
            for variable_name in self._assignment_variable_names()
            if variable_name not in declared_variables
        )

    def _assignment_variable_names(self) -> tuple[str, ...]:
        return tuple(
            f"assign_{item}_{slot}"
            for item, slot_costs in self.cost_by_item_and_slot.items()
            for slot in slot_costs
        )

    def _to_variable_assignments(self, assignments: dict[str, object]) -> dict[str, int]:
        return {
            f"assign_{item}_{slot}": 1 if assignments.get(item) == slot else 0
            for item, slot_costs in self.cost_by_item_and_slot.items()
            for slot in slot_costs
        }


def _not_run_from_issues(issues: tuple[ValidationIssue, ...]) -> SolveReport:
    return SolveReport(
        status="not_run",
        objective_value=None,
        diagnostics=tuple(
            f"{issue.code} at {issue.location}: {issue.message}"
            for issue in issues
        ),
    )
