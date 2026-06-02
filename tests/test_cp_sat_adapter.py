import json
import subprocess
import sys
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
    run_solver,
)


def test_cp_sat_adapter_solves_binary_linear_problem() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("CP-SAT fixture", "Select the lowest-cost feasible option.", "Test."),
        rules=(
            RuleSpec("hard.coverage", "Select at least one option.", "hard", 100),
            RuleSpec("soft.cost", "Prefer lower cost.", "soft", 10),
        ),
        variables=(
            DecisionVariable("x", "binary"),
            DecisionVariable("y", "binary"),
        ),
        constraints=(LinearConstraint("hard.coverage", {"x": 1, "y": 1}, ">=", 1),),
        objective=Objective("soft.cost", "minimize", {"x": 1, "y": 3}),
    )

    report = run_solver(problem, CpSatAdapter(), SolverOptions(time_limit_seconds=5))

    assert report.status == "optimal"
    assert report.assignments == {"x": 1, "y": 0}
    assert report.rule_trace == ("hard.coverage", "soft.cost")


def test_cp_sat_adapter_reports_unsupported_public_continuous_variable() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("CP-SAT fixture", "Reject unsupported variable kinds.", "Test."),
        rules=(RuleSpec("soft.cost", "Prefer lower cost.", "soft"),),
        variables=(DecisionVariable("x", "continuous", 0, 1),),
        constraints=(),
        objective=Objective("soft.cost", "minimize", {"x": 1}),
    )

    report = run_solver(problem, CpSatAdapter())

    assert report.status == "not_run"
    assert "unsupported_variable_kind" in report.diagnostics[0]


def test_cp_sat_adapter_honors_fixed_binary_bounds() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("CP-SAT fixture", "Honor fixed public binary bounds.", "Test."),
        rules=(RuleSpec("soft.cost", "Prefer lower cost.", "soft"),),
        variables=(
            DecisionVariable("x", "binary", 1, 1),
            DecisionVariable("y", "binary", 0, 0),
        ),
        constraints=(),
        objective=Objective("soft.cost", "minimize", {"x": 1, "y": 1}),
    )

    report = run_solver(problem, CpSatAdapter(), SolverOptions(time_limit_seconds=5))

    assert report.status == "optimal"
    assert report.objective_value == 1
    assert report.assignments == {"x": 1, "y": 0}


def test_workforce_cp_sat_example_is_synthetic_and_runs() -> None:
    data = json.loads(Path("examples/workforce_rostering_cp_sat.json").read_text(encoding="utf-8"))
    assert len(data["operators"]) * len(data["shifts"]) == 30
    assert data["source"] == "synthetic_public_example"

    result = subprocess.run(
        [sys.executable, "examples/cp_sat_workforce_demo.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "status=optimal" in result.stdout
    assert "objective=" in result.stdout
    assert "slot_1" in result.stdout
