from pygame.math import Vector2
from pygame.color import Color
from pygame.surface import Surface
from pygame import draw
from various import key_map

class Snake:
    def __init__(self,
                 color: Color,
                 keybindings: key_map,
                 pos: Vector2 = Vector2(0,0),
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

        # State 1 is alive, 0 is dead
        self.state = 1
        # Create the pieces of the snake
        self.pieces = [Vector2(pos) for _ in range(length)]
    
    def move(self, key) -> None:
        match key:
            case self.keybindings.up:    self.direction = Vector2(0,-1)
            case self.keybindings.down:  self.direction = Vector2(0,1)
            case self.keybindings.left:  self.direction = Vector2(-1,0)
            case self.keybindings.right: self.direction = Vector2(1,0)
    
    def update(self) -> None:
        # Update the heads position
        self.pos += Vector2(self.direction.x * self.thikness.x, self.direction.y * self.thikness.y)

        # Update the pieces
        self.pieces = [Vector2(self.pos)] + self.pieces
        self.pieces.pop()
    
    def eat(self, power: int) -> None:
        '''Power is the length added to the snake'''
        # Add pieces to the snake
        for _ in range(power):
            self.pieces.append(self.pieces[-1])
    
    def frame(self, display: Surface) -> None:

        match self.state:
            # Normal state
            case 1:
                draw.rect(display, self.color, (self.pos, self.thikness))
                for piece in self.pieces:
                    draw.rect(display, self.color, (piece, self.thikness))
            # Death state
            case 0:
                ...

class Walls:
    def __init__(self, external_box: Vector2, custom_walls: list[Vector2], thikness: Vector2, color: Color):
        self.external_box = external_box
        self.custom = custom_walls
        self.color = color
        self.thikness = thikness

    def __contains__(self, snake: Snake) -> bool:
        '''Check collision for a given snake and the walls'''
        # Check for boarders collisions
        if snake.pos.x not in range(int(self.external_box.x)): return True
        if snake.pos.y not in range(int(self.external_box.y)): return True
        # Check for custom walls collisions
        if snake.pos in self.custom: return True
        
        return False
    
    def frame(self, display: Surface):
        # Draw the custom walls
        for wall in self.custom:
            draw.rect(display, self.color, (wall, self.thikness))

class Apple:
    def __init__(self, pos: Vector2, power: int, thikness: Vector2, color: Color, texture: str = ''):
        self.pos = pos
        self.power = power
        self.thikness = thikness
        self.color = color
        self.texture = texture
    
    def frame(self, display: Surface):
        draw.rect(display, self.color, (self.pos, self.thikness))