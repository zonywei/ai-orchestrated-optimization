"""Solver adapter interface for public AI OR workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .contracts import OptimizationProblem, SolveReport
from .demo_solver import solve_assignment_problem
from .planner import build_rule_first_plan
from .validation import validate_problem


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
        return SolveReport(
            status="not_run",
            objective_value=None,
            diagnostics=tuple(
                f"{issue.code} at {issue.location}: {issue.message}"
                for issue in validation_issues
            ),
        )
    return adapter.solve(problem, options)


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
        plan = build_rule_first_plan(problem.rules)
        return solve_assignment_problem(self.cost_by_item_and_slot, rule_trace=plan.rule_ids)
