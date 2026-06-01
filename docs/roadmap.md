# Roadmap

This roadmap keeps the public repository focused on reusable AI plus operations research infrastructure. It is not a promise of delivery dates; it is a technical direction for contributors and reviewers.

## Near-Term Technical Work

1. **Rule extraction fixtures**
   - Add public fixtures that show how natural language briefs become `RuleSpec` objects.
   - Keep the first version deterministic so tests do not depend on a live model call.

2. **Conflict-set diagnostics**
   - Move beyond single-constraint bound checks.
   - Identify small groups of rules that jointly create infeasibility.

3. **Relaxation suggestions**
   - Represent candidate rule revisions, penalty changes, or bound adjustments.
   - Rank suggestions by feasibility impact and business cost.

4. **Solver adapter coverage**
   - Keep OR-Tools CP-SAT as the first serious adapter.
   - Add adapter capability metadata for model classes, variable types, and status mapping.

5. **Public benchmark-style examples**
   - Add synthetic workforce, manufacturing, logistics, and capacity allocation examples.
   - Keep every example small enough for CI but rich enough to exercise traceability.

6. **Maintainer automation**
   - Use Codex to draft tests, review pull requests, update docs, inspect dependency changes, and generate release notes.
   - Keep human review in the loop for public API and boundary decisions.

## Non-Goals

- Publishing private vertical systems.
- Publishing customer data or historical outputs.
- Competing with mature solvers.
- Replacing human ownership of business rules.

## Definition Of Progress

A change moves the project forward when it improves at least one of:

- traceability from business rules to model artifacts;
- diagnostics for infeasible or low-quality plans;
- solver adapter reliability;
- contributor onboarding;
- release-boundary confidence.
