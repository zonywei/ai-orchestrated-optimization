"""Public contracts for rule-first AI optimization workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


RuleKind = Literal["hard", "soft"]
VariableKind = Literal["binary", "integer", "continuous"]
ObjectiveSense = Literal["minimize", "maximize"]
SolveStatus = Literal["optimal", "feasible", "infeasible", "not_run"]


@dataclass(frozen=True)
class BusinessBrief:
    """Human-readable business intent before mathematical modeling."""

    title: str
    goal: str
    context: str
    success_metrics: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleSpec:
    """A business rule that must be traceable through the model."""

    rule_id: str
    description: str
    kind: RuleKind
    priority: int = 0
    source: str = "public_example"

    def is_hard(self) -> bool:
        return self.kind == "hard"


@dataclass(frozen=True)
class DecisionVariable:
    """A public variable declaration."""

    name: str
    kind: VariableKind
    lower_bound: int | float = 0
    upper_bound: int | float = 1
    description: str = ""


@dataclass(frozen=True)
class LinearConstraint:
    """A simple linear constraint descriptor for public examples."""

    rule_id: str
    expression: dict[str, int | float]
    operator: Literal["<=", "==", ">="]
    rhs: int | float
    description: str = ""


@dataclass(frozen=True)
class Objective:
    """A linear objective descriptor."""

    rule_id: str
    sense: ObjectiveSense
    coefficients: dict[str, int | float]
    description: str = ""


@dataclass(frozen=True)
class OptimizationProblem:
    """A complete public problem contract."""

    brief: BusinessBrief
    rules: tuple[RuleSpec, ...]
    variables: tuple[DecisionVariable, ...]
    constraints: tuple[LinearConstraint, ...]
    objective: Objective


@dataclass(frozen=True)
class RuleFirstPlan:
    """Rules ordered before model execution."""

    ordered_rules: tuple[RuleSpec, ...]

    @property
    def rule_ids(self) -> tuple[str, ...]:
        return tuple(rule.rule_id for rule in self.ordered_rules)


@dataclass(frozen=True)
class SolveReport:
    """Public solve output with rule trace and diagnostics."""

    status: SolveStatus
    objective_value: int | float | None
    assignments: dict[str, Any] = field(default_factory=dict)
    rule_trace: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
