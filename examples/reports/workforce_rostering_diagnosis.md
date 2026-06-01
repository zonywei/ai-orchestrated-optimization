# Synthetic Workforce Rostering Diagnosis

This curated public report demonstrates the CP-SAT example without exposing any private vertical assets.

## Input Scale

- Operators: 6
- Demand slots: 5
- Binary decision variables: 30
- Rule groups: coverage, capacity, skill fit, assignment cost

## Expected Result

The model should solve to an optimal public plan. Each demand slot receives exactly one qualified operator, each operator stays within capacity, and the objective explains the selected operator-slot cost.

## Diagnostic Path

The example runs through the same public framework boundary as other adapters:

```text
OptimizationProblem
  -> validate_problem
  -> audit_constraints
  -> CpSatAdapter
  -> validate_solve_report
  -> diagnose_infeasibility
  -> analyze_objective_contributions
```

This is a synthetic reference case. It is not derived from private production data, historical outputs, or private vertical rules.
