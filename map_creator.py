import pygame
import os.path
import yaml
import toml

from pygame.math import Vector2

from main import Game
from game_objects import Snake, Walls


class Map_creator(Game):
    def __init__(self, config_file = 'config.toml'):

        # Set up global config
        if os.path.isfile(config_file):
            config = toml.load(config_file)
        else:
            print(f"Config file {config_file} not found. Using default settings.")
            config = {}

        # Assign global config variables
        self.screen_size =     Vector2(config['display']['screen_size']['x'], config['display']['screen_size']['y'])
        self.snake_grid_size = Vector2(config['game']['grid_size']['x'],      config['game']['grid_size']['y'])
        self.walls_textures = config['walls']['textures']
        self.wall_map =       config['walls']['map']
        self.bg_texture =     config['background']['textures']

        self.snake_grid_thikness = Vector2(self.screen_size.x // self.snake_grid_size.x, self.screen_size.y // self.snake_grid_size.y)


        # Initialize pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Advanced Snake - Map Creator')
        self.clock = pygame.time.Clock()

        # Scale the background texture
        self.bg_texture = pygame.image.load('textures/background/'+self.bg_texture).convert_alpha()
        self.bg_texture = pygame.transform.scale(self.bg_texture, self.snake_grid_thikness)

        # Load walls
        self.walls = Walls(self.screen_size,self.wall_map,self.snake_grid_thikness,self.walls_textures)

        # Load the players
        self.snakes: list[Snake] = self.init_players()

        # Render static objects
        self.bg_surface = pygame.Surface(self.screen_size)
        self.bg_surface.fill((0, 0, 0))
        self.bg_surface = self.render_background(self.bg_surface)

    def run(self) -> None:

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
                            self.walls.export(file_name)
                            pygame.quit()
                            quit()
                            
                
            # Render the background
            self.display.blit(self.bg_surface, (0, 0))


            # When a button is pressed
            pressed_buttons = pygame.mouse.get_pressed()
            if any(pressed_buttons):

                mouse_pos = pygame.mouse.get_pos()

                # Check if mouse is in the screen
                if mouse_pos[0] in range(int(self.screen_size.x)) and \
                   mouse_pos[1] in range(int(self.screen_size.y)):

                    tile = Vector2()
                    tile.x = (mouse_pos[0] // self.snake_grid_thikness.x) * self.snake_grid_thikness.x
                    tile.y = (mouse_pos[1] // self.snake_grid_thikness.y) * self.snake_grid_thikness.y

                    # pressed_buttons[0] is left click, pressed_buttons[2] is right click
                    if pressed_buttons[0]:
                        
                        pygame.draw.rect(self.display, 'blue', (*tile, *self.snake_grid_thikness))
                        self.walls.add(tile)

                    elif pressed_buttons[2]:
                        
                        pygame.draw.rect(self.display, 'red', (*tile, *self.snake_grid_thikness))
                        self.walls.remove(tile)


            # Render all the other stuff
            self.render_snakes()
            self.display.blit(self.render_walls(self.display), (0, 0))

            pygame.display.update()

            # Limit the refresh rate to the tps
            self.clock.tick(60)


if __name__ == '__main__':
    map_creator = Map_creator()
    map_creator.run()