# Players and multiplayer settings

The game automatically searches for player config files in the `players` folder.

Inside tha players folder every `.yml` file is considered a different player, the name of the file is not relevant and can be changed to whatever you like.

## yml files variables

`name` : Name of the player, this is what is visualised in the death message.

`starting_pos` : Vector of two integer representing the starting position in the grid.

`textures` : Name of the textures file in the `textures/snakes` folder (see [`Custom Snake Textures`](./textures/snakes.md) for more informations).

`starting_length` : Starting lenght of the snakes tail.

`keybindings` : Array of keys used to control the snake, the key must be in the following order: [up key, down key, left key, right key], key are directly used as inputs for the [`pygame.key.key_code`](https://www.pygame.org/docs/ref/key.html#pygame.key.key_code) function and so you can use special word to define special keys such as 'up' for the up arrow or 'space' for the space bar