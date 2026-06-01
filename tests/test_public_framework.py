from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    SolveReport,
    build_default_agent_topology,
    build_rule_first_plan,
    solve_assignment_problem,
    validate_problem,
    validate_solve_report,
)


def test_agent_topology_has_expected_handoffs() -> None:
    roles, handoffs = build_default_agent_topology()

    assert [role.role_id for role in roles] == [
        "business_expert",
        "chief_architect",
        "mathematical_modeler",
        "reduction_optimizer",
        "execution_agent",
        "diagnostics_agent",
    ]
    assert handoffs[-1].artifact == "solve_report"


def test_rule_first_plan_orders_hard_rules_before_soft_rules() -> None:
    rules = (
        RuleSpec("soft.cost", "Prefer lower cost.", "soft", 100),
        RuleSpec("hard.capacity", "Respect capacity.", "hard", 10),
        RuleSpec("hard.coverage", "Cover required demand.", "hard", 20),
    )

    plan = build_rule_first_plan(rules)

    assert plan.rule_ids == ("hard.coverage", "hard.capacity", "soft.cost")


def test_demo_solver_finds_lowest_cost_assignment() -> None:
    report = solve_assignment_problem(
        {
            "alpha": {"north": 4, "south": 7, "east": 8},
            "beta": {"north": 6, "south": 2, "east": 5},
            "gamma": {"north": 9, "south": 6, "east": 3},
        },
        rule_trace=("hard.capacity", "soft.cost"),
    )

    assert report.status == "optimal"
    assert report.objective_value == 9
    assert report.assignments == {"alpha": "north", "beta": "south", "gamma": "east"}
    assert report.rule_trace == ("hard.capacity", "soft.cost")


def test_demo_solver_reports_infeasible_when_slots_are_missing() -> None:
    report = solve_assignment_problem(
        {
            "alpha": {"north": 1},
            "beta": {"north": 2},
        }
    )

    assert report.status == "infeasible"
    assert report.objective_value is None


def test_validation_accepts_traceable_problem_and_report() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief(
            "Anonymous resource allocation",
            "Assign scarce capacity with explainable tradeoffs.",
            "Public validation fixture.",
        ),
        rules=(
            RuleSpec("hard.capacity", "Respect capacity.", "hard", 100),
            RuleSpec("soft.cost", "Prefer lower cost.", "soft", 50),
        ),
        variables=(
            DecisionVariable("assign_alpha_north", "binary", 0, 1),
            DecisionVariable("assign_alpha_south", "binary", 0, 1),
        ),
        constraints=(
            LinearConstraint(
                "hard.capacity",
                {"assign_alpha_north": 1, "assign_alpha_south": 1},
                "<=",
                1,
            ),
        ),
        objective=Objective(
            "soft.cost",
            "minimize",
            {"assign_alpha_north": 4, "assign_alpha_south": 7},
        ),
    )
    report = SolveReport(
        status="optimal",
        objective_value=4,
        assignments={"assign_alpha_north": 1, "assign_alpha_south": 0},
        rule_trace=("hard.capacity", "soft.cost"),
    )

    assert validate_problem(problem) == ()
    assert validate_solve_report(problem, report) == ()


def test_validation_reports_unknown_rule_and_variable_references() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Invalid public fixture", "Expose validation failures.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary"),),
        constraints=(
            LinearConstraint("hard.missing", {"x": 1, "y": 1}, "<=", 1),
        ),
        objective=Objective("soft.missing", "minimize", {"z": 3}),
    )

    issues = validate_problem(problem)

    assert [issue.code for issue in issues] == [
        "unknown_constraint_rule",
        "unknown_constraint_variable",
        "unknown_objective_rule",
        "unknown_objective_variable",
    ]


def test_validation_reports_duplicate_ids_invalid_bounds_and_unknown_report_trace() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Invalid public fixture", "Expose validation failures.", "Test."),
        rules=(
            RuleSpec("hard.capacity", "Respect capacity.", "hard"),
            RuleSpec("hard.capacity", "Duplicate rule.", "hard"),
        ),
        variables=(
            DecisionVariable("x", "binary", 2, 1),
            DecisionVariable("x", "binary"),
        ),
        constraints=(),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )
    report = SolveReport(
        status="feasible",
        objective_value=1,
        assignments={"x": 1},
        rule_trace=("hard.capacity", "soft.unknown"),
    )

    problem_issues = validate_problem(problem)
    report_issues = validate_solve_report(problem, report)

    assert [issue.code for issue in problem_issues] == [
        "duplicate_rule_id",
        "duplicate_variable_name",
        "invalid_variable_bounds",
    ]
    assert [issue.code for issue in report_issues] == ["unknown_report_rule"]
