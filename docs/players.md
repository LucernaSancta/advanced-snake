# 🧑‍🤝‍🧑 Players and multiplayer settings

The game automatically searches for player config in the `config.json` file.

You can add how many players you want under the `players` section and modify the settings as you want.

## 📄 players variables

- `name` : Name of the player, this is what is visualised in the death message.
- `starting_pos` : Vector of two integer representing the starting position in the grid.
- `textures` : Name of the textures file in the `textures/snakes` folder (see [`Custom Snake Textures`](./textures/snakes.md) for more informations).
- `starting_length` : Starting lenght of the snakes tail.
- `speed` : Speed in block per second of the snake
- `keybindings` : Array of keys used to control the snake, the key must be in the following order: [up key, down key, left key, right key], key are directly used as inputs for the [`pygame.key.key_code`](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) function and so you can use special word to define special keys such as 'up' for the up arrow or 'space' for the space bar

## 🧪 Code example:

```json
    "players": [
        {
            "name": "Alex",
            "starting_pos": [14, 7],
            "textures": "google.png",
            "starting_length": 2,
            "speed": 1,
            "keybindings": ["UP", "DOWN", "LEFT", "RIGHT"]
        },
        {
            "name": "Steve",
            "starting_pos": [0, 7],
            "textures": "google_yellow.png",
            "starting_length": 2,
            "speed": 2,
            "keybindings": ["w", "s", "a", "d"]
        }
    ]
```