<p align="right">
  <a href="README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/lang-中文-red.svg"></a>
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/lang-English-blue.svg"></a>
</p>

# AI-Orchestrated Optimization

[![CI](https://github.com/zonywei/ai-orchestrated-optimization/actions/workflows/ci.yml/badge.svg)](https://github.com/zonywei/ai-orchestrated-optimization/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)

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
  -> Validation gate
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
- contract validation for rule traceability and variable references;
- constraint audit for bound-based pre-solve checks;
- infeasibility diagnostics that connect failed constraints back to rules;
- solver adapter interface for plugging execution engines behind the same public contract;
- objective contribution analysis for explaining where a solution's cost or value comes from;
- OR-Tools CP-SAT adapter with a synthetic workforce rostering example;
- a tiny exhaustive demo optimizer for public examples;
- generic examples that do not depend on any private vertical application;
- release-boundary checks to keep private implementation material out.

## What Is Not Included

This repository does not publish private vertical applications, customer data, proprietary solver internals, production model-building code, historical outputs, or business-specific rule libraries.

The public goal is to share the AI + OR framework direction and a runnable minimal surface. Production-grade vertical systems should live in separate private repositories unless they are intentionally cleaned and released.

## Current Capability

This repository currently proves a narrow but runnable public slice:

- rule-first public contracts for business briefs, rules, model artifacts, plans, and reports;
- validation gates for runtime domain values, traceability, variable references, and report consistency;
- pre-solve constraint audit and basic infeasibility diagnostics;
- deterministic RHS relaxation suggestions for structurally impossible constraints;
- solver adapter protocol for connecting execution engines behind one framework contract;
- OR-Tools CP-SAT execution for binary and integer linear models;
- a synthetic workforce rostering example with 30 binary decision variables;
- objective contribution analysis that maps solution cost or value back to rules.

It intentionally does not yet provide live LLM orchestration, production vertical applications, private rule libraries, large benchmark suites, or automatic natural-language-to-model generation.

## Maintenance And OSS Signals

This repository is structured as a maintained open-source project, not a one-off code dump:

- CI runs tests and the public release-boundary audit on every push and pull request;
- Dependabot tracks Python and GitHub Actions updates;
- contribution, security, issue, and pull request templates define the maintainer workflow;
- the roadmap separates near-term technical work from non-goals;
- Codex for Open Source application notes explain how maintainer automation and API credits would be used.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [docs/roadmap.md](docs/roadmap.md), and [docs/codex_for_oss.md](docs/codex_for_oss.md).

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe examples\assignment_demo.py
.\.venv\Scripts\python.exe -m pip install -e ".[cp-sat]"
.\.venv\Scripts\python.exe examples\cp_sat_workforce_demo.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\check_release_boundary.py
.\.venv\Scripts\python.exe scripts\run_quality_gates.py
```

Expected demo output:

```text
status=optimal
objective=9
assignments={'alpha': 'north', 'beta': 'south', 'gamma': 'east'}
```

Expected CP-SAT demo output:

```text
status=optimal
objective=5.0
slot_1=ava
slot_2=cy
slot_3=ben
slot_4=dia
slot_5=eli
```

## Public Repository Layout

```text
src/ai_or_optimization/
  agents.py       # AI OR role topology and handoff map
  contracts.py    # public optimization artifact contracts
  planner.py      # rule-first ordering
  validation.py   # contract-level traceability checks
  audit.py        # constraint-level pre-solve audit
  diagnostics.py  # infeasibility explanation helpers
  relaxations.py  # deterministic RHS relaxation suggestions
  contributions.py # objective contribution analysis
  solver_adapters.py # solver adapter protocol and public demo adapter
  cp_sat_adapter.py # OR-Tools CP-SAT adapter
  demo_solver.py  # small public exhaustive optimizer
examples/
  assignment_demo.py
  cp_sat_workforce_demo.py
  resource_allocation_brief.json
  workforce_rostering_cp_sat.json
  reports/workforce_rostering_diagnosis.md
docs/
  architecture.md
  use_cases.md
  public_boundary.md
  roadmap.md
  codex_for_oss.md
scripts/
  check_release_boundary.py
  run_quality_gates.py
tests/
  test_public_framework.py
  test_constraint_audit.py
  test_infeasibility_diagnostics.py
  test_relaxations.py
  test_solver_adapters.py
  test_objective_contributions.py
  test_cp_sat_adapter.py
.github/
  workflows/ci.yml
  dependabot.yml
  ISSUE_TEMPLATE/
  pull_request_template.md
```

## Status

This is an early public framework seed. It is intentionally small, auditable, and domain-neutral. The immediate goal is to establish the vocabulary and release boundary for AI-assisted optimization systems before adding heavier solver integrations.

## License

Apache License 2.0.
