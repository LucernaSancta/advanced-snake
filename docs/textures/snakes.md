# 🐍Custom Snake Textures

## 📄Where Textures Are Defined
Snake textures are assigned in the player's `.yml` config file

👉 See [`players & multiplayer configs`](../players.md) for more

## 📁Where Texture Files Go
All snake texture images live in:
```
📂 textures/snakes/
```
Each one defines a complete skin for a snake — head, body, tail, curves — all packed into a single sheet.

## 🧩Texture Format
| 📊Column   | 🧠Description |
| -------- | ------- |
| 0 | Head tiles |
| 1 | Body tiles |
| 2 | Tail tiles |

|↕️Row   | ↔️Direction / Shape |
| -------- | ------- |
| 0 | Up / Still |
| 1 | Left |
| 2 | Down |
| 3 | Right |
| 4-5 | Body curves (for turns) |

📐The engine automatically slices this grid so it will always match the snake dimensions.

## 🖼️Image Guidelines
- 🧱Must be a 3×6 grid of equally sized tiles
- 🖌️Use .png for transparency support

## 🎨How to Make Your Own
1. 📝Duplicate default.png in textures/snakes/
2. 🧑‍🎨Open it in your favorite editor
3. ✏️Replace each tile with your own design
4. 💾Save as a new .png file
5. 🔧In the player's .yml, set:
```
textures: your_texture_name.png
```