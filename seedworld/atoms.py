"""Fundamental atomic units for emergent game generation.

These are the primitive types from which all game systems are constructed.
They follow combinatorial design principles with well-defined composition rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ResourceType(str, Enum):
    """Types of resource atoms that drive game dynamics."""

    SCARCE = "scarce"  # Limited, high stakes (oxygen, health)
    RENEWABLE = "renewable"  # Regenerates over time (mana, stamina)
    CUMULATIVE = "cumulative"  # Accumulates (experience, gold)
    FLOW = "flow"  # Rate-based resource (movement speed, production)


class StateTransition(str, Enum):
    """Types of state changes that can occur."""

    LINEAR = "linear"  # A += delta
    THRESHOLD = "threshold"  # if A >= threshold: trigger
    DECAY = "decay"  # A -= rate * time
    COMPOUND = "compound"  # A = A * (1 + rate)
    TRANSFER = "transfer"  # A -= delta, B += delta


@dataclass(frozen=True, slots=True)
class ResourceAtom:
    """A numeric resource that constrains or enables player actions.

    Examples: health, oxygen, mana, money, ammunition.
    """

    name: str
    resource_type: ResourceType
    initial: float
    min: float = 0.0
    max: float = float("inf")
    decay_rate: float = 0.0  # Per time unit, if applicable
    renew_rate: float = 0.0  # Per time unit, if applicable

    def is_conservation_constrained(self) -> bool:
        """Whether this resource follows conservation (limited pool)."""
        return self.resource_type in (ResourceType.SCARCE, ResourceType.FLOW)


@dataclass(frozen=True, slots=True)
class BooleanStateAtom:
    """A binary flag representing a condition or capability.

    Examples: has_key, is_poisoned, can_swim, door_locked.
    """

    name: str
    initial: bool = False
    persistence: str = "global"  # "global", "location", "session"


@dataclass(frozen=True, slots=True)
class PerceptionAtom:
    """Information about game state that is available to the player.

    Models information flow and uncertainty.
    """

    name: str
    observed_property: str  # What property this reveals
    visibility: str  # "always", "proximity", "active", "conditional"
    precision: str  # "exact", "approximate", "binary", "tiered"
    cost: float = 0.0  # Resource cost to observe, if any


@dataclass(frozen=True, slots=True)
class AffordanceAtom:
    """A possible action available to the player in certain conditions.

    Models player agency and the interaction language of the game.
    """

    name: str
    requires_resources: dict[str, tuple[float, float]]  # resource: (min, max)
    grants_resources: dict[str, float]
    requires_state: set[str]  # Boolean flags that must be true
    toggles_state: set[str]  # Boolean flags to flip
    duration: float = 0.0  # Time to execute
    cooldown: float = 0.0  # Minimum time between uses


@dataclass(frozen=True, slots=True)
class FeedbackAtom:
    """A signal sent to the player indicating a state change.

    Models the feedback loop that closes the cycle of action-perception.
    """

    name: str
    trigger_type: str  # "on_change", "on_threshold", "on_enter", "on_exit"
    target_property: str
    modality: str  # "visual", "audio", "haptic", "narrative"
    intensity: float  # 0.0 to 1.0, affects salience


@dataclass(frozen=True, slots=True)
class TransitionRule:
    """A conditional state transition representing a game rule.

    Combines perception, affordance, and transition to form atomic mechanics.
    """

    name: str
    condition: str  # Logical expression
    transition_type: StateTransition
    source: str  # State/resource being modified
    target: str | None = None  # For transfer operations
    delta: float = 0.0
    rate: float = 0.0
    threshold: float = 0.0
    probability: float = 1.0  # Stochastic rules


@dataclass(frozen=True, slots=True)
class TemporalAtom:
    """A time-based constraint or opportunity.

    Models pacing and temporal agency.
    """

    name: str
    type: str  # "deadline", "window", "rhythm", "delay"
    duration: float
    repeats: bool = False
    decay: float = 0.0  # Rate of change in duration/intensity
