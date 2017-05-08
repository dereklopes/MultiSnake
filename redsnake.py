
import random

class Snake (object):

    """docstring for Snake """

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def head(self):

        rand_row = random.randint(0,self.row -1 )
        rand_col = random.randint(0,self.col -1 )
        self.body = {'row': [rand_row] , 'col': [rand_col]}

    def moveLeft(self):

        #body's head points
        point_row = self.body.get('row')[len(self.body.get('row')) -1 ]
        point_col = self.body.get('col')[len(self.body.get('col')) -1 ]

        point_col = point_col - 1

        #add new head points
        self.body.get('col').append(point_col)
        self.body.get('row').append(point_row)

        #remove the tail
        self.body.get('row').pop(0)
        self.body.get('col').pop(0)

    def moveRight(self):

        #body's head points
        point_row = self.body.get('row')[len(self.body.get('row')) -1 ]
        point_col = self.body.get('col')[len(self.body.get('col')) -1 ]

        point_col = point_col + 1

        #add new head points
        self.body.get('col').append(point_col)
        self.body.get('row').append(point_row)

        #remove the tail
        self.body.get('row').pop(0)
        self.body.get('col').pop(0)

        self.sendSnakeDataToServer()

    def moveUp(self):

        #body's head points
        point_row = self.body.get('row')[len(self.body.get('row')) -1 ]
        point_col = self.body.get('col')[len(self.body.get('col')) -1 ]

        point_row = point_row -1

        #self.body.get('row')[len(self.body.get('row')) -1 ] = self.body.get('row')[len(self.body.get('row')) -1 ] -1

        #add new head points
        self.body.get('col').append(point_col)
        self.body.get('row').append(point_row)

        #remove the tail
        self.body.get('row').pop(0)
        self.body.get('col').pop(0)

        self.sendSnakeDataToServer()

    def moveDown(self):

        #body's head points
        point_row = self.body.get('row')[len(self.body.get('row')) -1 ]
        point_col = self.body.get('col')[len(self.body.get('col')) -1 ]

        point_row = point_row +1

        #add new head points
        self.body.get('col').append(point_col)
        self.body.get('row').append(point_row)

        #remove the tail
        self.body.get('row').pop(0)
        self.body.get('col').pop(0)

        self.sendSnakeDataToServer()

    def getSnake(self):

        return self.body

    def sendSnakeDataToServer(self):
        self.getSnake()
