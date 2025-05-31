import socket, threading, pickle
import pygame
from main import Game
from logger import logger as log


log.name = 'game' # Set the logger name


class CustomGame(Game):
    def check_win_condition(self, *args, **kwargs): return
    def manage_events(self, *args, **kwargs): return
    def update_snake(self, *args, **kwargs): return
    def food_spawner(self, *args, **kwargs): return


class GameClient:
    def __init__(self, host='localhost', port=7373) -> None:

        # Create socket and connect to the server
        log.info(f'Creating socket and connecting to {host}:{port}')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.state = {}

        # Create custom game
        self.game = CustomGame
        self.game.load_configs_file = self.custom_config
        self.game.custom_method = self.render_and_send

        # Set all snakes states to 1 (if set to 0 they wont render properly)
        self.game = self.game()
        for snake in self.game.snakes:
            snake.state = 1
    
    def custom_config(self, _) -> dict:
        '''Recive configuration'''

        log.debug('Reciving configuration...')

        data = b''
        while True:
            part = self.socket.recv(4096)
            if not part:
                break
            data += part
            if len(part) < 4096:
                break

        return pickle.loads(data)

    def send_input(self, key) -> None:
        try:
            self.socket.sendall(pickle.dumps(key))
        except Exception:
            # Server disconnected
            log.critical("Lost connection to server")
            exit()

    def receive_state(self) -> None:
        while True:
            try:
                # Recive state
                data = b''
                while True:
                    part = self.socket.recv(4096)
                    if not part:
                        break
                    data += part
                    if len(part) < 4096:
                        break
                
                # Load recived state
                self.state = pickle.loads(data)

            except:
                break

    def run(self) -> None:
        log.info('Starting client')
        threading.Thread(target=self.receive_state, daemon=True).start()
        self.game.run()

    def render_and_send(self) -> None:

        # Sent keys events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self.send_input(event.key)

        # First frames...
        if not self.state: return
        
        # Remove snakes that are not in the sent list
        for snake in self.game.snakes[:]:
            if snake.name not in [sn[0] for sn in self.state['snakes']]:
                self.game.snakes.remove(snake)

        # Update snakes
        for name, pos, direction, pieces in self.state['snakes']:
            for snake in self.game.snakes:
                if snake.name == name:
                    snake.pos = pos
                    snake.pieces = pieces
                    snake.direction = direction

        # Remove old foods
        foods_pos = [food[0] for food in self.state['foods']]
        for food in self.game.foods[:]:
            if food.pos not in foods_pos:
                self.game.foods.remove(food)

        # Add new foods
        foods_pos_current = [food.pos for food in self.game.foods]
        for food in foods_pos:

            # Check if its a new food
            if food not in foods_pos_current:

                # Get all sent foods
                for food_pos, food_type, food_kwargs in self.state['foods']:
                    
                    if food_pos == food:

                        # Get new food class
                        for food in self.game.foods_types:
                            if food.__name__ == food_type:
                                food_to_spawn = food
                                break

                        # Spawn new food
                        log.debug(f'Adding new food: {food_to_spawn} at {food_pos}')
                        food = food_to_spawn(food_pos, self.game.snake_grid_thikness, food_kwargs)
                        self.game.foods.append(food)


if __name__ == '__main__':
    GameClient().run()