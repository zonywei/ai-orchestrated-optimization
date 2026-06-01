# AI-Orchestrated Optimization

> AI + Operations Research for the next generation of decision automation.

Most organizations already have enough data to make better operational decisions. What they often lack is the translation layer between human policy and mathematical action: the messy rules, preferences, tradeoffs, and exceptions that live in meetings, spreadsheets, messages, and expert intuition.

AI-Orchestrated Optimization is an open framework direction for that missing layer. It treats AI agents as the front end of operations research: agents clarify intent, turn business language into rule-first optimization artifacts, run transparent model plans, and hand diagnostics back to humans. The result is not just "AI suggestions"; it is auditable decision automation.

## Why This Matters

The next wave of productivity will not come only from writing text faster or generating code snippets. It will come from changing how organizations allocate scarce resources.

AI plus operations research can become a new operating paradigm for:

- **workforce rostering:** balance coverage, fairness, fatigue, compliance, skill mix, and labor cost;
- **manufacturing dispatch:** coordinate machines, jobs, materials, changeovers, throughput, and delivery promises;
- **logistics optimization:** assign routes, loads, time windows, hubs, fleets, and disruption responses;
- **inventory and capacity planning:** decide what to produce, reserve, move, or replenish under uncertainty;
- **cost reduction:** expose the hidden price of constraints and find better tradeoffs without losing control;
- **resilience:** re-optimize quickly when reality changes.

Large language models are strong at understanding context, goals, and exceptions. Operations research is strong at feasibility, optimality, and tradeoff discipline. Put together, they can turn operational decision-making from a manual negotiation process into a repeatable, inspectable, continuously improving system.

## Core Idea

This framework is built around a rule-first flow:

```text
Business pain point
  -> AI agent handoff
  -> Rule catalog
  -> Decision variables
  -> Constraints
  -> Objective
  -> Solver run
  -> Diagnostics and next action
```

Rules are first-class citizens. A hard rule defines feasibility. A soft rule defines a preference, penalty, or tradeoff. Every variable, constraint, and objective term can point back to the business rule that created it.

That trace is the difference between a black-box model and an operational system a team can trust.

## Agent Workflow

```text
Business Expert
  -> Chief Architect Agent
    -> Mathematical Modeling Agent
    -> Reduction and Optimization Agent
      -> Code Execution Agent
        -> Diagnostics Agent
```

Each agent has a distinct responsibility:

- clarify business intent;
- separate hard rules from soft preferences;
- design model structure;
- reduce search space;
- execute the optimization workflow;
- explain outcomes, infeasibility, and tradeoffs.

## What Is Included

This public repository contains a small, clean framework surface:

- typed contracts for briefs, rules, variables, constraints, objectives, plans, and reports;
- a canonical AI OR agent topology;
- a rule-first planner;
- a tiny exhaustive demo optimizer for public examples;
- generic examples that do not depend on any private vertical application;
- release-boundary checks to keep private implementation material out.

## What Is Not Included

This repository does not publish private vertical applications, customer data, proprietary solver internals, production model-building code, historical outputs, or business-specific rule libraries.

The public goal is to share the AI + OR framework direction and a runnable minimal surface. Production-grade vertical systems should live in separate private repositories unless they are intentionally cleaned and released.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe examples\assignment_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\check_release_boundary.py
```

Expected demo output:

```text
status=optimal
objective=9
assignments={'alpha': 'north', 'beta': 'south', 'gamma': 'east'}
```

## Public Repository Layout

```text
src/ai_or_optimization/
  agents.py       # AI OR role topology and handoff map
  contracts.py    # public optimization artifact contracts
  planner.py      # rule-first ordering
  demo_solver.py  # small public exhaustive optimizer
examples/
  assignment_demo.py
  resource_allocation_brief.json
docs/
  architecture.md
  use_cases.md
  public_boundary.md
scripts/
  check_release_boundary.py
tests/
  test_public_framework.py
```

## Status

This is an early public framework seed. It is intentionally small, auditable, and domain-neutral. The immediate goal is to establish the vocabulary and release boundary for AI-assisted optimization systems before adding heavier solver integrations.

## License

MIT.
