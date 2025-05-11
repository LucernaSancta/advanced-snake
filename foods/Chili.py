import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from .default import Food


class Chili(Food):

    def initialize(self) -> None:
        self.speed_multiplier = self.kwargs['speed_multiplier']
        self.init_texture('chili.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        snake.speed *= self.speed_multiplier