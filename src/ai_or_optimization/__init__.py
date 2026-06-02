"""Public AI plus operations research framework primitives."""

from .agents import AgentRole, Handoff, build_default_agent_topology
from .audit import ConstraintAuditItem, ConstraintAuditReport, audit_constraints
from .contributions import (
    ObjectiveContribution,
    ObjectiveContributionReport,
    analyze_objective_contributions,
)
from .cp_sat_adapter import CpSatAdapter
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
from .diagnostics import (
    InfeasibilityDiagnosis,
    InfeasibilityFinding,
    diagnose_infeasibility,
)
from .demo_solver import solve_assignment_problem
from .planner import build_rule_first_plan
from .relaxations import (
    ConstraintRelaxationSuggestion,
    RelaxationReport,
    suggest_constraint_relaxations,
)
from .solver_adapters import (
    ExhaustiveAssignmentAdapter,
    SolverAdapter,
    SolverOptions,
    run_solver,
)
from .validation import ValidationIssue, validate_problem, validate_solve_report

__all__ = [
    "AgentRole",
    "BusinessBrief",
    "ConstraintAuditItem",
    "ConstraintAuditReport",
    "CpSatAdapter",
    "DecisionVariable",
    "ExhaustiveAssignmentAdapter",
    "Handoff",
    "InfeasibilityDiagnosis",
    "InfeasibilityFinding",
    "LinearConstraint",
    "Objective",
    "ObjectiveContribution",
    "ObjectiveContributionReport",
    "OptimizationProblem",
    "ConstraintRelaxationSuggestion",
    "RuleFirstPlan",
    "RuleSpec",
    "RelaxationReport",
    "SolveReport",
    "SolverAdapter",
    "SolverOptions",
    "ValidationIssue",
    "analyze_objective_contributions",
    "audit_constraints",
    "build_default_agent_topology",
    "build_rule_first_plan",
    "diagnose_infeasibility",
    "run_solver",
    "solve_assignment_problem",
    "suggest_constraint_relaxations",
    "validate_problem",
    "validate_solve_report",
]
