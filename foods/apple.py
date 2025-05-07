import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from .default import Food


class Apple(Food):

    def initialize(self) -> None:
        self.power = self.kwargs['power'] if 'power' in self.kwargs else 1
        self.init_texture('apple.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        for _ in range(self.power):
            snake.pieces.append(snake.last_removed)