import pygame
from pygame.math import Vector2
import random

from logger import logger as log
from game_objects import Snake
from .default import Food


class LGBTQ(Food):
    '''Shuffles the snakes positions'''

    def initialize(self) -> None:
        # self. = self.kwargs[]
        self.init_texture('lgbtq.png')
        pass
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        log.info('Magic')

        # Get all players heads and tails
        players_data = []
        for player in snakes+[snake]:
            log.critical(str((Vector2(player.pos), Vector2(snake.direction), player.pieces[:])))
            players_data.append((Vector2(player.pos), Vector2(snake.direction), player.pieces[:]))

        # Shuffle the data
        while True:
            shuffled_data = random.sample(players_data, len(players_data))
            if shuffled_data != players_data:
                break

        # Reassign casually all heads and tails
        for player in snakes+[snake]:
            player.pos, player.direction, player.pieces = shuffled_data.pop(0)