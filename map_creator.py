import easygui
import os
import pygame
from pygame.math import Vector2

from main import Game
from game_objects import Snake, Walls
from logger import logger as log
from menus.menu_components import Menu
from various import print_new_game


class Map_creator(Game):
    def __init__(self):

        log.name = 'map_creator' # Set the logger name

        self.config = self.load_configs_file('config.json')
        self.load_configs_vars()

        self.snake_grid_thikness = Vector2(self.screen_size.x // self.snake_grid_size.x, self.screen_size.y // self.snake_grid_size.y)
        log.debug(f'Snake grid thikness: {self.snake_grid_thikness}')

        log.debug('Initializing pygame')
        # Initialize pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Advanced Snake - Map Creator')
        self.clock = pygame.time.Clock()

        # Translate exit and pause keys
        self.pause_key = pygame.key.key_code(self.pause_key)
        self.force_pause_key = pygame.key.key_code(self.force_pause_key)
        self.exit_key = pygame.key.key_code(self.exit_key)

        # Load walls
        self.walls = Walls(self.screen_size,self.wall_map,self.snake_grid_thikness,self.walls_textures)

        # Load the players
        self.snakes: list[Snake] = self.init_players()

        log.debug('Render static objects')
        # Render static objects
        self.bg_surface = pygame.Surface(self.screen_size)
        self.bg_surface.fill((0, 0, 0))
        self.bg_surface = self.render_background(self.bg_surface)

    def export_map(self) -> None:

        # Ask user to choose where to save the file
        save_path = easygui.filesavebox(default='./maps/new_map.csv', title="Save Map As")
        if not save_path:
            log.info("Save operation cancelled.")
            return

        if save_path:
            self.walls.export(save_path)
            log.info('Map exported succesfully')

    def pause(self) -> None:

        log.info('Game paused')

        # Initialize pause menu
        menu = Menu(
            screen_size=self.screen_size,
            font_path='menu_assets/font.ttf',
            font_size=32,    
            inherit_screen=self.display
        )

        # Define buttun costants
        b_th = (400, 60) # Button dimensions
        delta_height = 35

        # Define buttons
        options = [
            ['resume',    'RESUME',    menu.quit,                    b_th, [menu.center.x, menu.center.y - 3*delta_height]],
            ['save_map',  'SAVE MAP',  self.export_map,              b_th, [menu.center.x, menu.center.y -   delta_height]],
            ['main_menu', 'MAIN MENU', lambda: self.stop_game(menu), b_th, [menu.center.x, menu.center.y +   delta_height]],
            ['quit',      'QUIT',      self.game_quit,               b_th, [menu.center.x, menu.center.y + 3*delta_height]]
        ]

        # Add buttons to menu
        for option in options:
            menu.add_option(*option)

        log.debug('Running menu')
        menu.run()

        log.info('Game resumed')

    def run(self) -> None:

        # The game renders only when is necessary so the first frame must be rendered manually
        self.display.blit(self.bg_surface, (0, 0)) # Render the background
        self.render_snakes() # Render the snakes
        self.display.blit(self.render_walls(self.display), (0, 0)) # Render the walls
        pygame.display.update() # Update the display

        # The map creator is entered while continuously pressing some buttons
        block_pressing = any(pygame.mouse.get_pressed())

        self.running = True

        while self.running:

            # Get events
            for event in pygame.event.get():

                # Quit when closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # KEYBOARD PRESS EVENTS
                if event.type == pygame.KEYDOWN:

                    # Force quit
                    if event.key == self.exit_key:
                        log.info('Quitting game by pressing exit key')
                        self.game_quit()

                    # Pause menu
                    elif event.key == self.pause_key:
                        self.pause()


            # When a button is pressed
            pressed_buttons = pygame.mouse.get_pressed()
            if block_pressing and pressed_buttons:
                pressed_buttons = [False]
            elif block_pressing and not pressed_buttons:
                block_pressing = False
                
            if any(pressed_buttons):

                # Render the background
                # This is done separately so that the blue and red rectangels are not drawn under the background
                self.display.blit(self.bg_surface, (0, 0))

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


                # Render the snakes
                self.render_snakes()
                # Render the walls
                self.display.blit(self.render_walls(self.display), (0, 0))

                pygame.display.update()


            # Limit the refresh rate to the tps
            self.clock.tick(60)


if __name__ == '__main__':

    print_new_game('MAP CREATOR SCRIPT') # Log the start message

    log.info('Initialize map creator')
    map_creator = Map_creator()

    log.info('Run map creator')
    map_creator.run()