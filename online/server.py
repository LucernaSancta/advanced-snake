import time
import socket, threading, pickle
from main import Game
from menus.menu_components import Menu
from logger import logger as log


class CustomGame(Game):
    def game_quit(self, menu: Menu = None):
        if menu is not None:
            menu.quit()

        self.running = False

    def pause(self) -> None:

        log.info('Game paused')

        # Initialize pause menu
        menu = Menu(
            screen_size=self.screen_size,
            font_path='menu_assets/font.ttf',
            font_size=32,    
            inherit_screen=self.display
        )

        # Define buttun costants
        b_th = (400, 60) # Button dimensions
        delta_height = 35

        # Define buttons
        options = [
            ['resume',    'RESUME',    menu.quit,                    b_th, [menu.center.x, menu.center.y - delta_height]],
            ['quit',      'QUIT',      lambda: self.game_quit(menu), b_th, [menu.center.x, menu.center.y + delta_height]]
        ]

        # Add buttons to menu
        for option in options:
            menu.add_option(*option)

        log.debug('Running menu')
        menu.run()

        # Make sure the games running so that the screen can update and remove the pause menu
        self.paused = False
        log.info('Game resumed')


def get_local_ip():
    '''Returns the IP of the machine in the LAN'''
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable — we just want to get the right interface
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        # Use loopback IP (localhost)
        IP = '127.0.0.1'
    finally:
        s.close()

    return IP


class GameServer:
    def __init__(self, port=7373) -> None:

        log.name = 'server' # Set the logger name

        # Create socket
        ip = get_local_ip()
        log.info(f'Creating socket binded to {ip}:{port}')
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.settimeout(0.2) # timeout for listening
            self.server.bind((ip, port))
            self.server.listen()
        except Exception as e:
            log.critical(f'Could not create socket: {e}')
            exit()

        self.clients = []
        self.inputs = []
        self.running = True

        # Init game
        self.game = CustomGame()
        self.game.custom_method = self.custom_method
        
        self.lock = threading.Lock()

    def custom_method(self) -> None:

            self.broadcast_state()

            # Update the snakes
            with self.lock:
                for key_event in self.inputs:
                    for snake in self.game.snakes:
                        if key_event in snake.keybindings:
                            snake.move(key_event)
                # Resent inputs buffer
                self.inputs.clear()

    def broadcast_state(self) -> None:

        # Get game state
        game_state = pickle.dumps(self.serialize_state())

        # Send state to all connected clients
        for client, addr in self.clients:
            try:
                client.sendall(game_state)
            except Exception:
                log.warning(f'Client {addr} disconnected')
                self.clients.remove((client, addr))

    def serialize_state(self) -> dict:
        return {
            'snakes': [(s.name, s.pos, s.direction, s.pieces) for s in self.game.snakes],
            'foods': [(f.pos, type(f).__name__, f.kwargs) for f in self.game.foods]
        }

    def handle_client(self, conn, addr) -> None:
        while self.running:
            try:
                # Recive data
                data = conn.recv(1024)
                if not data: break
                key_event = pickle.loads(data)

                # Add data to inputs buffer
                with self.lock:
                    self.inputs.append(key_event)
            except:
                break
        
        # Client disconnected
        log.warning(f'Client {addr} disconnected')
        conn.close()

    def accept_clients(self) -> None:
        while self.running:

            try:
                conn, addr = self.server.accept()
            except TimeoutError:
                continue

            log.warning(f'Client connected from {addr}')

            # Sent config
            log.debug(f'Sending configuration to {addr}')
            self.send_config(conn, addr)

            self.clients.append((conn, addr))

            # Start client handling thread
            threading.Thread(target=self.handle_client, args=(conn, addr,)).start()
    
    def send_config(self, conn, addr) -> None:

        # Get game config
        config = pickle.dumps(self.game.config)

        # Send config
        try:
            conn.send(config)
        except Exception:
            log.warning(f'Client {addr} disconnected')

    def run(self) -> None:
        log.info('Server started')
        threading.Thread(target=self.accept_clients).start()
        self.game.run()

        # Stop threads
        log.debug('Stopping threads')
        self.running = False
        time.sleep(.3) # Let the threads stop

        # Close socket
        log.debug('Closing server socket')
        self.server.close()

        log.info('Server closed')
        
        exit()


if __name__ == '__main__':
    GameServer().run()