from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    SolveReport,
    diagnose_infeasibility,
)


def test_diagnostics_identifies_structural_infeasibility_from_constraint_audit() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Diagnostic fixture", "Explain impossible bounds.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, ">=", 4),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    diagnosis = diagnose_infeasibility(problem)

    assert diagnosis.status == "structural_infeasible"
    assert diagnosis.implicated_rule_ids == ("hard.capacity",)
    assert diagnosis.findings[0].constraint_index == 0
    assert "0..3" in diagnosis.findings[0].message


def test_diagnostics_uses_infeasible_solve_report_when_audit_has_no_structural_failure() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Diagnostic fixture", "Explain solver report.", "Test."),
        rules=(
            RuleSpec("hard.coverage", "Cover demand.", "hard"),
            RuleSpec("hard.capacity", "Respect capacity.", "hard"),
        ),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", 3),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )
    report = SolveReport(
        status="infeasible",
        objective_value=None,
        rule_trace=("hard.coverage", "hard.capacity"),
        diagnostics=("Solver found no feasible assignment.",),
    )

    diagnosis = diagnose_infeasibility(problem, report)

    assert diagnosis.status == "solver_reported_infeasible"
    assert diagnosis.implicated_rule_ids == ("hard.coverage", "hard.capacity")
    assert diagnosis.findings[0].message == "Solver found no feasible assignment."


def test_diagnostics_reports_no_infeasibility_when_audit_and_report_are_clean() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Diagnostic fixture", "Explain clean case.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", 3),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )
    report = SolveReport(status="optimal", objective_value=0)

    diagnosis = diagnose_infeasibility(problem, report)

    assert diagnosis.status == "no_infeasibility_detected"
    assert diagnosis.findings == ()
