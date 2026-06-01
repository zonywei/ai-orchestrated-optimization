from ai_or_optimization import (
    RuleSpec,
    build_default_agent_topology,
    build_rule_first_plan,
    solve_assignment_problem,
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
