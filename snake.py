from pygame.math import Vector2
from pygame.color import Color
from pygame.surface import Surface
from pygame import draw
from various import key_map

class Snake:
    def __init__(self,
                 color: Color,
                 keybindings: key_map,
                 pos: Vector2 = Vector2(5,5),
                 length: int = 3,
                 textures: str = '',
                 direction: Vector2 = Vector2(0,0),
                 thikness: Vector2 = Vector2(10,10)
                 ) -> None:
        
        self.color = color
        self.keybindings = keybindings
        self.pos = pos
        self.textures = textures
        self.direction = direction
        self.thikness = thikness

        self.state = 1
        self.pieces = [Vector2(pos) for _ in range(length)]
    
    def move(self, key) -> None:
        match key:
            case self.keybindings.up:    self.direction = Vector2(0,-1)
            case self.keybindings.down:  self.direction = Vector2(0,1)
            case self.keybindings.left:  self.direction = Vector2(-1,0)
            case self.keybindings.right: self.direction = Vector2(1,0)
    
    def update(self) -> None:
        self.pos += Vector2(self.direction.x * self.thikness.x, self.direction.y * self.thikness.y)

        self.pieces = [self.pos] + self.pieces
        self.pieces.pop()
    
    def eat(self, power: int) -> None:
        '''Power is the length added to the snake'''
        for _ in range(power):
            self.pieces.append(self.pieces[-1])
    
    def frame(self, display: Surface) -> None:

        match self.state:
            # Normal state
            case 1:
                draw.rect(display, self.color, (self.pos, self.thikness))
            # Death state
            case 2:
                ...