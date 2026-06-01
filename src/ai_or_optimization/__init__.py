"""Public AI plus operations research framework primitives."""

from .agents import AgentRole, Handoff, build_default_agent_topology
from .contracts import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleFirstPlan,
    RuleSpec,
    SolveReport,
)
from .demo_solver import solve_assignment_problem
from .planner import build_rule_first_plan
from .validation import ValidationIssue, validate_problem, validate_solve_report

__all__ = [
    "AgentRole",
    "BusinessBrief",
    "DecisionVariable",
    "Handoff",
    "LinearConstraint",
    "Objective",
    "OptimizationProblem",
    "RuleFirstPlan",
    "RuleSpec",
    "SolveReport",
    "ValidationIssue",
    "build_default_agent_topology",
    "build_rule_first_plan",
    "solve_assignment_problem",
    "validate_problem",
    "validate_solve_report",
]
