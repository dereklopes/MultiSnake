import socket, sys, networking, pygame
from pygame.locals import *

player = networking.Player()

pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('MultiSnake')
screen.fill([0, 0, 0])

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                player.send_message("LEFT")
            if pressed_keys[pygame.K_RIGHT]:
                player.send_message("RIGHT")
            if pressed_keys[pygame.K_UP]:
                player.send_message("UP")
            if pressed_keys[pygame.K_DOWN]:
                player.send_message("DOWN")
