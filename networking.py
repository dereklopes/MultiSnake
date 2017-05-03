import socket, sys, threading

class Client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print("Client sent:", self.sock.recv(1024).decode())
            self.sock.send(b'ACK')

class Server(object):
    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', 8080))
        self.listener.listen(1)

    def accept_connection(self):
        socket, info = self.listener.accept()
        connection = Connection(socket, info)
        thread = threading.Thread(target=self.process_connection, args=(connection,))
        thread.start()

    def process_connection(self, connection):
        print("[INFO] New user connected from {}".format(connection.ip))
        data = connection.recv_from_client()
        print("[INFO] User from {} now logged at {}".format(connection.ip))

class Connection():
    def __init__(self, socket, info=None):
        self.socket = socket
        if info:
            self.ip = info[0]
            self.port = info[1]

    def connect_to_server(self, ip, port):
        self.socket.connect((ip, port))

    def send_to_server(self, msg):
        self.socket.send(msg.encode())

    def recv_from_client(self):
        return self.socket.recv(1024).decode()

class Player():
    def __init__(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = Connection(connection)
        self.connection.connect_to_server("localhost", 8080)

    def send_message(self, msg):
        self.connection.send_to_server(msg)