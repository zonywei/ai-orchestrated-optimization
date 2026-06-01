from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    build_rule_first_plan,
    solve_assignment_problem,
)


def build_demo_problem() -> OptimizationProblem:
    brief = BusinessBrief(
        title="Anonymous resource allocation",
        goal="Assign work items to available capacity with explainable tradeoffs.",
        context="A public example for AI-assisted operations research workflows.",
        success_metrics=("minimize total cost", "keep rule trace readable"),
    )
    rules = (
        RuleSpec("hard.one_item_one_slot", "Each work item is assigned exactly once.", "hard", 100),
        RuleSpec("hard.capacity_one", "Each slot accepts at most one work item.", "hard", 90),
        RuleSpec("soft.cost_efficiency", "Prefer lower-cost assignments.", "soft", 50),
    )
    variables = (
        DecisionVariable("assign_alpha_north", "binary", description="Alpha assigned to north."),
        DecisionVariable("assign_beta_south", "binary", description="Beta assigned to south."),
    )
    constraints = (
        LinearConstraint(
            "hard.one_item_one_slot",
            {"assign_alpha_north": 1},
            "<=",
            1,
            "Public placeholder constraint for the demo contract.",
        ),
    )
    objective = Objective(
        "soft.cost_efficiency",
        "minimize",
        {"assign_alpha_north": 4, "assign_beta_south": 2},
        "Minimize total assignment cost.",
    )
    return OptimizationProblem(brief, rules, variables, constraints, objective)


def main() -> None:
    problem = build_demo_problem()
    plan = build_rule_first_plan(problem.rules)
    report = solve_assignment_problem(
        {
            "alpha": {"north": 4, "south": 7, "east": 8},
            "beta": {"north": 6, "south": 2, "east": 5},
            "gamma": {"north": 9, "south": 6, "east": 3},
        },
        rule_trace=plan.rule_ids,
    )
    print(f"status={report.status}")
    print(f"objective={report.objective_value}")
    print(f"assignments={report.assignments}")


if __name__ == "__main__":
    main()
