import pygame
import os.path
import random
import yaml
import toml

from pygame.math import Vector2

from game_objects import Snake, Walls, Apple
from logger import logger as log


class Game:
    def __init__(self):

        config_file = 'config.toml'
        log.debug(f'Loading config file: {config_file}')
        # Set up global config
        if os.path.isfile(config_file):
            config = toml.load(config_file)
        else:
            log.critical(f'Config file {config_file} not found.')

        # Assign global config variables
        self.screen_size =     Vector2(config['display']['screen_size']['x'], config['display']['screen_size']['y'])
        self.snake_grid_size = Vector2(config['game']['grid_size']['x'],      config['game']['grid_size']['y'])
        self.apples_textures =    config['apples']['textures']
        self.walls_textures =     config['walls']['textures']
        self.bg_texture =         config['background']['textures']
        self.initial_apples = int(config['apples']['number'])
        self.apple_power =    int(config['apples']['power'])
        self.pause_key =  config['keys']['pause']
        self.exit_key =   config['keys']['exit']
        self.wall_map =   config['walls']['map']
        self.tps =      float(config['game']['tps'])


        # Calculate tils thikness
        self.snake_grid_thikness = Vector2(self.screen_size.x // self.snake_grid_size.x, self.screen_size.y // self.snake_grid_size.y)
        log.debug(f'Snake grid thikness: {self.snake_grid_thikness}')

        log.debug('Initializing pygame')
        # Initialize pygame
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Advanced Snake - main')
        self.clock = pygame.time.Clock()

        log.debug('Loading background textures')
        # Scale the background texture
        self.bg_texture = pygame.image.load('textures/background/'+self.bg_texture).convert_alpha()
        self.bg_texture = pygame.transform.scale(self.bg_texture, self.snake_grid_thikness)

        # Store the exit key to print it later when the player wins
        self.original_exit_key = str(self.exit_key)
        # Translate exit and pause keys
        self.pause_key = pygame.key.key_code(self.pause_key)
        self.exit_key = pygame.key.key_code(self.exit_key)

        # Load walls
        self.walls: Walls = self.init_walls()
        # Load the players
        self.snakes: list[Snake] = self.init_players()
        # Initiate apples
        self.apples: list[Apple] = [] # To spawn new apples there must be an existing 'apples' list
        self.apples: list[Apple] = self.init_apples()

        log.debug('Render static objects')
        # Render static objects
        self.static_surface = pygame.Surface(self.screen_size)
        self.static_surface.fill((0, 0, 0))
        self.static_surface = self.render_background(self.static_surface)
        self.static_surface = self.render_walls(self.static_surface)
    
    def init_walls(self) -> Walls:
        return Walls(self.screen_size,self.wall_map,self.snake_grid_thikness,self.walls_textures)
    
    def init_players(self) -> list[Snake]:
        log.debug('Loading players')
        players = []
        for filename in os.listdir('players'):
            if filename.endswith(".yaml"):
                with open('players/'+filename, 'r') as file:
                    player_data = yaml.safe_load(file)
                    players.append(
                        Snake(
                            name=player_data['name'],
                            keybindings=player_data['keybindings'],
                            thikness=self.snake_grid_thikness,
                            textures=player_data['textures'],
                            pos=Vector2(player_data['starting_pos'][0]*self.snake_grid_thikness.x,player_data['starting_pos'][1]*self.snake_grid_thikness.y),
                            length=player_data['starting_length']
                            )
                        )
        return players
    
    def init_apples(self) -> list[Apple]:
        log.debug('Loading apples')
        apples = []
        for _ in range(self.initial_apples):
            apple = self.apple_spawner()
            if apple is not None:
                apples.append(apple)
        return apples

    def apple_spawner(self) -> Apple:

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
        for apple in self.apples:
            if apple.pos in spots: spots.remove(apple.pos)
        
        if len(spots) == 0:
            log.warning('No space to spawn new food, removing one, total food remaining:', len(self.apples))
            return None

        pos = random.choice(spots)
        log.debug(f'Spawning apple at: {pos}')
        return Apple(pos, self.apple_power, self.snake_grid_thikness, self.apples_textures)

    def render_background(self, surface: pygame.surface.Surface) -> pygame.surface.Surface:
        # Fill the screen with the background texture
        for x in range(int(self.snake_grid_size.x)):
            for y in range(int(self.snake_grid_size.y)):
                surface.blit(self.bg_texture, (x*self.snake_grid_thikness.x,y*self.snake_grid_thikness.y))
        
        return surface

    def render_snakes(self) -> None:
        # Draw the snakes in whatever state they are
        for snake in self.snakes:
            snake.render(self.display)

    def render_apples(self) -> None:
        # Remove None elements from apple list, None elements are created by the apple spawner
        self.apples = list(filter(lambda x: x is not None, self.apples))

        # Draw the apples
        for apple in self.apples:
            apple.render(self.display)

    def render_walls(self, surface: pygame.surface.Surface) -> pygame.surface.Surface:
        # Draw the walls
        self.walls.render(surface)

        return surface

    def update_snakes(self) -> None:
        # Update snakes logics
        for snake in self.snakes:

            # Update the position
            snake.update()

            # Check for walls collisions
            if snake in self.walls:
                log.debug(f'{snake.name} collided with a wall at {snake.pos}')
                snake.kill()
                self.snakes.remove(snake)
                continue
            
            # Check for collision with itself
            if snake.pos in snake.pieces:
                log.debug(f'{snake.name} collided with itself at {snake.pos}')
                snake.kill()
                self.snakes.remove(snake)
                continue
            
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
                for apple in self.apples:
                    if apple.pos == snake.pos:
                        log.debug(f'{snake.name} ate an apple at {apple.pos}')
                        # Update the snake
                        snake.eat(apple.power)
                        # Remove the pervious apple from the list and add a new one
                        self.apples.remove(apple)
                        self.apples.append(self.apple_spawner())
                        break

    def run(self) -> None:
        paused = False
        frames = 0

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
                    if event.key == self.exit_key:
                        log.debug('Quitting game by pressing exit key')
                        pygame.quit()
                        quit()
                    
                    elif event.key == self.pause_key:
                        log.debug('Game paused')
                        paused = not paused

                    if paused:
                        continue

                    # Update snakes moves
                    for snake in self.snakes:
                        if event.key in snake.keybindings:
                            log.debug(f'{snake.name} moved {pygame.key.name(event.key)}')
                            snake.move(event.key)
            
            # Winning condition
            if len(self.apples) == 0 and paused == False:
                paused = True
                log.info('Game over, you won!')
                log.info(f'press {self.original_exit_key} to exit')


            # If the game is poused, skip the updates
            if paused:
                self.clock.tick(60)
                continue

            
            # Update snakes logics
            self.update_snakes()
            
            
            # Quit by game over
            if not len(self.snakes):
                log.info('Game over, every one is dead.')

                # Possible compenetration message (#32)
                if not frames:
                    log.critical('└── This is probably caused by a misplaced snakes compenetration with walls or borders')
                    log.critical('    Please check the snakes setting or open the map creator for a static view')

                pygame.quit()
                quit()


            # Render static objects
            self.display.blit(self.static_surface, (0, 0))
            # Render moving objects
            self.render_snakes()
            self.render_apples()

            pygame.display.update()

            # Limit the refresh rate to the tps
            self.clock.tick(self.tps)

            frames += 1


if __name__ == '__main__':
    log.info('Initialize game')
    game = Game()
    log.info('Run game')
    game.run()