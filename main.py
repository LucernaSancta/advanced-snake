import pygame
import os.path

from pygame.math import Vector2
from os import environ
from os import getenv
from dotenv import load_dotenv

from various import colors


# Get program envirement
if os.path.isfile('.env'): load_dotenv('.env')
else:                      load_dotenv('.env.example')

screen_size = Vector2(getenv('SCREEN_SIZE'))
snake_grid_size = Vector2(getenv('SNAKE_GRID_SIZE'))
tps = int(getenv('TICK_PER_SECOND'))
colors.bg = getenv('C_BACKGROUND')
colors.apples = getenv('C_APPLES')
colors.snake_default = getenv('C_SNAKE')
colors.tails_default = getenv('C_TAILS')


# Initialize pygame
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()
display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


while True:

    # Limit the refresh rate to the tps
    clock.tick(tps)

    # Get events
    for event in pygame.event.get():

        # Quit when closing the window
        if event.type == pygame.QUIT:
            pygame.quit()
            quitvar = True


        # KEYBOARD PRESS EVENTS
        if event.type == pygame.KEYDOWN:
            
            ...
            
    pygame.display.update()
