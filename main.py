import pygame
import os.path

from pygame.math import Vector2
from pygame.color import Color
from os import getenv
from dotenv import load_dotenv

from various import colors
from snake import Snake


# Get program envirement
if os.path.isfile('.env'): load_dotenv('.env')
else:                      load_dotenv('.env.example')

screen_size =     Vector2(int(getenv('SCREEN_SIZE_X')),    int(getenv('SCREEN_SIZE_Y')))
snake_grid_size = Vector2(int(getenv('SNAKE_GRID_SIZE_X')),int(getenv('SNAKE_GRID_SIZE_Y')))
tps = int(getenv('TICK_PER_SECOND'))
colors.bg = Color(getenv('C_BACKGROUND'))
colors.apples = Color(getenv('C_APPLES'))
colors.snake_default = Color(getenv('C_SNAKE'))
colors.tails_default = Color(getenv('C_TAILS'))


# Initialize pygame
pygame.init()
display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

snakes = [
    Snake(
        colors.snake_default,
        (pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d)
        )
]

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

            # Update snakes moves
            for snake in snakes:
                if event.key in snake:
                    snake.move(event.key)
            


    display.fill(colors.bg)
    pygame.display.update()

    # Limit the refresh rate to the tps
    clock.tick(tps)