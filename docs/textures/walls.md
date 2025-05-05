# 🧱 Walls textures docs

## 🔧 How They Work
- Each texture is a 4×4 tile grid.
- Each tile corresponds to a wall piece depending on how it connects to its neighbors (like corners, sides, junctions).
- The system auto-selects the right tile based on adjacency — so you only need to provide a clean texture sheet.

## 🖼️ Image Rules
- Must be a PNG file
- Must contain 48 tiles, laid out in a 4×12 grid
- Each tile must be equally sized
- Transparent backgrounds work great (for rounded or styled walls)

🔍You can scale up or down, just keep that grid clean and 4×12.

## 📁 Where to Put Them
- All wall textures live in:
    ```
    textures/walls/
    ```
- Default used: `default.png`

You can swap textures in the `walls.textures` variable of the `config.json`

## 🎯 Tips for custom textures
- Try starting from `default.png` as a template, then recolor, reshape, or stylize as you like.
- Keep alignment clean: Make sure edges line up perfectly across tiles.

## 🧪 Testing
To simplify the texture creation process we created a map (`test_textures21x15.csv`) that uses all walls textures.