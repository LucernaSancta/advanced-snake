import pygame
import os.path

from pygame.math import Vector2
from pygame.color import Color
from os import getenv
from dotenv import load_dotenv

from various import colors, key_map
from game_objects import Snake, Walls


# Get program envirement
if os.path.isfile('.env'): load_dotenv('.env')
else:                      load_dotenv('.env.example')

screen_size =     Vector2(int(getenv('SCREEN_SIZE_X')),    int(getenv('SCREEN_SIZE_Y')))
snake_grid_size = Vector2(int(getenv('SNAKE_GRID_SIZE_X')),int(getenv('SNAKE_GRID_SIZE_Y')))
tps = int(getenv('TICK_PER_SECOND'))
colors.bg = Color(getenv('C_BACKGROUND'))
colors.apples = Color(getenv('C_APPLES'))
colors.snake_default = Color(getenv('C_SNAKE'))
colors.walls_default = Color(getenv('C_WALLS'))

snake_grid_thikness = Vector2(screen_size.x / snake_grid_size.x, screen_size.y / snake_grid_size.y)


def apple_spawner(snakes: list, walls: Walls):
    def __init__(self):
        pass


# Initialize pygame
pygame.init()
display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

snakes = [
    Snake(
        colors.snake_default,
        key_map(pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d),
        thikness=snake_grid_thikness
        )
]

paused = False

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
            
            elif event.key == pygame.K_SPACE:
                paused = not paused

            if paused:
                continue

            # Update snakes moves
            for snake in snakes:
                if event.key in snake.keybindings:
                    snake.move(event.key)
    
    if paused:
        continue
    
    # Update snakes logics
    for snake in snakes:
        snake.update()

    # Clear the screen and update
    display.fill(colors.bg)

    # Draw the snakes in whatever state they are
    for snake in snakes:
        snake.frame(display)

    pygame.display.update()

    # Limit the refresh rate to the tps
    clock.tick(tps)