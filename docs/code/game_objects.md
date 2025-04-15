# 🧰 Game objects

## `key_map` Class
Handles the mapping between user input keys and in-game snake movement.

##### `__init__(self, up, down, left, right)`
- **Purpose:**  
  Initializes key bindings for snake control.
- **Arguments:**
  - `up`, `down`, `left`, `right`: String representations of keys (e.g., `'w'`, `'a'`, `'s'`, `'d'`).
- **Details:**  
  Converts these strings to Pygame keycodes and stores them in `self.keys` for easy checking.

---

#### `__contains__(self, key)`
- **Purpose:**  
  Allows direct use of `in` to check if a key belongs to this snake's controls.
- **Returns:**  
  `True` if key is one of the movement keys, otherwise `False`.


## `Snake` Class
Represents a controllable snake entity, its logic, and rendering.

#### `__init__(...)`
- **Purpose:**  
  Sets up snake properties: name, position, keybindings, appearance, and initial state.
- **Arguments:**
  - `name`: Snake’s name.
  - `keybindings`: List of 4 keys (up, down, left, right).
  - `pos`: Starting `Vector2` position.
  - `textures`: Path to the snake’s texture image.
  - `thikness`: Size of each body part.
  - `length`: Initial number of body segments.
- **Details:**  
  Also loads and scales the texture and creates initial snake segments.

---

#### `move(self, key)`
- **Purpose:**  
  Updates the snake’s direction based on user input.
- **Arguments:**  
  `key` - pressed key.
- **Details:**  
  Uses a match-case to assign direction vectors when a valid key is pressed.

---

#### `update(self)`
- **Purpose:**  
  Advances the snake’s position if it's moving.
- **Details:**  
  Moves the snake forward by shifting its body parts, stores the last removed tail part for future growth.

---

#### `eat(self, power)`
- **Purpose:**  
  Adds `power` segments to the snake after "eating" something.
- **Arguments:**  
  `power`: number of segments to grow.

---

#### `render(self, display)`
- **Purpose:**  
  Renders the snake on the game window.
- **Details:**  
  Chooses the right sprite from the texture sheet for the head, body, and tail, based on direction and neighbor positions.  
  If `state == 2` (dead), rendering is skipped.

---

#### `kill(self)`
- **Purpose:**  
  Logs a message when the snake dies.
- **Details:**  
  Uses an external `logger` to log the elimination and the final score.

## `Walls` Class
Represents game boundaries and user-placed obstacles.

#### `__init__(...)`
- **Purpose:**  
  Loads wall layout from a CSV file and creates map borders.
- **Arguments:**
  - `external_box`: Size of the map in pixels.
  - `walls_map`: CSV filename for custom wall layout.
  - `thikness`: Wall segment size.
  - `textures`: Path to wall texture image.
- **Details:**  
  Borders are automatically generated to prevent the snake from escaping the play area.

---

#### `__contains__(self, snake)`
- **Purpose:**  
  Checks if the snake has collided with any wall.
- **Returns:**  
  `True` if collision detected, `False` otherwise.

---

#### `add(self, pos)`
- **Purpose:**  
  Adds a new wall segment at the given position.
- **Arguments:**  
  `pos`: Position in pixel coordinates.

---

#### `remove(self, pos)`
- **Purpose:**  
  Removes a wall segment at the given position.
- **Arguments:**  
  `pos`: Position in pixel coordinates.

---

#### `export(self, file_name)`
- **Purpose:**  
  Exports the current wall layout to a CSV file.
- **Arguments:**  
  `file_name`: Name for the saved CSV file (no `.csv` extension needed).

---

#### `render(self, display)`
- **Purpose:**  
  Draws the wall tiles on the display.
- **Details:**  
  Chooses the correct texture based on neighboring walls to create seamless tiling and a more natural look.

---

💡 **Developer Notes:**
- The snake rendering logic is very dum — it uses the relative position of neighboring segments to select the right texture for bends, straight parts, or end pieces.
- Wall rendering uses the same principle but with 8-direction neighbor checks.

---

⚠️ATTENTION⚠️ Code documentation is NOT regualary updated, this docs may be outdated