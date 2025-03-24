from pygame.math import Vector2
from pygame.color import Color
from various import key_map

class Snake:
    def __init__(self,
                 color: Color,
                 keybindings: key_map,
                 pos: Vector2 = Vector2(5,5),
                 length: int = 3,
                 textures: str = ''
                 ) -> None:
        
        self.color = color
        self.keybindings = keybindings
        self.pos = pos
        self.textures = textures

        self.pieces = [Vector2(pos) for _ in range(length)]
    
    def move(self, key) -> None:
        match key:
            case self.keybindings.up:    self.direction = Vector2(1,0)
            case self.keybindings.down:  self.direction = Vector2(-1,0)
            case self.keybindings.left:  self.direction = Vector2(0,-1)
            case self.keybindings.right: self.direction = Vector2(0,1)
    
    def update(self) -> None:
        self.pieces = [self.pos] + self.pieces
        self.pieces.pop()
    
    def eat(self, power: int) -> None:
        '''Power is the length added to the snake'''
        for _ in range(power):
            self.pieces.append(self.pieces[-1])
        