# 🌍 Global Variables for Advanced Snake Game

The `config.json` file is used to configure the game settings. Here’s what each variable does:

---

- `display`
    - `screen_size` : Defines the screen width and height in pixels.
    - `fps` : defines the frame per second of the game

- `game`
    - `grid_size` : Defines the number of grid cells in the X and Y direction.

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
    - `console_level` : set the logging level for console logs (see [logging docs](./code/logging.md) for more)
    - `file_level` : set the logging level for file written logs
    - `max_file_size` : set max file size for file written logs
    - `max_file_count` : set max files for file written logs
---

File example:

```toml
[display]
screen_size = [900, 900]
fps = 60

[game]
grid_size = [15, 15]

[apples]
number = 3
power = 1
textures = "apple.png"

[walls]
map = "zen15x15.csv"
textures = "mud.png"

[background]
textures = "grass.png"
    [background.tiling]
    active = true
    size = [1, 1]

[keys]
pause = "SPACE"
exit = "ESCAPE"

[logger]
console_level="INFO"
file_level="DEBUG"
max_file_size=131072 #128KB
max_file_count=5
```