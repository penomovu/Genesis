"""Atomic assembler: combines atoms into mechanics through constrained assembly.

This module implements combinatorial assembly rules that determine which
atoms can combine and in what configurations. It applies principles from
molecular chemistry (binding sites, reaction conditions) to game mechanics.
"""

from __future__ import annotations

import random
from typing import Any

from .atoms import (
    AffordanceAtom,
    BooleanStateAtom,
    FeedbackAtom,
    PerceptionAtom,
    ResourceAtom,
    ResourceType,
    StateTransition,
    TemporalAtom,
    TransitionRule,
)
from .cosmology import CosmologicalConstants
from .emergence import self_organize_system
from .frameworks import FrameworkConstraints


class AtomAssembler:
    """Assembles atoms into coherent emergent systems.

    The assembler uses the cosmological constants as reaction conditions
    and framework constraints as binding site requirements. It applies
    mutation and selection principles to evolve viable game systems.
    """

    def __init__(
        self,
        constants: CosmologicalConstants,
        framework: FrameworkConstraints,
        rng: random.Random,
    ):
        self.constants = constants
        self.framework = framework
        self.rng = rng

    def generate_resources(self) -> list[ResourceAtom]:
        """Generate resource atoms based on framework and constants."""
        count = self.rng.randint(
            self.framework.resource_count_min,
            self.framework.resource_count_max,
        )

        resources: list[ResourceAtom] = []

        # Always generate at least one primary resource of each required type
        for resource_type in self.framework.primary_resource_types:
            resources.append(self._generate_resource(resource_type))

        # Fill remaining slots with secondary resources
        while len(resources) < count:
            # Bias toward framework's primary types but allow variety
            resource_type = self.rng.choice(list(ResourceType))
            resources.append(self._generate_resource(resource_type))

        return resources

    def _generate_resource(self, resource_type: ResourceType) -> ResourceAtom:
        """Generate a single resource atom with derived properties."""
        # Scale based on resource_constraint
        constraint = self.constants.resource_constraint

        if resource_type == ResourceType.SCARCE:
            initial = self.rng.uniform(50.0, 100.0)
            decay_rate = self.rng.uniform(0.5, 2.0) * constraint
            name = self._resource_name(resource_type)
            return ResourceAtom(
                name=name,
                resource_type=resource_type,
                initial=initial,
                min=0.0,
                max=initial * 1.5,
                decay_rate=decay_rate,
                renew_rate=0.0,
            )

        elif resource_type == ResourceType.RENEWABLE:
            initial = self.rng.uniform(30.0, 100.0)
            renew_rate = self.rng.uniform(1.0, 5.0) * (1.0 - constraint)
            name = self._resource_name(resource_type)
            return ResourceAtom(
                name=name,
                resource_type=resource_type,
                initial=initial,
                min=0.0,
                max=100.0,
                decay_rate=0.0,
                renew_rate=renew_rate,
            )

        elif resource_type == ResourceType.CUMULATIVE:
            initial = 0.0
            name = self._resource_name(resource_type)
            return ResourceAtom(
                name=name,
                resource_type=resource_type,
                initial=initial,
                min=0.0,
                max=float("inf"),
                decay_rate=0.0,
                renew_rate=0.0,
            )

        else:  # FLOW
            initial = self.rng.uniform(1.0, 10.0)
            name = self._resource_name(resource_type)
            return ResourceAtom(
                name=name,
                resource_type=resource_type,
                initial=initial,
                min=0.0,
                max=initial * 5.0,
                decay_rate=0.0,
                renew_rate=0.0,
            )

    def _resource_name(self, resource_type: ResourceType) -> str:
        """Generate a thematic resource name."""
        # Simplified naming - in a full system, this would use thematic tables
        names = {
            ResourceType.SCARCE: ["health", "oxygen", "energy", "stamina"],
            ResourceType.RENEWABLE: ["mana", "focus", "charge", "moral"],
            ResourceType.CUMULATIVE: ["gold", "experience", "score", "influence"],
            ResourceType.FLOW: ["speed", "production", "throughput", "flow"],
        }
        return self.rng.choice(names[resource_type])

    def generate_boolean_states(self, count: int) -> list[BooleanStateAtom]:
        """Generate boolean state atoms for conditions and capabilities."""
        states: list[BooleanStateAtom] = []

        # Generate states relevant to mechanics
        state_types = ["flag", "door", "key", "buff", "debuff"]
        for _ in range(count):
            name = f"{self.rng.choice(state_types)}_{len(states)}"
            persistence = self.rng.choice(["global", "location", "session"])
            states.append(
                BooleanStateAtom(name=name, initial=False, persistence=persistence)
            )

        return states

    def generate_perception(self, resources: list[ResourceAtom]) -> list[PerceptionAtom]:
        """Generate perception atoms based on information theory regime."""
        perceptions: list[PerceptionAtom] = []

        # Resource visibility depends on revelation constant
        for resource in resources:
            visibility = self._determine_visibility()
            precision = self._determine_precision()

            # Cost depends on revelation (higher revelation = lower cost)
            cost = max(0.0, 1.0 - self.constants.revelation)

            perceptions.append(
                PerceptionAtom(
                    name=f"see_{resource.name}",
                    observed_property=resource.name,
                    visibility=visibility,
                    precision=precision,
                    cost=cost,
                )
            )

        return perceptions

    def _determine_visibility(self) -> str:
        """Determine visibility based on information theory regime."""
        if self.constants.information_theory == "complete":
            return "always"
        elif self.constants.information_theory == "fog":
            return "conditional"
        else:
            return self.rng.choice(["proximity", "active"])

    def _determine_precision(self) -> str:
        """Determine information precision."""
        if self.constants.revelation > 0.7:
            return "exact"
        elif self.constants.revelation < 0.3:
            return "binary"
        else:
            return self.rng.choice(["approximate", "tiered"])

    def generate_affordances(
        self,
        resources: list[ResourceAtom],
        boolean_states: list[BooleanStateAtom],
    ) -> list[AffordanceAtom]:
        """Generate affordance atoms for player agency."""
        affordances: list[AffordanceAtom] = []

        # Generate affordances for resource manipulation
        for resource in resources:
            # Consumption affordance
            affordances.append(
                AffordanceAtom(
                    name=f"use_{resource.name}",
                    requires_resources={},
                    grants_resources={resource.name: -5.0},
                    requires_state=set(),
                    toggles_state=set(),
                    duration=0.0,
                    cooldown=1.0,
                )
            )

            # Acquisition affordance
            affordances.append(
                AffordanceAtom(
                    name=f"acquire_{resource.name}",
                    requires_resources={},
                    grants_resources={resource.name: 10.0},
                    requires_state=set(),
                    toggles_state=set(),
                    duration=1.0,
                    cooldown=0.0,
                )
            )

        # Generate affordances for state toggling
        for state in boolean_states:
            affordances.append(
                AffordanceAtom(
                    name=f"toggle_{state.name}",
                    requires_resources={},
                    grants_resources={},
                    requires_state=set(),
                    toggles_state={state.name},
                    duration=0.5,
                    cooldown=0.0,
                )
            )

        return affordances

    def generate_feedback(
        self,
        resources: list[ResourceAtom],
    ) -> list[FeedbackAtom]:
        """Generate feedback atoms for state changes."""
        feedback: list[FeedbackAtom] = []

        modality = self.rng.choice(["visual", "audio", "haptic", "narrative"])

        # Feedback for resource changes
        for resource in resources:
            feedback.append(
                FeedbackAtom(
                    name=f"{resource.name}_change",
                    trigger_type="on_change",
                    target_property=resource.name,
                    modality=modality,
                    intensity=0.5 * self.constants.revelation,
                )
            )

        # Feedback for critical thresholds
        for resource in resources:
            if resource.decay_rate > 0:
                feedback.append(
                    FeedbackAtom(
                        name=f"{resource.name}_critical",
                        trigger_type="on_threshold",
                        target_property=resource.name,
                        modality="audio",
                        intensity=0.9,
                    )
                )

        return feedback

    def generate_transitions(
        self,
        resources: list[ResourceAtom],
        boolean_states: list[BooleanStateAtom],
    ) -> list[TransitionRule]:
        """Generate transition rules for game dynamics."""
        transitions: list[TransitionRule] = []

        # Decay transitions for scarce resources
        for resource in resources:
            if resource.decay_rate > 0:
                transitions.append(
                    TransitionRule(
                        name=f"{resource.name}_decay",
                        condition="always",
                        transition_type=StateTransition.DECAY,
                        source=resource.name,
                        delta=0.0,
                        rate=resource.decay_rate * self.constants.time_dilation,
                        probability=1.0,
                    )
                )

        # Renew transitions for renewable resources
        for resource in resources:
            if resource.renew_rate > 0:
                transitions.append(
                    TransitionRule(
                        name=f"{resource.name}_renew",
                        condition="always",
                        transition_type=StateTransition.LINEAR,
                        source=resource.name,
                        delta=resource.renew_rate * self.constants.time_dilation,
                        rate=0.0,
                        probability=1.0,
                    )
                )

        # Threshold-based transitions
        for resource in resources:
            if resource.min > 0:
                transitions.append(
                    TransitionRule(
                        name=f"{resource.name}_depletion",
                        condition=f"{resource.name} <= {resource.min}",
                        transition_type=StateTransition.THRESHOLD,
                        source=resource.name,
                        delta=0.0,
                        rate=0.0,
                        threshold=resource.min,
                        probability=1.0,
                    )
                )

        return transitions

    def generate_temporal(self) -> list[TemporalAtom]:
        """Generate temporal atoms for pacing."""
        temporals: list[TemporalAtom] = []

        # Time pressure based on framework
        if self.framework.time_pressure > 0.5:
            temporals.append(
                TemporalAtom(
                    name="decay_pressure",
                    type="deadline",
                    duration=100.0 * self.constants.time_dilation,
                    repeats=False,
                )
            )

        # Rhythmic elements for variety
        if self.framework.pacing_variety > 0.5:
            temporals.append(
                TemporalAtom(
                    name="opportunity_window",
                    type="window",
                    duration=10.0 * self.constants.time_dilation,
                    repeats=True,
                    decay=0.1,
                )
            )

        return temporals

    def assemble(self) -> dict[str, Any]:
        """Assemble all atoms into a coherent system."""
        resources = self.generate_resources()
        boolean_states = self.generate_boolean_states(
            self.rng.randint(2, 5),
        )
        perception = self.generate_perception(resources)
        affordances = self.generate_affordances(resources, boolean_states)
        feedback = self.generate_feedback(resources)
        transitions = self.generate_transitions(resources, boolean_states)
        temporals = self.generate_temporal()

        # Self-organize into emergent system
        emergent = self_organize_system(
            resources=resources,
            rules=transitions,
            affordances=affordances,
            feedback=feedback,
            perception=perception,
        )

        return {
            "resources": resources,
            "boolean_states": boolean_states,
            "perception": perception,
            "affordances": affordances,
            "feedback": feedback,
            "transitions": transitions,
            "temporals": temporals,
            "emergent_system": emergent,
        }
