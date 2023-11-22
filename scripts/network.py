__author__ = "Aybuke Ozturk Suri, Johvany Gustave"
__copyright__ = "Copyright 2023, IN512, IPSA 2023"
__credits__ = ["Aybuke Ozturk Suri", "Johvany Gustave"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"

import socket, pickle


class Network:
    """ Class that is used by the agent to communicate with the server """
    def __init__(self, server_ip="localhost"):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conf = (server_ip, 5555)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.conf)
            return pickle.loads(self.client.recv(1024))
        except Exception as e:
            raise
    
    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
        except Exception as e:
            print(e)
    
    def receive(self):
        return pickle.loads(self.client.recv(1024))