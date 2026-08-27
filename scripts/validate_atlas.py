#!/usr/bin/env python3
"""Validate the public Phoebe Codex Pet runtime package.

This is intentionally a small, repository-local check rather than a generator.
It catches the most common distribution mistakes: a missing runtime pair,
invalid metadata, wrong atlas dimensions, missing alpha, and visible pixels
touching a frame boundary.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
EXPECTED_SIZE = (1536, 2288)
EXPECTED_GRID = (8, 11)
EXPECTED_CELL = (192, 208)


def load_metadata(errors: list[str]) -> dict[str, Any]:
    path = ASSETS / "pet.json"
    if not path.is_file():
        errors.append(f"missing file: {path}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append("pet.json must contain a JSON object")
        return {}
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a machine-readable result instead of the human summary",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    metadata = load_metadata(errors)

    if metadata.get("id") != "phoebe-codex":
        errors.append("pet.json id must be 'phoebe-codex'")
    if metadata.get("spriteVersionNumber") != 2:
        errors.append("pet.json spriteVersionNumber must be 2")
    if metadata.get("spritesheetPath") != "spritesheet.webp":
        errors.append("pet.json spritesheetPath must be 'spritesheet.webp'")

    sprite_path = ASSETS / "spritesheet.webp"
    if not sprite_path.is_file():
        errors.append(f"missing file: {sprite_path}")

    result: dict[str, Any] = {
        "ok": False,
        "metadata": metadata,
        "spritesheet": str(sprite_path.relative_to(ROOT)),
        "expected": {
            "size": list(EXPECTED_SIZE),
            "grid": list(EXPECTED_GRID),
            "cell": list(EXPECTED_CELL),
            "mode": "RGBA",
            "format": "WEBP",
        },
        "usedCells": 0,
        "edgeHitCells": [],
        "transparentRgbResiduePixels": 0,
        "errors": errors,
        "warnings": warnings,
    }

    if sprite_path.is_file():
        try:
            from PIL import Image
        except ModuleNotFoundError:
            errors.append("Pillow is required: python3 -m pip install Pillow")
        else:
            try:
                with Image.open(sprite_path) as image:
                    image.load()
                    result["format"] = image.format
                    result["mode"] = image.mode
                    result["size"] = list(image.size)
                    if image.format != "WEBP":
                        errors.append(
                            f"spritesheet format is {image.format!r}, expected 'WEBP'"
                        )
                    if image.mode != "RGBA":
                        errors.append(
                            f"spritesheet mode is {image.mode!r}, expected 'RGBA'"
                        )
                    if image.size != EXPECTED_SIZE:
                        errors.append(
                            f"spritesheet size is {image.size}, expected {EXPECTED_SIZE}"
                        )

                    rgba = image.convert("RGBA")
                    alpha = rgba.getchannel("A")
                    cell_width, cell_height = EXPECTED_CELL
                    used_cells = 0
                    edge_hits: list[dict[str, int]] = []
                    raw = rgba.tobytes()
                    residue = sum(
                        1
                        for index in range(0, len(raw), 4)
                        if raw[index + 3] == 0 and raw[index : index + 3] != b"\x00\x00\x00"
                    )

                    for row in range(EXPECTED_GRID[1]):
                        for column in range(EXPECTED_GRID[0]):
                            left = column * cell_width
                            top = row * cell_height
                            box = (left, top, left + cell_width, top + cell_height)
                            cell_alpha = alpha.crop(box)
                            if cell_alpha.getbbox() is None:
                                continue
                            used_cells += 1
                            cell = cell_alpha.load()
                            edge_count = sum(
                                1
                                for x in range(cell_width)
                                if cell[x, 0] > 0 or cell[x, cell_height - 1] > 0
                            )
                            edge_count += sum(
                                1
                                for y in range(1, cell_height - 1)
                                if cell[0, y] > 0 or cell[cell_width - 1, y] > 0
                            )
                            if edge_count:
                                edge_hits.append(
                                    {
                                        "row": row,
                                        "column": column,
                                        "edgePixels": edge_count,
                                    }
                                )

                    result["usedCells"] = used_cells
                    result["edgeHitCells"] = edge_hits
                    result["transparentRgbResiduePixels"] = residue
                    if edge_hits:
                        errors.append(
                            f"{len(edge_hits)} used cell(s) contain visible pixels on a frame edge"
                        )
                    if residue:
                        warnings.append(
                            f"{residue} fully transparent pixel(s) retain non-black RGB values"
                        )
            except Exception as exc:  # Pillow can raise several image-format errors.
                errors.append(f"cannot inspect spritesheet.webp: {exc}")

    result["errors"] = errors
    result["warnings"] = warnings
    result["ok"] = not errors

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Phoebe Codex Pet atlas validation")
        print(f"  asset:       {result['spritesheet']}")
        print(f"  format/mode: {result.get('format', '?')} / {result.get('mode', '?')}")
        print(f"  size:        {tuple(result.get('size', []))}")
        print(f"  used cells:  {result['usedCells']}")
        print(f"  edge hits:   {len(result['edgeHitCells'])}")
        for warning in warnings:
            print(f"  warning:     {warning}")
        for error in errors:
            print(f"  error:       {error}")
        print("  result:      PASS" if result["ok"] else "  result:      FAIL")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
