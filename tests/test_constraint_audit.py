from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    audit_constraints,
)


def test_constraint_audit_computes_activity_range_and_binding_status() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Capacity audit", "Audit public constraints.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(
            DecisionVariable("x", "integer", 0, 3),
            DecisionVariable("y", "integer", 2, 5),
        ),
        constraints=(
            LinearConstraint("hard.capacity", {"x": 2, "y": -1}, "<=", 3),
        ),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    report = audit_constraints(problem)

    assert report.summary_by_status == {"binding_candidate": 1}
    assert report.items[0].activity_min == -5
    assert report.items[0].activity_max == 4
    assert report.items[0].status == "binding_candidate"


def test_constraint_audit_detects_always_satisfied_and_always_violated() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Constraint audit", "Audit public constraints.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(
            LinearConstraint("hard.capacity", {"x": 1}, "<=", 5),
            LinearConstraint("hard.capacity", {"x": 1}, ">=", 4),
            LinearConstraint("hard.capacity", {"x": 1}, "==", 9),
        ),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    report = audit_constraints(problem)

    assert [item.status for item in report.items] == [
        "always_satisfied",
        "always_violated",
        "always_violated",
    ]
    assert report.summary_by_status == {
        "always_satisfied": 1,
        "always_violated": 2,
    }


def test_constraint_audit_reports_unknown_variable_reference() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Constraint audit", "Audit public constraints.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.capacity", {"missing": 1}, "<=", 1),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    report = audit_constraints(problem)

    assert report.items[0].status == "invalid_reference"
    assert report.items[0].unknown_variables == ("missing",)
