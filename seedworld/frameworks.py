"""Game frameworks: constraint sets that bias generation toward play patterns.

Rather than hardcoding genres, frameworks provide constraint sets and biases that
allow the same atomic building blocks to organize into very different types of
games. Think of these as "boundary conditions" for the game universe.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .atoms import ResourceType
from .cosmology import CosmologicalConstants


@dataclass(frozen=True, slots=True)
class FrameworkConstraints:
    """Constraints that bias generation toward certain patterns.

    These don't hardcode specific mechanics, but create biases in how
    atoms combine and what structures emerge.
    """

    # Resource biases
    primary_resource_types: list[ResourceType]
    resource_count_min: int
    resource_count_max: int

    # Temporal biases
    time_pressure: float  # 0-1: how much time pressure
    pacing_variety: float  # 0-1: variability in pacing

    # Information biases
    information_asymmetry: float  # 0-1: player information disadvantage
    discovery_importance: float  # 0-1: role of exploration

    # Complexity biases
    mechanic_depth_min: int
    mechanic_depth_max: int
    coupling_density: float  # 0-1: how interconnected systems are

    # Goal structure
    goal_clarity: float  # 0-1: how explicit goals are
    solution_variety: float  # 0-1: multiple paths encouraged

    # Narrative structure
    narrative_emergence: float  # 0-1: story emerges vs is told
    stakes_magnitude: float  # 0-1: scale of consequences


class FrameworkRegistry:
    """Registry of framework templates for common play patterns."""

    @staticmethod
    def survival() -> FrameworkConstraints:
        """Survival framework: resource management, decay, accumulation.

        Biases toward:
        - Scarce resources with decay
        - Time pressure
        - Clear immediate threats
        - Accumulation as win condition
        """
        return FrameworkConstraints(
            primary_resource_types=[
                ResourceType.SCARCE,
                ResourceType.SCARCE,
                ResourceType.CUMULATIVE,
            ],
            resource_count_min=3,
            resource_count_max=5,
            time_pressure=0.8,
            pacing_variety=0.4,
            information_asymmetry=0.5,
            discovery_importance=0.6,
            mechanic_depth_min=2,
            mechanic_depth_max=4,
            coupling_density=0.6,
            goal_clarity=0.8,
            solution_variety=0.5,
            narrative_emergence=0.3,
            stakes_magnitude=0.9,
        )

    @staticmethod
    def puzzle() -> FrameworkConstraints:
        """Puzzle framework: state space exploration, information hiding.

        Biases toward:
        - Binary state exploration
        - Information discovery
        - Low time pressure
        - Clear solution states
        - Logical deduction
        """
        return FrameworkConstraints(
            primary_resource_types=[ResourceType.FLOW, ResourceType.FLOW],
            resource_count_min=1,
            resource_count_max=2,
            time_pressure=0.2,
            pacing_variety=0.8,
            information_asymmetry=0.9,
            discovery_importance=1.0,
            mechanic_depth_min=3,
            mechanic_depth_max=5,
            coupling_density=0.7,
            goal_clarity=0.6,
            solution_variety=0.8,
            narrative_emergence=0.2,
            stakes_magnitude=0.4,
        )

    @staticmethod
    def strategy() -> FrameworkConstraints:
        """Strategy framework: multi-objective optimization, tradeoffs.

        Biases toward:
        - Multiple competing resources
        - Interconnected systems
        - Long-term planning
        - Risk/reward decisions
        - Adaptation to changing conditions
        """
        return FrameworkConstraints(
            primary_resource_types=[
                ResourceType.CUMULATIVE,
                ResourceType.RENEWABLE,
                ResourceType.FLOW,
            ],
            resource_count_min=4,
            resource_count_max=7,
            time_pressure=0.4,
            pacing_variety=0.6,
            information_asymmetry=0.4,
            discovery_importance=0.5,
            mechanic_depth_min=4,
            mechanic_depth_max=6,
            coupling_density=0.9,
            goal_clarity=0.4,
            solution_variety=0.9,
            narrative_emergence=0.6,
            stakes_magnitude=0.7,
        )

    @staticmethod
    def exploration() -> FrameworkConstraints:
        """Exploration framework: discovery, mapping, sensory engagement.

        Biases toward:
        - Information discovery
        - Spatial progression
        - Sensory feedback
        - Optional challenges
        - Low stakes
        """
        return FrameworkConstraints(
            primary_resource_types=[
                ResourceType.SCARCE,
                ResourceType.RENEWABLE,
            ],
            resource_count_min=2,
            resource_count_max=3,
            time_pressure=0.3,
            pacing_variety=0.9,
            information_asymmetry=0.8,
            discovery_importance=1.0,
            mechanic_depth_min=2,
            mechanic_depth_max=3,
            coupling_density=0.4,
            goal_clarity=0.3,
            solution_variety=0.7,
            narrative_emergence=0.8,
            stakes_magnitude=0.3,
        )

    @staticmethod
    def hybrid_survival_strategy() -> FrameworkConstraints:
        """Hybrid: survival mechanics with strategic depth.

        Combines resource pressure with meaningful tradeoffs.
        """
        return FrameworkConstraints(
            primary_resource_types=[
                ResourceType.SCARCE,
                ResourceType.CUMULATIVE,
                ResourceType.RENEWABLE,
            ],
            resource_count_min=3,
            resource_count_max=5,
            time_pressure=0.6,
            pacing_variety=0.6,
            information_asymmetry=0.5,
            discovery_importance=0.6,
            mechanic_depth_min=3,
            mechanic_depth_max=5,
            coupling_density=0.8,
            goal_clarity=0.6,
            solution_variety=0.7,
            narrative_emergence=0.5,
            stakes_magnitude=0.8,
        )


def select_framework(constants: CosmologicalConstants) -> FrameworkConstraints:
    """Select a framework based on cosmological constants.

    This allows the same seed-derived constants to determine which
    play patterns are emphasized, creating genre emergence from
    fundamental parameters.
    """
    # Framework selection based on energy and information regimes
    if constants.energy_regime == "conservation":
        if constants.information_theory == "fog":
            return FrameworkRegistry.puzzle()
        elif constants.information_theory == "partial":
            return FrameworkRegistry.survival()
        else:
            return FrameworkRegistry.exploration()
    elif constants.energy_regime == "growth":
        if constants.coherence > 0.6:
            return FrameworkRegistry.strategy()
        else:
            return FrameworkRegistry.hybrid_survival_strategy()
    else:  # flow regime
        if constants.temporal_structure == "steady":
            return FrameworkRegistry.exploration()
        else:
            return FrameworkRegistry.hybrid_survival_strategy()
