import pygame
import socket
import threading
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-u', required=True)
args = parser.parse_args()

username = args.u

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 6565))

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GREEN = (50, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("{name}'s game".format(name=username))
client.send(username.encode('utf-8'))

local_player = pygame.Rect((300, 250, 50, 50))
players = {} #key = username, value = coordinates
players[username] = local_player

def client_recv():
    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)
        op, rem = message.split(',', 1)
        match op:
            case "update":
                 # the message will contain the updated coordinates of a player
                new_username, x, y = rem.split(',', 2)

                if new_username == username:
                    continue
                
                x = int(x)
                y = int(y)
                player = players[new_username]
                player.update(x, y, player.width, player.height)
            case "new_player":
                players[rem] = pygame.Rect((300, 250, 50, 50))
            case "connection":
                print("Successfully connected to server and created client thread")
                print("Welcome to the game {name}!".format(name=username))
            case "player_state":
                # i_username = incoming username
                i_username, x, y = rem.split(',', 2)
                players[i_username] = pygame.Rect((int(x), int(y), 50, 50))

recv_thread = threading.Thread(target=client_recv)
recv_thread.start() 

def draw_window():
    screen.fill(GREEN)
    for player in players:
        pygame.draw.rect(screen, RED, players[player])
    pygame.display.update()
    
def main():
    coords_changed = False
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        draw_window()

        key = pygame.key.get_pressed()
    
        if key[pygame.K_a]:
            if local_player.left != 0:
                local_player.move_ip(-1, 0) #move in place
                coords_changed = True
        elif key[pygame.K_d]:
            if local_player.right != SCREEN_WIDTH:
                local_player.move_ip(1, 0)
                coords_changed = True
        elif key[pygame.K_w]:
            if local_player.top != 0:
                local_player.move_ip(0, -1)
                coords_changed = True
        elif key[pygame.K_s]:
            if local_player.bottom != SCREEN_HEIGHT:
                local_player.move_ip(0, 1)
                coords_changed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if coords_changed:
            client.send("update,{usn},{x},{y}".format(usn=username, x=local_player.left, y=local_player.top).encode('utf-8'))
            time.sleep(0.01)
            coords_changed = False
        
    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()
