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
