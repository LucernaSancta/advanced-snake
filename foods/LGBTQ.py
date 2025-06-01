import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from .default import Food


class LGBTQ(Food):
    '''AAnimation example'''

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

        pass
