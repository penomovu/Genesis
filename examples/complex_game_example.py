"""
Demonstration: How v2.0 generates a complex game with emergent gameplay.

This example shows the complete emergence pipeline from atoms to gameplay.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from seedworld.generator_v2 import generate_v2
import json


def demonstrate_complete_emergence():
    """Show full emergence from atoms to gameplay."""
    seed = 65537
    print("=" * 80)
    print(f"COMPLETE EMERGENCE DEMONSTRATION: SEED {seed}")
    print("=" * 80)
    print()

    # Generate the game
    spec = generate_v2(seed)

    # Step 1: Show cosmological constants (the "physics" of this universe)
    print("STEP 1: COSMOLOGICAL CONSTANTS")
    print("-" * 80)
    constants = spec['cosmological_constants']
    print("These constants govern all interactions in this game universe:")
    print()
    primary = constants['primary_dimensions']
    print("Primary Dimensions:")
    for k, v in primary.items():
        print(f"  {k:15s}: {v:.3f}")
    print()
    categorical = constants['categorical']
    print("Categorical Regimes:")
    for k, v in categorical.items():
        print(f"  {k:15s}: {v}")
    print()

    # Step 2: Show atoms (building blocks)
    print("\nSTEP 2: ATOMIC BUILDING BLOCKS")
    print("-" * 80)
    atoms = spec['atoms']
    print("Composable primitives that will self-organize:")
    print()
    print(f"Resources ({len(atoms['resources'])} atomic types):")
    for r in atoms['resources']:
        decay_str = f", decay={r['decay_rate']:.2f}" if r['decay_rate'] > 0 else ""
        renew_str = f", renew={r['renew_rate']:.2f}" if r['renew_rate'] > 0 else ""
        print(f"  • {r['name']:12s} ({r['resource_type']:10s}){decay_str}{renew_str}")

    print()
    print(f"Affordances ({len(atoms['affordances'])} atomic actions):")
    for i, a in enumerate(atoms['affordances'][:6], 1):
        reqs = ", ".join(f"{k}>=({min_v},{max_v})" for k, (min_v, max_v) in a['requires_resources'].items())
        grants = ", ".join(f"{k}{v:+.1f}" for k, v in a['grants_resources'].items())
        print(f"  {i}. {a['name']:15s} reqs: [{reqs}] → grants: [{grants}]")
    print(f"  ... and {len(atoms['affordances']) - 6} more")
    print()

    # Step 3: Show emergent system
    print("\nSTEP 3: EMERGENT SYSTEM")
    print("-" * 80)
    emergent = spec['emergent_system']
    print("Structure that self-organized from atomic interactions:")
    print()
    print(f"Complexity Score: {emergent['complexity']}")
    print(f"System Stability: {'STABLE' if emergent['is_stable'] else 'UNSTABLE (chaotic)'}")
    print()
    print(f"Feedback Loops ({len(emergent['feedback_loops'])} self-organized cycles):")
    for i, loop in enumerate(emergent['feedback_loops'], 1):
        print(f"  {i}. {loop['loop_type'].upper()} LOOP: {loop['primary_resource']}")
        print(f"     Equilibria: {loop['equilibria']} (states system prefers)")
        print(f"     Type: {'Homeostatic' if loop['loop_type'] == 'negative' else 'Amplifying' if loop['loop_type'] == 'positive' else 'Mixed'}")

    print()
    print(f"Attractor Basins ({len(emergent['attractors'])} natural objectives):")
    for i, att in enumerate(emergent['attractors'], 1):
        print(f"  {i}. {att['name']}")
        print(f"     Target state: {att['center_state']}")
        print(f"     Basin depth: {att['basin_depth']:.2f} (escape difficulty)")
        print(f"     Reward value: {att['reward']:.2f}")
        print(f"     Stability: {att['stability']}")

    print()
    print(f"Critical Events ({len(emergent['critical_events'])} phase transitions):")
    for i, evt in enumerate(emergent['critical_events'], 1):
        print(f"  {i}. {evt['name']}")
        print(f"     Trigger: {evt['trigger_condition']}")
        print(f"     Hysteresis: {evt['hysteresis']:.2f} (resistance to reversal)")

    # Step 4: Show emergent mechanics
    print("\nSTEP 4: EMERGENT MECHANICS")
    print("-" * 80)
    mechanics = spec['mechanics']
    print("Gameplay mechanics that emerged from feedback loops:")
    print()
    for i, mech in enumerate(mechanics, 1):
        print(f"{i}. {mech['name']}")
        print(f"   {mech['description']}")
        print(f"   Actions: {', '.join(mech['actions'][:5])}")
        if mech['rules']:
            print(f"   Rules: {len(mech['rules'])} transitions")
        if mech['feedback']:
            print(f"   Feedback: {', '.join(mech['feedback'][:3])}")
        print()

    # Step 5: Show emergent world
    print("STEP 5: EMERGENT WORLD")
    print("-" * 80)
    world = spec['world']
    print("Locations that formed from attractor basins:")
    print()
    for loc in world['locations']:
        items = ", ".join(loc['items']) if loc['items'] else "none"
        hazards = ", ".join(loc['hazards']) if loc['hazards'] else "none"
        print(f"• {loc['name']:20s} ({', '.join(loc['tags'])})")
        print(f"  Items: {items}")
        print(f"  Hazards: {hazards}")
        print()

    # Step 6: Show emergent quests
    print("STEP 6: EMERGENT QUESTS")
    print("-" * 80)
    quests = spec['quests']
    print("Objectives that emerged from attractor basins:")
    print()
    for i, quest in enumerate(quests, 1):
        print(f"{i}. {quest['name']}")
        print(f"   Objective: {quest['objective']}")
        print(f"   Steps: {len(quest['steps'])}")
        for j, step in enumerate(quest['steps'][:3], 1):
            reqs = f" (requires: {', '.join(step['requires'])})" if step['requires'] else ""
            grants = f" → grants: {', '.join(step['grants'])}" if step['grants'] else ""
            print(f"      {j}. {step['description']}{reqs}{grants}")
        if len(quest['steps']) > 3:
            print(f"      ... and {len(quest['steps']) - 3} more steps")
        print()

    # Step 7: Show playability validation
    print("STEP 7: PLAYABILITY VALIDATION")
    print("-" * 80)
    metrics = spec['playability_metrics']
    print("Results from Monte Carlo agent simulation (50 test agents):")
    print()
    print(f"  Win Rate:           {metrics['win_rate']:.2%}")
    print(f"  Strategy Diversity: {metrics['strategy_diversity']:.2%}")
    print(f"  Balance Score:      {metrics['balance_score']:.2f}")
    print()

    # Interpret metrics
    if 0.3 <= metrics['win_rate'] <= 0.7:
        print("  ✓ Win rate is in optimal range (30-70%)")
    else:
        print("  ⚠ Win rate outside optimal range (may be too easy or too hard)")

    if metrics['strategy_diversity'] >= 0.5:
        print("  ✓ High strategic variety - multiple solution paths exist")
    else:
        print("  ⚠ Low strategic variety - may be too linear")

    if metrics['balance_score'] >= 0.5:
        print("  ✓ Good balance - fair challenge level")
    else:
        print("  ⚠ Balance issues - difficulty may need adjustment")

    # Summary
    print("\n" + "=" * 80)
    print("EMERGENCE SUMMARY")
    print("=" * 80)
    print("""
This game demonstrates TRUE EMERGENCE:

✓ Mechanics were NOT authored - they emerged from atomic interactions
✓ World structure was NOT designed - it self-organized from attractors
✓ Quests were NOT written - they were discovered from basin states
✓ Strategic depth was NOT planned - it arose from feedback loops
✓ Playability was NOT assumed - it was validated through simulation

The player experience will be shaped by:
- Scarcity (from resource constraints)
- Time pressure (from decay rates)
- Exploration (from perception limits)
- Tradeoffs (from cross-resource affordances)
- Progression (from attractor gradients)
- Critical moments (from phase transitions)

None of this was explicitly authored by a designer—it EMERGED
from the interaction of simple atomic building blocks under
the governing influence of cosmological constants.

This is the power of SeedWorld v2.0: Games that are GROWN,
not built.
""")

    # Save for inspection
    with open('/home/engine/project/complex_emergence_example.json', 'w') as f:
        json.dump(spec, f, indent=2, default=str)
    print("=" * 80)
    print("Full specification saved to: complex_emergence_example.json")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_complete_emergence()
