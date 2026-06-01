"""Agent topology for AI-assisted operations research workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentRole:
    """A public role in the AI OR workflow."""

    role_id: str
    title: str
    responsibility: str


@dataclass(frozen=True)
class Handoff:
    """A directed handoff between two AI OR roles."""

    source_role_id: str
    target_role_id: str
    artifact: str


def build_default_agent_topology() -> tuple[tuple[AgentRole, ...], tuple[Handoff, ...]]:
    """Return the canonical public AI OR workflow."""

    roles = (
        AgentRole(
            "business_expert",
            "Business Expert",
            "Describe operational pain, policies, exceptions, and success criteria.",
        ),
        AgentRole(
            "chief_architect",
            "Chief Architect Agent",
            "Convert business language into entities, rules, decisions, and modeling scope.",
        ),
        AgentRole(
            "mathematical_modeler",
            "Mathematical Modeling Agent",
            "Define variables, constraints, objective terms, and feasibility structure.",
        ),
        AgentRole(
            "reduction_optimizer",
            "Reduction and Optimization Agent",
            "Reduce search space, identify decomposition, and propose solver strategy.",
        ),
        AgentRole(
            "execution_agent",
            "Code Execution Agent",
            "Run the optimization workflow and collect structured solve evidence.",
        ),
        AgentRole(
            "diagnostics_agent",
            "Diagnostics Agent",
            "Explain infeasibility, tradeoffs, and next actions in business terms.",
        ),
    )
    handoffs = (
        Handoff("business_expert", "chief_architect", "business_brief"),
        Handoff("chief_architect", "mathematical_modeler", "modeling_scope"),
        Handoff("chief_architect", "reduction_optimizer", "search_strategy_brief"),
        Handoff("mathematical_modeler", "execution_agent", "optimization_contract"),
        Handoff("reduction_optimizer", "execution_agent", "solver_strategy"),
        Handoff("execution_agent", "diagnostics_agent", "solve_report"),
    )
    return roles, handoffs
