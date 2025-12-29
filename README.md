# seedworld

A small, code-first framework for **seed-based** procedural generation of **coherent video-game blueprints** from minimal, composable building blocks ("atoms").

This repo intentionally focuses on *structure and correctness* (ontology, mechanics, dependencies, constraints), not on rendering or a real-time engine.

## Core idea

A playable game concept can be generated if you can reliably produce and validate:

- **Atoms**: entities, components (state), actions (operators), rules/systems (dynamics), events (observations)
- **Molecules**: mechanics (closed feedback loops)
- **Organisms**: quests/challenges (goal graphs over world state)
- **Worlds**: locations + gating + progression + constraints that ensure reachability and solvability

The `seedworld.generator.generate()` function returns a `GameSpec` that can be serialized to JSON for downstream consumption.

## Quickstart

### CLI

```bash
python -m seedworld 104729
```

or

```bash
seedworld 104729
```

### Web Interface

Launch the web interface to generate and explore game blueprints interactively:

```bash
python -m seedworld.web
```

or (after installation):

```bash
seedworld-web
```

Then open your browser to `http://localhost:5000`

## Output

The CLI prints a deterministic JSON blueprint containing:

- seed-derived constants ("cosmological constants")
- mechanics and their dependencies
- world graph (locations, edges, gates)
- quests (goal graph / critical path)

## Files

- `seedworld/spec.py`: pure datamodels for the generated blueprint
- `seedworld/ecs.py`: minimal ECS-style state container (optional runtime substrate)
- `seedworld/generator.py`: deterministic generator from seed → game blueprint
- `seedworld/validate.py`: small validation utilities (reachability / dependency checks)

## Example mini-game

The included generator produces a small hub-and-spokes survival mini-game (oxygen + light + repair gate) similar to the narrative example in the prompt.

Run:

```bash
python -m seedworld 104729 > game.json
```

and inspect `game.json`.
