# Public QA summary

The checked-in runtime asset is the repaired Codex v2 package from the final
visual QA pass. The original generation workspace is intentionally not part of
this repository; it contained machine-local absolute paths and intermediate
reference material.

## Results

See [`summary.json`](summary.json) for the public, path-sanitized result. The
important checks are:

- `spritesheet.webp` is transparent RGBA WEBP;
- atlas dimensions are 1536 × 2288 px with an 8 × 11 grid;
- `spriteVersionNumber` is 2;
- all 74 used cells have zero visible alpha on their cell boundaries;
- no used cell has a second connected sprite component that could leak from an
  adjacent frame;
- final visual QA passed without requesting another repair.

The most recent repair rebuilt the complete `idle`, `running-left`, and
`review` rows with safe gaps around the wide hat brim. This addresses the
reported left-brim crop and right-side neighboring-brim fragment.

## Re-run locally

Install the optional image dependency and run the repository check from the
project root:

```bash
python3 -m pip install Pillow
python3 scripts/validate_atlas.py
```

The preview sheet and look-direction sheet are available at
[`assets/preview-sheet.png`](../../assets/preview-sheet.png) and
[`assets/look-directions.png`](../../assets/look-directions.png).
