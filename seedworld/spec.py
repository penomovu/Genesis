from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class MechanicSpec:
    name: str
    description: str
    actions: list[str]
    rules: list[str]
    feedback: list[str]
    depends_on: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class GateSpec:
    kind: Literal["hard", "soft"]
    requirement: str
    rationale: str


@dataclass(frozen=True, slots=True)
class LocationSpec:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=list)
    hazards: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class EdgeSpec:
    src: str
    dst: str
    gate: GateSpec | None = None


@dataclass(frozen=True, slots=True)
class WorldGraphSpec:
    locations: list[LocationSpec]
    edges: list[EdgeSpec]


@dataclass(frozen=True, slots=True)
class QuestStepSpec:
    id: str
    description: str
    requires: list[str] = field(default_factory=list)
    grants: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class QuestSpec:
    name: str
    objective: str
    steps: list[QuestStepSpec]


@dataclass(frozen=True, slots=True)
class GameSpec:
    seed: int
    title: str
    genre: list[str]
    constants: JsonObject
    mechanics: list[MechanicSpec]
    world: WorldGraphSpec
    quests: list[QuestSpec]

    def to_dict(self) -> JsonObject:
        return asdict(self)
