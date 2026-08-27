# Contributing

感谢你愿意让这只小宠物变得更好。这个仓库的目标是提供一个轻量、易安装、可检查的 Codex v2 桌宠包。

## 提交前检查

```bash
python3 -m pip install Pillow
python3 scripts/validate_atlas.py
```

请确认：

- `assets/pet.json` 与 `assets/spritesheet.webp` 的 id、路径和版本号一致；
- 图集仍为 1536 × 2288 px、8 × 11 网格、每格 192 × 208 px；
- 透明背景没有变成纯色底；
- 每个已使用帧的四条边保持透明，帽檐、头发、披肩不会跨到邻帧；
- 预览 GIF 与图集内容一致；
- 新增素材拥有可公开发布的权利，并在 PR 中说明来源或授权情况。

## 动画约束

Codex v2 的标准行契约见 [`docs/animation-rows.md`](docs/animation-rows.md)。如果要增加 `success`、`sleeping` 或 `loading` 等非标准状态，请先放在 `assets/extra-state-prototypes/`，不要直接改变运行时图集的行顺序。

## 提交 PR 时请说明

1. 改动了哪些状态或安装行为；
2. 如何验证；
3. 是否附带了新的预览图；
4. 相关素材的版权/授权情况。
