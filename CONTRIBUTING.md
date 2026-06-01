# Contributing

AI-Orchestrated Optimization is an early public framework seed. Contributions should keep the package small, auditable, and domain-neutral.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe scripts\run_quality_gates.py
```

On Unix-like shells, use the same Python module commands with your environment's Python executable.

## Quality Gates

Before opening a pull request, run:

```powershell
python scripts\run_quality_gates.py
```

The quality gate runs tests, examples, and the release-boundary check. A contribution that fails it should be treated as not ready for review.

## Public Boundary

Safe contributions:

- generic rule-first contracts;
- validation, audit, diagnostics, and solver adapter improvements;
- synthetic examples with no private data;
- documentation that clarifies the public framework;
- tests that improve confidence in public behavior.

Do not contribute:

- private vertical applications;
- customer, operator, or account data;
- proprietary solver internals;
- private rule libraries;
- generated logs, archives, spreadsheets, or binary artifacts.

## Pull Request Expectations

Keep pull requests narrow. Include a short summary, the quality gates you ran, and any known limitation. If a change adds a public behavior, add or update tests in the same pull request.
