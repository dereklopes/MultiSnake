#####################################################################
#
#
#
#  SNAKER.py  - A simple SNAKE game written in Python and Pygame
#
#  This is my first Python / Pygame game written as a learning
#  exercise.
#
#
#  Version: 0.1
#  Date:  24 August 2008
#  Author:  R Brooks
#  Author email:  rsbrooks@gmail.com
#
#
#
#####################################################################

######### IMPORTS ###################################################

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

######### MAIN #####################################################

def main():

    #server = networking.Server()
    #server.accept_connection()

    showstartscreen = 1

    while 1:
        ######## CONSTANTS

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
        MAXX = 760
        MINX = 20
        MAXY = 560
        MINY = 80
        SNAKESTEP = 20
        TRUE = True
        FALSE = False

        ######## VARIABLES

        isHost = True
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
        #screen.fill(BLACK)

        #### show initial start screen

        if showstartscreen == TRUE:
            showstartscreen = FALSE

            s = [[180,120],[180,100],[160,100],[140,100],[120,100],[100,100],[100,120],[100,140],[100,160],
                 [120,160],[140,160],[160,160],[180,160],[180,180],[180,200],[180,220],[160,220],[140,220],
                 [120,220],[100,220],[100,200]]
            apple = [100,200]
            applexy = apple

            pygame.draw.rect(screen,GREEN,Rect(apple,BLOCKSIZE))
            pygame.display.flip()
            clock.tick(8)

            for e in s:
                pygame.draw.rect(screen,BLUE,Rect(e,BLOCKSIZE))
                pygame.display.flip()
                clock.tick(8)

            font = pygame.font.SysFont("arial", 64)
            text_surface = font.render("NAKE", True, BLUE)
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
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]: exit()
                elif pressed_keys[K_h]:
                    # host a new game
                    isHost = True
                    screen.fill(BLACK)
                    text_surface = font.render('Waiting for player to join', True, BLUE)
                    screen.blit(text_surface, (50, 300))
                    pygame.display.flip()
                    server = networking.Server()
                    server.accept_connection()
                    break
                elif pressed_keys[K_j]:
                    # join a new game
                    isHost = False
                    screen.fill(BLACK)
                    text_surface = font.render('Searching for host', True, BLUE)
                    screen.blit(text_surface, (50, 300))
                    pygame.display.flip()
                if not isHost:
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

            ###### get input events  ####

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()

            olddirection = direction
            if pressed_keys[K_LEFT] and olddirection is not RIGHT:
                direction = LEFT
            if pressed_keys[K_RIGHT] and olddirection is not LEFT:
                direction = RIGHT
            if pressed_keys[K_UP] and olddirection is not DOWN:
                direction = UP
            if pressed_keys[K_DOWN] and olddirection is not UP:
                direction = DOWN
            if pressed_keys[K_q]: snakedead = TRUE
            #if pressed_keys[K_p]: gamepaused = 1

            # If not the host, send input to the host
            if player is not None and direction != olddirection:
                player.send_message(direction)
            # Otherwise, get the direction sent
            elif server is not None and server.data is not None:
                direction2 = server.data

            ### wait here if p key is pressed until p key is pressed again

            while gamepaused == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_r]:
                    gamepaused = 0
                clock.tick(10)


            ### added gameregulator because setting a very low clock ticks
            ### caused the keyboard input to be hit and miss.  So I up the
            ### gameticks and the input and screen refresh is at this rate
            ### but the snake moving and all other logic is at the slower
            ### "regulated" speed


            if gameregulator == 6 and isHost:

                ##### now lets move the snake according to the direction
                ##### if we hit the wall the snake dies
                ##### need to make it less twitchy when you hit the walls

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

                # Apply direction to snake 2
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

                ### is the snake crossing over itself
                ### had to put the > 1 test in there as I was
                ### initially matching on first pass otherwise - not sure why

                if len(snakelist) > 3 and snakelist.count(snakexy) > 0:
                    snakedead = TRUE
                elif len(snakelist2) > 3 and snakelist2.count(snakexy2) > 0:
                    snakedead2 = TRUE



                #### generate an apple at a random position if one is not on screen
                #### make sure apple never appears in snake position

                if appleonscreen == 0:
                    good = FALSE
                    while good == FALSE:
                        x = random.randrange(1,39)
                        y = random.randrange(5,29)
                        applexy = [int(x*SNAKESTEP),int(y*SNAKESTEP)]
                        if snakelist.count(applexy) == 0:
                            good = TRUE
                    appleonscreen = 1

                #### add new position of snake head
                #### if we have eaten the apple don't pop the tail ( grow the snake )
                #### if we have not eaten an apple then pop the tail ( snake same size )

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

                # check if snake 2 has eaten apple
                # TODO: Score for snake2 for snake2
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

            if not isHost:
                if player.data is None:
                    gameInfo = GameInfo(score, score2, snakelist, snakelist2, applexy, snakedead, snakedead2)
                else:
                    gameInfo = pickle.loads(player.data)

            ###### RENDER THE SCREEN ###############

            ###### Clear the screen
            screen.fill(BLACK)

            ###### Draw the screen borders
            ### horizontals
            pygame.draw.line(screen,GREEN,(0,9),(799,9),20)
            pygame.draw.line(screen,GREEN,(0,590),(799,590),20)
            pygame.draw.line(screen,GREEN,(0,69),(799,69),20)
            ### verticals
            pygame.draw.line(screen,GREEN,(9,0),(9,599),20)
            pygame.draw.line(screen,GREEN,(789,0),(789,599),20)

            ###### Print the score
            font = pygame.font.SysFont("arial", 38)
            if isHost:
                text_surface = font.render("SNAKE!     Your Score: " + str(gameInfo.score), True, RED)
            else:
                text_surface = text_surface = font.render("SNAKE!     Your Score: " + str(gameInfo.score2), True, BLUE)
            screen.blit(text_surface, (50,18))

            ###### Output the array elements to the screen as rectangles ( the snake)
            for element in gameInfo.snakelist:
                pygame.draw.rect(screen,RED,Rect(element,BLOCKSIZE))
            for element in gameInfo.snakelist2:
                pygame.draw.rect(screen,BLUE,Rect(element,BLOCKSIZE))

            ###### Draw the apple
            pygame.draw.rect(screen,GREEN,Rect(gameInfo.apple,BLOCKSIZE))

            ###### Flip the screen to display everything we just changed
            pygame.display.flip()



            gameregulator = gameregulator + 1

            clock.tick(25)


        ##### if the snake is dead then it's game over

        if gameInfo.snakedead and gameInfo.snakedead2:
            if isHost:
                # send final info so client knows game is over
                gameInfo = GameInfo(score, score2, snakelist, snakelist2, applexy, snakedead, snakedead2)
                gameInfoString = pickle.dumps(gameInfo)
                server.send_data(gameInfoString)
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
                        exit()

                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_q]:
                    exit()
                if pressed_keys[K_m]:
                    showstartscreen = True
                    break

                clock.tick(10)

if __name__ == '__main__':
    main()
