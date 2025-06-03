import pygame
from pygame.math import Vector2
import random

from logger import logger as log
from game_objects import Snake
from .default import Food


class Communism(Food):
    '''Takes the speed and length of each snake and it distribute it to everyone, adds one to everyone'''

    def initialize(self) -> None:
        self.init_texture('communism.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        log.info('Welcome comrade, to Communist Snake')

        # Get the total ammounts of speed and length
        total_length = 0
        total_speed = 0
        for player in snakes+[snake]:
            total_length += len(player.pieces)
            total_speed += player.speed

        # Speed can be a float, pieces, obviously, no
        avarage_length = total_length // len(snakes+[snake])
        avarage_speed = total_speed / len(snakes+[snake])

        # Prevent avarage_length to be 0
        if avarage_length == 0:
            avarage_length = 1

        for player in snakes+[snake]:

            # Add one piece
            if player.state == 1:
                player.speed = avarage_speed
                # Set the pieces length equal to the avarage
                while len(player.pieces) != avarage_length:
                    # Remove pieces
                    if len(player.pieces) > avarage_length:
                        player.pieces.pop()
                    # Add pieces
                    elif len(player.pieces) < avarage_length:
                        player.pieces.append(snake.last_removed)

            log.debug(f'Loading snake textures: lenin.png')
            # Load the textures and scale them to the right size
            player.textures = pygame.image.load('textures/snakes/lenin.png').convert_alpha()
            player.textures = pygame.transform.scale(player.textures, (player.thikness.x*4, player.thikness.y*5))