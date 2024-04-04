import socket, threading

class Server:
    def __init__(self, data):
        print('SERVER')
        self.HOST, self.PORT, self.name = data
        self.type = None
        self.client = None
        self.start_server()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        print(self.HOST)
        print("Waiting for Client...")
        self.server.listen(5)
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def stop_server(self):
        self.server.close()

    def accept_clients(self):
        while True:
            if not self.client:
                self.conn, addr = self.server.accept()
                self.client_name = self.conn.recv(4096).decode()
                self.conn.send(self.name.encode())
                print(self.client_name)
                threading.Thread(target=self.get_types, daemon=True).start()

    def get_types(self):
        while not self.type:
            pass
        print(self.type, self.types)
        self.conn.send(self.types[int(not bool(self.types.index(self.type)))].encode())
