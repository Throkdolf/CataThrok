import socket
import time
import threading
from user import User

#upon joining the new player needs all of the currently joined players coordinates
#fix new players appearing as massive rectangles instead of the fixed sized ones

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #should change to SOCK_DGRAM for UDP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 6565))
server.listen()
print("Starting up socket and listening")

users = {}

def receive():
    while True:
        client, _ = server.accept()
        username = client.recv(1024).decode('utf-8')
        new_user = User(username, client, 300, 250)
        client.send("connection,True".encode('utf-8'))
        time.sleep(1)
        broadcast("new_player,{username}".format(username=username))
        for user in users:
            client.send("player_state,{username},{x},{y}".format(username=users[user].getUsername, x=users[user].getX, y=users[user].getY).encode('utf-8'))
        users[client] = new_user
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def handle_client(client):
    while True:
        # continue
        message = client.recv(1024).decode('utf-8')
        print(message)
        if 'update' in message:
            _, _, x, y = message.split(',', 3)
            users[client].setX(int(x))
            users[client].setY(int(y))
            broadcast(message)
            # if the message is updated coordinates broadcast updated coordinates to all other users

def broadcast(message):
    for user in users:
        user.send(message.encode('utf-8'))

try:
    receive()
except KeyboardInterrupt:
    print("Shutting Down Server")
finally:
    server.close()
    for user in users:
        user.close()
        

