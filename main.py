import json
import pygame
import random
import os.path

from importlib import import_module
from pygame.math import Vector2

from game_objects import Snake, Walls
from foods.default import Food
from logger import logger as log
from menus.menu_components import Menu
from various import print_new_game


class Game:
    def __init__(self):

        log.name = 'game' # Set the logger name

        # Load config file
        self.load_configs('config.json')

        # Calculate tiles thikness
        self.snake_grid_thikness = Vector2(self.screen_size.x // self.snake_grid_size.x, self.screen_size.y // self.snake_grid_size.y)
        log.debug(f'Snake grid thikness: {self.snake_grid_thikness}')
        self.check_visual_ratios()

        log.debug('Initializing pygame')
        # Initialize pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Advanced Snake - main')
        self.clock = pygame.time.Clock()

        log.debug('Loading and scaling the background texture')
        # Scale the background texture
        self.bg_texture = pygame.image.load('textures/background/'+self.bg_texture).convert_alpha()
        if self.bg_tiling['active']:
            self.bg_texture = pygame.transform.scale(self.bg_texture, (self.snake_grid_thikness.x*self.bg_tiling_size.x, self.snake_grid_thikness.y*self.bg_tiling_size.y))
        else:
            # Scale the background texture to the screen size
            self.bg_texture = pygame.transform.scale(self.bg_texture, (self.screen_size.x, self.screen_size.y))


        # Store the exit key to print it later when the player wins
        self.original_pause_key = str(self.pause_key)
        # Translate exit and pause keys
        self.pause_key = pygame.key.key_code(self.pause_key)
        self.force_pause_key = pygame.key.key_code(self.force_pause_key)
        self.exit_key = pygame.key.key_code(self.exit_key)

        # Load walls
        self.walls: Walls = self.init_walls()

        # Load the players and create custom events (for their different speeds)
        self.snakes: list[Snake] = self.init_players()

        # Initiate foods
        self.init_foods()

        log.debug('Render static objects')
        # Render static objects
        self.static_surface = pygame.Surface(self.screen_size)
        self.static_surface.fill((0, 0, 0))
        self.static_surface = self.render_background(self.static_surface)
        self.static_surface = self.render_walls(self.static_surface)
    
    def check_visual_ratios(self) -> None:
        """Simple checks for the wondow ratio and shit"""

        # Float (with float division) thikness
        flt_thikness = Vector2(self.screen_size.x / self.snake_grid_size.x, self.screen_size.y / self.snake_grid_size.y)

        # The float thikness is not equal to the absolute thikness
        if not ((flt_thikness.x == self.snake_grid_thikness.x) and (flt_thikness.x == self.snake_grid_thikness.y)):
            log.error('The screen size and the grid size are not compatible')
            if self.flt_th_noti:
                input('Press anter to ignore the message... (you can disable this message by setting the notifications.flt_th to false)')

        # The ration of the x and y thikness is not a square
        if flt_thikness.x / flt_thikness.y != 1:
            log.error('The screen ratio is not simmetrical to the grid ratio')
            if self.ratios_noti:
                input('Press anter to ignore the message... (you can disable this message by setting the notifications.ratios to false)')
    
    def load_configs(self, config_path: str) -> None:
        """Load the config file and assign the variables to the class"""

        log.debug(f'Loading config file: {config_path}')
        # Set up global config
        if not os.path.isfile(config_path):
            log.critical(f'Config file {config_path} not found.')
        else:

            with open(config_path, 'r') as config_file:
                config = json.load(config_file)

                # Assign global config variables
                self.screen_size =     Vector2(config['display']['screen_size'])
                self.snake_grid_size = Vector2(config['game']['grid_size'])
                self.end_condition =  int(config['game']['end_condition'])
                self.walls_textures =     config['walls']['textures']
                self.bg_texture =         config['background']['textures']
                self.pause_key =       config['keys']['pause']
                self.force_pause_key = config['keys']['force_pause']
                self.exit_key =        config['keys']['exit']
                self.wall_map =   config['walls']['map']
                self.fps =  float(config['display']['fps'])

                self.bg_tiling = config['background']['tiling']
                self.bg_tiling_size = Vector2(config['background']['tiling']['size'])

                self.player_configs = config['players']
                self.foods_config =   config['foods']

                self.ratios_noti =   config['notifications']['ratios']
                self.flt_th_noti =   config['notifications']['flt_th']
    
    def init_walls(self) -> Walls:
        return Walls(self.screen_size,self.wall_map,self.snake_grid_thikness,self.walls_textures)
    
    def init_players(self) -> list[Snake]:
        log.debug('Loading players')
        players = []

        for player_data in self.player_configs:
            # Load the player config
            players.append(
                Snake(
                    name=player_data['name'],
                    keybindings=player_data['keybindings'],
                    thikness=self.snake_grid_thikness,
                    textures=player_data['textures'],
                    speed=player_data['speed'],
                    pos=Vector2(player_data['starting_pos'][0]*self.snake_grid_thikness.x,player_data['starting_pos'][1]*self.snake_grid_thikness.y),
                    length=player_data['starting_length']
                    )
                )
        return players
    
    def init_foods(self):

        log.debug('Loading foods')


        # Get foods classes, weights and kwargs
        self.foods_types = []
        self.foods_kwargs = {}
        self.foods_weights = []
        for food in self.foods_config['types']:
            food_class = getattr(import_module('foods.'+food['name']), food['name'])
            self.foods_types.append(food_class)
            self.foods_kwargs[food_class] = food['kwargs']
            self.foods_weights.append(food['weight'])


        # Spawn the initial foods
        self.foods: list[Food] = []
        for _ in range(int(self.foods_config['number'])):
            food = self.food_spawner()
            if food is not None:
                self.foods.append(food)

    def food_spawner(self) -> Food:

        # Create a list with every spot in the grid
        spots = []
        for x in range(int(self.snake_grid_size.x)):
            for y in range(int(self.snake_grid_size.y)):
                spots.append(Vector2(x*self.snake_grid_thikness.x, y*self.snake_grid_thikness.y))
        
        # Remove the spots where the snakes are
        for snake in self.snakes:
            if snake.pos in spots: spots.remove(snake.pos)
            for piece in snake.pieces:
                if piece in spots: spots.remove(piece)
        
        # Remove the spots where the walls are
        for wall in self.walls.walls_absolute:
            if wall in spots: spots.remove(wall)

        # Fix: Remove spots where apples already exist
        for food in self.foods:
            if food.pos in spots: spots.remove(food.pos)
        
        if len(spots) == 0:
            log.warning('No space to spawn new food, removing one, total food remaining:', len(self.foods))
            return None

        # Chose random food type based on the foods weights
        pos = random.choice(spots)
        food_to_spawn = random.choices(self.foods_types, weights=self.foods_weights, k=1)[0]

        log.debug(f'Spawning food "{food_to_spawn.__name__}"at: {pos}')

        # Enter the foods position thikness and custom arguments then spawn it
        return food_to_spawn(pos, self.snake_grid_thikness, self.foods_kwargs[food_to_spawn])

    def render_background(self, surface: pygame.surface.Surface) -> pygame.surface.Surface:

        log.debug(f'Rendering background, tiling={self.bg_tiling}')

        if self.bg_tiling['active']:
            # Fill the screen with the tiled background texture
            for x in range(int(self.snake_grid_size.x)):
                for y in range(int(self.snake_grid_size.y)):
                    surface.blit(self.bg_texture, (
                        x*self.snake_grid_thikness.x*self.bg_tiling_size.x,
                        y*self.snake_grid_thikness.y*self.bg_tiling_size.y
                    ))
        
        else:
            # Fill the screen with a non tiled background texture
            surface.blit(self.bg_texture, (0, 0))
        
        return surface

    def render_snakes(self) -> None:
        # Draw the snakes in whatever state they are
        for snake in self.snakes:
            snake.render(self.display)

    def render_foods(self) -> None:
        # Remove None elements from apple list, None elements are created by the apple spawner
        self.foods = list(filter(lambda x: x is not None, self.foods))

        # Draw the apples
        for food in self.foods:
            food.render(self.display)

    def render_walls(self, surface: pygame.surface.Surface) -> pygame.surface.Surface:
        # Draw the walls
        self.walls.render(surface)

        return surface

    def game_quit(self) -> None:
        pygame.quit()
        quit()

    def stop_game(self, menu: Menu = None) -> None:
        '''Stops the game without exiting python'''
        self.running = False
        if menu is not None:
            menu.quit()

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
            ['resume',    'RESUME',    menu.quit,                    b_th, [menu.center.x, menu.center.y - 2*delta_height]],
            ['main_menu', 'MAIN MENU', lambda: self.stop_game(menu), b_th, [menu.center.x, menu.center.y]],
            ['quit',      'QUIT',      self.game_quit,               b_th, [menu.center.x, menu.center.y + 2*delta_height]]
        ]

        # Add buttons to menu
        for option in options:
            menu.add_option(*option)

        log.debug('Running menu')
        menu._run()

        log.info('Game resumed')

    def check_win_condition(self) -> bool:
        '''Returns True when the game end condition is meet'''

        match self.end_condition:

            case 0:
                # Never win
                return False
            
            case 1:
                # Win when there is no food left
                if len(self.foods) == 0:
                    return True
            
            case 2:
                # Win when only one snake is alive
                if len(self.snakes) == 1:
                    return True
            
            case 3:
                # Win when no one is alive
                if len(self.snakes) == 0:
                    return True
            
        return False

    def update_snake(self, snake: Snake) -> None:
        '''Update snakes logics'''

        # Update the position
        snake.update()

        # Check for walls collisions
        if snake in self.walls:
            log.debug(f'{snake.name} collided with a wall at {snake.pos}')
            snake.kill()
            self.snakes.remove(snake)
            return
        
        # Check for collision with itself
        if snake.pos in snake.pieces:
            log.debug(f'{snake.name} collided with itself at {snake.pos}')
            snake.kill()
            self.snakes.remove(snake)
            return
        
        # Check for snake to snake collisions
        snakes_copy = self.snakes[:]
        snakes_copy.remove(snake)
        for second_snake in snakes_copy:
            # Head to head collision
            if snake.pos == second_snake.pos:
                log.debug(f'{snake.name} collided with {second_snake.name} at {snake.pos}')
                snake.kill()
                second_snake.kill()
                self.snakes.remove(snake)
                self.snakes.remove(second_snake)
                break
            # Head to tail collision
            if snake.pos in second_snake.pieces:
                log.debug(f'{snake.name} collided with {second_snake.name} at {snake.pos}')
                snake.kill()
                self.snakes.remove(snake)
                break
        
        # If no collision was found then continue
        else:

            # Check for apple collisions
            for food in self.foods:
                if food.pos == snake.pos:
                    log.debug(f'{snake.name} ate some food at {food.pos}')
                    # Update the snakeat {apple.pos}')
                    # Update the snake
                    food.eaten(self.display, snake, [x for x in self.snakes if x != snake])
                    # Remove the pervious apple from the list and add a new one
                    self.foods.remove(food)
                    self.foods.append(self.food_spawner())
                    break

    def _run(self) -> None:
        '''Main game loop'''

        paused = False
        frames = 0
        deltaTime = 0
        self.running = True

        while self.running:

            # Get events
            for event in pygame.event.get():

                # Quit when closing the window
                if event.type == pygame.QUIT:
                    self.game_quit()
                
                # KEYBOARD PRESS EVENTS
                if event.type == pygame.KEYDOWN:
                    
                    # Force quit
                    if event.key == self.exit_key:
                        log.info('Quitting game by pressing exit key')
                        self.game_quit()
                    
                    # Force pause
                    elif event.key == self.force_pause_key:
                        if paused:
                            log.warning('Game resumed forcefully')
                            paused = False
                        else:
                            log.warning('Game paused forcefully')
                            paused = True
                    
                    # Normal pause
                    elif event.key == self.pause_key:
                        self.pause()


                    if paused:
                        continue

                    # Update snakes moves
                    for snake in self.snakes:
                        if event.key in snake.keybindings:
                            log.debug(f'{snake.name} changed direction with {pygame.key.name(event.key)}')
                            snake.move(event.key)


            # If the game is poused, skip the updates
            if paused:
                self.clock.tick(60)
                continue


            # Snake events
            for snake in self.snakes:
                # Start the timer only when the snakes start moving
                if snake.state != 0:
                    update = snake.timer_event.tick(deltaTime)
                    if update:
                        self.update_snake(snake)
            
            
            # Possible compenetration message (#32)
            if (not len(self.snakes)) and (not frames):

                log.critical('Game over, every one is dead.')
                log.critical('└── This is probably caused by a misplaced snakes compenetration with walls or borders')
                log.critical('    Please check the snakes setting or open the map creator for a static view')

                pygame.quit()
                quit()


            # Render static objects
            self.display.blit(self.static_surface, (0, 0))
            # Render moving objects
            self.render_snakes()
            self.render_foods()

            pygame.display.update()


            # Winning condition
            if self.check_win_condition():
                paused = True
                log.info('Game over, you won!')
                log.info(f'press {self.original_pause_key} to exit')


            # Limit the refresh rate to the fps
            deltaTime = self.clock.tick(self.fps)

            frames += 1


if __name__ == '__main__':

    print_new_game('MAIN GAME SCRIPT') # Log the start message
    
    log.info('Initialize game')
    game = Game()

    log.info('Run game')
    game._run()