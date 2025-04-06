# 🧱Walls Usage docs

Walls are more than just barriers, they shape the level and influence gameplay.🕹️

## 🔍What Walls Do
- 🧭Define the playable boundaries (both visual and collision-based)
- 🗺️Load optional level-specific walls from a map file
- 🎨Use tile-aware rendering to make things look smooth and connected

## ✏️Want to Edit or Add Walls?
You can customize walls using a simple CSV file:

- 📁Location: maps/
- 📄Format:
```
x,y
5,10
6,10
7,10
```
- 🧩Each entry adds a wall tile at `(x * tile_width, y * tile_height)`
- ⚙️Change the `WALLS_MAP` variable in the `config.toml` file to the name of your CSV file

## 🖼️Wall Textures
You can swap out how the walls look by adding a texture file and changing the `config.toml` file accordingly.

🔗For more info check the [`textures walls docs`](./textures/walls.md)