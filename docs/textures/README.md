# 🎨 Textures docs
Make your snake stand out. Reskin the apples. Redefine the walls.
__Advanced Snake__ supports full texture customization for every game element — all configured through easy-to-edit files.

## 📁 Where Textures Are Stored
Textures are organized into folders based on what they represent:
```
textures/
├── snakes/    ← Textures for each snake
├── food/      ← Textures for apples
├── walls/     ← Textures for walls
└── backgrund/ ← Textures for the bacground
```
Each folder contains `.png` files that can be referenced dynamically at runtime.

## 🧠 How the Game Loads Textures
Texture names are pulled directly from the main config file 📄`config.json`

These are the default texture settings:
```json
{
    "walls": {
        ...,
        "textures": "mud.png"
    },
    "background": {
        "textures": "grass.png",
        ...
    },
    "players": [
        {
            ...,
            "textures": "google.png",
            ...
        }
    ]
}

```

## 📌 Texture Assignment by Type
| Type | Source of Texture Info | Location |
| ------- | ------- | ------- |
| Snake | Set in `config.json` | `textures/snakes/` |
| Food | Set in the foods `.py files` | `textures/food/` |
| Walls | Set in `config.json` | `textures/walls/` |
| Background | Set in `config.json` | `textures/background/` |

<br>

Each section has its own detailed guide:
- 🐍[`Snakes`](./snakes.md) – How to design full snake spritesheets
- 🍎[`Food`](./food.md) – How to add custom apples or bonus items
- 🧱[`Walls`](./walls.md) – How to reskin map walls
- 🎑[`Background`](./background.md) – How to reskin background tiles