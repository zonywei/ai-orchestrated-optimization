from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    Objective,
    OptimizationProblem,
    RuleSpec,
    SolveReport,
    analyze_objective_contributions,
)


def test_objective_contribution_analysis_breaks_down_solution_value() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Contribution fixture", "Explain objective value.", "Test."),
        rules=(RuleSpec("soft.cost", "Prefer lower cost.", "soft"),),
        variables=(
            DecisionVariable("x", "binary"),
            DecisionVariable("y", "integer", 0, 5),
            DecisionVariable("z", "binary"),
        ),
        constraints=(),
        objective=Objective(
            "soft.cost",
            "minimize",
            {"x": 4, "y": -2, "z": 0},
        ),
    )
    report = SolveReport(
        status="optimal",
        objective_value=0,
        assignments={"x": 1, "y": 2, "z": 1},
        rule_trace=("soft.cost",),
    )

    analysis = analyze_objective_contributions(problem, report)

    assert analysis.rule_id == "soft.cost"
    assert analysis.sense == "minimize"
    assert analysis.total_contribution == 0
    assert analysis.missing_variables == ()
    assert [(item.variable_name, item.value, item.contribution, item.direction) for item in analysis.items] == [
        ("x", 1, 4, "increases_objective"),
        ("y", 2, -4, "reduces_objective"),
        ("z", 1, 0, "neutral"),
    ]


def test_objective_contribution_analysis_reports_missing_assignments() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Contribution fixture", "Explain incomplete reports.", "Test."),
        rules=(RuleSpec("soft.cost", "Prefer lower cost.", "soft"),),
        variables=(DecisionVariable("x", "binary"), DecisionVariable("y", "binary")),
        constraints=(),
        objective=Objective("soft.cost", "minimize", {"x": 3, "y": 5}),
    )
    report = SolveReport(
        status="feasible",
        objective_value=3,
        assignments={"x": 1},
        rule_trace=("soft.cost",),
    )

    analysis = analyze_objective_contributions(problem, report)

    assert analysis.is_complete is False
    assert analysis.missing_variables == ("y",)
    assert analysis.total_contribution == 3


def test_objective_contribution_analysis_reports_non_numeric_assignments() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Contribution fixture", "Explain invalid reports.", "Test."),
        rules=(RuleSpec("soft.cost", "Prefer lower cost.", "soft"),),
        variables=(DecisionVariable("x", "binary"),),
        constraints=(),
        objective=Objective("soft.cost", "minimize", {"x": 3}),
    )
    report = SolveReport(
        status="feasible",
        objective_value=None,
        assignments={"x": "north"},
        rule_trace=("soft.cost",),
    )

    analysis = analyze_objective_contributions(problem, report)

    assert analysis.is_complete is False
    assert analysis.invalid_variables == ("x",)
    assert analysis.items == ()
