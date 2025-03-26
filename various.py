from boarders import Walls

class colors:
    bg = ''
    apples = ''
    snake_default = ''
    walls_default = ''

class key_map:
    def __init__(self,up,down,left,right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        self.keys = [up,down,left,right]

def apple_spawner(snakes: list, walls: Walls):
    def __init__(self):
        pass