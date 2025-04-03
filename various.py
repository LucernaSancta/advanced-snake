import pygame

class key_map:
    def __init__(self,up,down,left,right):
        self.up =    pygame.key.key_code(up)    if type(up)    != int else up
        self.down =  pygame.key.key_code(down)  if type(down)  != int else down
        self.left =  pygame.key.key_code(left)  if type(left)  != int else left
        self.right = pygame.key.key_code(right) if type(right) != int else right

        self.keys = [self.up,self.down,self.left,self.right]
        print(*self.keys)
    def __contains__(self, key) -> bool:
        return key in self.keys
