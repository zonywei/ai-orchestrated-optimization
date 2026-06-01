"""Infeasibility diagnostics for public optimization contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .audit import audit_constraints
from .contracts import OptimizationProblem, SolveReport


DiagnosisStatus = Literal[
    "structural_infeasible",
    "solver_reported_infeasible",
    "no_infeasibility_detected",
]


@dataclass(frozen=True)
class InfeasibilityFinding:
    """One human-readable reason an optimization problem may be infeasible."""

    rule_id: str
    message: str
    constraint_index: int | None = None
    suggested_action: str = ""


@dataclass(frozen=True)
class InfeasibilityDiagnosis:
    """A compact diagnosis that connects infeasibility evidence to rules."""

    status: DiagnosisStatus
    findings: tuple[InfeasibilityFinding, ...] = ()

    @property
    def implicated_rule_ids(self) -> tuple[str, ...]:
        rule_ids: list[str] = []
        for finding in self.findings:
            if finding.rule_id not in rule_ids:
                rule_ids.append(finding.rule_id)
        return tuple(rule_ids)


def diagnose_infeasibility(
    problem: OptimizationProblem,
    report: SolveReport | None = None,
) -> InfeasibilityDiagnosis:
    """Explain structural or reported infeasibility in rule-level terms."""

    audit_report = audit_constraints(problem)
    structural_findings = tuple(
        InfeasibilityFinding(
            rule_id=item.rule_id,
            constraint_index=item.constraint_index,
            message=(
                f"Constraint {item.constraint_index} cannot be satisfied under declared "
                f"variable bounds: activity range {_format_range(item.activity_min, item.activity_max)} "
                f"{item.operator} {item.rhs}."
            ),
            suggested_action=(
                "Check the linked rule, variable bounds, coefficient signs, or RHS."
            ),
        )
        for item in audit_report.violated_items
    )
    if structural_findings:
        return InfeasibilityDiagnosis("structural_infeasible", structural_findings)

    if report is not None and report.status == "infeasible":
        return InfeasibilityDiagnosis(
            "solver_reported_infeasible",
            _findings_from_solve_report(problem, report),
        )

    return InfeasibilityDiagnosis("no_infeasibility_detected")


def _findings_from_solve_report(
    problem: OptimizationProblem,
    report: SolveReport,
) -> tuple[InfeasibilityFinding, ...]:
    rule_ids = report.rule_trace or tuple(rule.rule_id for rule in problem.rules if rule.is_hard())
    messages = report.diagnostics or ("Solver reported infeasibility without diagnostics.",)
    findings: list[InfeasibilityFinding] = []
    for message in messages:
        for rule_id in rule_ids:
            findings.append(
                InfeasibilityFinding(
                    rule_id=rule_id,
                    message=message,
                    suggested_action="Inspect the linked rule and nearby hard constraints.",
                )
            )
    return tuple(findings)


def _format_range(
    activity_min: int | float | None,
    activity_max: int | float | None,
) -> str:
    return f"{activity_min}..{activity_max}"
