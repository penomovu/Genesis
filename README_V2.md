# SeedWorld v2.0: Emergent Procedural Game Generation

## Overview

SeedWorld is a code-first framework for **seed-based procedural generation** of coherent video-game blueprints. v2.0 introduces a revolutionary **emergent architecture** that generates games through self-organization of atomic building blocks, applying principles from physics, biology, chemistry, and systems theory.

## Quickstart

### v1.0 (Handcrafted - Original)

```bash
# Generate using the original handcrafted system
python -m seedworld 104729
```

### v2.0 (Emergent - New!)

```bash
# Generate using the new emergent system
python examples/demo_v2.py

# Or directly
python -c "from seedworld.generator_v2 import generate_v2; import json; print(json.dumps(generate_v2(104729), indent=2))"
```

## Key Concepts

### Atomic Architecture

v2.0 breaks games down into 7 primitive atomic types:

1. **ResourceAtom**: Numeric values (health, oxygen, gold)
2. **BooleanStateAtom**: Binary flags (has_key, is_poisoned)
3. **PerceptionAtom**: Information flow (what player knows)
4. **AffordanceAtom**: Player actions (use_item, toggle_switch)
5. **FeedbackAtom**: State signals (screen flash, audio cue)
6. **TransitionRule**: Game rules (if A then B)
7. **TemporalAtom**: Time constraints (deadline, window)

These atoms combine through **constrained assembly** to form:

- **Feedback Loops**: Self-referential cycles creating persistent behavior
- **Attractor Basins**: States the system naturally converges toward
- **Critical Events**: Phase transitions at thresholds

### Cosmological Constants

The seed is interpreted as initial conditions for a dynamical system:

```python
CosmologicalConstants:
  Primary Dimensions (0-1):
    entropy: Rate of decay and disorder
    fertility: Resource abundance and renewal
    volatility: Probability of stochastic events
    coherence: How tightly coupled systems are
    revelation: Information visibility

  Derived Constants:
    resource_constraint: How scarce resources are
    emergent_complexity: Maximum system depth
    chaos_threshold: Threshold for phase transitions
    time_dilation: Multiplier on temporal constants
    discovery_rate: Information becoming available

  Categorical Constants:
    energy_regime: conservation | flow | growth
    information_theory: complete | partial | fog
    temporal_structure: steady | pulsing | accelerating
```

Small seed changes create cascading divergence through **chaotic mixing** (logistic map with r=4).

### Framework-Based Genres

Instead of hardcoding genres, v2.0 uses **constraint sets**:

- **Survival**: Scarce resources, decay, accumulation
- **Puzzle**: State exploration, information hiding
- **Strategy**: Multi-objective optimization, tradeoffs
- **Exploration**: Discovery, spatial progression

The framework emerges from cosmological constants, not hardcoded!

### Self-Organizing Worlds

World structure emerges from attractor basins:
- High-value attractors → Resource-rich locations
- Low-value attractors → Hazardous areas
- Critical events → Gated passages

### Emergent Quests

Goals are **discovered**, not authored:
- Main quest from primary attractor (deepest basin)
- Secondary quests from significant attractors
- Multiple solution paths naturally emerge

## Architecture Comparison

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| Generation Method | Handcrafted templates | Emergent from atoms |
| Seed Expressiveness | 12 variations (4×3) | Infinite (chaotic mixing) |
| Mechanics | Fixed 3 | Variable (1-5) |
| World Generation | Handcrafted | Self-organizing |
| Quests | Authored | Discovered |
| Emergence | None | True |
| Information Flow | Not modeled | Explicit perception atoms |
| Validation | Structural only | Agent-based simulation |

## Output Structure

### v2.0 Game Spec

```json
{
  "seed": 104729,
  "title": "Flourishing Conquest",
  "genre": ["procedural", "strategy"],
  "version": "2.0",

  "cosmological_constants": {
    "primary_dimensions": {...},
    "derived_constants": {...},
    "categorical": {...}
  },

  "playability_metrics": {
    "win_rate": 0.65,
    "strategy_diversity": 0.82,
    "balance_score": 0.72
  },

  "atoms": {
    "resources": [...],
    "boolean_states": [...],
    "perception": [...],
    "affordances": [...],
    "feedback": [...],
    "transitions": [...],
    "temporals": [...]
  },

  "emergent_system": {
    "complexity": 10,
    "is_stable": true,
    "feedback_loops": [...],
    "attractors": [...],
    "critical_events": [...]
  },

  "mechanics": [...],
  "world": {...},
  "quests": [...]
}
```

## File Structure

```
seedworld/
├── atoms.py              # Atomic building blocks (NEW v2.0)
├── cosmology.py          # Seed → cosmological constants (NEW v2.0)
├── frameworks.py         # Genre constraint sets (NEW v2.0)
├── assembler.py          # Atomic assembly with mutation (NEW v2.0)
├── emergence.py          # Feedback loops, attractors (NEW v2.0)
├── simulation.py         # Agent-based playability testing (NEW v2.0)
├── generator_v2.py       # v2.0 emergent generator (NEW v2.0)
├── generator.py          # v1.0 handcrafted generator (PRESERVED)
├── spec.py               # Shared data models
├── validate.py           # Structural validation
└── ecs.py                # Runtime substrate

examples/
├── demo_v2.py            # v2.0 demonstration (NEW)
├── compare_generations.py # v1 vs v2 comparison (NEW)
└── generate_minigame.py  # Original v1 example (PRESERVED)

Documentation/
├── ARCHITECTURE_V2.md    # Detailed v2.0 architecture (NEW)
└── EVOLUTION_REPORT.md   # Scientific evolution analysis (NEW)
```

## Examples

### Basic Generation

```python
from seedworld.generator_v2 import generate_v2

# Generate a game from seed
spec = generate_v2(104729)

print(f"Title: {spec['title']}")
print(f"Genre: {spec['genre']}")
print(f"Complexity: {spec['emergent_system']['complexity']}")
```

### Exploring Expressive Range

```bash
# See how different seeds create different games
python examples/demo_v2.py
```

Output:
```
Seed    Title                     Genre                          Complexity  Stable
--------------------------------------------------------------------------------
10000   Eternal Conquest          procedural, strategy          8          False
10001   Frugal Endurance          procedural, survival          6          True
10002   Flourishing Discovery     procedural, exploration       10         True
10003   Fluid Enigma             procedural, puzzle            4          False
10004   Frugal Strategy          procedural, survival, strategy 7          True
```

### Comparing v1.0 vs v2.0

```bash
# Side-by-side comparison
python examples/compare_generations.py
```

## Scientific Principles

### Physics
- **Conservation Laws**: Resources follow conservation or flow
- **Energy Gradients**: Attractors create potential gradients
- **State Transitions**: Conditional modifications

### Biology
- **Natural Selection**: Simulation tests viability
- **Mutation**: Constants perturbed and reassembled
- **Adaptation**: Agents adapt strategies during testing

### Chemistry
- **Binding Sites**: Frameworks determine compatibility
- **Reaction Conditions**: Constants govern assembly
- **Emergent Properties**: Higher-level from atomic interactions

### Systems Theory
- **Feedback Loops**: Positive (amplifying) and negative (stabilizing)
- **Attractor Dynamics**: States systems converge toward
- **Criticality**: Phase transitions at thresholds
- **Self-Organization**: Global from local interactions

## Validation

### Structural Validation (v1.0)
- Location ID uniqueness
- Edge connectivity
- Quest step dependency satisfaction

### Playability Simulation (v2.0)
```python
from seedworld.simulation import run_playability_test, is_playable

metrics = run_playability_test(resources, affordances, transitions, num_simulations=100)

if is_playable(metrics):
    print("Game is winnable and balanced!")
else:
    print("Game needs adjustment...")
```

**Metrics**:
- `win_rate`: 30-70% is ideal
- `strategy_diversity`: ≥0.3 for variety
- `frustration_index`: ≤0.8 for playability
- `meaningful_choices`: ≥0.2 for depth
- `balance_score`: ≥0.5 for fairness

## Advanced Usage

### Custom Frameworks

```python
from seedworld.frameworks import FrameworkConstraints, FrameworkRegistry

# Define custom framework
custom_framework = FrameworkConstraints(
    primary_resource_types=[ResourceType.CUMULATIVE],
    resource_count_min=2,
    resource_count_max=3,
    time_pressure=0.2,
    pacing_variety=0.5,
    information_asymmetry=0.3,
    discovery_importance=0.7,
    mechanic_depth_min=2,
    mechanic_depth_max=3,
    coupling_density=0.4,
    goal_clarity=0.5,
    solution_variety=0.8,
    narrative_emergence=0.9,
    stakes_magnitude=0.3,
)

# Use in custom generator
from seedworld.assembler import AtomAssembler
from seedworld.cosmology import derive_constants

constants = derive_constants(12345)
assembler = AtomAssembler(constants, custom_framework, random.Random(12345))
system = assembler.assemble()
```

### Direct Atom Manipulation

```python
from seedworld.emergence import self_organize_system
from seedworld.atoms import ResourceAtom, AffordanceAtom, ...

# Manually define atoms
resources = [
    ResourceAtom(name="health", resource_type=ResourceType.SCARCE, ...),
    ResourceAtom(name="mana", resource_type=ResourceType.RENEWABLE, ...),
]

affordances = [
    AffordanceAtom(name="heal", ...),
    AffordanceAtom(name="cast_spell", ...),
]

# Let emergence take over
emergent = self_organize_system(resources, transitions, affordances, feedback, perception)
```

## Testing

```bash
# Run existing v1.0 tests (still pass)
python -m pytest tests/

# Test v2.0 generation
python test_v2.py
```

## Documentation

- **ARCHITECTURE_V2.md**: Detailed v2.0 architecture and design rationale
- **EVOLUTION_REPORT.md**: Scientific analysis of v1.0 → v2.0 evolution
- **README.md**: Original v1.0 documentation (this file replaces it)

## Philosophy

v2.0 embodies the principle that **emergent behavior** arises from simple rules:

> "Games are not built, they are grown. Provide the right atoms, binding sites, and reaction conditions, and complex gameplay self-organizes."

This contrasts with traditional handcrafted design:

**v1.0 Approach (Handcrafted):**
- Author mechanics explicitly
- Create world manually
- Write quests linearly
- Test through iteration
- Limited expressive range

**v2.0 Approach (Emergent):**
- Define atomic primitives
- Establish binding rules
- Set reaction conditions (constants)
- Validate through simulation
- Infinite expressive range

## Future Work

See EVOLUTION_REPORT.md for detailed roadmap:

**Phase 2**: Enhanced emergence (cellular automata worlds, dynamic mutation)
**Phase 3**: Advanced features (cross-seed hybridization, self-modifying rules)
**Phase 4**: Scientific advancements (quantum mechanics, thermodynamics)

## Contributing

v2.0 is designed for extensibility:

1. Add new atom types in `atoms.py`
2. Add new frameworks in `frameworks.py`
3. Improve emergence detection in `emergence.py`
4. Enhance simulation in `simulation.py`

All changes should maintain:
- Determinism from seed
- Backward compatibility with v1.0
- Playability validation

## Citation

If you use SeedWorld v2.0 in research:

```
SeedWorld: Emergent Procedural Game Generation from Atomic Building Blocks
Using Principles from Physics, Biology, Chemistry, and Systems Theory
Version 2.0, 2025
```

## License

See LICENSE file for details.

---

**Version**: 2.0 (with v1.0 preserved)
**Status**: Production-ready (v1.0), Experimental (v2.0)
**Authors**: SeedWorld Architecture Team
