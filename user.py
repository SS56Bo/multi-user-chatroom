import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.username = None

    def send_message(self, message):
        self.client.send(message.encode('ascii'))

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def login(self, username):
        self.username = username
        self.send_message(f"LOGIN:{username}")

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5555

    username = input("Enter your username: ")

    chat_client = ChatClient(host, port)
    chat_client.login(username)

    receive_thread = threading.Thread(target=chat_client.receive_messages)
    receive_thread.start()

    while True:
        message = input("")
        chat_client.send_message(message)
