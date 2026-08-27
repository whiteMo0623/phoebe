# Codex v2 animation rows

The runtime atlas is a fixed **8 × 11** grid:

- Canvas: `1536 × 2288 px`
- Cell: `192 × 208 px`
- Format: transparent RGBA WEBP
- Metadata: `spriteVersionNumber: 2`

Rows are zero-indexed from the top:

| Row | State | Intended use | Typical frames |
| ---: | --- | --- | ---: |
| 0 | `idle` | Quiet breathing / standby | 7 |
| 1 | `running-right` | Move right | 8 |
| 2 | `running-left` | Move left | 8 |
| 3 | `waving` | Greeting / acknowledgement | 4 |
| 4 | `jumping` | Short celebratory jump | 5 |
| 5 | `failed` | Error or failed action | 8 |
| 6 | `waiting` | Approval / input wait | 6 |
| 7 | `running` | Coding / active work | 6 |
| 8 | `review` | Thinking / review | 6 |
| 9 | look directions `000–157.5°` | First look-direction sweep | 8 |
| 10 | look directions `180–337.5°` | Second look-direction sweep | 8 |

Unused cells remain transparent. They are intentional padding, not missing
frames.

## Frame-safety rule

Every used cell must keep a transparent safety margin on all four edges. This
is especially important for the wide hat brim, long hair, and blue scarf. If a
new pose touches a cell edge, expand or recompose the pose before assembling
the atlas; do not rely on neighboring cells to hide the overflow.

Run the repository validator after any atlas change:

```bash
python3 scripts/validate_atlas.py
```
