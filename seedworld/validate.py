from __future__ import annotations

from dataclasses import dataclass

from .spec import GameSpec


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str


def validate(spec: GameSpec) -> list[ValidationIssue]:
    """Lightweight, structural validation.

    This is not a full simulation; it validates that:
    - location ids are unique
    - edges reference known locations
    - quest steps are topologically plausible (requirements appear earlier or are seed-granted)
    """

    issues: list[ValidationIssue] = []

    location_ids = [loc.id for loc in spec.world.locations]
    if len(location_ids) != len(set(location_ids)):
        issues.append(
            ValidationIssue(
                code="world.duplicate_location_id",
                message="WorldGraphSpec contains duplicate location ids.",
            )
        )

    known = set(location_ids)
    for edge in spec.world.edges:
        if edge.src not in known:
            issues.append(
                ValidationIssue(
                    code="world.edge_unknown_src",
                    message=f"Edge src '{edge.src}' is not a known location id.",
                )
            )
        if edge.dst not in known:
            issues.append(
                ValidationIssue(
                    code="world.edge_unknown_dst",
                    message=f"Edge dst '{edge.dst}' is not a known location id.",
                )
            )

    for quest in spec.quests:
        acquired: set[str] = set()
        for step in quest.steps:
            missing = [req for req in step.requires if req not in acquired]
            if missing:
                issues.append(
                    ValidationIssue(
                        code="quest.unsatisfied_requirement",
                        message=(
                            f"Quest '{quest.name}' step '{step.id}' requires {missing} "
                            "before they are granted by earlier steps."
                        ),
                    )
                )
            acquired.update(step.grants)

    return issues
