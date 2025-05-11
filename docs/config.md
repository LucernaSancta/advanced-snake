# 🌍 Global Variables for Advanced Snake Game

The `config.json` file is used to configure the game settings. Here’s what each variable does:

---

- `display`
    - `screen_size` : Defines the screen width and height in pixels.
    - `fps` : defines the frame per second of the game

- `game`
    - `grid_size` : Defines the number of grid cells in the X and Y direction.
    - `end_condition` : Define the condition for ending the game, the options are:
        - 0: Never win
        - 1: Win when there are no apple
        - 2: Win when only one snake is alive

- `notifications`
    - `flt_th` : If set to true will show a message if the ratio of the grid size and the screen size are not whole numbers (int) (eg. 800x800 and 30x30, 800/30=26.666 <= not an int)
    - `ratios` : If set to true will show a message if the ratio of the screen is different to the one of the grid (eg. 800x800 and 10x20, 800/10 is not equal to 800/20)

- `apples`
    - `number` : Number of apples generated at the start.
    - `power` : Defines the power value of an apple.
    - `textures` : Specifies the file path for the apples texture.

- `walls`
    - `map` : Path to the CSV file that defines the wall placement in the game.
    - `textures` : Specifies the file path for the wall textures.

- `background`
    - `textures` :  Specifies the file path for the background texture.
    - `tiling`:
        - `active`: Set tu `true` to activate background tiling
        - `size`: Background tiling size relative to the game grid size

- `keys`
    - `pause` : Key to pause the game
    - `exit` : Key to exit the game

- `logs`
    - `console_level` : set the logging level for console logs (see [logging docs](./logger.md) for more)
    - `file_level` : set the logging level for file written logs
    - `max_file_size` : set max file size for file written logs
    - `max_file_count` : set max files for file written logs
---

## 🧪 File example:

```json
{
    "_comment": "Check the docs/config.md for informations on how to configure this file",
    "display": {
        "screen_size": [900, 900],
        "fps": 60
    },
    "game": {
        "grid_size": [15, 15],
        "end_condition": 1
    },
    "notifications": {
        "flt_th": false,
        "ratios": false
    },
    "foods": {
        "number": 3,
        "types": [
            {
                "name": "Apple",
                "weight": 5,
                "kwargs": {
                    "power": 1
                }
            },
            {
                "name": "Banana",
                "weight": 1,
                "kwargs": {
                    "power": 3
                }
            }
        ]
    },
    "walls": {
        "map": "zen15x15.csv",
        "textures": "mud.png"
    },
    "background": {
        "textures": "grass.png",
        "tiling": {
            "active": true,
            "size": [1, 1]
        }
    },
    "keys": {
        "pause": "ESCAPE",
        "force_pause": "SPACE",
        "exit": "\\"
    },
    "logger": {
        "console_level": "DEBUG",
        "file_level": "DEBUG",
        "max_file_size": 131072,
        "max_file_count": 5
    },
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
}

```