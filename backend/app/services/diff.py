from __future__ import annotations

from difflib import SequenceMatcher

from app.schemas import PatchDiff, PatchDiffEntry


def _normalize_text(value: str) -> str:
    return " ".join(value.lower().strip().split())


def _flatten_sections(sections: list[dict]) -> dict[str, list[tuple[str, str]]]:
    flattened: dict[str, list[tuple[str, str]]] = {}
    for section in sections:
        category = str(section.get("category", "")).strip() or "General"
        items = [str(item).strip() for item in section.get("items", []) if str(item).strip()]
        flattened[category] = [(_normalize_text(item), item) for item in items]
    return flattened


def build_patch_diff(
    current_sections: list[dict],
    previous_sections: list[dict] | None,
) -> PatchDiff:
    if not previous_sections:
        return PatchDiff(
            initial_release=True,
            added=[
                PatchDiffEntry(category=section.get("category", "General"), current_text=item)
                for section in current_sections
                for item in section.get("items", [])
            ],
        )

    current = _flatten_sections(current_sections)
    previous = _flatten_sections(previous_sections)
    added: list[PatchDiffEntry] = []
    changed: list[PatchDiffEntry] = []
    removed: list[PatchDiffEntry] = []
    matched_previous: set[tuple[str, str]] = set()

    for category, current_items in current.items():
        previous_items = previous.get(category, [])
        previous_norms = {normalized for normalized, _ in previous_items}
        if not previous_items:
            added.extend(
                PatchDiffEntry(category=category, current_text=original) for _, original in current_items
            )
            continue

        for normalized, original in current_items:
            if normalized in previous_norms:
                matched_previous.add((category, normalized))
                continue

            best_match: tuple[str, str] | None = None
            best_ratio = 0.0
            for previous_normalized, previous_original in previous_items:
                ratio = SequenceMatcher(None, normalized, previous_normalized).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = (previous_normalized, previous_original)

            if best_match and best_ratio >= 0.45:
                matched_previous.add((category, best_match[0]))
                changed.append(
                    PatchDiffEntry(
                        category=category,
                        current_text=original,
                        previous_text=best_match[1],
                    )
                )
            else:
                added.append(PatchDiffEntry(category=category, current_text=original))

    for category, previous_items in previous.items():
        for normalized, original in previous_items:
            if (category, normalized) not in matched_previous:
                removed.append(PatchDiffEntry(category=category, previous_text=original))

    return PatchDiff(initial_release=False, added=added, changed=changed, removed=removed)

