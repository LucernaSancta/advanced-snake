# 🧠 Main Module

## Imports
- `pygame` — Handles graphics, input, and timing.
- `os.path` — Checks for configuration files.
- `random` — Randomly selects positions for apples.
- `yaml` — Reads player configuration.
- `toml` — Reads global game configuration.
- `Vector2` — Simplifies 2D position handling.
- `Snake`, `Walls`, `Apple` — Custom game objects.
- `logger` — Logs game events and critical errors.

---

## `Game` class

The `Game` class is responsible for:
- Loading configurations.
- Initializing assets.
- Managing game loops and rendering.
- Handling input, updates, and collision logic.

---

#### `__init__(self)`

Initializes the game by:
- Loading configuration from `conf.toml`.
- Setting up display properties and controls.
- Loading and scaling textures.
- Creating walls, snakes, and apples.
- Pre-rendering static elements (background, walls).

---

#### `init_walls(self) -> Walls`

Creates and returns a `Walls` object based on the configured wall map and textures.

---

#### `init_players(self) -> list[Snake]`

Loads snake player configurations from `.yaml` files located in the `/players` directory and creates `Snake` objects.

---

#### `init_apples(self) -> list[Apple]`

Spawns the initial set of apples based on `initial_apples` from the config file, using `apple_spawner()` for positioning.

---

#### `apple_spawner(self) -> Apple | None`

Generates a new `Apple` in an unoccupied space on the grid, avoiding:
- Snake positions.
- Wall positions.
- Existing apples.

Returns:
- An `Apple` object if space is available.
- `None` if the grid is full.

---

#### `render_background(self, surface: pygame.Surface) -> pygame.Surface`

Tiles the background texture across the entire game grid.

---

#### `render_snakes(self) -> None`

Draws all active snakes on the screen.

---

#### `render_apples(self) -> None`

Cleans up `None` apples and renders all valid `Apple` objects onto the screen.

---

#### `render_walls(self, surface: pygame.Surface) -> pygame.Surface`

Draws walls onto a given surface and returns the updated surface.

---

#### `update_snakes(self) -> None`

Updates each snake's:
- Movement logic.
- Collision detection:
  - Walls.
  - Itself.
  - Other snakes (head-to-head or head-to-body).
  - Apples.

Handles death and apple consumption.

---

#### `run(self) -> None`

The core game loop:
- Processes input events.
- Toggles pause state.
- Detects game-over and win conditions.
- Updates game objects.
- Renders the frame.
- Limits frame rate to the configured `tps`.

---

⚠️ATTENTION⚠️ Code documentation is NOT regualary updated, this docs may be outdated