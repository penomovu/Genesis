"""Agent-based simulation for validating playability and winnability.

This module implements lightweight agent simulations that test whether generated
games are:
- Winnable (at least one path to victory exists)
- Interesting (meaningful choices exist)
- Balanced (appropriate challenge level)
- Internally consistent (no logical contradictions)

The simulation uses Monte Carlo methods to explore the state space and
identify optimal, suboptimal, and failed strategies.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass
from typing import Any

from .atoms import ResourceAtom, AffordanceAtom, TransitionRule
from .spec import GameSpec


@dataclass(frozen=True, slots=True)
class SimulationState:
    """State of a simulation agent during testing."""

    resources: dict[str, float]
    boolean_state: set[str]
    time_elapsed: float
    victory: bool = False
    death: bool = False
    stuck: bool = False


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Results from running a single simulation."""

    success: bool
    time_elapsed: float
    resources_remaining: dict[str, float]
    path_length: int
    actions_taken: list[str]


@dataclass(frozen=True, slots=True)
class PlayabilityMetrics:
    """Aggregate metrics from multiple simulation runs."""

    win_rate: float  # Proportion of successful simulations
    avg_completion_time: float
    avg_path_length: float
    strategy_diversity: float  # How many distinct solution paths
    frustration_index: float  # How often agents get stuck
    meaningful_choices: float  # Proportion of decisions that matter
    balance_score: float  # 0-1, optimal challenge


class Agent:
    """A simulated player agent for testing game winnability."""

    def __init__(
        self,
        resources: list[ResourceAtom],
        affordances: list[AffordanceAtom],
        transitions: list[TransitionRule],
        exploration_rate: float = 0.3,
        rng: random.Random | None = None,
    ):
        self.resources = resources
        self.affordances = affordances
        self.transitions = transitions
        self.exploration_rate = exploration_rate
        self.rng = rng or random.Random()

    def simulate(
        self,
        max_steps: int = 1000,
        max_time: float = 1000.0,
    ) -> SimulationResult:
        """Run a single simulation attempt."""
        # Initialize state
        state = SimulationState(
            resources={r.name: r.initial for r in self.resources},
            boolean_state=set(),
            time_elapsed=0.0,
        )

        actions_taken: list[str] = []
        path_length = 0

        for step in range(max_steps):
            # Check termination conditions
            if state.time_elapsed >= max_time:
                break

            # Apply transitions (passive effects)
            state = self._apply_transitions(state)

            # Check for death conditions
            if self._check_death(state):
                return SimulationResult(
                    success=False,
                    time_elapsed=state.time_elapsed,
                    resources_remaining=state.resources,
                    path_length=path_length,
                    actions_taken=actions_taken,
                )

            # Check for victory conditions
            if self._check_victory(state):
                return SimulationResult(
                    success=True,
                    time_elapsed=state.time_elapsed,
                    resources_remaining=state.resources,
                    path_length=path_length,
                    actions_taken=actions_taken,
                )

            # Choose an action
            action = self._choose_action(state)
            if action is None:
                # No valid actions available
                return SimulationResult(
                    success=False,
                    time_elapsed=state.time_elapsed,
                    resources_remaining=state.resources,
                    path_length=path_length,
                    actions_taken=actions_taken,
                )

            # Apply action
            state = self._apply_action(state, action)
            actions_taken.append(action.name)
            path_length += 1

            # Advance time
            state = SimulationState(
                resources=state.resources,
                boolean_state=state.boolean_state,
                time_elapsed=state.time_elapsed + action.duration,
                victory=state.victory,
                death=state.death,
                stuck=state.stuck,
            )

        # Ran out of steps/time
        return SimulationResult(
            success=self._check_victory(state),
            time_elapsed=state.time_elapsed,
            resources_remaining=state.resources,
            path_length=path_length,
            actions_taken=actions_taken,
        )

    def _apply_transitions(self, state: SimulationState) -> SimulationState:
        """Apply passive transition rules."""
        new_resources = state.resources.copy()

        for transition in self.transitions:
            # Simple evaluation of condition
            if transition.condition == "always":
                if transition.transition_type.value == "decay":
                    new_resources[transition.source] = max(
                        0.0,
                        new_resources[transition.source]
                        - transition.rate * 0.1,  # dt = 0.1
                    )
                elif transition.transition_type.value == "linear":
                    new_resources[transition.source] = (
                        new_resources[transition.source] + transition.delta * 0.1
                    )

        return SimulationState(
            resources=new_resources,
            boolean_state=state.boolean_state,
            time_elapsed=state.time_elapsed,
        )

    def _check_death(self, state: SimulationState) -> bool:
        """Check if the agent has died."""
        for resource in self.resources:
            if state.resources[resource.name] <= resource.min:
                # Check if this is a critical resource
                if resource.resource_type.value == "scarce":
                    return True
        return False

    def _check_victory(self, state: SimulationState) -> bool:
        """Check if victory condition has been met."""
        # Simplified: victory if any cumulative resource is high enough
        for resource in self.resources:
            if resource.resource_type.value == "cumulative":
                if state.resources[resource.name] >= 50.0:
                    return True
        return False

    def _choose_action(self, state: SimulationState) -> AffordanceAtom | None:
        """Choose an action using exploration-exploitation."""
        valid_actions = [
            action
            for action in self.affordances
            if self._can_perform(action, state)
        ]

        if not valid_actions:
            return None

        # Exploration: sometimes choose random valid action
        if self.rng.random() < self.exploration_rate:
            return self.rng.choice(valid_actions)

        # Exploitation: choose action that maximizes progress
        return self._best_action(state, valid_actions)

    def _can_perform(self, action: AffordanceAtom, state: SimulationState) -> bool:
        """Check if an action can be performed."""
        # Check resource requirements
        for resource, (min_val, max_val) in action.requires_resources.items():
            val = state.resources.get(resource, 0.0)
            if val < min_val or val > max_val:
                return False

        # Check state requirements
        for req in action.requires_state:
            if req not in state.boolean_state:
                return False

        return True

    def _best_action(
        self,
        state: SimulationState,
        valid_actions: list[AffordanceAtom],
    ) -> AffordanceAtom:
        """Choose the best action using a simple heuristic."""
        # Prefer actions that increase scarce or cumulative resources
        best_score = float("-inf")
        best_action = valid_actions[0]

        for action in valid_actions:
            score = 0.0
            for resource, delta in action.grants_resources.items():
                if "scarce" in resource or "cumulative" in resource:
                    score += delta
            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def _apply_action(
        self,
        state: SimulationState,
        action: AffordanceAtom,
    ) -> SimulationState:
        """Apply an action to modify state."""
        new_resources = state.resources.copy()
        new_boolean = state.boolean_state.copy()

        # Apply resource changes
        for resource, delta in action.grants_resources.items():
            new_resources[resource] = new_resources.get(resource, 0.0) + delta

        # Toggle boolean states
        for state_name in action.toggles_state:
            if state_name in new_boolean:
                new_boolean.remove(state_name)
            else:
                new_boolean.add(state_name)

        return SimulationState(
            resources=new_resources,
            boolean_state=new_boolean,
            time_elapsed=state.time_elapsed,
        )


def run_playability_test(
    resources: list[ResourceAtom],
    affordances: list[AffordanceAtom],
    transitions: list[TransitionRule],
    num_simulations: int = 100,
) -> PlayabilityMetrics:
    """Run Monte Carlo simulations to assess playability."""
    results: list[SimulationResult] = []
    action_sequences: list[tuple[str, ...]] = []

    for i in range(num_simulations):
        # Vary exploration rate to test different play styles
        exploration_rate = 0.1 + (i % 5) * 0.2
        rng = random.Random(i)

        agent = Agent(
            resources=resources,
            affordances=affordances,
            transitions=transitions,
            exploration_rate=exploration_rate,
            rng=rng,
        )

        result = agent.simulate()
        results.append(result)
        action_sequences.append(tuple(result.actions_taken))

    # Calculate metrics
    successes = [r for r in results if r.success]
    win_rate = len(successes) / len(results) if results else 0.0

    if successes:
        avg_time = sum(r.time_elapsed for r in successes) / len(successes)
        avg_length = sum(r.path_length for r in successes) / len(successes)
    else:
        avg_time = float("inf")
        avg_length = float("inf")

    # Strategy diversity: proportion of unique action sequences
    unique_sequences = set(action_sequences)
    strategy_diversity = len(unique_sequences) / len(action_sequences) if action_sequences else 0.0

    # Frustration index: proportion of runs that get stuck or die
    failures = [r for r in results if not r.success]
    frustration_index = len(failures) / len(results) if results else 0.0

    # Meaningful choices: inverse of action repetition
    action_counts = Counter(a for seq in action_sequences for a in seq)
    if action_counts:
        entropy = -sum(
            (c / len(action_counts)) * (c / len(action_counts))
            for c in action_counts.values()
        )
        meaningful_choices = min(1.0, entropy / 10.0)  # Normalize
    else:
        meaningful_choices = 0.0

    # Balance score: win rate should be neither too high nor too low
    optimal_range = (0.3, 0.7)
    if optimal_range[0] <= win_rate <= optimal_range[1]:
        balance_score = 1.0
    elif win_rate < optimal_range[0]:
        balance_score = win_rate / optimal_range[0]
    else:
        balance_score = max(0.0, 1.0 - (win_rate - optimal_range[1]) / 0.3)

    return PlayabilityMetrics(
        win_rate=win_rate,
        avg_completion_time=avg_time,
        avg_path_length=avg_length,
        strategy_diversity=strategy_diversity,
        frustration_index=frustration_index,
        meaningful_choices=meaningful_choices,
        balance_score=balance_score,
    )


def is_playable(metrics: PlayabilityMetrics) -> bool:
    """Determine if a game meets minimum playability thresholds."""
    return (
        metrics.win_rate >= 0.1  # At least 10% winnable
        and metrics.strategy_diversity >= 0.3  # Some strategic variety
        and metrics.frustration_index <= 0.8  # Not too frustrating
        and metrics.meaningful_choices >= 0.2  # Some meaningful decisions
    )
