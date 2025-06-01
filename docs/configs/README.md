# 🌍 Global Variables for Advanced Snake Game

The `config.json` file allows customization of key game settings. Below is a breakdown of each section:

## 🎮 Display

`screen_size`: The screen dimensions in pixels (e.g., `[800, 800]`).

`fps`: Frames per second for the game loop.

## 🕹️ Game

`grid_size`: Number of grid cells along the X and Y axes.

`end_condition`: Game-ending condition:
- `0`: Never ends (infinite).
- `1`: Win when all apples are collected.
- `2`: Win when only one snake remains.

## 🔔 Notifications

`flt_th`: Warns if screen_size / grid_size does not yield whole numbers.

`ratios`: Warns if the screen and grid have mismatched aspect ratios.

## 🍽️ Foods

See the [foods docs](./foods.md) for full details.

## 🧱 Walls

`map`: CSV file path defining wall layout.

`textures`: Wall texture file.

## 🌄 Background

`textures`: Background texture file.

`tiling`:
- `active`: Enables tiled background if `true`.
- `size`: Tiling size relative to grid (e.g., `[1, 1]`).

## ⌨️ Keys

`pause`: Key to pause the game.

`force_pause`: Key to force-pause the game.

`exit`: Key to exit the game.

## 📜 Logger

`console_level`: Log level for console output.

`file_level`: Log level for log file output.

`max_file_size`: Max size (in bytes) for each log file.

`max_file_count`: Max number of log files to retain.

More details in the logger docs.

## 🧑‍🤝‍🧑 Players

See the [players docs](./players.md) for configuration options.

## 🧪 Example config.json

```json
{
    "display": {
        "screen_size": [900, 900],
        "fps": 60
    },
    "game": {
        "grid_size": [15, 15],
        "end_condition": 1
    },
    "notifications": {
        "flt_th": true,
        "ratios": true
    },
    "foods": {
        "number": 1,
        "types": [
            {
                "name": "Apple",
                "weight": 60,
                "kwargs": {
                    "power": 1
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