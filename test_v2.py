#!/usr/bin/env python3
"""Quick test of v2.0 generator."""

from seedworld.generator_v2 import generate_v2
import json

# Generate a game
seed = 104729
print(f"Generating v2.0 game from seed {seed}...")
print()

spec = generate_v2(seed)

# Print summary
print("=" * 80)
print("V2.0 GAME GENERATION SUCCESS")
print("=" * 80)
print()
print(f"Title: {spec['title']}")
print(f"Version: {spec['version']}")
print(f"Genre: {', '.join(spec['genre'])}")
print()
print("Cosmological Constants:")
primary = spec['cosmological_constants']['primary_dimensions']
for k, v in primary.items():
    print(f"  {k}: {v:.3f}")
print()
print("Emergent System:")
emergent = spec['emergent_system']
print(f"  Complexity: {emergent['complexity']}")
print(f"  Stable: {emergent['is_stable']}")
print(f"  Feedback loops: {len(emergent['feedback_loops'])}")
print(f"  Attractors: {len(emergent['attractors'])}")
print(f"  Critical events: {len(emergent['critical_events'])}")
print()
print("Atoms:")
atoms = spec['atoms']
print(f"  Resources: {len(atoms['resources'])}")
print(f"  Boolean states: {len(atoms['boolean_states'])}")
print(f"  Perception: {len(atoms['perception'])}")
print(f"  Affordances: {len(atoms['affordances'])}")
print(f"  Feedback: {len(atoms['feedback'])}")
print(f"  Transitions: {len(atoms['transitions'])}")
print(f"  Temporals: {len(atoms['temporals'])}")
print()
print("Playability Metrics:")
metrics = spec['playability_metrics']
print(f"  Win rate: {metrics['win_rate']:.2%}")
print(f"  Strategy diversity: {metrics['strategy_diversity']:.2%}")
print(f"  Balance score: {metrics['balance_score']:.2f}")
print()
print("Game Structure:")
print(f"  Mechanics: {len(spec['mechanics'])}")
print(f"  Locations: {len(spec['world']['locations'])}")
print(f"  Quests: {len(spec['quests'])}")
print()

# Show some mechanics
print("Sample Mechanics:")
for i, m in enumerate(spec['mechanics'][:3], 1):
    print(f"\n{i}. {m['name']}")
    if m.get('description'):
        print(f"   {m['description'][:120]}...")
    print(f"   Actions: {', '.join(m['actions'][:3])}")
    print(f"   Rules: {len(m['rules'])}, Feedback: {len(m['feedback'])}")

print()
print("=" * 80)
print("Full JSON specification saved to v2_output.json")
print("=" * 80)

# Save full spec
with open('/home/engine/project/v2_output.json', 'w') as f:
    json.dump(spec, f, indent=2, default=str)
