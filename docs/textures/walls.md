# 🧱Walls textures docs

## 🔧How They Work
- 🟩Each texture is a 4×4 tile grid.
- 🧩Each tile corresponds to a wall piece depending on how it connects to its neighbors (like corners, sides, junctions).
- 🤖The system auto-selects the right tile based on adjacency — so you only need to provide a clean texture sheet.

## 🖼️Image Rules
- 📁Must be a PNG file
- 🔲Must be a square image (1:1 ratio)
- 🔢Must contain 16 tiles, laid out in a 4×4 grid
- 📏Each tile must be equally sized
- ✨Transparent backgrounds work great (for rounded or styled walls)

📐For example:

- 128×128 → 32×32 tiles
- 256×256 → 64×64 tiles
- 512×512 → 128×128 tiles

🔍You can scale up or down, just keep that grid clean.

## 📁Where to Put Them
- All wall textures live in:
```
textures/walls/
```
- 🖼️Default used: `default.png`

🔄You can swap textures in the `WALLS_DEFAULT_TEXTURES` variable of the `config.toml`

## 🎨Tips for custom textures
- 🧪Try starting from `default.png` as a template, then recolor, reshape, or stylize as you like.
- 🎯Keep alignment clean: Make sure edges line up perfectly across tiles.

## Testing
To simplify the texture creation process we created a map (`📄testing.csv`) that uses all walls textures🧱.