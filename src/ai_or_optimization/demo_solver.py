"""Small public demo optimizer.

This module is intentionally simple. It demonstrates the public contract shape
without exposing production model-building or solver internals.
"""

from __future__ import annotations

from itertools import permutations

from .contracts import SolveReport


def solve_assignment_problem(
    cost_by_item_and_slot: dict[str, dict[str, int]],
    rule_trace: tuple[str, ...] = (),
) -> SolveReport:
    """Solve a tiny one-to-one assignment problem by exhaustive search."""

    if not cost_by_item_and_slot:
        return SolveReport(
            status="infeasible",
            objective_value=None,
            diagnostics=("No items were provided.",),
        )

    items = tuple(cost_by_item_and_slot)
    slots = tuple(next(iter(cost_by_item_and_slot.values())))
    if len(slots) < len(items):
        return SolveReport(
            status="infeasible",
            objective_value=None,
            diagnostics=("Not enough slots for a one-to-one assignment.",),
        )

    best_cost: int | None = None
    best_assignment: dict[str, str] | None = None
    for candidate_slots in permutations(slots, len(items)):
        assignment = dict(zip(items, candidate_slots, strict=True))
        try:
            cost = sum(cost_by_item_and_slot[item][slot] for item, slot in assignment.items())
        except KeyError:
            continue
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_assignment = assignment

    if best_assignment is None or best_cost is None:
        return SolveReport(
            status="infeasible",
            objective_value=None,
            rule_trace=rule_trace,
            diagnostics=("No complete assignment had defined costs.",),
        )

    return SolveReport(
        status="optimal",
        objective_value=best_cost,
        assignments=best_assignment,
        rule_trace=rule_trace,
        diagnostics=("Solved by public exhaustive demo optimizer.",),
    )
