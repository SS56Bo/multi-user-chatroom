import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.clients = []
        self.usernames = {}

    def broadcast(self, message, sender=None):
        for client_socket, username in self.clients:
            if client_socket != sender:
                client_socket.send(message)

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('ascii')
                if message.startswith('LOGIN'):
                    username = message.split(':')[1]
                    self.usernames[client_socket] = username
                    self.broadcast(f"{username} joined the chat!\n".encode('ascii'))
                else:
                    username = self.usernames.get(client_socket)
                    print(f"{username}: {message}")
                    self.broadcast(f"{username}: {message}".encode('ascii'), client_socket)
            except:
                if client_socket in self.usernames:
                    username = self.usernames[client_socket]
                    self.broadcast(f"{username} left the chat!\n".encode('ascii'))
                self.clients.remove((client_socket, self.usernames.get(client_socket)))
                break

    def start(self):
        self.server.listen()
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server.accept()
            print(f"New connection from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()
            self.clients.append((client_socket, None))

if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.start()
