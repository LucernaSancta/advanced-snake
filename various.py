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

    def __contains__(self, key) -> bool:
        return True if key in self.keys else False
