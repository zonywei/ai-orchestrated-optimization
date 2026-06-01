from __future__ import annotations

import json
from pathlib import Path

from ai_or_optimization import (
    BusinessBrief,
    CpSatAdapter,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    SolverOptions,
    analyze_objective_contributions,
    diagnose_infeasibility,
    run_solver,
)


EXAMPLE_PATH = Path(__file__).with_name("workforce_rostering_cp_sat.json")


def build_problem(data: dict[str, object]) -> OptimizationProblem:
    operators = data["operators"]
    shifts = data["shifts"]
    costs = data["costs"]

    rules = (
        RuleSpec("hard.coverage", "Every demand slot receives exactly one operator.", "hard", 100),
        RuleSpec("hard.capacity", "Each operator stays within its maximum slot count.", "hard", 90),
        RuleSpec("hard.skill_fit", "Operators can only cover slots matching their skills.", "hard", 80),
        RuleSpec("soft.assignment_cost", "Prefer lower-cost operator-slot assignments.", "soft", 50),
    )
    variables = tuple(
        DecisionVariable(
            _variable_name(operator["id"], shift["id"]),
            "binary",
            description=f"{operator['id']} covers {shift['id']}.",
        )
        for operator in operators
        for shift in shifts
    )

    constraints: list[LinearConstraint] = []
    for shift in shifts:
        constraints.append(
            LinearConstraint(
                "hard.coverage",
                {
                    _variable_name(operator["id"], shift["id"]): 1
                    for operator in operators
                },
                "==",
                1,
                f"{shift['id']} receives exactly one operator.",
            )
        )

    for operator in operators:
        constraints.append(
            LinearConstraint(
                "hard.capacity",
                {
                    _variable_name(operator["id"], shift["id"]): 1
                    for shift in shifts
                },
                "<=",
                operator["max_slots"],
                f"{operator['id']} stays within capacity.",
            )
        )

    for operator in operators:
        for shift in shifts:
            if shift["required_skill"] not in operator["skills"]:
                variable_name = _variable_name(operator["id"], shift["id"])
                constraints.append(
                    LinearConstraint(
                        "hard.skill_fit",
                        {variable_name: 1},
                        "==",
                        0,
                        f"{variable_name} is blocked by skill fit.",
                    )
                )

    objective = Objective(
        "soft.assignment_cost",
        "minimize",
        {
            _variable_name(operator["id"], shift["id"]): costs[operator["id"]][shift["id"]]
            for operator in operators
            for shift in shifts
        },
        "Minimize public synthetic assignment cost.",
    )
    return OptimizationProblem(
        brief=BusinessBrief(data["title"], data["goal"], "Synthetic public CP-SAT example."),
        rules=rules,
        variables=variables,
        constraints=tuple(constraints),
        objective=objective,
    )


def main() -> None:
    data = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    problem = build_problem(data)
    report = run_solver(
        problem,
        CpSatAdapter(),
        SolverOptions(time_limit_seconds=10, random_seed=7),
    )
    diagnosis = diagnose_infeasibility(problem, report)
    contributions = analyze_objective_contributions(problem, report)

    print(f"status={report.status}")
    print(f"objective={report.objective_value}")
    print(f"rule_trace={report.rule_trace}")
    print(f"diagnosis={diagnosis.status}")
    print(f"contribution_total={contributions.total_contribution}")
    for shift in data["shifts"]:
        assigned = _assigned_operator_for_shift(report.assignments, data["operators"], shift["id"])
        print(f"{shift['id']}={assigned}")


def _variable_name(operator_id: str, shift_id: str) -> str:
    return f"assign_{operator_id}_{shift_id}"


def _assigned_operator_for_shift(
    assignments: dict[str, object],
    operators: list[dict[str, object]],
    shift_id: str,
) -> str:
    for operator in operators:
        variable_name = _variable_name(operator["id"], shift_id)
        if assignments.get(variable_name) == 1:
            return operator["id"]
    return "unassigned"


if __name__ == "__main__":
    main()
