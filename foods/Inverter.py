import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from .default import Food


class Inverter(Food):
    '''Inverts the head with the tail of the snake'''

    def initialize(self) -> None:
        self.init_texture('inverter.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:

        # Invert the current tail
        new_tail = snake.pieces[::-1]
        # remove last piece and set it as the new head
        new_head = Vector2(new_tail.pop(0))
        # Add the old head at the end of the new tail
        new_tail.append(Vector2(snake.pos))

        # Replace variables
        snake.pos = new_head
        snake.pieces = new_tail
        # Invert direction
        snake.direction.x *= -1
        snake.direction.y *= -1