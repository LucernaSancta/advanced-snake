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
    def __init__(self, pos: Vector2, thikness: Vector2, kwargs: dict = {}): ...
    def initialize(self): ...
    def init_texture(self, file_name: str): ...
    def eaten(self, surface: Surface, snake: Snake, snakes: list[Snake]): ...
    def render(self, display: Surface): ...
```

### 🔧 Key responsibilities:

- `initialize()`
  
  Override this method to load custom textures and read configuration (`kwargs`).

- `eaten(surface, snake, snakes)`
  
  Called when the food is eaten. Implement what happens when a snake eats this food (e.g., grow, teleport, damage).

- `render(display)`

  Handles drawing the food to the screen.

- `kwargs`


  A dictionary passed via `config.json` under `foods.types[].kwargs` to let you customize behavior.

# 🍎 Example: Creating a Custom Food

Here's a complete example of a custom `Apple` food that increases the snake's length when eaten:

### `foods/Apple.py`
```python
from pygame.math import Vector2
from .default import Food
from game_objects import Snake

class Apple(Food):
    def initialize(self) -> None:
        self.power = self.kwargs['power']
        self.init_texture('apple.png')
    
    def eaten(self, surface, snake: Snake, snakes: list[Snake]) -> None:
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
            "weight": 5,
            "kwargs": {
                "power": 2
            }
        }
    ]
}
```

# ⚙️ Tips for Customization

- 🔁 Use `self.kwargs` for dynamic behavior without hardcoding.
- 🖼️ Call `self.init_texture("your_texture.png")` to load and scale textures.
- 📦 All textures must be placed in `textures/food/`.
- 🐍 Access the snake instance and all snakes via `eaten()` to perform custom effects.