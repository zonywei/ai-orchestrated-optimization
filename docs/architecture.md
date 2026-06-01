# Architecture

AI-Orchestrated Optimization separates business language from mathematical execution through explicit, inspectable artifacts.

```text
Business Expert
  -> Chief Architect Agent
    -> Mathematical Modeling Agent
    -> Reduction and Optimization Agent
      -> Code Execution Agent
        -> Diagnostics Agent
```

## Artifact Flow

```text
BusinessBrief
  -> RuleSpec[]
  -> DecisionVariable[]
  -> ConstraintSpec[]
  -> Objective
  -> RuleFirstPlan
  -> ValidationIssue[]
  -> SolveReport
```

The public package keeps this flow intentionally small. It is a vocabulary and reference implementation for building AI-assisted optimization systems, not a dump of private vertical implementation code.

## Rule-First Design

Rules are not comments. They are the spine of the optimization workflow.

- Hard rules define feasibility.
- Soft rules define preferences, penalties, and tradeoffs.
- Constraints and objective terms keep a `rule_id`.
- Reports preserve the rule trace for diagnostics.

This lets an AI system explain outcomes in business language instead of asking humans to inspect anonymous mathematical expressions.

## Validation Gate

AI-generated optimization artifacts need a small deterministic audit before execution. The public validation layer checks duplicate rule and variable identifiers, unknown rule references, unknown variable references, invalid variable bounds, and solve-report rule traces.

This is intentionally not a solver. It is a contract gate between agent output and mathematical execution. A production system can add deeper domain, solver, and data checks behind the same pattern while keeping the public boundary clean.
