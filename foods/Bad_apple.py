from .default import Food
from game_objects import Snake

class Bad_apple(Food):
    def initialize(self) -> None:
        self.damage = self.kwargs['damage']
        self.init_texture('bad_apple.png')

    def eaten(self, surface, snake: Snake, snakes: list[Snake]) -> None:
        for _ in range(self.damage):
            if len(snake.pieces) > 1:
                snake.pieces.pop()
            else:
                snake.state = 2
                snake.kill()
                break