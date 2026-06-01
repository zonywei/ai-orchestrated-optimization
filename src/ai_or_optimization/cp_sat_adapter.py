"""OR-Tools CP-SAT adapter for public optimization contracts."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import DecisionVariable, OptimizationProblem, SolveReport
from .planner import build_rule_first_plan
from .solver_adapters import SolverOptions

try:  # pragma: no cover - exercised when optional dependency is absent.
    from ortools.sat.python import cp_model
except ModuleNotFoundError:  # pragma: no cover
    cp_model = None


@dataclass(frozen=True)
class CpSatAdapter:
    """Adapter that solves integer public contracts with OR-Tools CP-SAT."""

    name: str = "ortools.cp_sat"
    capabilities: tuple[str, ...] = ("binary", "integer", "linear", "cp_sat")

    def solve(
        self,
        problem: OptimizationProblem,
        options: SolverOptions | None = None,
    ) -> SolveReport:
        if cp_model is None:
            return SolveReport(
                status="not_run",
                objective_value=None,
                diagnostics=("ortools_not_installed: install ai-or-optimization[cp-sat]",),
            )

        unsupported = tuple(
            variable.name for variable in problem.variables if variable.kind == "continuous"
        )
        if unsupported:
            return SolveReport(
                status="not_run",
                objective_value=None,
                diagnostics=tuple(
                    f"unsupported_variable_kind: {variable_name} is continuous"
                    for variable_name in unsupported
                ),
            )

        non_integer_values = _non_integer_model_values(problem)
        if non_integer_values:
            return SolveReport(
                status="not_run",
                objective_value=None,
                diagnostics=tuple(
                    f"non_integer_cp_sat_value: {value_name}" for value_name in non_integer_values
                ),
            )

        model = cp_model.CpModel()
        cp_variables = {
            variable.name: _new_cp_variable(model, variable)
            for variable in problem.variables
        }
        for constraint in problem.constraints:
            expression = _linear_expression(cp_variables, constraint.expression)
            if constraint.operator == "<=":
                model.Add(expression <= int(constraint.rhs))
            elif constraint.operator == "==":
                model.Add(expression == int(constraint.rhs))
            elif constraint.operator == ">=":
                model.Add(expression >= int(constraint.rhs))

        objective = _linear_expression(cp_variables, problem.objective.coefficients)
        if problem.objective.sense == "minimize":
            model.Minimize(objective)
        else:
            model.Maximize(objective)

        solver = cp_model.CpSolver()
        if options is not None:
            if options.time_limit_seconds is not None:
                solver.parameters.max_time_in_seconds = options.time_limit_seconds
            if options.random_seed is not None:
                solver.parameters.random_seed = options.random_seed

        status_code = solver.Solve(model)
        status_name = solver.StatusName(status_code)
        if status_code == cp_model.OPTIMAL:
            status = "optimal"
        elif status_code == cp_model.FEASIBLE:
            status = "feasible"
        elif status_code == cp_model.INFEASIBLE:
            status = "infeasible"
        else:
            status = "not_run"

        if status not in {"optimal", "feasible"}:
            return SolveReport(
                status=status,
                objective_value=None,
                rule_trace=build_rule_first_plan(problem.rules).rule_ids,
                diagnostics=(f"cp_sat_status={status_name}",),
            )

        return SolveReport(
            status=status,
            objective_value=solver.ObjectiveValue(),
            assignments={
                variable.name: solver.Value(cp_variables[variable.name])
                for variable in problem.variables
            },
            rule_trace=build_rule_first_plan(problem.rules).rule_ids,
            diagnostics=(f"cp_sat_status={status_name}",),
        )


def _new_cp_variable(model: object, variable: DecisionVariable) -> object:
    lower_bound = int(variable.lower_bound)
    upper_bound = int(variable.upper_bound)
    if variable.kind == "binary":
        return model.NewBoolVar(variable.name)
    return model.NewIntVar(lower_bound, upper_bound, variable.name)


def _linear_expression(
    cp_variables: dict[str, object],
    coefficients: dict[str, int | float],
) -> object:
    return sum(
        int(coefficient) * cp_variables[variable_name]
        for variable_name, coefficient in coefficients.items()
    )


def _non_integer_model_values(problem: OptimizationProblem) -> tuple[str, ...]:
    value_names: list[str] = []
    for variable in problem.variables:
        if not _is_integer(variable.lower_bound):
            value_names.append(f"{variable.name}.lower_bound")
        if not _is_integer(variable.upper_bound):
            value_names.append(f"{variable.name}.upper_bound")
    for index, constraint in enumerate(problem.constraints):
        if not _is_integer(constraint.rhs):
            value_names.append(f"constraints[{index}].rhs")
        for variable_name, coefficient in constraint.expression.items():
            if not _is_integer(coefficient):
                value_names.append(f"constraints[{index}].expression[{variable_name}]")
    for variable_name, coefficient in problem.objective.coefficients.items():
        if not _is_integer(coefficient):
            value_names.append(f"objective.coefficients[{variable_name}]")
    return tuple(value_names)


def _is_integer(value: int | float) -> bool:
    return isinstance(value, int) or float(value).is_integer()
