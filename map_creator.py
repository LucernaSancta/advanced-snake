import pygame
import os.path
import yaml
import toml

from pygame.math import Vector2
from pygame.color import Color

from game_objects import Snake, Walls


def init_players(snake_grid_thikness: Vector2) -> list[Snake]:
    players = []
    for filename in os.listdir('players'):
        if filename.endswith(".yml"):
            with open('players/'+filename, 'r') as file:
                player_data = yaml.safe_load(file)
                players.append(
                    Snake(
                        name=player_data['name'],
                        keybindings=player_data['keybindings'],
                        thikness=snake_grid_thikness,
                        textures=player_data['textures'],
                        pos=Vector2(player_data['starting_pos'][0]*snake_grid_thikness.x,player_data['starting_pos'][1]*snake_grid_thikness.y),
                        length=player_data['starting_length']
                        )
                    )
    return players


def main() -> None:

    # Set up global config
    config_file = 'config.toml'

    if os.path.isfile(config_file):
        config = toml.load(config_file)
    else:
        print(f"Config file {config_file} not found. Using default settings.")
        config = {}

    # Assign global config variables
    screen_size =     Vector2(config.get('SCREEN_SIZE_X',     800), config.get('SCREEN_SIZE_Y',     800))
    snake_grid_size = Vector2(config.get('SNAKE_GRID_SIZE_X', 10),  config.get('SNAKE_GRID_SIZE_Y', 10))
    walls_default_textures =  config.get('WALLS_DEFAULT_TEXTURES', "default.png")
    wall_map =       config.get('WALLS_MAP', 'default.csv')
    bg_color = Color(config.get('BACKGROUND_COLOR', '#eeeeee'))

    snake_grid_thikness = Vector2(screen_size.x // snake_grid_size.x, screen_size.y // snake_grid_size.y)


    # Initialize pygame
    pygame.init()
    display = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    # Load walls
    walls = Walls(screen_size,wall_map,snake_grid_thikness,walls_default_textures)

    # Load the players
    snakes: list[Snake] = init_players(snake_grid_thikness)


    while True:

        # Get events
        for event in pygame.event.get():

            # Quit when closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # KEYBOARD PRESS EVENTS
            if event.type == pygame.KEYDOWN:
                
                # Quality of life, quit when ESC
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
                # Export key
                elif event.key == pygame.K_SPACE:
                    file_name = input('Enter name of the new CSV file (leave blank to continue editing): ')

                    if file_name:
                        walls.export(file_name)
                        pygame.quit()
                        quit()
                        
            
        # Clear the screen
        display.fill(bg_color)


        # When a button is pressed
        pressed_buttons = pygame.mouse.get_pressed()
        if any(pressed_buttons):

            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is in the screen
            if mouse_pos[0] in range(int(screen_size.x)) and \
               mouse_pos[1] in range(int(screen_size.y)):

                tile = Vector2()
                tile.x = (mouse_pos[0] // snake_grid_thikness.x) * snake_grid_thikness.x
                tile.y = (mouse_pos[1] // snake_grid_thikness.y) * snake_grid_thikness.y

                # pressed_buttons[0] is left click, pressed_buttons[2] is right click
                if pressed_buttons[0]:
                    
                    pygame.draw.rect(display, 'blue', (*tile, *snake_grid_thikness))
                    walls.add(tile)

                elif pressed_buttons[2]:
                    
                    pygame.draw.rect(display, 'red', (*tile, *snake_grid_thikness))
                    walls.remove(tile)


        # Draw the snakes in whatever state they are
        for snake in snakes:
            snake.frame(display)

        # Draw the walls
        walls.frame(display)

        pygame.display.update()

        # Limit the refresh rate to the tps
        clock.tick(60)


if __name__ == '__main__':
    main()