class colors:
    bg = ''
    apples = ''
    snake_default = ''
    tails_default = ''

class key_map:
    def __init__(self,up,down,left,right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        self.keys = [up,down,left,right]