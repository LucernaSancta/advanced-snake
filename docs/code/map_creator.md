# 🗺️ Advanced Snake - Map Creator Module

This module provides a simple graphical map editor.
It allows users to **add** or **remove walls** interactively and **export** the map as a CSV file.


## Imports
- `pygame` — Used for rendering, input, and window management.
- `os.path` — For verifying the existence of the config file.
- `toml` — Parses map editor configuration.
- `Vector2` — Simplifies coordinate calculations.
- `Game` — Inherits shared logic for grid and texture setup.
- `Snake`, `Walls` — Game object representations.
- `logger` — Logs status and errors.

---

## `Map_creator` class

An extension of the `Game` class specifically for building and editing wall layouts.


#### `__init__(self, config_file='config.toml')`

Initializes the map creator by:
- Loading configuration from a TOML file.
- Setting up screen, grid, and wall parameters.
- Initializing `pygame` display and clock.
- Loading and scaling the background texture.
- Loading existing walls and players.
- Preparing a background surface for rendering.

---

#### `run(self) -> None`

The main loop of the map editor.

Handles:
- **Event Listening**  
   Detects:
   - Quit events (window close or `ESC` key).
   - Export requests (`SPACE` key) for saving the map to a CSV file.
  
- **Mouse Interaction**  
   Allows:
   - **Left Click**: Add a wall at the clicked tile.
   - **Right Click**: Remove a wall at the clicked tile.

- **Rendering**  
   Continuously:
   - Displays the background.
   - Highlights tiles being edited.
   - Shows snakes (if any) for reference.
   - Renders walls in real-time.

- **Performance**  
   The game loop is limited to 60 FPS using `pygame.time.Clock`.

---

## Notes
- The design relies on the same grid logic (`snake_grid_thikness`) to ensure wall positions perfectly match in-game tiles.

---

⚠️ATTENTION⚠️ Code documentation is NOT regualary updated, this docs may be outdated
