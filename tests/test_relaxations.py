from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    diagnose_infeasibility,
    suggest_constraint_relaxations,
)


def test_relaxation_suggestion_increases_too_low_upper_rhs() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Relaxation fixture", "Explain a strict upper bound.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", -1),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    report = suggest_constraint_relaxations(problem)

    assert report.has_suggestions is True
    suggestion = report.suggestions[0]
    assert suggestion.rule_id == "hard.capacity"
    assert suggestion.constraint_index == 0
    assert suggestion.current_rhs == -1
    assert suggestion.suggested_rhs == 0
    assert suggestion.delta == 1


def test_relaxation_suggestion_decreases_too_high_lower_rhs() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Relaxation fixture", "Explain a strict lower bound.", "Test."),
        rules=(RuleSpec("hard.coverage", "Cover demand.", "hard"),),
        variables=(DecisionVariable("x", "integer", 0, 3),),
        constraints=(LinearConstraint("hard.coverage", {"x": 1}, ">=", 4),),
        objective=Objective("hard.coverage", "minimize", {"x": 1}),
    )

    diagnosis = diagnose_infeasibility(problem)

    assert diagnosis.status == "structural_infeasible"
    assert "nearest reachable bound 3" in diagnosis.findings[0].suggested_action
