#!/usr/bin/env python3
"""Demonstrate the expressive range of v2.0 across diverse seeds."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from seedworld.generator_v2 import generate_v2
import json


def demonstrate_expressive_range() -> None:
    """Show how small seed changes cascade through the system."""
    print("=" * 80)
    print("EXPRESSIVE RANGE DEMONSTRATION")
    print("=" * 80)
    print()
    print("How small seed changes cascade through the emergent system")
    print()

    # Seeds that are close in value but produce different games
    seeds = [10000, 10001, 10002, 10003, 10004]

    print(f"{'Seed':<8} {'Title':<25} {'Genre':<30} {'Complexity':<10} {'Stable':<8}")
    print("-" * 80)

    for seed in seeds:
        spec = generate_v2(seed)
        constants = spec['cosmological_constants']['primary_dimensions']
        emergent = spec['emergent_system']

        print(f"{seed:<8} ", end="")
        print(f"{spec['title']:<25} ", end="")
        print(f"{', '.join(spec['genre']):<30} ", end="")
        print(f"{emergent['complexity']:<10} ", end="")
        print(f"{str(emergent['is_stable']):<8}")

    print()
    print("Note: Each seed creates unique games through chaotic mixing")

    # Show detailed breakdown for one seed
    print()
    print("=" * 80)
    print("DETAILED ANALYSIS: SEED 104729")
    print("=" * 80)
    print()

    spec = generate_v2(104729)

    print("COSMOLOGICAL CONSTANTS:")
    print("-" * 40)
    primary = spec['cosmological_constants']['primary_dimensions']
    derived = spec['cosmological_constants']['derived_constants']
    categorical = spec['cosmological_constants']['categorical']

    print("Primary Dimensions:")
    for k, v in primary.items():
        print(f"  {k:12s}: {v:.3f}")

    print()
    print("Derived Constants:")
    for k, v in derived.items():
        print(f"  {k:20s}: {v:.3f}")

    print()
    print("Categorical:")
    for k, v in categorical.items():
        print(f"  {k:20s}: {v}")

    print()
    print("EMERGENT SYSTEM:")
    print("-" * 40)
    emergent = spec['emergent_system']
    print(f"  Complexity: {emergent['complexity']}")
    print(f"  Stable: {emergent['is_stable']}")
    print(f"  Feedback loops: {len(emergent['feedback_loops'])}")
    print(f"  Attractors: {len(emergent['attractors'])}")
    print(f"  Critical events: {len(emergent['critical_events'])}")

    print()
    print("  Feedback Loops:")
    for loop in emergent['feedback_loops']:
        print(f"    - {loop['loop_type'].upper()}: {loop['primary_resource']}")
        print(f"      Equilibria: {loop['equilibria']}")

    print()
    print("  Attractors:")
    for att in emergent['attractors']:
        print(f"    - {att['name']}")
        print(f"      State: {att['center_state']}")
        print(f"      Reward: {att['reward']:.2f}, Stability: {att['stability']}")

    print()
    print("ATOMS GENERATED:")
    print("-" * 40)
    atoms = spec['atoms']
    print(f"  Resources: {len(atoms['resources'])}")
    for r in atoms['resources'][:3]:
        print(f"    - {r['name']}: {r['resource_type']}, decay={r['decay_rate']:.2f}")

    print()
    print(f"  Affordances: {len(atoms['affordances'])}")
    for a in atoms['affordances'][:4]:
        grants = ", ".join(f"{k}={v:.1f}" for k, v in a['grants_resources'].items())
        print(f"    - {a['name']}: {grants}")

    print()
    print("MECHANICS (EMERGENT):")
    print("-" * 40)
    for i, m in enumerate(spec['mechanics'], 1):
        print(f"  {i}. {m['name']}")
        if m.get('description'):
            print(f"     {m['description'][:80]}")
        print(f"     Actions: {', '.join(m['actions'][:4])}")
        print()

    print("PLAYABILITY METRICS:")
    print("-" * 40)
    metrics = spec['playability_metrics']
    print(f"  Win rate: {metrics['win_rate']:.2%}")
    print(f"  Strategy diversity: {metrics['strategy_diversity']:.2%}")
    print(f"  Balance score: {metrics['balance_score']:.2f}")

    print()
    print("=" * 80)
    print("V1 vs V2 COMPARISON")
    print("=" * 80)
    print()

    # Generate v1 for comparison
    from seedworld.generator import generate as generate_v1
    v1 = generate_v1(104729)

    print(f"v1.0 (Handcrafted):")
    print(f"  Title: {v1.title}")
    print(f"  Mechanics: {len(v1.mechanics)} (always same 3)")
    print(f"  Locations: {len(v1.world.locations)}")
    print(f"  Quests: {len(v1.quests)}")
    print()
    print(f"v2.0 (Emergent):")
    print(f"  Title: {spec['title']}")
    print(f"  Mechanics: {len(spec['mechanics'])} (varies by seed)")
    print(f"  Locations: {len(spec['world']['locations'])}")
    print(f"  Quests: {len(spec['quests'])}")
    print()

    print("=" * 80)
    print("KEY DIFFERENCES")
    print("=" * 80)
    print("""
v1.0 LIMITATIONS:
- Handcrafted templates (4 tones × 3 sizes = 12 variations)
- Same mechanics in every game
- No emergence - everything explicitly authored
- Limited seed expressiveness

v2.0 ADVANCES:
- Atomic architecture with combinatorial assembly
- True emergence from local interactions
- Infinite variety from seed-derived constants
- Chaotic mixing creates expressive range
- Self-organizing mechanics and quests
- Information flow modeling
- Simulation-based playability validation

The v2.0 system is a true "Seed" - capable of generating
entire coherent game universes from minimal initial conditions.
""")


if __name__ == "__main__":
    demonstrate_expressive_range()
