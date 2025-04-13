# 🌍 Global Variables for Advanced Snake Game

The `config.toml` file is used to configure the game settings. Here’s what each variable does:

---

- `display`
    - `screen_size.x` & `screen_size.y` : Defines the screen width and height in pixels.

- `game`
    - `tps` : Controls the game speed (higher value = faster game)
    - `grid_size.x` & `grid_size.y` : Defines the number of grid cells in the X and Y direction.

- `apples`
    - `number` : Number of apples generated at the start.
    - `power` : Defines the power value of an apple.
    - `textures` : Specifies the file path for the apples texture.

- `walls`
    - `map` : Path to the CSV file that defines the wall placement in the game.
    - `textures` : Specifies the file path for the wall textures.

- `background`
    - `textures` :  Specifies the file path for the background texture.

- `keys`
    - `pause` : Key to pause the game
    - `exit` : Key to exit the game

---

File example:

```toml
[display]
screen_size.x = 900
screen_size.y = 900

[game]
tps = 2
grid_size.x = 15
grid_size.y = 15

[apples]
number = 3
power = 1
textures = "apple.png"

[walls]
map = "zen15x15.csv"
textures = "mud.png"

[background]
textures = "grass.png"

[keys]
pause = "SPACE"
exit = "ESCAPE"
```