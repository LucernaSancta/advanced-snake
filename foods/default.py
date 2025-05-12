import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake


class Food:
    def __init__(
            self,
            pos: Vector2,
            thikness: Vector2,
            kwargs: dict = {}
        ) -> None:

        self.pos = pos
        self.thikness = thikness
        self.kwargs = kwargs
        self.offset = Vector2(0,0)

        self.initialize()
    
    def init_texture(self, file_name: str = 'default.png') -> None:
        log.debug(f'Loading food texture {file_name}')
        # Load the textures and scale them to the right size
        self.texture = pygame.image.load('textures/food/'+file_name).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, self.thikness)

    def initialize(self) -> None:
        self.init_texture('default.png')
    
    def eaten(
            self,
            surface: pygame.surface.Surface,
            snake: Snake,
            snakes: list[Snake]
        ) -> None:
        ...
    
    def update(self, display: pygame.surface.Surface, deltaTime) -> None:
        display.blit(self.texture, self.pos+self.offset)