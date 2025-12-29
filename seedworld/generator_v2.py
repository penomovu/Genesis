"""v2.0 Generator: Emergent game generation from seed.

This is the evolved generator that uses the new atomic architecture.
It replaces the handcrafted template system with true emergence:
- Seed → cosmological constants (physics of game universe)
- Constants → framework constraints (boundary conditions)
- Framework + constants → atomic assembly
- Atoms → emergent systems (self-organizing mechanics)
- Emergent systems → world structure and goals
- Simulation validates winnability and playability
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict
from typing import Any

from .assembler import AtomAssembler
from .atoms import (
    AffordanceAtom,
    BooleanStateAtom,
    FeedbackAtom,
    PerceptionAtom,
    ResourceAtom,
    ResourceType,
    TemporalAtom,
    TransitionRule,
)
from .cosmology import CosmologicalConstants, derive_constants
from .emergence import EmergentSystem
from .frameworks import FrameworkConstraints, select_framework
from .simulation import is_playable, run_playability_test
from .spec import (
    EdgeSpec,
    GameSpec,
    GateSpec,
    LocationSpec,
    MechanicSpec,
    QuestSpec,
    QuestStepSpec,
    WorldGraphSpec,
)


class GameGeneratorV2:
    """Emergent game generator using atomic assembly."""

    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

    def generate(self) -> dict[str, Any]:
        """Generate a complete game specification through emergence."""
        # Step 1: Derive cosmological constants
        constants = derive_constants(self.seed)

        # Step 2: Select framework based on constants
        framework = select_framework(constants)

        # Step 3: Assemble atoms
        assembler = AtomAssembler(constants, framework, self.rng)
        atomic_system = assembler.assemble()

        # Step 4: Validate playability through simulation
        playability = run_playability_test(
            resources=atomic_system["resources"],
            affordances=atomic_system["affordances"],
            transitions=atomic_system["transitions"],
            num_simulations=50,  # Quick validation
        )

        # If not playable, apply mutations and retry
        if not is_playable(playability):
            atomic_system = self._mutate_and_retry(
                assembler,
                atomic_system,
                max_attempts=3,
            )

        # Step 5: Generate world structure from emergent systems
        world = self._generate_world(
            constants,
            framework,
            atomic_system["emergent_system"],
            atomic_system["resources"],
        )

        # Step 6: Generate quests from attractors
        quests = self._generate_quests(
            framework,
            atomic_system["emergent_system"],
            atomic_system["resources"],
        )

        # Step 7: Convert atomic system to mechanic specs
        mechanics = self._atoms_to_mechanics(atomic_system)

        # Step 8: Generate title and metadata
        title = self._generate_title(constants, framework)

        # Assemble complete specification
        spec = {
            "seed": self.seed,
            "title": title,
            "genre": self._derive_genre(framework),
            "version": "2.0",
            "mechanics": mechanics,
            "cosmological_constants": constants.to_dict(),
            "framework": self._framework_to_dict(framework),
            "playability_metrics": {
                "win_rate": playability.win_rate,
                "strategy_diversity": playability.strategy_diversity,
                "balance_score": playability.balance_score,
            },
            "atoms": {
                "resources": [self._resource_to_dict(r) for r in atomic_system["resources"]],
                "boolean_states": [asdict(b) for b in atomic_system["boolean_states"]],
                "perception": [asdict(p) for p in atomic_system["perception"]],
                "affordances": [self._affordance_to_dict(a) for a in atomic_system["affordances"]],
                "feedback": [asdict(f) for f in atomic_system["feedback"]],
                "transitions": [asdict(t) for t in atomic_system["transitions"]],
                "temporals": [asdict(t) for t in atomic_system["temporals"]],
            },
            "emergent_system": self._emergent_to_dict(atomic_system["emergent_system"]),
            "mechanics": mechanics,
            "world": {
                "locations": [asdict(l) for l in world["locations"]],
                "edges": [asdict(e) for e in world["edges"]],
            },
            "quests": [asdict(q) for q in quests],
        }

        return spec

    def _mutate_and_retry(
        self,
        assembler: AtomAssembler,
        atomic_system: dict[str, Any],
        max_attempts: int = 3,
    ) -> dict[str, Any]:
        """Apply mutations and retry assembly if playability fails."""
        for attempt in range(max_attempts):
            # Mutate assembler with slightly different constants
            mutated_assembler = AtomAssembler(
                assembler.constants,
                assembler.framework,
                random.Random(self.seed + attempt + 1),
            )
            atomic_system = mutated_assembler.assemble()

            playability = run_playability_test(
                resources=atomic_system["resources"],
                affordances=atomic_system["affordances"],
                transitions=atomic_system["transitions"],
                num_simulations=30,
            )

            if is_playable(playability):
                return atomic_system

        # Return best attempt if all fail
        return atomic_system

    def _generate_world(
        self,
        constants: CosmologicalConstants,
        framework: FrameworkConstraints,
        emergent: EmergentSystem,
        resources: list[ResourceAtom],
    ) -> dict[str, Any]:
        """Generate world structure from emergent systems."""
        # Number of locations scales with world_size
        size_map = {"micro": 3, "small": 5, "medium": 8, "large": 12}
        num_locations = size_map.get("small", 5)  # Use small for now

        locations: list[LocationSpec] = []

        # Central hub
        locations.append(
            LocationSpec(
                id="hub",
                name="Central Hub",
                tags=["safe_zone", "spawn"],
                items=[r.name for r in resources[:2]],  # Initial resources
                hazards=[],
            )
        )

        # Generate locations based on attractors
        for i, attractor in enumerate(emergent.attractors[: num_locations - 1]):
            loc_type = self._determine_location_type(attractor, framework)
            items = []
            hazards = []

            # Location properties based on attractor
            for resource_name, target_value in attractor.center_state.items():
                if target_value > 50:
                    # High-value attractor provides resources
                    matching_resource = next(
                        (r for r in resources if r.name == resource_name),
                        None,
                    )
                    if matching_resource:
                        items.append(matching_resource.name)
                else:
                    # Low-value attractor has hazards
                    hazards.append(f"hazard_{resource_name}")

            locations.append(
                LocationSpec(
                    id=f"zone_{i}",
                    name=f"{loc_type.capitalize()} Zone {i}",
                    tags=[loc_type],
                    items=items,
                    hazards=hazards,
                )
            )

        # Generate edges with gates based on feedback loops
        edges: list[EdgeSpec] = []

        # Connect hub to outer zones
        for i in range(1, min(num_locations, 4)):
            edges.append(EdgeSpec(src="hub", dst=f"zone_{i}", gate=None))

        # Connect outer zones
        for i in range(1, num_locations - 1):
            edges.append(
                EdgeSpec(
                    src=f"zone_{i}",
                    dst=f"zone_{(i % (num_locations - 1)) + 1}",
                    gate=self._generate_gate(resources, emergent),
                )
            )

        return {"locations": locations, "edges": edges}

    def _determine_location_type(
        self,
        attractor: any,
        framework: FrameworkConstraints,
    ) -> str:
        """Determine location type based on attractor properties."""
        if framework.stakes_magnitude > 0.7:
            return "danger"
        elif framework.discovery_importance > 0.7:
            return "exploration"
        else:
            return "resource"

    def _generate_gate(
        self,
        resources: list[ResourceAtom],
        emergent: EmergentSystem,
    ) -> GateSpec | None:
        """Generate a gate condition based on system properties."""
        # 30% chance of no gate
        if self.rng.random() < 0.3:
            return None

        # Gate based on critical events
        if emergent.critical_events:
            event = self.rng.choice(emergent.critical_events)
            # Use a resource as requirement
            resource = self.rng.choice(resources)

            gate_kind = "hard" if event.hysteresis > 0.5 else "soft"
            return GateSpec(
                kind=gate_kind,
                requirement=resource.name,
                rationale=(
                    f"Phase transition requires {resource.name} "
                    f"threshold: {event.trigger_condition}"
                ),
            )

        return None

    def _generate_quests(
        self,
        framework: FrameworkConstraints,
        emergent: EmergentSystem,
        resources: list[ResourceAtom],
    ) -> list[QuestSpec]:
        """Generate quests from emergent attractors."""
        quests: list[QuestSpec] = []

        # Main quest from primary attractor
        if emergent.attractors:
            primary = max(
                emergent.attractors,
                key=lambda a: a.basin_depth,
            )

            main_quest = self._attractor_to_quest("Primary Objective", primary, resources)
            quests.append(main_quest)

        # Secondary quests from other attractors
        for attractor in emergent.attractors[1:]:
            if attractor.reward > 0.5:  # Only significant attractors
                quest = self._attractor_to_quest(
                    f"Secondary Objective {len(quests)}",
                    attractor,
                    resources,
                )
                quests.append(quest)

        return quests

    def _attractor_to_quest(
        self,
        name: str,
        attractor: any,
        resources: list[ResourceAtom],
    ) -> QuestSpec:
        """Convert an attractor basin into a quest."""
        # Attractor target states become quest objectives
        steps: list[QuestStepSpec] = []

        for resource_name, target_value in attractor.center_state.items():
            if target_value > 50:
                # High-value target
                steps.append(
                    QuestStepSpec(
                        id=f"acquire_{resource_name}",
                        description=f"Acquire sufficient {resource_name}",
                        requires=[],
                        grants=[resource_name],
                    )
                )
            else:
                # Low-value state might be a prerequisite
                steps.append(
                    QuestStepSpec(
                        id=f"navigate_{resource_name}",
                        description=f"Navigate through {resource_name} constraints",
                        requires=[],
                        grants=[f"access_{resource_name}"],
                    )
                )

        objective = f"Reach the {name} state: {attractor.center_state}"

        return QuestSpec(
            name=name,
            objective=objective,
            steps=steps,
        )

    def _atoms_to_mechanics(self, atomic_system: dict[str, Any]) -> list[dict]:
        """Convert atomic system to mechanic specs."""
        mechanics: list[dict] = []
        seen_resources = set()

        # Convert each feedback loop to a mechanic (deduplicate by resource)
        for loop in atomic_system["emergent_system"].feedback_loops:
            # Skip if we already created a mechanic for this resource
            if loop.primary_resource in seen_resources:
                continue
            seen_resources.add(loop.primary_resource)

            mechanic: dict[str, Any] = {
                "name": f"{loop.loop_type.capitalize()} Loop: {loop.primary_resource}",
                "description": (
                    f"A {loop.loop_type} feedback loop centered on {loop.primary_resource}. "
                    f"Stable equilibria at {loop.equilibria}."
                ),
                "actions": [],
                "rules": [],
                "feedback": [],
                "depends_on": [],
            }

            # Add related affordances as actions (deduplicate)
            seen_actions = set()
            for aff in atomic_system["affordances"]:
                if loop.primary_resource in aff.grants_resources and aff.name not in seen_actions:
                    mechanic["actions"].append(aff.name)
                    seen_actions.add(aff.name)

            # Add related transitions as rules
            for trans in atomic_system["transitions"]:
                if trans.source == loop.primary_resource:
                    mechanic["rules"].append(
                        f"{trans.transition_type.value}: {trans.source} with rate {trans.rate:.3f}"
                    )

            # Add related feedback
            for fb in atomic_system["feedback"]:
                if loop.primary_resource in fb.target_property:
                    mechanic["feedback"].append(
                        f"{fb.modality} feedback on {fb.trigger_type} (intensity: {fb.intensity:.2f})"
                    )

            # Only add if we have some content
            if mechanic["actions"] or mechanic["rules"]:
                mechanics.append(mechanic)

        return mechanics

    def _generate_title(
        self,
        constants: CosmologicalConstants,
        framework: FrameworkConstraints,
    ) -> str:
        """Generate a title from system properties."""
        prefixes = {
            "conservation": "Frugal",
            "flow": "Fluid",
            "growth": "Flourishing",
        }

        suffixes = {
            "survival": "Endurance",
            "puzzle": "Enigma",
            "strategy": "Conquest",
            "exploration": "Discovery",
        }

        # Detect framework type from properties
        if framework.stakes_magnitude > 0.8:
            suffix = suffixes["survival"]
        elif framework.coupling_density > 0.8:
            suffix = suffixes["strategy"]
        elif framework.discovery_importance > 0.8:
            suffix = suffixes["exploration"]
        else:
            suffix = suffixes["puzzle"]

        prefix = prefixes.get(constants.energy_regime, "Eternal")

        return f"{prefix} {suffix}"

    def _derive_genre(self, framework: FrameworkConstraints) -> list[str]:
        """Derive genre tags from framework properties."""
        genres = ["procedural"]

        if framework.stakes_magnitude > 0.7:
            genres.append("survival")
        if framework.coupling_density > 0.7:
            genres.append("strategy")
        if framework.discovery_importance > 0.7:
            genres.append("exploration")
        if framework.information_asymmetry > 0.7:
            genres.append("puzzle")

        if len(genres) == 1:
            genres.append("adventure")

        return genres

    def _framework_to_dict(self, framework: FrameworkConstraints) -> dict[str, Any]:
        """Convert framework to dictionary."""
        return asdict(framework)

    def _resource_to_dict(self, resource: ResourceAtom) -> dict[str, Any]:
        """Convert resource to dictionary."""
        return asdict(resource)

    def _affordance_to_dict(self, affordance: AffordanceAtom) -> dict[str, Any]:
        """Convert affordance to dictionary (handle tuples and sets)."""
        d = asdict(affordance)
        # Convert tuples to lists for JSON serialization
        if 'requires_resources' in d:
            d['requires_resources'] = {
                k: list(v) if isinstance(v, tuple) else v
                for k, v in d['requires_resources'].items()
            }
        # Convert sets to lists for JSON serialization
        if 'requires_state' in d and isinstance(d['requires_state'], set):
            d['requires_state'] = list(d['requires_state'])
        if 'toggles_state' in d and isinstance(d['toggles_state'], set):
            d['toggles_state'] = list(d['toggles_state'])
        return d

    def _emergent_to_dict(self, emergent: EmergentSystem) -> dict[str, Any]:
        """Convert emergent system to dictionary."""
        return {
            "name": emergent.name,
            "complexity": emergent.complexity(),
            "is_stable": emergent.is_stable(),
            "feedback_loops": [
                {
                    "name": loop.name,
                    "loop_type": loop.loop_type.value,
                    "primary_resource": loop.primary_resource,
                    "equilibria": loop.equilibria,
                }
                for loop in emergent.feedback_loops
            ],
            "attractors": [
                {
                    "name": a.name,
                    "center_state": a.center_state,
                    "basin_depth": a.basin_depth,
                    "stability": a.stability,
                    "reward": a.reward,
                }
                for a in emergent.attractors
            ],
            "critical_events": [
                {
                    "name": e.name,
                    "trigger_condition": e.trigger_condition,
                    "hysteresis": e.hysteresis,
                }
                for e in emergent.critical_events
            ],
        }


def generate_v2(seed: int) -> dict[str, Any]:
    """Generate a v2.0 game specification."""
    generator = GameGeneratorV2(seed)
    return generator.generate()


def to_json_v2(spec: dict[str, Any]) -> str:
    """Convert specification to JSON."""
    return json.dumps(spec, indent=2, sort_keys=True)
