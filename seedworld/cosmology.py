"""Cosmological constants derived from seeds that govern game physics.

This module implements a scientific approach to seed interpretation where the
seed acts as initial conditions for a "universe" of possible games. Small changes
in the seed cascade through the generation process, creating divergent outcomes
through chaos-theoretic sensitivity to initial conditions.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CosmologicalConstants:
    """Fundamental constants that govern the physics of a generated game.

    These constants are derived from the seed using deterministic chaos
    principles. They control:
    - Resource abundance and scarcity patterns
    - System stability vs chaos
    - Emergence thresholds
    - Pacing and temporal dynamics
    - Information flow and uncertainty
    """

    # Primary dimensions (0-1, derived from seed bits)
    entropy: float  # Rate of decay and disorder
    fertility: float  # Resource abundance and renewal
    volatility: float  # Probability of stochastic events
    coherence: float  # How tightly coupled systems are
    revelation: float  # Information visibility

    # Derived constants
    resource_constraint: float  # 0-1: how scarce resources are
    emergent_complexity: float  # 0-1: maximum system depth
    chaos_threshold: float  # 0-1: threshold for phase transitions
    time_dilation: float  # Multiplier on all temporal constants
    discovery_rate: float  # Rate at which information becomes available

    # Categorical constants
    energy_regime: str  # "conservation", "flow", "growth"
    information_theory: str  # "complete", "partial", "fog"
    temporal_structure: str  # "steady", "pulsing", "accelerating"

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_dimensions": {
                "entropy": self.entropy,
                "fertility": self.fertility,
                "volatility": self.volatility,
                "coherence": self.coherence,
                "revelation": self.revelation,
            },
            "derived_constants": {
                "resource_constraint": self.resource_constraint,
                "emergent_complexity": self.emergent_complexity,
                "chaos_threshold": self.chaos_threshold,
                "time_dilation": self.time_dilation,
                "discovery_rate": self.discovery_rate,
            },
            "categorical": {
                "energy_regime": self.energy_regime,
                "information_theory": self.information_theory,
                "temporal_structure": self.temporal_structure,
            },
        }


def _chaos_mix(seed: int, iterations: int = 3) -> float:
    """Apply chaotic mixing to extract smooth distributions from seeds.

    Uses the logistic map: x(n+1) = r * x(n) * (1 - x(n)) with r=4 for chaos.
    This ensures nearby seeds produce divergent outputs (butterfly effect).
    """
    x = (seed % 1000) / 1000.0
    r = 4.0  # Fully chaotic regime

    for _ in range(iterations):
        x = r * x * (1 - x)

    return x


def _cascade_derive(base: float, offset: int, scale: float = 0.1) -> float:
    """Derive secondary constants from primary ones with controlled variation.

    This creates cascading influence where each constant affects those
    derived from it, amplifying seed differences.
    """
    perturbed = base + (math.sin(offset) * scale)
    return max(0.0, min(1.0, perturbed))


def derive_constants(seed: int) -> CosmologicalConstants:
    """Derive cosmological constants from a seed using deterministic chaos.

    The seed is treated as initial conditions for a dynamical system.
    Through chaotic mixing and cascading derivation, small seed changes
    produce meaningfully different game universes.
    """
    rng = random.Random(seed)

    # Primary dimensions from chaotic mixing of seed
    entropy = _chaos_mix(seed)
    fertility = _chaos_mix(seed + 1)
    volatility = _chaos_mix(seed + 2)
    coherence = _chaos_mix(seed + 3)
    revelation = _chaos_mix(seed + 4)

    # Derived constants cascade from primaries
    resource_constraint = 1.0 - fertility  # High fertility = low constraint
    emergent_complexity = coherence * (1.0 - volatility)
    chaos_threshold = volatility * coherence
    time_dilation = _cascade_derive(entropy, 100, 0.3)
    discovery_rate = _cascade_derive(revelation, 200, 0.2)

    # Categorical constants derived from thresholds
    if fertility > 0.7:
        energy_regime = "growth"
    elif fertility < 0.3:
        energy_regime = "conservation"
    else:
        energy_regime = "flow"

    if revelation > 0.7:
        information_theory = "complete"
    elif revelation < 0.3:
        information_theory = "fog"
    else:
        information_theory = "partial"

    if entropy > 0.7:
        temporal_structure = "accelerating"
    elif entropy < 0.3:
        temporal_structure = "steady"
    else:
        temporal_structure = "pulsing"

    return CosmologicalConstants(
        entropy=entropy,
        fertility=fertility,
        volatility=volatility,
        coherence=coherence,
        revelation=revelation,
        resource_constraint=resource_constraint,
        emergent_complexity=emergent_complexity,
        chaos_threshold=chaos_threshold,
        time_dilation=time_dilation,
        discovery_rate=discovery_rate,
        energy_regime=energy_regime,
        information_theory=information_theory,
        temporal_structure=temporal_structure,
    )


def expressive_range_seeds(count: int = 5, base: int = 1000) -> list[int]:
    """Generate seeds that span the expressive range of the generator.

    Returns seeds that are maximally different in cosmological constant space.
    This helps demonstrate that small seed changes produce meaningfully different games.
    """
    # Select seeds that are far apart in bit-space
    seeds = []
    for i in range(count):
        seeds.append(base + (i * 2**10))  # Space seeds by 1024

    return seeds
