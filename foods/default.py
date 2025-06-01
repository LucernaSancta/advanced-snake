import pygame
from pygame.math import Vector2

from logger import logger as log
from game_objects import Snake
from various import TimerObj


class Food:
    '''
    ## Default Food class
    refer to the foods config
    '''

    def __init__(
            self,
            pos: Vector2,
            thikness: Vector2,
            animation: dict = {},
            kwargs: dict = {}
        ) -> None:

        self.pos = pos
        self.thikness = thikness
        self.animation = animation
        self.kwargs = kwargs

        if self.animation:
            self.animation_timer = TimerObj(self.animation['time_ms'])
            self.last_frame = 0

        self.initialize()
    
    def init_texture(self, file_name: str = 'default.png') -> None:
        log.debug(f'Loading food texture {file_name}')
        # Load the textures and scale them to the right size
        self.texture = pygame.image.load('textures/food/'+file_name).convert_alpha()
        # Scale according to the animation frames
        if self.animation:
            self.texture = pygame.transform.scale(self.texture, (self.thikness.x, self.thikness.y*self.animation['frames']))
        else:
            # Scale normally
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
    
    def update(
        self,
        display: pygame.surface.Surface,
        deltaTime: int | float
        ) -> None:
        
        self.render(display, deltaTime)
    
    def render(
        self,
        display: pygame.surface.Surface,
        deltaTime: int | float
        ) -> None:

        if self.animation:
            # Render animation
            new = self.animation_timer.tick(deltaTime)
            if new:
                self.last_frame += 1
                self.last_frame %= self.animation['frames']
            
            display.blit(self.texture, self.pos, (0, self.thikness.y*self.last_frame, self.thikness.x, self.thikness.y))
            
        else:
            # Render without animation
            display.blit(self.texture, self.pos)