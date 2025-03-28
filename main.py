import pygame
import os.path
import random

from pygame.math import Vector2
from pygame.color import Color
from os import getenv
from dotenv import load_dotenv

from various import colors, key_map
from game_objects import Snake, Walls, Apple


# Get program envirement
if os.path.isfile('.env'): load_dotenv('.env')
else:                      load_dotenv('.env.example')

screen_size =     Vector2(int(getenv('SCREEN_SIZE_X')),    int(getenv('SCREEN_SIZE_Y')))
snake_grid_size = Vector2(int(getenv('SNAKE_GRID_SIZE_X')),int(getenv('SNAKE_GRID_SIZE_Y')))
tps = float (getenv('TICK_PER_SECOND'))

snake_default_textures = getenv('SNAKE_DEFAULT_TEXTURES')
food_default_textures = getenv('FOOD_DEFAULT_TEXTURES')

wall_map = getenv('WALLS_MAP')

colors.bg = Color(getenv('C_BACKGROUND'))
colors.walls_default = Color(getenv('C_WALLS'))

initial_apples = int(getenv('INITIAL_APPLES'))
default_apple_power = int(getenv('DEFAULT_APPLES_POWER'))

snake_grid_thikness = Vector2(screen_size.x / snake_grid_size.x, screen_size.y / snake_grid_size.y)

# Apple generator function
def apple_spawner(snakes: list[Snake], walls: Walls) -> Apple:

    # Create a list with every spot in the grid
    spots = []
    for x in range(int(snake_grid_size.x)):
        for y in range(int(snake_grid_size.y)):
            spots.append(Vector2(x*snake_grid_thikness.x,y*snake_grid_thikness.y))
    
    # Remove the spots where the snakes are
    for snake in snakes:
        if snake.pos in spots: spots.remove(snake.pos)
        for piece in snake.pieces:
            if piece in spots: spots.remove(piece)
    
    # Remove the spots where the walls are
    for wall in walls.custom_walls:
        if wall in spots: spots.remove(wall)

    if not len(spots):
        print('You won!')

    pos = random.choice(spots)
    return Apple(pos, default_apple_power, snake_grid_thikness, food_default_textures)

# Initialize pygame
pygame.init()
display = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

walls = Walls(screen_size,wall_map,snake_grid_thikness,colors.walls_default)

snakes: list[Snake] = [
    Snake(
        key_map(pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d),
        thikness=snake_grid_thikness,
        textures=snake_default_textures,
        pos=Vector2(snake_grid_size.x // 2 * snake_grid_thikness.x, snake_grid_size.y // 2 * snake_grid_thikness.y)
        )
]

apples: list[Apple] = [apple_spawner(snakes, walls) for _ in range(initial_apples)]

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

        # Update the position
        snake.update()

        # Check for walls collisions
        if snake in walls:
            snake.kill()
            continue
        
        # Check for collision with itself
        if snake.pos in snake.pieces:
            snake.kill()
            continue
        
        # Check fro snake to snake collisions
        snakes_copy = snakes[:]
        snakes_copy.remove(snake)
        for second_snake in snakes_copy:
            # Head to head collision
            if snake.pos == second_snake.pos:
                snake.kill()
                second_snake.kill()
                break
            # Head to tail collision
            if snake.pos in second_snake.pieces:
                snake.kill()
                break
        
        # If no collision was found then continue
        else:

            # Check for apple collisions
            for apple in apples:
                if apple.pos == snake.pos:
                    # Update the snake
                    snake.eat(apple.power)
                    # Remove the pervious apple from the list and add a new one
                    apples.remove(apple)
                    apples.append(apple_spawner(snakes,walls))
                    break
        

    # Clear the screen and update
    display.fill(colors.bg)

    # Draw the snakes in whatever state they are
    for snake in snakes:
        snake.frame(display)

    # Draw the apples
    for apple in apples:
        apple.frame(display)

    # Draw the walls
    walls.frame(display)

    pygame.display.update()

    # Limit the refresh rate to the tps
    clock.tick(tps)