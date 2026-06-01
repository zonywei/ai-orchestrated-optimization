from ai_or_optimization import (
    BusinessBrief,
    DecisionVariable,
    ExhaustiveAssignmentAdapter,
    LinearConstraint,
    Objective,
    OptimizationProblem,
    RuleSpec,
    SolveReport,
    SolverOptions,
    run_solver,
)


class RecordingAdapter:
    name = "recording"
    capabilities = ("test",)

    def __init__(self) -> None:
        self.called = False
        self.options: SolverOptions | None = None

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        self.called = True
        self.options = options
        return SolveReport(
            status="feasible",
            objective_value=3,
            rule_trace=tuple(rule.rule_id for rule in problem.rules),
        )


def test_run_solver_delegates_valid_problem_to_adapter() -> None:
    problem = _valid_problem()
    adapter = RecordingAdapter()
    options = SolverOptions(time_limit_seconds=5.0, random_seed=7)

    report = run_solver(problem, adapter, options)

    assert adapter.called is True
    assert adapter.options == options
    assert report.status == "feasible"
    assert report.rule_trace == ("hard.capacity",)


def test_run_solver_blocks_invalid_problem_before_adapter_execution() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Invalid adapter fixture", "Block invalid contracts.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary"),),
        constraints=(),
        objective=Objective("hard.capacity", "minimize", {"missing": 1}),
    )
    adapter = RecordingAdapter()

    report = run_solver(problem, adapter)

    assert adapter.called is False
    assert report.status == "not_run"
    assert "unknown_objective_variable" in report.diagnostics[0]


def test_exhaustive_assignment_adapter_runs_public_demo_solver() -> None:
    problem = _valid_problem()
    adapter = ExhaustiveAssignmentAdapter(
        {
            "alpha": {"north": 4, "south": 7, "east": 8},
            "beta": {"north": 6, "south": 2, "east": 5},
            "gamma": {"north": 9, "south": 6, "east": 3},
        }
    )

    report = run_solver(problem, adapter)

    assert report.status == "optimal"
    assert report.objective_value == 9
    assert report.rule_trace == ("hard.capacity",)


def _valid_problem() -> OptimizationProblem:
    return OptimizationProblem(
        brief=BusinessBrief("Adapter fixture", "Run through a solver adapter.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary"),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", 1),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )
