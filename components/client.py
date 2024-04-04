import socket


class Client:
    def __init__(self, data, logic):
        print('CLIENT')
        self.HOST, self.PORT, self.name = data
        self.level = None
        self.logic = logic
        self.connect_to_server()

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        self.client.send(self.name.encode())
        self.server_name = self.client.recv(4096).decode()
        self.type = self.client.recv(4096).decode()
        self.logic.type = self.type
        self.level = self.client.recv(4096).decode()
        self.logic.level = self.level
        print(self.server_name, self.level, self.type)


'''
class A:
    def __init__(self):
        self.a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


obj = A()
b = obj.a
b[1][1] = 101
print(obj.a, b)
'''
