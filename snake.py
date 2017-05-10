#####################################################################
#
#
#
#  MultiSake - A networked snake game using Pygame
#
#
#  Authors: Derek Lopes, John Moon, Pierre Vachon, Manzoor Ahmed
#
#
#
#####################################################################

import sys, socket, random, math, pygame, networking, pickle
from pygame.locals import *

counter = 0

class GameInfo(object):
    def __init__(self, score, score2, snakelist, snakelist2, apple, snakedead, snakedead2):
        self.score = score
        self.score2 = score2
        self.snakelist = snakelist
        self.snakelist2 = snakelist2
        self.apple = apple
        self.snakedead = snakedead
        self.snakedead2 = snakedead2

# Constants
WINSIZE = [800,600]
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
BLOCKSIZE = [20,20]
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEFT = 'LEFT'
PAUSE = 'PAUSE'
RESUME = 'RESUME'
MAXX = 760
MINX = 20
MAXY = 560
MINY = 80
SNAKESTEP = 20
TRUE = True
FALSE = False

def main():

    showstartscreen = True

    while 1:

        is_host = True
        server = None
        player = None

        direction = RIGHT
        direction2 = RIGHT
        snakexy = [300,400]
        snakelist = [[300,400],[280,400],[260,400]]
        snakexy2 = [600, 400]
        snakelist2 = [[600, 400], [580, 400], [560, 400]]
        counter = 0
        score = 0
        score2 = 0
        appleonscreen = 0
        applexy = [0,0]
        snakedead = FALSE
        snakedead2 = FALSE
        gameregulator = 6
        gamepaused = 0
        growsnake = 0  # added to grow tail by two each time
        snakegrowunit = 2 # added to grow tail by two each time

        gameInfo = GameInfo(score, score2, snakelist, snakelist2, applexy, snakedead, snakedead2)

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('MultiSnake')

        # show initial start screen

        if showstartscreen == TRUE:
            showstartscreen = FALSE

            font = pygame.font.SysFont("arial", 64)
            text_surface = font.render("SNAKE", True, BLUE)
            screen.blit(text_surface, (220,180))
            font = pygame.font.SysFont("arial", 24)
            text_surface = font.render("Move the snake with the arrow keys to eat the apples", True, BLUE)
            screen.blit(text_surface, (50,300))
            text_surface = font.render("Avoid the walls and yourself !", True, BLUE)
            screen.blit(text_surface, (50,350))
            text_surface = font.render("Press h to host a new game - Press j to join a new game", True, BLUE)
            screen.blit(text_surface, (50,400))
            text_surface = font.render("Press p to pause r to resume at any time", True, BLUE)
            screen.blit(text_surface, (50,450))
            text_surface = font.render('Press q to quit at any time', True, BLUE)
            screen.blit(text_surface, (50, 500))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if player is not None:
                            player.close_connection()
                            snakedead2 = True
                        if server is not None:
                            server.close_connection()
                            snakedead = True
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]:
                        if player is not None:
                            player.close_connection()
                            snakedead2 = True
                        if server is not None:
                            snakedead = True
                            server.close_connection()
                        exit()
                elif pressed_keys[K_h]:
                    # host a new game
                    is_host = True
                    screen.fill(BLACK)
                    text_surface = font.render('Waiting for player to join', True, BLUE)
                    screen.blit(text_surface, (50, 300))
                    pygame.display.flip()
                    server = networking.Server()
                    server.accept_connection()
                    break
                elif pressed_keys[K_j]:
                    # join a new game
                    is_host = False
                    screen.fill(BLACK)
                    text_surface = font.render('Searching for host', True, BLUE)
                    screen.blit(text_surface, (50, 300))
                    pygame.display.flip()
                if not is_host:
                    # connect to host and listen for data
                    try:
                        player = networking.Player()
                        player.process_connection()
                        break
                    except:
                        print('No host found')
                        pass

                clock.tick(10)

        while not gameInfo.snakedead or not gameInfo.snakedead2:

            # get input events from pygame

            for event in pygame.event.get():
                if event.type == QUIT:
                    if player is not None:
                        player.close_connection()
                        snakedead2 = True
                    if server is not None:
                        server.close_connection()
                        snakedead = True
                    exit()

            pressed_keys = pygame.key.get_pressed()

            olddirection = direction
            olddirection2 = direction2
            if pressed_keys[K_LEFT] and olddirection is not RIGHT:
                direction = LEFT
            if pressed_keys[K_RIGHT] and olddirection is not LEFT:
                direction = RIGHT
            if pressed_keys[K_UP] and olddirection is not DOWN:
                direction = UP
            if pressed_keys[K_DOWN] and olddirection is not UP:
                direction = DOWN
            if pressed_keys[K_p]:
                direction = PAUSE
                gamepaused = 1
            if pressed_keys[K_q]: snakedead = TRUE

            # If not the host, send input to the host
            if player is not None and direction != olddirection:
                player.send_message(direction)
            # Otherwise, get the direction sent
            elif server is not None and server.data is not None:
                direction2 = server.data
                if direction2 == PAUSE:
                    gamepaused = 1
                    direction2 = olddirection2

            if direction == PAUSE:
                    direction = olddirection
                    directoin2 = olddirection2

            # wait here if p key is pressed until r key is pressed
            while gamepaused == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if player is not None:
                            player.close_connection()
                            snakedead2 = True
                        if server is not None:
                            server.close_connection()
                            snakedead = True
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if player is not None:
                    if pressed_keys[K_r]:
                        player.send_message(RESUME)
                if server is not None and server.data is not None:
                    if server.data == RESUME:
                        gamepaused = 0
                        direction2 = olddirection2
                if pressed_keys[K_r]:
                    gamepaused = 0
                clock.tick(10)

            # game regulator allows for checking snake separately from other game functions
            if gameregulator == 6 and is_host:

                # move the snake and check for collision
                if not snakedead:
                    if direction == RIGHT:
                        snakexy[0] = snakexy[0] + SNAKESTEP
                        if snakexy[0] > MAXX:
                            snakedead = TRUE

                    elif direction == LEFT:
                        snakexy[0] = snakexy[0] - SNAKESTEP
                        if snakexy[0] < MINX:
                            snakedead = TRUE

                    elif direction == UP:
                        snakexy[1] = snakexy[1] - SNAKESTEP
                        if snakexy[1] < MINY:
                            snakedead = TRUE

                    elif direction == DOWN:
                        snakexy[1] = snakexy[1] + SNAKESTEP
                        if snakexy[1] > MAXY:
                            snakedead = TRUE

                # Also for snake 2
                if not snakedead2:
                    if direction2 == RIGHT:
                        snakexy2[0] = snakexy2[0] + SNAKESTEP
                        if snakexy2[0] > MAXX:
                            snakedead2 = TRUE

                    elif direction2 == LEFT:
                        snakexy2[0] = snakexy2[0] - SNAKESTEP
                        if snakexy2[0] < MINX:
                            snakedead2 = TRUE

                    elif direction2 == UP:
                        snakexy2[1] = snakexy2[1] - SNAKESTEP
                        if snakexy2[1] < MINY:
                            snakedead2 = TRUE

                    elif direction2 == DOWN:
                        snakexy2[1] = snakexy2[1] + SNAKESTEP
                        if snakexy2[1] > MAXY:
                            snakedead2 = TRUE

                # check if snake collides with itself
                if len(snakelist) > 3 and snakelist.count(snakexy) > 0:
                    snakedead = TRUE
                elif len(snakelist2) > 3 and snakelist2.count(snakexy2) > 0:
                    snakedead2 = TRUE

                # check if snake collides with other snake - both die
                if any(point in snakelist for point in snakelist2):
                    snakedead = TRUE
                    snakedead2 = TRUE

                # generate an apple at a random position that is not occupied by a snake
                if appleonscreen == 0:
                    good = FALSE
                    while good == FALSE:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        applexy = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        if snakelist.count(applexy) == 0:
                            good = TRUE
                    appleonscreen = 1

                # grow the snake, discard if it hasn't eaten an apple
                snakelist.insert(0,list(snakexy))
                if snakexy[0] == applexy[0] and snakexy[1] == applexy[1]:
                    appleonscreen = 0
                    score = score + 1
                    growsnake = growsnake + 1
                elif growsnake > 0:
                    growsnake = growsnake + 1
                    if growsnake == snakegrowunit:
                        growsnake = 0
                else:
                    snakelist.pop()

                # check for snake2
                snakelist2.insert(0, list(snakexy2))
                if snakexy2[0] == applexy[0] and snakexy2[1] == applexy[1]:
                    appleonscreen = 0
                    score2 = score2 + 1
                    growsnake = growsnake + 1
                elif growsnake > 0:
                    growsnake = growsnake + 1
                    if growsnake == snakegrowunit:
                        growsnake = 0
                else:
                    snakelist2.pop()

                # set game info object and send to client
                gameInfo = GameInfo(score, score2, snakelist, snakelist2, applexy, snakedead, snakedead2)
                gameInfoString = pickle.dumps(gameInfo)
                server.send_data(gameInfoString)


                gameregulator = 0

            if not is_host:
                if player.data is None:
                    gameInfo = GameInfo(score, score2, snakelist, snakelist2, applexy, snakedead, snakedead2)
                else:
                    gameInfo = pickle.loads(player.data)

            # Render the screen

            # clear screen first
            screen.fill(BLACK)

            # Draw borders
            # horizontals
            pygame.draw.line(screen,GREEN,(0,9),(799,9),20)
            pygame.draw.line(screen,GREEN,(0,590),(799,590),20)
            pygame.draw.line(screen,GREEN,(0,69),(799,69),20)
            # verticals
            pygame.draw.line(screen,GREEN,(9,0),(9,599),20)
            pygame.draw.line(screen,GREEN,(789,0),(789,599),20)

            # Print the score depending on player
            font = pygame.font.SysFont("arial", 38)
            if is_host:
                text_surface = font.render("SNAKE!     Your Score: " + str(gameInfo.score), True, RED)
            else:
                text_surface = text_surface = font.render("SNAKE!     Your Score: " + str(gameInfo.score2), True, BLUE)
            screen.blit(text_surface, (50,18))

            # Draw the snakes
            for element in gameInfo.snakelist:
                pygame.draw.rect(screen,RED,Rect(element,BLOCKSIZE))
            for element in gameInfo.snakelist2:
                pygame.draw.rect(screen,BLUE,Rect(element,BLOCKSIZE))

            # Draw the apple
            pygame.draw.rect(screen,GREEN,Rect(gameInfo.apple,BLOCKSIZE))

            # Flip the screen to display everything
            pygame.display.flip()

            gameregulator = gameregulator + 1

            clock.tick(25)


        # if both snakes are dead, display game over

        if gameInfo.snakedead and gameInfo.snakedead2:
            screen.fill(BLACK)
            font = pygame.font.SysFont("arial", 48)
            if gameInfo.score > gameInfo.score2:
                text_surface = font.render("Player1 Wins", True, GREEN)
            elif gameInfo.score < gameInfo.score2:
                text_surface = font.render("Player2 Wins", True, GREEN)
            else:
                text_surface = font.render("TIE!", True, GREEN)
            screen.blit(text_surface, (250,200))
            text_surface = font.render("Player1 Score: " + str(gameInfo.score), True, RED)
            screen.blit(text_surface, (50,300))
            text_surface = font.render("Player2 Score: " + str(gameInfo.score2), True, BLUE)
            screen.blit(text_surface, (400, 300))
            font = pygame.font.SysFont("arial", 24)
            text_surface = font.render("Press q to quit", True, GREEN)
            screen.blit(text_surface, (300,400))
            text_surface = font.render("Press m to return to menu", True, GREEN)
            screen.blit(text_surface, (275,450))

            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        if player is not None:
                            player.close_connection()
                            snakedead2 = True
                        if server is not None:
                            server.close_connection()
                            snakedead = True
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]:
                    if player is not None:
                        player.close_connection()
                        snakedead2 = True
                    if server is not None:
                        server.close_connection()
                        snakedead = True
                    exit()
                if pressed_keys[K_m]:
                    showstartscreen = True
                    break

                clock.tick(10)

if __name__ == '__main__':
    main()
