"""
Demonstration of a successfully emerged game with good playability.

This example shows the complete emergence pipeline producing a playable game.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from seedworld.generator_v2 import generate_v2


def find_playable_seeds(start=10000, count=20):
    """Find seeds that generate playable games."""
    print("Searching for seeds with good emergence...")
    print()

    playable_games = []

    for i in range(start, start + count):
        spec = generate_v2(i)
        metrics = spec['playability_metrics']

        # Good criteria:
        # - Win rate 30-70%
        # - At least 1 feedback loop
        # - At least 2 attractors
        # - At least 1 mechanic
        emergent = spec['emergent_system']

        if (0.3 <= metrics['win_rate'] <= 0.7
            and len(emergent['feedback_loops']) > 0
            and len(emergent['attractors']) >= 2
            and len(spec['mechanics']) > 0):

            playable_games.append((i, spec))
            print(f"✓ Seed {i}: {spec['title']} (win_rate={metrics['win_rate']:.0%}, "
                  f"complexity={emergent['complexity']})")

            if len(playable_games) >= 3:
                break

    return playable_games


def analyze_playable_game(seed, spec):
    """Deep dive into one playable game."""
    print()
    print("=" * 80)
    print(f"SUCCESSFUL EMERGENCE ANALYSIS: SEED {seed}")
    print("=" * 80)
    print()

    # Summary
    print("GAME SUMMARY")
    print("-" * 80)
    print(f"Title: {spec['title']}")
    print(f"Genre: {', '.join(spec['genre'])}")
    print(f"Version: {spec['version']}")
    print()

    # Constants
    print("COSMOLOGICAL CONSTANTS")
    print("-" * 80)
    primary = spec['cosmological_constants']['primary_dimensions']
    print(f"Entropy: {primary['entropy']:.2f} (disorder rate)")
    print(f"Fertility: {primary['fertility']:.2f} (resource abundance)")
    print(f"Volatility: {primary['volatility']:.2f} (stochastic events)")
    print(f"Coherence: {primary['coherence']:.2f} (system coupling)")
    print(f"Revelation: {primary['revelation']:.2f} (information visibility)")
    print()

    categorical = spec['cosmological_constants']['categorical']
    print(f"Energy Regime: {categorical['energy_regime']}")
    print(f"Information Theory: {categorical['information_theory']}")
    print(f"Temporal Structure: {categorical['temporal_structure']}")
    print()

    # Emergent system
    emergent = spec['emergent_system']
    print("EMERGENT SYSTEM")
    print("-" * 80)
    print(f"Complexity Score: {emergent['complexity']}")
    print(f"System Stability: {emergent['is_stable']}")
    print()

    print(f"Feedback Loops ({len(emergent['feedback_loops'])}):")
    for i, loop in enumerate(emergent['feedback_loops'], 1):
        print(f"  {i}. {loop['loop_type'].upper()} - {loop['primary_resource']}")
        print(f"     Type: {loop['loop_type']}")
        print(f"     Equilibria: {loop['equilibria']}")
        if loop['loop_type'] == 'negative':
            print(f"     Effect: Homeostatic (stabilizes around equilibria)")
        elif loop['loop_type'] == 'positive':
            print(f"     Effect: Amplifying (drives toward extremes)")
        else:
            print(f"     Effect: Mixed (complex dynamics)")
        print()

    print(f"Attractor Basins ({len(emergent['attractors'])}):")
    for i, att in enumerate(emergent['attractors'], 1):
        print(f"  {i}. {att['name']}")
        print(f"     Target: {att['center_state']}")
        print(f"     Depth: {att['basin_depth']:.2f} (harder to escape)")
        print(f"     Reward: {att['reward']:.2f}")
        print(f"     Stability: {att['stability']}")
        print()

    # Atoms
    atoms = spec['atoms']
    print("ATOMIC BUILDING BLOCKS")
    print("-" * 80)
    print(f"Resources ({len(atoms['resources'])}):")
    for r in atoms['resources']:
        type_info = f"{r['resource_type']}"
        if r['decay_rate'] > 0:
            type_info += f", decay={r['decay_rate']:.2f}"
        if r['renew_rate'] > 0:
            type_info += f", renew={r['renew_rate']:.2f}"
        print(f"  • {r['name']:12s} ({type_info})")

    print()
    print(f"Affordances ({len(atoms['affordances'])} actions):")
    for i, a in enumerate(atoms['affordances'][:6], 1):
        grants = ", ".join(f"{k}{v:+.0f}" for k, v in a['grants_resources'].items())
        print(f"  {i}. {a['name']:15s} → {grants}")
    if len(atoms['affordances']) > 6:
        print(f"  ... and {len(atoms['affordances']) - 6} more")
    print()

    # Emergent mechanics
    print("EMERGENT MECHANICS")
    print("-" * 80)
    for i, mech in enumerate(spec['mechanics'], 1):
        print(f"{i}. {mech['name']}")
        print(f"   {mech['description']}")
        if mech['actions']:
            print(f"   Actions: {', '.join(mech['actions'][:4])}")
        if mech['rules']:
            print(f"   Rules: {len(mech['rules'])}")
        print()

    # World
    world = spec['world']
    print("EMERGENT WORLD")
    print("-" * 80)
    print(f"Locations ({len(world['locations'])}):")
    for loc in world['locations']:
        items = f", items: {', '.join(loc['items'])}" if loc['items'] else ""
        hazards = f", hazards: {', '.join(loc['hazards'])}" if loc['hazards'] else ""
        print(f"  • {loc['name']:20s} [{', '.join(loc['tags'])}]{items}{hazards}")
    print()

    print(f"Edges ({len(world['edges'])}):")
    for i, edge in enumerate(world['edges'][:5], 1):
        gate = f" [gate: {edge['gate']['requirement']}]" if edge['gate'] else ""
        print(f"  {i}. {edge['src']} → {edge['dst']}{gate}")
    print()

    # Quests
    print("EMERGENT QUESTS")
    print("-" * 80)
    for i, quest in enumerate(spec['quests'], 1):
        print(f"{i}. {quest['name']}")
        print(f"   Objective: {quest['objective']}")
        print(f"   Steps: {len(quest['steps'])}")
        for j, step in enumerate(quest['steps'][:3], 1):
            reqs = f" (req: {', '.join(step['requires'])})" if step['requires'] else ""
            grants = f" → {', '.join(step['grants'])}" if step['grants'] else ""
            print(f"      {j}. {step['description']}{reqs}{grants}")
        if len(quest['steps']) > 3:
            print(f"      ... and {len(quest['steps']) - 3} more")
        print()

    # Playability
    metrics = spec['playability_metrics']
    print("PLAYABILITY VALIDATION")
    print("-" * 80)
    print(f"Win Rate: {metrics['win_rate']:.2%}")
    if 0.3 <= metrics['win_rate'] <= 0.7:
        print("  ✓ Optimal range (30-70%) - Good balance!")
    else:
        print("  ⚠ Outside optimal range")

    print()
    print(f"Strategy Diversity: {metrics['strategy_diversity']:.2%}")
    if metrics['strategy_diversity'] >= 0.5:
        print("  ✓ High diversity - Multiple solution paths!")
    else:
        print("  ⚠ Low diversity - May be linear")

    print()
    print(f"Balance Score: {metrics['balance_score']:.2f}")
    if metrics['balance_score'] >= 0.5:
        print("  ✓ Good balance - Fair challenge!")
    else:
        print("  ⚠ Balance issues")

    # Emergence analysis
    print()
    print("=" * 80)
    print("EMERGENCE ANALYSIS")
    print("=" * 80)
    print()

    print("How gameplay emerges from these components:")
    print()

    # Find the primary feedback loop
    if emergent['feedback_loops']:
        primary_loop = emergent['feedback_loops'][0]
        resource = primary_loop['primary_resource']
        print(f"1. Primary Dynamic: {primary_loop['loop_type'].upper()} loop on {resource}")
        print(f"   This creates the core gameplay loop:")
        print(f"   - {primary_loop['loop_type']} feedback drives player behavior")
        print(f"   - Equilibria at {primary_loop['equilibria']} create natural targets")
        print(f"   - Player must balance approaching vs avoiding these states")
        print()

    # Find the primary attractor
    if emergent['attractors']:
        primary_att = max(emergent['attractors'], key=lambda a: a['basin_depth'])
        print(f"2. Primary Objective: {primary_att['name']}")
        print(f"   Attractor basin creates goal:")
        print(f"   - Target state: {primary_att['center_state']}")
        print(f"   - Basin depth: {primary_att['basin_depth']:.2f} (investment required)")
        print(f"   - Reward: {primary_att['reward']:.2f} (motivation)")
        print(f"   - Player naturally gravitates toward this through affordances")
        print()

    # Show how resources create tradeoffs
    print("3. Resource Tradeoffs:")
    for r in atoms['resources']:
        if r['decay_rate'] > 0 and r['renew_rate'] == 0:
            print(f"   - {r['name']} decays ({r['decay_rate']:.2f}/time)")
            print(f"     → Creates time pressure, must acquire repeatedly")
        elif r['renew_rate'] > 0:
            print(f"   - {r['name']} renews ({r['renew_rate']:.2f}/time)")
            print(f"     → Can wait to recover, strategic choice")
        elif r['resource_type'] == 'cumulative':
            print(f"   - {r['name']} accumulates")
            print(f"     → Long-term goal, invest in early")
    print()

    # Show how perception affects gameplay
    info_theory = categorical['information_theory']
    print(f"4. Information Flow ({info_theory}):")
    if info_theory == 'complete':
        print("   - Player sees everything (complete information)")
        print("   → Focus on optimization, not exploration")
    elif info_theory == 'partial':
        print("   - Player sees some information (partial)")
        print("   → Balance between exploration and planning")
    else:  # fog
        print("   - Player sees little (fog of war)")
        print("   → Heavy emphasis on exploration and memory")
    print()

    # Show how time affects gameplay
    temporal = categorical['temporal_structure']
    print(f"5. Temporal Dynamics ({temporal}):")
    if temporal == 'steady':
        print("   - Constant pace (steady)")
        print("   → Predictable rhythm, good for mastery")
    elif temporal == 'pulsing':
        print("   - Variable pace (pulsing)")
        print("   → Rhythm management, windows of opportunity")
    else:  # accelerating
        print("   - Increasing pace (accelerating)")
        print("   → Rising tension, urgency increases over time")
    print()

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print(f"""
This game demonstrates the power of emergent generation:

✓ From {len(atoms['resources'])} resource atoms and {len(atoms['affordances'])} affordances,
  {len(emergent['feedback_loops'])} feedback loops self-organized
✓ These created {len(emergent['attractors'])} attractor basins,
  which became {len(spec['quests'])} quests
✓ World structure emerged from attractor properties:
  {len(world['locations'])} locations with {len(world['edges'])} connections
✓ Simulation validated playability: {metrics['win_rate']:.0%} win rate
✓ Mechanics emerged, not authored: {len(spec['mechanics'])} systems

The player will experience:
- Strategic depth from resource tradeoffs
- Exploration from information limits
- Tension from time dynamics
- Progression from attractor gradients
- Meaningful choices from affordance combinations

NONE of this was explicitly written by a designer.
It ALL emerged from atomic interactions under
cosmological constants.

This is the promise of SeedWorld v2.0:
Games that GROW, not built.
""")


def main():
    """Run the demonstration."""
    print("=" * 80)
    print("SEEDWORLD v2.0: SUCCESSFUL EMERGENCE DEMONSTRATION")
    print("=" * 80)
    print()

    # Find playable games
    playable = find_playable_seeds()

    if not playable:
        print("No playable games found in search range. Expanding search...")
        playable = find_playable_seeds(100000, 100)

    if not playable:
        print("Warning: Could not find well-playable games in range.")
        print("Showing the first game with feedback loops...")
        for i in range(10000, 10100):
            spec = generate_v2(i)
            if len(spec['emergent_system']['feedback_loops']) > 0:
                playable = [(i, spec)]
                break

    # Analyze the best one
    if playable:
        # Pick the one with best balance score
        seed, spec = max(playable, key=lambda x: x[1]['playability_metrics']['balance_score'])
        analyze_playable_game(seed, spec)
    else:
        print("Error: Could not find any games with feedback loops")


if __name__ == "__main__":
    main()
