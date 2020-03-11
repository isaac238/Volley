import socket
from _thread import *
from player import Player
import pickle

server = str(socket.gethostbyname(socket.gethostname()))
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
white = (255, 255, 255)
black = (0, 0, 0)
grey = (111, 111, 111)
players = [Player(5, 0, 10, 75, white, 0), Player(625, 0, 10, 75, grey, 0)]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    conn.close()


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1