import csv
import pygame
from pygame.math import Vector2

from various import Timer, key_map
from logger import logger as log


class Snake:
    def __init__(
            self,
            name: str,
            keybindings: list,
            pos: Vector2 = Vector2(0,0),
            speed: int = 2,
            textures: str = 'default.png',
            thikness: Vector2 = Vector2(10,10),
            length: int = 3
        ) -> None:
        
        log.debug(f'Initializing snake {name}')

        self.name = name
        self.pos = pos
        self.keybindings = key_map(*keybindings)
        self.thikness = thikness
        self.direction = Vector2(0,0)
        self.speed = speed

        # Create custom event for the snake updating
        # Set the initial time to the maximum time so it doesn't update at the beginning (#62)
        self.timer_event = Timer(1000/speed, 1000/speed)

        log.debug(f'Loading snake textures: {textures}')
        # Load the textures and scale them to the right size
        self.textures = pygame.image.load('textures/snakes/'+textures).convert_alpha()
        self.textures = pygame.transform.scale(self.textures, (thikness.x*4, thikness.y*5))

        # State 0 is 'not moving', 1 is normal and 2 is dead
        self.state = 0
        # Create the pieces of the snake
        self.pieces = [Vector2(pos) + Vector2(0, thikness.y*(i+1)) for i in range(length)]
    
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
    
    def render(
            self,
            display: pygame.surface.Surface
        ) -> None:

        # 0 is not moving and 1 is normal
        if self.state in [0,1]:

            # thikness (not really necessary to reassign it, but whatever)
            th = self.thikness

            # Head
            delta = self.pieces[0] - self.pos
            if   self.state == 0: display.blit(self.textures, self.pos, (th.x*0, 0, th.x, th.y))
            elif delta == Vector2(0, th.y): display.blit(self.textures, self.pos, (th.x*0, 0, th.x, th.y))
            elif delta == Vector2( th.x,0): display.blit(self.textures, self.pos, (th.x*1, 0, th.x, th.y))
            elif delta == Vector2(0,-th.y): display.blit(self.textures, self.pos, (th.x*2, 0, th.x, th.y))
            elif delta == Vector2(-th.x,0): display.blit(self.textures, self.pos, (th.x*3, 0, th.x, th.y))
            else: log.error(f'Delta out of range: {delta}')


            # Middle pieces
            for i, piece in enumerate(self.pieces[:-1]):
                
                # Define the tre pieces used to determinate the right texture
                pc1 = self.pos if i == 0 else self.pieces[i-1] # If we are considering the fist piece then use the head as pc1
                pc2 = piece
                pc3 = self.pieces[i+1]
                d21 = (pc2-pc1)
                d31 = (pc3-pc1)

                # At first only God and i new how this code was written, now only God nows
                if   d21.y ==  th.y:
                    if   d31 == Vector2( -th.x,th.y): display.blit(self.textures, pc2,      (0, th.y*1, th.x, th.y))
                    elif d31 == Vector2(   0,2*th.y): display.blit(self.textures, pc2,      (0, th.y*2, th.x, th.y))
                    elif d31 == Vector2(  th.x,th.y): display.blit(self.textures, pc2,      (0, th.y*3, th.x, th.y))
                elif d21.x == -th.x:
                    if   d31 == Vector2(-th.x,-th.y): display.blit(self.textures, pc2,   (th.x, th.y*1, th.x, th.y))
                    elif d31 == Vector2(  -2*th.x,0): display.blit(self.textures, pc2,   (th.x, th.y*2, th.x, th.y))
                    elif d31 == Vector2( -th.x,th.y): display.blit(self.textures, pc2,   (th.x, th.y*3, th.x, th.y))
                elif d21.y == -th.y:
                    if   d31 == Vector2( th.x,-th.y): display.blit(self.textures, pc2, (th.x*2, th.y*1, th.x, th.y))
                    elif d31 == Vector2(  0,-2*th.y): display.blit(self.textures, pc2, (th.x*2, th.y*2, th.x, th.y))
                    elif d31 == Vector2(-th.x,-th.y): display.blit(self.textures, pc2, (th.x*2, th.y*3, th.x, th.y))
                elif d21.x ==  th.x:
                    if   d31 == Vector2(  th.x,th.y): display.blit(self.textures, pc2, (th.x*3, th.y*1, th.x, th.y))
                    elif d31 == Vector2(   2*th.x,0): display.blit(self.textures, pc2, (th.x*3, th.y*2, th.x, th.y))
                    elif d31 == Vector2( th.x,-th.y): display.blit(self.textures, pc2, (th.x*3, th.y*3, th.x, th.y))

            # Last piece
            pc1 = self.pieces[-1]
            pc2 = self.pieces[-2] if len(self.pieces) > 1 else self.pos
            if   pc1-pc2 == Vector2(0, th.y): display.blit(self.textures, pc1, (th.x*0, th.y*4, th.x, th.y))
            elif pc1-pc2 == Vector2(th.x, 0): display.blit(self.textures, pc1, (th.x*1, th.y*4, th.x, th.y))
            elif pc1-pc2 == Vector2(0,-th.y): display.blit(self.textures, pc1, (th.x*2, th.y*4, th.x, th.y))
            elif pc1-pc2 == Vector2(-th.x,0): display.blit(self.textures, pc1, (th.x*3, th.y*4, th.x, th.y))

        # Death state
        elif self.state == 2:
            ...
    
    def kill(self):
        log.info(f'Player {self.name} elimenated with a total score of {len(self.pieces)} points!')


class Walls:
    def __init__(
            self,
            external_box: Vector2,
            walls_map: str,
            thikness: Vector2,
            textures: str = 'default.png'
        ) -> None:
        
        self.external_box = external_box
        self.thikness = thikness
        self.custom_walls: list[Vector2] = []

        log.debug(f'Loading wall map: {walls_map}')
        # Open the csv file
        with open('maps/'+walls_map) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Extract the values
            for i, row in enumerate(csv_reader):
                # Exclude the first row (key row)
                if i == 0:
                    continue
                try:
                    self.custom_walls.append(Vector2(int(row[0]),int(row[1])))
                except (IndexError, ValueError):
                    raise SyntaxError('Wrong walls tiling')
        
        log.debug('Creating wall boarders')
        # Create boarders
        self.boarders = []
        for i in range(-1, int(external_box.x // thikness.x)+1):
            self.boarders.append(Vector2(i,-1))
            self.boarders.append(Vector2(i,int(external_box.y // thikness.y)))
        for i in range(int(external_box.y // thikness.y)):
            self.boarders.append(Vector2(-1,i))
            self.boarders.append(Vector2(int(external_box.x // thikness.x),i))


        log.debug(f'Loading walls texture: {textures}')
        # Load the textures and scale them to the right size
        self.textures = pygame.image.load('textures/walls/'+textures).convert_alpha()
        self.textures = pygame.transform.scale(self.textures, (thikness.x*12, thikness.y*4))

    def __contains__(self, snake: Snake) -> bool:
        # Check for custom walls collisions
        for wall in (self.custom_walls + self.boarders):
            if snake.pos == Vector2(wall.x*self.thikness.x,wall.y*self.thikness.y):
                return True
        
        return False
    
    def add(self, pos: Vector2) -> None:
        '''Add a wall to the current walls'''

        tile = Vector2(pos.x // self.thikness.x, pos.y // self.thikness.y)
        
        # Check if the wall exists in the list
        if tile not in self.custom_walls:
            log.debug(f'Adding wall at {pos} - {tile}')
            self.custom_walls.append(tile)
    
    def remove(self, pos: Vector2) -> None:
        '''Remove a wall to the current walls'''

        tile = Vector2(pos.x // self.thikness.x, pos.y // self.thikness.y)
        
        # Check if the wall exists in the list
        if tile in self.custom_walls:
            log.debug(f'Removing wall at {pos} - {tile}')
            self.custom_walls.remove(tile)

    def export(self, file_name: str) -> None:
        '''Export the current walls to a CSV file'''

        log.info(f'Exporting wall map with name {file_name} -> maps/{file_name}.csv')

        # Open the csv file
        with open(f'maps/{file_name}.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(('x','y')) # Write first row

            walls = [(int(v.x),int(v.y)) for v in self.custom_walls] # Clear walls (convert from float to int)
            csv_writer.writerows(walls)

    def render(self, display: pygame.surface.Surface):
        """Render the walls considering the surroundings"""

        # Reassign for better performances
        th = self.thikness

        # Draw the walls according to the four other walls in their surroundings
        for wall in (self.custom_walls + self.boarders):

            # Define surroundings
            pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8 = False, False, False, False, False, False, False, False
            for wall2 in (self.custom_walls + self.boarders):
                delta = wall - wall2

                if   delta == Vector2(0,1):  pc1 = True
                elif delta == Vector2(-1,0): pc2 = True
                elif delta == Vector2(0,-1): pc3 = True
                elif delta == Vector2(1,0):  pc4 = True

                elif delta == Vector2(1,1):  pc5 = True
                elif delta == Vector2(-1,1): pc6 = True
                elif delta == Vector2(-1,-1):pc7 = True
                elif delta == Vector2(1,-1): pc8 = True
            
            match [pc1,pc2,pc3,pc4,pc5,pc6,pc7,pc8]:
                case [False, False, False, False,     _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*0, th.y*0, th.x, th.y))
                case [True,  True,  True,  True,  False, False, False, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*0, th.y*1, th.x, th.y))
                case [True,  True,  True,  True,  True,  True,  True,  True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*0, th.y*2, th.x, th.y))

                case [False, True,  False, True,      _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*1, th.y*0, th.x, th.y))
                case [True,  False, True,  False,     _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*1, th.y*1, th.x, th.y))
                case [True,  True,  True,  True,  False, True,  False, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*1, th.y*2, th.x, th.y))
                case [True,  True,  True,  True,  True,  False, True,  False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*1, th.y*3, th.x, th.y))

                case [True,  True,  False, False,     _, False,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*2, th.y*0, th.x, th.y))
                case [False, True,  True,  False,     _,     _, False,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*2, th.y*1, th.x, th.y))
                case [False, False, True,  True,      _,     _,     _, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*2, th.y*2, th.x, th.y))
                case [True,  False, False, True,  False,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*2, th.y*3, th.x, th.y))

                case [False, False, True,  False,     _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*3, th.y*0, th.x, th.y))
                case [False, True,  False, False,     _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*3, th.y*1, th.x, th.y))
                case [True,  False, False, False,     _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*3, th.y*2, th.x, th.y))
                case [False, False, False, True,      _,     _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*3, th.y*3, th.x, th.y))

                case [False, True,  True,  True,      _,     _, False, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*4, th.y*0, th.x, th.y))
                case [True,  True,  True,  False,     _, False, False,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*4, th.y*1, th.x, th.y))
                case [True,  True,  False, True,  False, False,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*4, th.y*2, th.x, th.y))
                case [True,  False, True,  True,  False,     _,     _, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*4, th.y*3, th.x, th.y))

                case [True,  True,  False, False,     _, True,      _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*5, th.y*0, th.x, th.y))
                case [False, True,  True,  False,     _,     _, True,      _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*5, th.y*1, th.x, th.y))
                case [False, False, True,  True,      _,     _,     _, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*5, th.y*2, th.x, th.y))
                case [True,  False, False, True,  True,      _,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*5, th.y*3, th.x, th.y))

                case [True,  True,  True,  True,  True,      _, True,  True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*6, th.y*0, th.x, th.y))
                case [True,  True,  True,  True,  True,  True,      _, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*6, th.y*1, th.x, th.y))
                case [True,  True,  True,  True,  True,  True,  True,      _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*6, th.y*2, th.x, th.y))
                case [True,  True,  True,  True,  False, True,  True,  True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*6, th.y*3, th.x, th.y))

                case [False, True,  True,  True,      _,     _, True,  True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*7, th.y*0, th.x, th.y))
                case [True,  True,  True,  False,     _, True,  True,      _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*7, th.y*1, th.x, th.y))
                case [True,  True,  False, True,  True,  True,      _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*7, th.y*2, th.x, th.y))
                case [True,  False, True,  True,  True,      _,     _, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*7, th.y*3, th.x, th.y))

                case [True,  True,  True,  True,  True,  True,  False, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*8, th.y*0, th.x, th.y))
                case [True,  True,  True,  True,  True,  False, False, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*8, th.y*1, th.x, th.y))
                case [True,  True,  True,  True,  False, False, True,  True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*8, th.y*2, th.x, th.y))
                case [True,  True,  True,  True,  False, True,  True,  False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*8, th.y*3, th.x, th.y))

                case [True,  True,  True,  True,  False, False, False, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*9, th.y*0, th.x, th.y))
                case [True,  True,  True,  True,  True,  False, False, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*9, th.y*1, th.x, th.y))
                case [True,  True,  True,  True,  False, True,  False, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*9, th.y*2, th.x, th.y))
                case [True,  True,  True,  True,  False, False, True,  False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*9, th.y*3, th.x, th.y))

                case [False, True,  True,  True,      _,     _, False, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*10, th.y*0, th.x, th.y))
                case [True,  True,  True,  False,     _, False, True,      _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*10, th.y*1, th.x, th.y))
                case [True,  True,  False, True,  True,  False,     _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*10, th.y*2, th.x, th.y))
                case [True,  False, True,  True,  False,     _,     _, True ]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*10, th.y*3, th.x, th.y))

                case [False, True,  True,  True,      _,     _, True,  False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*11, th.y*0, th.x, th.y))
                case [True,  True,  True,  False,     _, True,  False,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*11, th.y*1, th.x, th.y))
                case [True,  True,  False, True,  False, True,      _,     _]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*11, th.y*2, th.x, th.y))
                case [True,  False, True,  True,  True,      _,     _, False]: display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*11, th.y*3, th.x, th.y))

                case _:
                    log.error(f'Wall without texture at {wall}')
                    display.blit(self.textures, (wall.x*th.x,wall.y*th.y), (th.x*0, th.y*3, th.x, th.y))

    @property
    def walls_absolute(self) -> list[Vector2]:
        '''Returns the absolute position of every wall'''

        # Initailize new list
        walls = []

        # Calcualte absolute positions based on the thikness
        th = self.thikness
        for wall in self.custom_walls:
            walls.append(Vector2(wall.x*th.x,wall.y*th.y))
        
        return walls
            

class Apple:
    def __init__(
            self,
            pos: Vector2,
            power: int,
            thikness: Vector2,
            texture: str = 'default.png',
        ) -> None:
        
        self.pos = pos
        self.power = power
        self.thikness = thikness

        log.debug(f'Loading food texture {texture}')
        # Load the textures and scale them to the right size
        self.texture = pygame.image.load('textures/food/'+texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, thikness)
    
    def render(self, display: pygame.surface.Surface):
        display.blit(self.texture, self.pos)