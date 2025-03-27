import pygame
from pygame.math import Vector2

from various import key_map

class Snake:
    def __init__(self,
                 keybindings: key_map,
                 pos: Vector2 = Vector2(0,0),
                 textures: str = 'default.png',
                 thikness: Vector2 = Vector2(10,10),
                 length: int = 3
                 ) -> None:
        
        self.pos = pos
        self.keybindings = keybindings
        self.thikness = thikness
        self.direction = Vector2(0,0)

        # Load the textures and scale them to the right size
        self.textures = pygame.image.load('textures\\snakes\\'+textures).convert_alpha()
        self.textures = pygame.transform.scale(self.textures, (thikness.x*3, thikness.y*6))

        # State 0 is 'not moving', 1 is normal and 2 is dead
        self.state = 0
        # Create the pieces of the snake
        self.pieces = [Vector2(pos)+Vector2(0,thikness.y) for _ in range(length)]
    
    def move(self, key) -> None:

        # If necessary, update the state from 'not moving' to default
        if self.state == 0:
            self.state = 1

        match key:
            case self.keybindings.up:    self.direction = Vector2(0,-1)
            case self.keybindings.left:  self.direction = Vector2(-1,0)
            case self.keybindings.down:  self.direction = Vector2(0,1)
            case self.keybindings.right: self.direction = Vector2(1,0)
    
    def update(self) -> None:

        # If the snake is not moving then don't update
        if self.state == 0:
            return

        # Update the pieces
        self.pieces = [Vector2(self.pos)] + self.pieces
        self.last_removed = self.pieces.pop()

        # Update the heads position
        self.pos += Vector2(self.direction.x * self.thikness.x, self.direction.y * self.thikness.y)
    
    def eat(self, power: int) -> None:
        '''Power is the length added to the snake'''
        # Add pieces to the snake
        for _ in range(power):
            self.pieces.append(self.last_removed)
    
    def frame(self, display: pygame.surface.Surface) -> None:

        # 0 is not moving and 1 is normal
        if self.state in [0,1]:

            # Head
            if   self.direction == Vector2(0,0):  display.blit(self.textures, self.pos, (0, self.thikness.y*0, self.thikness.x, self.thikness.y)) # State 0, the snake is still
            elif self.direction == Vector2(0,-1): display.blit(self.textures, self.pos, (0, self.thikness.y*0, self.thikness.x, self.thikness.y))
            elif self.direction == Vector2(-1,0): display.blit(self.textures, self.pos, (0, self.thikness.y*1, self.thikness.x, self.thikness.y))
            elif self.direction == Vector2(0,1):  display.blit(self.textures, self.pos, (0, self.thikness.y*2, self.thikness.x, self.thikness.y))
            elif self.direction == Vector2(1,0):  display.blit(self.textures, self.pos, (0, self.thikness.y*3, self.thikness.x, self.thikness.y))


            # Middle pieces
            for i, piece in enumerate(self.pieces[:-1]):
                
                # Define the tre pieces used to determinate the right texture
                pc1 = self.pos if i == 0 else self.pieces[i-1] # If we are considering the fist piece then use the head as pc1
                pc2 = piece
                pc3 = self.pieces[i+1]
                # thikness (not really necessary to reassign it, but whatever)
                th = self.thikness

                # At first only God and i new how this code was written, now only God nows
                if   abs((pc1-pc3).x) == th.x*2: display.blit(self.textures, pc2, (th.x, self.thikness.y*1, self.thikness.x, self.thikness.y))
                elif abs((pc1-pc3).y) == th.y*2: display.blit(self.textures, pc2, (th.x, self.thikness.y*0, self.thikness.x, self.thikness.y))

                elif (pc2-pc1) == Vector2(0,  th.y) and (pc1-pc3) == Vector2(-th.x, -th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*2, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(-th.x, 0) and (pc1-pc3) == Vector2(th.x,  -th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*3, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(0, -th.y) and (pc1-pc3) == Vector2(th.x,   th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*4, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(th.x,  0) and (pc1-pc3) == Vector2(-th.x,  th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*5, self.thikness.x, self.thikness.y))

                elif (pc2-pc1) == Vector2(th.x,  0) and (pc1-pc3) == Vector2(-th.x, -th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*4, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(0,  th.y) and (pc1-pc3) == Vector2(th.x,  -th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*5, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(-th.x, 0) and (pc1-pc3) == Vector2(th.x,   th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*2, self.thikness.x, self.thikness.y))
                elif (pc2-pc1) == Vector2(0, -th.y) and (pc1-pc3) == Vector2(-th.x,  th.y): display.blit(self.textures, pc2, (th.x, self.thikness.y*3, self.thikness.x, self.thikness.y))


            # Last piece
            if   self.pieces[-1]-self.pieces[-2] == Vector2(0,-self.thikness.y): display.blit(self.textures, self.pieces[-1], (self.thikness.x*2, self.thikness.y*0, self.thikness.x, self.thikness.y))
            elif self.pieces[-1]-self.pieces[-2] == Vector2(-self.thikness.x,0): display.blit(self.textures, self.pieces[-1], (self.thikness.x*2, self.thikness.y*1, self.thikness.x, self.thikness.y))
            elif self.pieces[-1]-self.pieces[-2] == Vector2(0,self.thikness.y):  display.blit(self.textures, self.pieces[-1], (self.thikness.x*2, self.thikness.y*2, self.thikness.x, self.thikness.y))
            elif self.pieces[-1]-self.pieces[-2] == Vector2(self.thikness.x,0):  display.blit(self.textures, self.pieces[-1], (self.thikness.x*2, self.thikness.y*3, self.thikness.x, self.thikness.y))

        # Death state
        elif self.state == 2:
            ...
    
    def kill(self):
        raise NotImplementedError

class Walls:
    def __init__(self, external_box: Vector2, custom_walls: list[Vector2], thikness: Vector2, color: pygame.color.Color):
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
    
    def frame(self, display: pygame.surface.Surface):
        # pygame.draw the custom walls
        for wall in self.custom:
            pygame.draw.rect(display, self.color, (wall, self.thikness))

class Apple:
    def __init__(self, pos: Vector2, power: int, thikness: Vector2, color: pygame.color.Color, texture: str = ''):
        self.pos = pos
        self.power = power
        self.thikness = thikness
        self.color = color
        self.texture = texture
    
    def frame(self, display: pygame.surface.Surface):
        pygame.draw.rect(display, self.color, (self.pos, self.thikness))