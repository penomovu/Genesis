# SeedWorld v2.0 Architecture: Emergent Game Generation

## Executive Summary

v2.0 represents a fundamental evolution from handcrafted template generation to true emergent gameplay. The system now treats games as complex systems that self-organize from atomic building blocks, applying principles from physics, biology, chemistry, and systems theory.

## Key Innovations

### 1. Atomic Architecture

The fundamental units have been refined from descriptive strings to executable primitives:

**v1.0 Atoms (Descriptive):**
- Mechanics: text descriptions of actions and rules
- No executable behavior
- No compositional semantics

**v2.0 Atoms (Executable):**
- `ResourceAtom`: numeric values with constraints (min, max, decay, renew)
- `BooleanStateAtom`: binary conditions and capabilities
- `PerceptionAtom`: information flow modeling
- `AffordanceAtom`: player agency and action space
- `FeedbackAtom`: state change signals to player
- `TransitionRule`: conditional state modifications
- `TemporalAtom`: time-based constraints and opportunities

### 2. Cosmological Constants

The seed is now interpreted as initial conditions for a dynamical system:

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

**Expressive Range:**
- Chaotic mixing ensures nearby seeds diverge (butterfly effect)
- Cascading derivation amplifies seed differences
- Small changes create meaningfully different games

### 3. Framework-Based Genre Emergence

Instead of hardcoding genres, we provide constraint sets:

**Survival Framework:**
- Scarce resources with decay
- High time pressure
- Clear immediate threats
- Accumulation as win condition

**Puzzle Framework:**
- Binary state exploration
- Information discovery
- Low time pressure
- Logical deduction

**Strategy Framework:**
- Multiple competing resources
- Interconnected systems
- Long-term planning
- Risk/reward decisions

**Exploration Framework:**
- Information discovery
- Spatial progression
- Sensory feedback
- Optional challenges

Framework selection emerges from cosmological constants, not hardcoded.

### 4. Emergent Systems

Mechanics are not authored but emerge from atomic interactions:

**Feedback Loops:**
- Negative (homeostatic, stabilizing)
- Positive (amplifying, destabilizing)
- Mixed (alternating dynamics)

**Attractor Basins:**
- Regions of state space that naturally converge
- Create strategic objectives
- Depth indicates escape difficulty

**Critical Events:**
- Phase transitions at thresholds
- Create meaningful choices
- Hysteresis creates commitment

Example: Resource decay + renewal + thresholds → self-organizing resource loop

### 5. Self-Organizing Worlds

World structure emerges from system constraints rather than being handcrafted:

- Locations generated based on attractor basins
- Gates created from critical events
- Items placed in high-value attractor locations
- Hazards in low-value attractor locations
- Edges connect based on feedback loop dependencies

**Cellular Automata Approach (Future):**
- Start with empty space
- Atoms interact locally using binding rules
- Territory formation emerges
- Dynamic gating self-organizes from requirements

### 6. Emergent Quests

Goals are discovered, not authored:

- Main quest from primary attractor (deepest basin)
- Secondary quests from significant attractors
- Quest steps from state transition requirements
- Multiple paths naturally arise from attractor accessibility

**No Hardcoded Critical Paths:**
Players can discover different solution strategies based on how they interact with the emergent systems.

### 7. Simulation-Based Validation

Playability is tested through agent simulation:

```python
PlayabilityMetrics:
  win_rate: Proportion of successful simulations
  avg_completion_time: Time to victory
  avg_path_length: Actions needed
  strategy_diversity: Distinct solution paths
  frustration_index: Getting stuck/dying rate
  meaningful_choices: Decisions that matter
  balance_score: Optimal challenge (30-70% win rate)
```

**Monte Carlo Testing:**
- Multiple agents with different exploration rates
- Test winnability and solvability
- Identify frustrating dead-ends
- Ensure strategic variety

### 8. Information Flow Modeling

The system explicitly models what the player knows:

- Visibility: always | proximity | active | conditional
- Precision: exact | approximate | binary | tiered
- Cost: Resource expenditure to observe

This creates genuine discovery and exploration mechanics.

## Scientific Principles Applied

### Physics
- **Conservation Laws:** Resources follow conservation or flow
- **Energy Gradients:** Attractors create potential gradients
- **State Transitions:** Conditional modifications to system state
- **Constraints:** Min/max values create hard boundaries

### Biology
- **Natural Selection:** Simulation tests viability of generated systems
- **Mutation:** Constants are perturbed and systems reassembled
- **Adaptation:** Player agents adapt strategies during testing
- **Evolution:** Successful patterns emerge over iterations

### Chemistry
- **Binding Sites:** Framework constraints determine atom compatibility
- **Reaction Conditions:** Cosmological constants govern assembly
- **Molecular Structure:** Atoms combine into molecules (mechanics)
- **Emergent Properties:** Higher-level behavior from atomic interactions

### Systems Theory
- **Feedback Loops:** Both positive (amplifying) and negative (stabilizing)
- **Attractor Dynamics:** States that systems naturally converge toward
- **Criticality:** Phase transitions at thresholds
- **Self-Organization:** Global structure from local interactions
- **Stability vs Chaos:** Balance between predictable and surprising

## File Structure

```
seedworld/
├── atoms.py              # Atomic building blocks
├── cosmology.py          # Seed → cosmological constants
├── frameworks.py         # Genre constraint sets
├── assembler.py         # Atomic assembly with mutation
├── emergence.py         # Feedback loops, attractors, critical events
├── simulation.py         # Agent-based playability testing
├── generator_v2.py       # v2.0 emergent generator
├── generator.py          # v1.0 handcrafted generator (preserved)
├── spec.py               # Shared data models
├── validate.py           # Structural validation
└── ecs.py                # Runtime substrate (unchanged)

examples/
├── compare_generations.py  # v1 vs v2 demonstration
└── generate_minigame.py    # Original example
```

## Comparison: v1.0 vs v2.0

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Generation Method** | Handcrafted templates | Emergent from atoms |
| **Seed Expressiveness** | 4 tones × 3 sizes = 12 variations | Infinite (chaotic mixing) |
| **Mechanics** | Fixed 3 mechanics | Variable number, emergent |
| **World Generation** | Handcrafted hub-and-spokes | Self-organizing from attractors |
| **Quests** | Authored critical path | Discovered from attractors |
| **Genre Support** | Hardcoded survival | Emergent from frameworks |
| **Playability Testing** | Structural validation only | Agent-based simulation |
| **Emergence** | None (predefined outcomes) | True (unpredictable from atoms) |
| **Information Flow** | Not modeled | Explicit perception atoms |
| **Player Agency** | Descriptive | Executable affordances |
| **Temporal Dynamics** | Only oxygen decay | Multiple temporal patterns |
| **Risk-Reward** | Not formalized | Attractor depth/reward |
| **Scalability** | Limited to 1 game type | Multi-genre capable |

## Generation Pipeline

### v1.0 Pipeline
```
Seed → (Choose 1 of 4 tones) → (Choose 1 of 3 sizes)
  → Generate constants (simple floats)
  → Use handcrafted mechanics, world, quests
  → Structural validation
  → Output
```

### v2.0 Pipeline
```
Seed → Chaotic mixing → Cosmological constants
  → Framework selection (from constants)
  → Atomic assembly (constrained by framework)
    ├─ Generate resources (type, decay, renew)
    ├─ Generate boolean states (flags, doors, keys)
    ├─ Generate perception (visibility, precision)
    ├─ Generate affordances (actions)
    ├─ Generate feedback (signals)
    ├─ Generate transitions (rules)
    └─ Generate temporals (pacing)
  → Self-organize into emergent systems
    ├─ Detect feedback loops
    ├─ Find attractors
    └─ Identify critical events
  → Agent simulation validation
    └─ If not playable: mutate and retry
  → Generate world (from attractors)
  → Generate quests (from attractors)
  → Convert atoms to mechanics
  → Output
```

## Example: How Emergence Works

**Atomic Inputs:**
```python
ResourceAtom: health (scarce, decay_rate=1.0)
ResourceAtom: food (renewable, renew_rate=0.5)
AffordanceAtom: eat (grants health, requires food)
TransitionRule: health_decay (always, decay)
TransitionRule: food_renew (always, renew)
FeedbackAtom: health_low (on_threshold, audio)
```

**Emergent Structure:**
```python
FeedbackLoop:
  name: "health_maintenance_loop"
  loop_type: NEGATIVE  # Homeostatic
  primary_resource: "health"
  triggers: [health_decay, eat]
  equilibria: [50.0]  # Stable equilibrium
  instabilities: []

AttractorBasin:
  name: "survival_state"
  center_state: {health: 50.0, food: 30.0}
  basin_depth: 0.7
  stability: "stable"
  reward: 0.5
```

**Quests That Emerge:**
1. Primary: "Survive" (maintain health above 0)
2. Secondary: "Find Food" (reach high food attractor)
3. Optional: "Maximize Health" (reach 100 health attractor)

**Player Experience:**
- Player discovers that food heals (exploration)
- Player learns to manage health vs food tradeoff (strategy)
- Multiple paths: scavenge, hunt, cultivate (variety)
- Tension from decay (time pressure)

None of this was explicitly authored—it emerged from atomic interactions!

## Validation and Quality Assurance

### Structural Validation (v1.0 preserved)
- Location ID uniqueness
- Edge connectivity
- Quest step dependency satisfaction

### Playability Simulation (v2.0 new)
- Winnability testing (agents must be able to win)
- Strategic variety (multiple viable paths)
- Balance assessment (30-70% win rate target)
- Frustration detection (stuck/death rate)

### Metrics
```
Good Game Thresholds:
- win_rate: 0.1 to 0.9 (not impossible, not trivial)
- strategy_diversity: ≥ 0.3 (some variety)
- frustration_index: ≤ 0.8 (playable)
- meaningful_choices: ≥ 0.2 (decisions matter)
- balance_score: ≥ 0.5 (fair challenge)
```

## Future Enhancements

### Phase 1: Current Foundation
✅ Atomic architecture
✅ Cosmological constants
✅ Framework-based genre emergence
✅ Emergent systems
✅ Simulation validation

### Phase 2: Enhanced Emergence
🔄 Cellular automata world generation
🔄 Dynamic mutation during play
🔄 Narrative generation from state history
🔄 Multiplayer emergence (interacting agents)

### Phase 3: Advanced Features
🔄 Learning systems (AI adapts to player)
🔄 Cross-seed hybridization (game genetics)
🔄 Self-modifying rules (games that evolve)
🔄 Infinite procedural expansion

## Migration Guide for Users

### For Current v1.0 Users
v1.0 generator is preserved and unchanged. To use v2.0:

```python
# Old way (still works)
from seedworld.generator import generate as generate_v1
spec = generate_v1(seed)

# New way (emergent)
from seedworld.generator_v2 import generate_v2
spec = generate_v2(seed)
```

### Key Differences in Output
v2.0 spec includes additional fields:
- `version`: "2.0"
- `cosmological_constants`: The physics of the game universe
- `framework`: Constraint set used
- `playability_metrics`: Simulation results
- `atoms`: Complete atomic breakdown
- `emergent_system`: Self-organized structure

### Integration with Existing Tools
v2.0 output is still JSON-serializable. The core `GameSpec` structure is compatible:
- `mechanics`: Still list of mechanic specs
- `world`: Still locations + edges
- `quests`: Still quest structure

## Conclusion

v2.0 transforms SeedWorld from a template-based generator to a true "Seed" capable of generating entire coherent game universes from minimal initial conditions. The system applies rigorous scientific principles from multiple disciplines to enable true emergence while maintaining validation and quality assurance.

The architecture supports infinite expansion, multi-genre generation, and meaningful expressive range—all while preserving the original vision of composable, structural game generation.
