# 🍽️ Foods Configuration & Customization

**Foods** let you extend and customize game behavior by defining unique interactions when a snake eats something. They are one of the most flexible features in the game.

# 📁 Structure & File Location

- All food types are stored in the `foods/` directory.
- Each food item must be defined in its own `.py` file.
- The file **must contain a class** with the **same name as the file** (case-sensitive).

# 🧬 Inheritance & Base Template

All food classes must inherit from the `Food` base class located in `foods/default.py`.

### ✔️ Example structure:
```
foods/
├── default.py   ← Base class
├── Apple.py     ← Custom food
├── Banana.py    ← Another custom food
```

# 🧱 Base Class: `Food` (from `default.py`)

Here's a quick overview of what the base class provides:

```python
class Food:
    def __init__(self, pos: Vector2, thikness: Vector2, animation: dict = {}, kwargs: dict = {}): ...
    def initialize(self): ...
    def init_texture(self, file_name: str = 'default.png'): ...
    def eaten(self, surface: Surface, snake: Snake, snakes: list[Snake]): ...
    def update(self, display: Surface, deltaTime: int | float ): ...
    def render(self, display: Surface, deltaTime: int | float ): ...
```

### 🔧 Key responsibilities:

- `initialize()`
  
    Override this method to load custom textures and read configuration (`kwargs`).

- `eaten(surface, snake, snakes)`
  
    Called when the food is eaten. Implement what happens when a snake eats this food (e.g., grow, teleport, damage).

- `update(display, deltaTime)`

    Handles the frame-tied logic, usually used only for rendering.

- `kwargs`

    A dictionary passed via `config.json` under `foods.types[].kwargs` to let you customize behavior.

# 🍎 Example: Creating a Custom Food

Here's a complete example of a custom `Apple` food that increases the snake's length when eaten:

### `foods/Apple.py`
```python
import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from .default import Food


class Apple(Food):
    '''Adds x (power) to the tail of the snake'''

    def initialize(self) -> None:
        self.power = self.kwargs['power']
        self.init_texture('apple.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        for _ in range(self.power):
            snake.pieces.append(snake.last_removed)
```

In `config.json`, you can then configure it like this:

```json
"foods": {
    "number": 3,
    "types": [
        {
            "name": "Apple",
            "weight": 60,
            "kwargs": {
                "power": 1
            }
        },
    ]
}
```

# 🎞️ Animated textures

To use animated textures you can simply create an `animation` section in the config file and set the desired preferences like so:

```json
{
    "name": ...,
    "weight": ...,
    "animation": {
        "frames": 6,
        "time_ms": 500
    },
    "kwargs": {...}
}
```

In this case the animation if 6 frames long, and the frame change with a 500 millisecond rate for a total animation time of `500 * 6 = 3000 ms` or 3 seconds

To know how to create animated textures you can refer to the [`foods textures docs`](../textures/food.md)

# ⚙️ Tips for Customization

- 🔁 Use `self.kwargs` for dynamic behavior without hardcoding.
- 🖼️ Call `self.init_texture("your_texture.png")` to load and scale textures.
- 📦 All textures must be placed in `textures/food/`.
- 🐍 Access the snake instance and all snakes via `eaten()` to perform custom effects.