from __future__ import annotations

import json
import random
from dataclasses import dataclass
from typing import Any

from .spec import (
    EdgeSpec,
    GameSpec,
    GateSpec,
    LocationSpec,
    MechanicSpec,
    QuestSpec,
    QuestStepSpec,
    WorldGraphSpec,
)
from .validate import validate


@dataclass(frozen=True, slots=True)
class SeedConstants:
    """High-level parameters derived from the seed.

    These act like "cosmological constants" that shape the kinds of stable game
    loops that will emerge.
    """

    tone: str
    lethality: float
    systemic_complexity: float
    world_size: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "tone": self.tone,
            "lethality": self.lethality,
            "systemic_complexity": self.systemic_complexity,
            "world_size": self.world_size,
        }


def _derive_constants(rng: random.Random) -> SeedConstants:
    tones = ["survival-mystery", "cozy-exploration", "tense-escape", "heroic-salvage"]
    world_sizes = ["micro", "small", "medium"]

    tone = rng.choice(tones)
    world_size = rng.choice(world_sizes)

    # Keep these bounded and interpretable.
    lethality = round(rng.uniform(0.35, 0.75), 2)
    systemic_complexity = round(rng.uniform(0.35, 0.65), 2)

    return SeedConstants(
        tone=tone,
        lethality=lethality,
        systemic_complexity=systemic_complexity,
        world_size=world_size,
    )


def generate(seed: int) -> GameSpec:
    """Generate a deterministic, coherent game blueprint from a seed.

    The output is intentionally an engine-agnostic *spec* that downstream tooling can
    materialize as a real game.
    """

    rng = random.Random(seed)
    constants = _derive_constants(rng)

    # --- Mechanics ("molecules")
    mechanics: list[MechanicSpec] = [
        MechanicSpec(
            name="Oxygen Loop",
            description=(
                "Oxygen decays over time; at zero oxygen, health decays. "
                "Consumables can restore oxygen, creating time pressure and route planning."
            ),
            actions=["Use(OxygenTank)", "Breathe"],
            rules=["Oxygen -= decay_rate * dt", "if Oxygen == 0 then Health -= suffocation_rate * dt"],
            feedback=["oxygen_meter", "breathing_audio", "screen_vignette"],
        ),
        MechanicSpec(
            name="Light-as-Tool",
            description=(
                "Temporary light clears certain hazards and changes predator behavior, "
                "turning illumination into a tactical resource (duration, positioning, timing)."
            ),
            actions=["Activate(GlowKelp)", "Throw(GlowKelp)", "Wait"],
            rules=[
                "Illuminated(ToxicCloud) => dissipate",
                "Illuminated(LampEel) => flee",
            ],
            feedback=["visibility_cone", "hazard_fade", "enemy_flee_animation"],
            depends_on=["Oxygen Loop"],
        ),
        MechanicSpec(
            name="Repair Gate",
            description=(
                "Progression is gated by repairing a jammed door using a scarce tool. "
                "This introduces a hard dependency chain and supports a clear critical path."
            ),
            actions=["Repair(JamDoor, RepairKit)", "Inspect(JamDoor)"],
            rules=["if has(RepairKit) then JamDoor.state = OPEN"],
            feedback=["door_animation", "map_update"],
            depends_on=["Light-as-Tool"],
        ),
    ]

    # --- World (hub-and-spokes) with a gated final chamber.
    locations = [
        LocationSpec(
            id="hub",
            name="Dive Bell Hub",
            tags=["safe_zone", "tutorial"],
            items=["OxygenTank"],
        ),
        LocationSpec(
            id="reef",
            name="Glow Reef",
            tags=["resource"],
            items=["GlowKelp"],
            hazards=["MildToxicCloud"],
        ),
        LocationSpec(
            id="wreck",
            name="Sunken Wreck",
            tags=["loot"],
            items=["RepairKit"],
            hazards=["DenseToxicCloud"],
        ),
        LocationSpec(
            id="vent_approach",
            name="Thermal Vent Approach",
            tags=["danger"],
            hazards=["LampEelPatrol"],
        ),
        LocationSpec(
            id="vent_chamber",
            name="Thermal Vent Chamber",
            tags=["objective"],
            items=["BlackBox"],
            hazards=["LampEelPatrol", "LowVisibility"],
        ),
    ]

    edges = [
        EdgeSpec(src="hub", dst="reef"),
        EdgeSpec(src="hub", dst="wreck"),
        EdgeSpec(src="hub", dst="vent_approach"),
        EdgeSpec(
            src="vent_approach",
            dst="vent_chamber",
            gate=GateSpec(
                kind="hard",
                requirement="RepairKit",
                rationale="Jammed door blocks entry; requires RepairKit to open.",
            ),
        ),
        EdgeSpec(
            src="wreck",
            dst="hub",
            gate=GateSpec(
                kind="soft",
                requirement="GlowKelp",
                rationale="Dense toxic corridor is survivable but strongly biased toward using light.",
            ),
        ),
    ]

    world = WorldGraphSpec(locations=locations, edges=edges)

    # --- Quest ("organism"): explicitly derived from gating and mechanic dependencies.
    quest = QuestSpec(
        name="Recover the Black Box",
        objective="Retrieve the black box from the Thermal Vent Chamber and return to the Dive Bell.",
        steps=[
            QuestStepSpec(
                id="learn_oxygen",
                description="Depart the hub and learn that oxygen is a limiting resource.",
                grants=["Understands(OxygenLoop)"],
            ),
            QuestStepSpec(
                id="acquire_light",
                description="Collect GlowKelp from the Glow Reef to gain controllable illumination.",
                requires=["Understands(OxygenLoop)"],
                grants=["GlowKelp", "Understands(LightAsTool)"],
            ),
            QuestStepSpec(
                id="reach_repairkit",
                description="Use light to traverse the wreck's toxic corridor and recover a RepairKit.",
                requires=["GlowKelp"],
                grants=["RepairKit", "Understands(RepairGate)"],
            ),
            QuestStepSpec(
                id="open_vent_chamber",
                description="Repair the jammed door at the vent approach to access the chamber.",
                requires=["RepairKit"],
                grants=["Access(VentChamber)"],
            ),
            QuestStepSpec(
                id="recover_blackbox",
                description="Enter the vent chamber, evade/repel the Lamp Eel, and retrieve the Black Box.",
                requires=["Access(VentChamber)", "GlowKelp"],
                grants=["BlackBox"],
            ),
            QuestStepSpec(
                id="extract",
                description="Return to the hub with the Black Box before oxygen runs out.",
                requires=["BlackBox"],
                grants=["Victory"],
            ),
        ],
    )

    title = {
        "survival-mystery": "Abyssal Circuit",
        "cozy-exploration": "Glow Below",
        "tense-escape": "Last Breath at the Vent",
        "heroic-salvage": "Black Box Salvage",
    }[constants.tone]

    spec = GameSpec(
        seed=seed,
        title=title,
        genre=["procedural", "adventure", "systems"],
        constants=constants.to_dict(),
        mechanics=mechanics,
        world=world,
        quests=[quest],
    )

    issues = validate(spec)
    if issues:
        formatted = "\n".join(f"- {i.code}: {i.message}" for i in issues)
        raise ValueError(f"Generated spec failed validation:\n{formatted}")

    return spec


def to_json(spec: GameSpec) -> str:
    return json.dumps(spec.to_dict(), indent=2, sort_keys=True)
