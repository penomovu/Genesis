"""Emergent systems that self-organize from atomic interactions.

This module implements principles from complex systems theory, including:
- Feedback loops (positive and negative)
- Attractor dynamics and state space landscapes
- Criticality and phase transitions
- Self-organization through local interactions
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .atoms import (
    AffordanceAtom,
    BooleanStateAtom,
    FeedbackAtom,
    PerceptionAtom,
    ResourceAtom,
    TransitionRule,
)


class LoopType(str, Enum):
    """Types of feedback loops that drive emergence."""

    NEGATIVE = "negative"  # Homeostatic, stabilizing (health decay -> heal)
    POSITIVE = "positive"  # Amplifying, destabilizing (money -> interest)
    MIXED = "mixed"  # Alternating or complex dynamics


@dataclass(frozen=True, slots=True)
class FeedbackLoop:
    """A closed loop of state transitions that creates persistent behavior.

    Feedback loops are the fundamental units of game mechanics. They create
    the "game feel" and strategic depth through their stable or chaotic dynamics.
    """

    name: str
    loop_type: LoopType
    primary_resource: str
    triggers: list[TransitionRule]
    equilibria: list[float]  # Stable states the system tends toward
    instabilities: list[float]  # Unstable states that cause cascades

    def timescale(self) -> str:
        """Return characteristic timescale of this loop."""
        return "fast" if len(self.triggers) <= 2 else "medium"


@dataclass(frozen=True, slots=True)
class AttractorBasin:
    """A region of state space that the system tends to converge toward.

    Attractors create strategic objectives and natural goals for players.
    """

    name: str
    center_state: dict[str, float]  # Target values of key variables
    basin_depth: float  # How strongly it pulls (escape difficulty)
    stability: str  # "stable", "metastable", "transient"
    reward: float  # Value of reaching this state


@dataclass(frozen=True, slots=True)
class CriticalEvent:
    """A phase transition that occurs when crossing a threshold.

    Critical events create meaningful choices and turning points.
    """

    name: str
    trigger_condition: str
    pre_state: dict[str, float]
    post_state: dict[str, float]
    hysteresis: float  # Resistance to reversal


@dataclass(frozen=True, slots=True)
class EmergentSystem:
    """A collection of interacting feedback loops that exhibit emergent behavior.

    Systems are higher-order structures that arise from the interaction of
    multiple feedback loops. They are not explicitly authored but emerge
    from the constraints and affordances of their constituent loops.
    """

    name: str
    feedback_loops: list[FeedbackLoop]
    attractors: list[AttractorBasin]
    critical_events: list[CriticalEvent]

    def complexity(self) -> int:
        """Return a measure of emergent complexity."""
        return (
            len(self.feedback_loops)
            * len(self.attractors)
            + len(self.critical_events) * 2
        )

    def is_stable(self) -> bool:
        """Return whether the system tends toward stable attractors."""
        stable_loops = sum(
            1 for loop in self.feedback_loops if loop.loop_type == LoopType.NEGATIVE
        )
        return stable_loops >= len(self.feedback_loops) // 2


def detect_loops(
    resources: list[ResourceAtom],
    rules: list[TransitionRule],
    affordances: list[AffordanceAtom],
) -> list[FeedbackLoop]:
    """Identify feedback loops in a collection of atoms.

    Detects:
    1. Self-referential loops (resource affects itself)
    2. 2-cycles (A→B→A)
    3. Multi-step cycles with affordances bridging transitions
    """
    loops: list[FeedbackLoop] = []

    # Type 1: Self-referential loops (resource has decay or renew)
    for resource in resources:
        has_decay = any(
            r.source == resource.name and r.transition_type.value == "decay"
            for r in rules
        )
        has_renew = any(
            r.source == resource.name and r.transition_type.value == "linear" and r.delta > 0
            for r in rules
        )

        if has_decay or has_renew:
            # Determine loop type based on balance
            if has_decay and has_renew:
                loop_type = LoopType.MIXED  # Decay vs renewal
                equilibria = [50.0, 75.0]
            elif has_decay:
                loop_type = LoopType.NEGATIVE  # Homeostatic decay
                equilibria = [0.0]
            else:
                loop_type = LoopType.POSITIVE  # Growth
                equilibria = [100.0]

            triggers = [r for r in rules if r.source == resource.name]

            loops.append(
                FeedbackLoop(
                    name=f"resource_loop_{resource.name}",
                    loop_type=loop_type,
                    primary_resource=resource.name,
                    triggers=triggers,
                    equilibria=equilibria,
                    instabilities=[],
                )
            )

    # Type 2: Affordance-mediated loops (action affects resource, which enables action)
    for affordance in affordances:
        # Find resources this affordance requires
        required_resources = list(affordance.requires_resources.keys())
        # Find resources this affordance affects
        affected_resources = list(affordance.grants_resources.keys())

        # If it requires and affects the same resource type -> loop
        for req in required_resources:
            for aff in affected_resources:
                if req == aff:
                    loops.append(
                        FeedbackLoop(
                            name=f"action_loop_{affordance.name}",
                            loop_type=LoopType.NEGATIVE,  # Resource consumption is stabilizing
                            primary_resource=req,
                            triggers=[],  # Affordances, not transitions
                            equilibria=[50.0],
                            instabilities=[],
                        )
                    )

    # Type 3: Cross-resource loops (A affects B, B affects A via affordances)
    for resource_a in resources:
        for resource_b in resources:
            if resource_a.name == resource_b.name:
                continue

            # Find affordances that consume A and produce B
            a_to_b = any(
                aff.grants_resources.get(resource_b.name, 0) > 0
                and aff.requires_resources.get(resource_a.name, (-1, 1))[0] > 0
                for aff in affordances
            )

            # Find affordances that consume B and produce A
            b_to_a = any(
                aff.grants_resources.get(resource_a.name, 0) > 0
                and aff.requires_resources.get(resource_b.name, (-1, 1))[0] > 0
                for aff in affordances
            )

            if a_to_b and b_to_a:
                loops.append(
                    FeedbackLoop(
                        name=f"cross_loop_{resource_a.name}_{resource_b.name}",
                        loop_type=LoopType.NEGATIVE,
                        primary_resource=resource_a.name,
                        triggers=[],
                        equilibria=[50.0],
                        instabilities=[],
                    )
                )

    return loops


def find_attractors(
    resources: list[ResourceAtom],
    loops: list[FeedbackLoop],
) -> list[AttractorBasin]:
    """Identify natural attractors in the state space.

    Attractors emerge from the interaction of feedback loops and constraints.
    """
    attractors: list[AttractorBasin] = []

    # Simple heuristic: min/max values create natural attractors
    for resource in resources:
        if resource.min > 0:
            attractors.append(
                AttractorBasin(
                    name=f"{resource.name}_depleted",
                    center_state={resource.name: resource.min},
                    basin_depth=resource.initial - resource.min,
                    stability="stable",
                    reward=0.0,  # Low resource states are usually negative
                )
            )
        if resource.max < float("inf"):
            attractors.append(
                AttractorBasin(
                    name=f"{resource.name}_maximized",
                    center_state={resource.name: resource.max},
                    basin_depth=resource.max - resource.initial,
                    stability="stable",
                    reward=1.0,  # High resource states are usually goals
                )
            )

    return attractors


def self_organize_system(
    resources: list[ResourceAtom],
    rules: list[TransitionRule],
    affordances: list[AffordanceAtom],
    feedback: list[FeedbackAtom],
    perception: list[PerceptionAtom],
) -> EmergentSystem:
    """Assemble atoms into an emergent system through self-organization.

    This function applies principles of complex systems theory to identify
    the emergent structure that arises from atomic interactions.
    """
    loops = detect_loops(resources, rules, affordances)
    attractors = find_attractors(resources, loops)

    # Critical events emerge from threshold crossings in feedback loops
    critical_events: list[CriticalEvent] = []
    for loop in loops:
        for eq in loop.equilibria:
            # Only create critical events for significant equilibria
            if eq > 10.0:  # Skip trivial equilibria near 0
                critical_events.append(
                    CriticalEvent(
                        name=f"{loop.name}_phase_change",
                        trigger_condition=f"{loop.primary_resource} crosses {eq}",
                        pre_state={loop.primary_resource: eq * 0.9},
                        post_state={loop.primary_resource: eq * 1.1},
                        hysteresis=0.15,
                    )
                )

    # Also create critical events for resource depletion thresholds
    for resource in resources:
        if resource.decay_rate > 0 and resource.min == 0.0:
            critical_events.append(
                CriticalEvent(
                    name=f"{resource.name}_depletion",
                    trigger_condition=f"{resource.name} <= {resource.initial * 0.2}",
                    pre_state={resource.name: resource.initial * 0.25},
                    post_state={resource.name: 0.0},
                    hysteresis=0.3,  # Requires 30% recovery to exit depletion state
                )
            )

    return EmergentSystem(
        name="EmergentSystem",
        feedback_loops=loops,
        attractors=attractors,
        critical_events=critical_events,
    )
