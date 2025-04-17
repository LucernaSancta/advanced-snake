import pygame
from pygame.math import Vector2

from main import Game
from game_objects import Snake, Walls
from logger import logger as log


class Map_creator(Game):
    def __init__(self):

        self.load_configs('config.toml')

        self.snake_grid_thikness = Vector2(self.screen_size.x // self.snake_grid_size.x, self.screen_size.y // self.snake_grid_size.y)
        log.debug(f'Snake grid thikness: {self.snake_grid_thikness}')

        log.debug('Initializing pygame')
        # Initialize pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Advanced Snake - Map Creator')
        self.clock = pygame.time.Clock()

        log.debug('Loading background textures')
        # Scale the background texture
        self.bg_texture = pygame.image.load('textures/background/'+self.bg_texture).convert_alpha()
        self.bg_texture = pygame.transform.scale(self.bg_texture, self.snake_grid_thikness)

        # Load walls
        self.walls = Walls(self.screen_size,self.wall_map,self.snake_grid_thikness,self.walls_textures)

        # Load the players
        self.snakes: list[Snake] = self.init_players()

        log.debug('Render static objects')
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
                        log.debug('Quitting game by pressing exit key')
                        pygame.quit()
                        quit()
                    
                    # Export key
                    elif event.key == pygame.K_SPACE:
                        file_name = input('Enter name of the new CSV file (leave blank to continue editing): ')

                        if file_name:
                            self.walls.export(file_name)
                            log.info('Map exported succesfully')
                            pygame.quit()
                            quit()


            # When a button is pressed
            pressed_buttons = pygame.mouse.get_pressed()
            if any(pressed_buttons):

                # Render the background
                # This is done separately so that the blue and red rectangels are not drawn under the background
                self.display.blit(self.bg_surface, (0, 0))

                mouse_pos = pygame.mouse.get_pos()
                log.debug(f'Mouse pressed at {mouse_pos}')

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


                # Render the snakes
                self.render_snakes()
                # Render the walls
                self.display.blit(self.render_walls(self.display), (0, 0))

                pygame.display.update()


            # Limit the refresh rate to the tps
            self.clock.tick(60)


if __name__ == '__main__':
    log.info('Initialize map creator')
    map_creator = Map_creator()
    log.info('Run map creator')
    map_creator.run()