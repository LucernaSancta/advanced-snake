from pygame.math import Vector2
from pygame.color import Color

class Snake:
    def __init__(self,
                 color: Color,
                 keybindings: tuple,
                 pos: Vector2 = Vector2(5,5),
                 length: int = 3,
                 textures: str = ''
                 ):
        self.color = color
        self.keybindings = keybindings
        self.pos = pos
        self.length = length
        self.textures = textures