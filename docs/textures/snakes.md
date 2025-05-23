# 🐍 Custom Snake Textures

## 📄 Where Textures Are Defined
Snake textures are assigned in the player's `config.json` config file section

👉 See [`players & multiplayer configs`](../players.md) for more

## 📁 Where Texture Files Go
All snake texture images live in:
```
textures/snakes/
```
Each one defines a complete skin for a snake — head, body, tail, curves — all packed into a single sheet.

## 🧩Texture Format
|Row   | Shape |
| -------- | ------- |
| 0 | Head tiles | 
| 1 | Curves |
| 2 | Straight pieces |
| 3 | Curves |
| 4 | Tail |

| Column | Description |
| ------- | ------- |
| 0 | Up / Still - curves |
| 1 | Left - curves |
| 2 | Down - curves |
| 3 | Right - curves |

The engine automatically slices this grid so it will always match the snake dimensions.

## 🖼️ Image Guidelines
- Must be a `4×5` grid of equally sized tiles
- Use .png for transparency support

## 🎨 How to Make Your Own
1. Duplicate `test.png` in textures/snakes/
2. Open it in your favorite editor
3. Replace each tile with your own design
4. Save as a new .png file
5. In the players section of the `config.json`, set:
```json
    "players": [
        {
            "textures": "google.png",
        }
    ]
```