import pygame
from logger import logger as log

class Timer:
    def __init__(
            self,
            duration: int,
            starting: float = 0,
            paused: bool = False
        ) -> None:
        '''
        duration: duration of the timer
        starting: starting point of the timer
        paused: create paused timer when set to True
        '''

        self.duration = duration
        self.paused = paused

        self.time = starting
    
    def tick(self, delta_time: float) -> bool:
        if self.paused:
            return False
        
        self.time += delta_time

        if self.time > self.duration:
            self.time %= self.duration
            return True
    
    def pause(self): self.paused = True
    def resume(self): self.paused = False


class key_map:
    def __init__(self,up,down,left,right):
        log.debug(f'Initializing keybindings: {up}, {down}, {left}, {right}')

        self.up =    pygame.key.key_code(up)
        self.down =  pygame.key.key_code(down)
        self.left =  pygame.key.key_code(left)
        self.right = pygame.key.key_code(right)

        self.keys = [self.up,self.down,self.left,self.right]

    def __contains__(self, key) -> bool:
        return key in self.keys
