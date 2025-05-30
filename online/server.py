import socket, threading, pickle
from main import Game


class GameServer:
    def __init__(self, host='localhost', port=7373):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

        self.clients = []
        self.inputs = []

        self.game = Game()
        self.game.custom_method = self.custom_method
        
        self.lock = threading.Lock()

    def custom_method(self):

            self.broadcast_state()

            with self.lock:
                for key_event in self.inputs:
                    for snake in self.game.snakes:
                        if key_event in snake.keybindings:
                            snake.move(key_event)
                self.inputs.clear()

    def broadcast_state(self):
        game_state = pickle.dumps(self.serialize_state())
        for client, addr in self.clients:
            try:
                client.sendall(game_state)
            except Exception:
                print(f'Client {addr} disconnected')
                self.clients.remove((client, addr))

    def serialize_state(self):
        return {
            'snakes': [(s.name, s.pos, s.direction, s.pieces) for s in self.game.snakes],
            'foods': [(f.pos, type(f).__name__, f.kwargs) for f in self.game.foods]
        }

    def handle_client(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
                key_event = pickle.loads(data)
                with self.lock:
                    self.inputs.append(key_event)
            except:
                break
        print(f'Client {addr} disconnected')
        conn.close()

    def accept_clients(self):
        while True:
            conn, addr = self.server.accept()
            print(f"Client connected from {addr}")
            self.send_config(conn, addr)
            self.clients.append((conn, addr))
            threading.Thread(target=self.handle_client, args=(conn, addr,)).start()
    
    def send_config(self, conn, addr):
        config = pickle.dumps(self.game.config)
        try:
            conn.send(config)
        except Exception:
            print(f'Client {addr} disconnected')

    def run(self):
        print("Server started")
        threading.Thread(target=self.accept_clients).start()
        self.game.run()

        print("Server closed")
        self.server.close()


if __name__ == '__main__':
    GameServer().run()