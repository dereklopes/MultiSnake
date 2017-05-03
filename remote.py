import socket
import sys, networking

player = networking.Player()

while 1:
    var = input("Enter: ")
    player.send_message(var)
