from pygame.math import Vector2
from pygame.surface import Surface
from pygame import draw
from snake import Snake

class Walls:
    def __init__(self, external_box, custom_walls):
        self.external_box = external_box
        self.custom = custom_walls

    def __contains__(self, snake: Snake) -> bool:
        '''Check collision for a given snake and the walls'''
        ...
    
    def frame(self, display: Surface):
        ...