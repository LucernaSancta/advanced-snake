# Textures docs
Make your snake stand out. Reskin the apples. Redefine the walls.
__Advanced Snake__ supports full texture customization for every game element — all configured through easy-to-edit files.

## Where Textures Are Stored
Textures are organized into folders based on what they represent:
```
textures/
├── snakes/   ← Textures for each snake
├── food/     ← Textures for apples
└── walls/    ← Textures for walls
```
Each folder contains `.png` files that can be referenced dynamically at runtime.

## How the Game Loads Textures
Texture names are pulled directly from the main config file `config.toml`

These are the default texture settings:
```
SNAKE_DEFAULT_TEXTURES = "default.png"
FOOD_DEFAULT_TEXTURES  = "default.png"
WALLS_DEFAULT_TEXTURES = "default.png"
```
If nothing else is specified (like in a player `.yml` file), these defaults are used.

## Texture Assignment by Type
| Type | Source of Texture Info | Location |
| ------- | ------- | ------- |
| Snake | Set per-player in `players/*.yml` | `textures/snakes/` |
| Food | Set in `config.toml` | `textures/food/` |
| Walls | Set in `config.toml` | `textures/walls/` |

Each section has its own detailed guide:
- [`Snakes`](./snakes.md) – How to design full snake spritesheets
- [`Food`](./food.md) – How to add custom apples or bonus items
- [`Walls`](./walls.md) – How to reskin map walls