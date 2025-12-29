from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Iterable


EntityId = int
ComponentType = str


@dataclass(slots=True)
class WorldState:
    """A minimal ECS-style state container.

    This is intentionally small: it exists to make the "atomic" model concrete and
    to provide a substrate for future simulation/validation.
    """

    _next_entity_id: int = 1
    _components: DefaultDict[ComponentType, dict[EntityId, Any]] | None = None

    def __post_init__(self) -> None:
        if self._components is None:
            from collections import defaultdict

            self._components = defaultdict(dict)

    def create_entity(self) -> EntityId:
        eid = self._next_entity_id
        self._next_entity_id += 1
        return eid

    def add_component(self, entity: EntityId, component_type: ComponentType, data: Any) -> None:
        assert self._components is not None
        self._components[component_type][entity] = data

    def get_component(self, entity: EntityId, component_type: ComponentType) -> Any | None:
        assert self._components is not None
        return self._components[component_type].get(entity)

    def entities_with(self, component_type: ComponentType) -> Iterable[EntityId]:
        assert self._components is not None
        return self._components[component_type].keys()

    def query(self, predicate: Callable[[EntityId], bool]) -> list[EntityId]:
        # Naive scan; good enough for small simulations.
        max_id = self._next_entity_id
        return [eid for eid in range(1, max_id) if predicate(eid)]
