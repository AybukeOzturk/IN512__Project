__author__ = "Aybuke Ozturk Suri, Johvany Gustave"
__copyright__ = "Copyright 2023, IN512, IPSA 2023"
__credits__ = ["Aybuke Ozturk Suri", "Johvany Gustave"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"


import socket, pickle
from threading import Thread, Lock
import sys, argparse, os
from game import Game
from my_constants import *
from time import sleep

if os.name == "nt": #If you are on Windows
    screen_resolution_to_fix = True  #Set this variable to True if you face resolution issues when the GUI appears
    if screen_resolution_to_fix:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Server:
    """ Server handling communication between the agents and the game """
    def __init__(self, conf, nb_agents, map_id):
        """ Initialize the server """
        self.game = Game(nb_agents, map_id)
        self.nb_disconnected = 0
        self.id_count = 0
        self.conf = conf
        self.nb_agents = nb_agents
        self.clients = []
        self.clients_lock = Lock()
        print(f"Server configuration: {conf}")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
        self.s.bind(conf)
        self.s.listen()
        self.start()


    def start(self):
        """ Start listening to incoming clients """
        print("Server ready! Waiting for connections...")
        while self.id_count < self.nb_agents:
            conn, addr = self.s.accept()
            with self.clients_lock:
                self.clients.append(conn)
            Thread(target=self.client_cb, daemon=True, args=(conn, addr, self.id_count)).start()
            self.id_count += 1
            sleep(0.1)
        self.game.gui.render()
    

    def client_cb(self, conn, addr, client_id):
        """ Handle the interactions with a client """
        print(f"Connected to {addr[0]} on port {addr[1]}")
        self.game.nb_ready += 1

        conn.send(pickle.dumps((client_id)))

        try:
            while True:
                msg = pickle.loads(conn.recv(1024))
                if msg["header"] == BROADCAST_MSG:
                    msg["sender"] = client_id
                    self.send_to_all(conn, msg)
                else:
                    reply = self.game.process(msg, client_id)
                    conn.send(pickle.dumps(reply))
        except Exception as e:
            pass
        finally:
            print(f"Closing connection with {addr[0]} on port {addr[1]}")
            with self.clients_lock:
                self.clients.remove(conn)
                conn.close()
                self.nb_disconnected += 1
                if self.nb_disconnected >= self.nb_agents:
                    self.game.gui.running = False
                    sys.exit()


    def send_to_all(self, sender, msg):
        """ Broadcast a msg to all clients except the 'sender' """
        with self.clients_lock:
            for client in self.clients:
                if client != sender:
                    client.send(pickle.dumps(msg))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip_server", help="Ip address of the server", type=str, default="localhost")
    parser.add_argument("-nb", "--nb_agents", help="Number of agents: 1, 2, 3 or 4", type=int, default=2)
    parser.add_argument("-mi", "--map_id", help="Map to load: 1 or 2", type=int, default=1)


    args = parser.parse_args()
    port = 5555

    if not args.nb_agents in range(1, 5):    #Game are only designed for 1 to 4 agents
        print("The number of agents should range between 1 and 4!")
        sys.exit()
    if not args.map_id in range(1, 3):    #There are only 2 maps
        print("There are only 2 maps!")
        sys.exit()
    server = Server((args.ip_server, port), args.nb_agents, args.map_id)