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
            assignments={"x": 0},
            rule_trace=tuple(rule.rule_id for rule in problem.rules),
        )


class BadTraceAdapter:
    name = "bad_trace"
    capabilities = ("test",)

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        return SolveReport(
            status="feasible",
            objective_value=3,
            rule_trace=("unknown.rule",),
        )


class BadAssignmentAdapter:
    name = "bad_assignment"
    capabilities = ("test",)

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        return SolveReport(
            status="feasible",
            objective_value=3,
            assignments={"undeclared_variable": 1},
            rule_trace=tuple(rule.rule_id for rule in problem.rules),
        )


class ViolatingAssignmentAdapter:
    name = "violating_assignment"
    capabilities = ("test",)

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        return SolveReport(
            status="feasible",
            objective_value=1,
            assignments={"x": 1},
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


def test_run_solver_blocks_structural_infeasibility_before_adapter_execution() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Impossible adapter fixture", "Block impossible contracts.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary", 0, 1),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, ">=", 2),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )
    adapter = RecordingAdapter()

    report = run_solver(problem, adapter)

    assert adapter.called is False
    assert report.status == "infeasible"
    assert "structural_infeasible" in report.diagnostics[0]


def test_run_solver_rejects_adapter_report_with_unknown_rule_trace() -> None:
    report = run_solver(_valid_problem(), BadTraceAdapter())

    assert report.status == "not_run"
    assert "unknown_report_rule" in report.diagnostics[0]


def test_run_solver_rejects_adapter_report_with_unknown_assignment_variable() -> None:
    report = run_solver(_valid_problem(), BadAssignmentAdapter())

    assert report.status == "not_run"
    assert "unknown_assignment_variable" in report.diagnostics[0]


def test_run_solver_rejects_adapter_report_that_violates_constraints() -> None:
    problem = OptimizationProblem(
        brief=BusinessBrief("Solution validation fixture", "Reject bad adapter outputs.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary", 0, 1),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", 0),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )

    report = run_solver(problem, ViolatingAssignmentAdapter())

    assert report.status == "not_run"
    assert "violated_constraint" in report.diagnostics[0]


def test_exhaustive_assignment_adapter_runs_public_demo_solver() -> None:
    problem = _assignment_problem()
    adapter = ExhaustiveAssignmentAdapter(
        {
            "alpha": {"north": 4, "south": 7},
            "beta": {"north": 6, "south": 2},
        }
    )

    report = run_solver(problem, adapter)

    assert report.status == "optimal"
    assert report.objective_value == 6
    assert report.assignments == {
        "assign_alpha_north": 1,
        "assign_alpha_south": 0,
        "assign_beta_north": 0,
        "assign_beta_south": 1,
    }
    assert report.rule_trace == ("hard.capacity",)


def test_exhaustive_assignment_adapter_rejects_missing_assignment_variables() -> None:
    adapter = ExhaustiveAssignmentAdapter(
        {
            "alpha": {"north": 4},
        }
    )

    report = run_solver(_valid_problem(), adapter)

    assert report.status == "not_run"
    assert "missing_assignment_variable" in report.diagnostics[0]


def _valid_problem() -> OptimizationProblem:
    return OptimizationProblem(
        brief=BusinessBrief("Adapter fixture", "Run through a solver adapter.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(DecisionVariable("x", "binary"),),
        constraints=(LinearConstraint("hard.capacity", {"x": 1}, "<=", 1),),
        objective=Objective("hard.capacity", "minimize", {"x": 1}),
    )


def _assignment_problem() -> OptimizationProblem:
    return OptimizationProblem(
        brief=BusinessBrief("Assignment adapter fixture", "Run through a solver adapter.", "Test."),
        rules=(RuleSpec("hard.capacity", "Respect capacity.", "hard"),),
        variables=(
            DecisionVariable("assign_alpha_north", "binary"),
            DecisionVariable("assign_alpha_south", "binary"),
            DecisionVariable("assign_beta_north", "binary"),
            DecisionVariable("assign_beta_south", "binary"),
        ),
        constraints=(
            LinearConstraint(
                "hard.capacity",
                {"assign_alpha_north": 1, "assign_beta_north": 1},
                "<=",
                1,
            ),
        ),
        objective=Objective(
            "hard.capacity",
            "minimize",
            {
                "assign_alpha_north": 4,
                "assign_alpha_south": 7,
                "assign_beta_north": 6,
                "assign_beta_south": 2,
            },
        ),
    )
