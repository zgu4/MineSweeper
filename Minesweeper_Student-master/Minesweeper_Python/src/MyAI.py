# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class board():
    '''
    variable :
            boardState: 2d array [][]
    function:
            display :
            update :
            get_surrounding : return a list of surroundings
    '''

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.boardState = [[-2 for _ in range(row)] for _ in range(col)]

    def display(self):
        output_string = ""
        for i in self.boardState:
            for j in i:
                if j >= 0:
                    output_string = output_string + " " + str(j) + " "
                else:
                    output_string = output_string + str(j) + " "
            output_string += "\n"
        print(output_string)

    def update(self, x, y, value):
        """
        Attributes :
                x:int
                        X coordinate
                y:int
                        Y coordinate
                value: int
                        Unknown = -2, flag = -1, 
        """

        self.boardState[x][y] = value



class MyAI(AI):
    '''
    variable : state, row, col, totalMines , uncovered, winCondition, lastMove
    '''

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.state = board(rowDimension, colDimension)
        # state.update(startX, startY, 0)
        # state.display()
        print("ruaaaa")
        print(startX,startY)
        self.row = rowDimension
        self.col = colDimension
        self.totalMines = totalMines
        self.uncovered = 1
        self.winCondition = rowDimension * colDimension - totalMines
        self.lastMove = (self.row - (startY + 1), startX)
        self.safeQueue = set()
        self.unsafeQueue = set()

    def getAction(self, number: int) -> "Action Object":
        self.state.update(self.lastMove[0], self.lastMove[1], number)
        #self.state.display()
        if self.uncovered == self.winCondition:
            return Action(AI.Action.LEAVE)



        #print(self.lastMove[0], self.lastMove[1])
        #print(self.row, self.col)
        if self.state.boardState[self.lastMove[0]][self.lastMove[1]] == 0:
            self.get_surrounding(self.lastMove[0], self.lastMove[1], 0)
        if self.state.boardState[self.lastMove[0]][self.lastMove[1]] > 0:
            self.unsafeQueue.add((self.lastMove[0], self.lastMove[1]))

        if len(self.safeQueue) == 0:
            if len(self.unsafeQueue) > 0:
                for block in self.unsafeQueue.copy():
                    stat = self.flag(block[0], block[1])
                    if stat in self.unsafeQueue:
                        self.unsafeQueue.remove(stat)
            for block in self.unsafeQueue.copy():
                stat = self.get_surrounding(block[0], block[1], self.state.boardState[block[0]][block[1]])
                if stat in self.unsafeQueue:
                    self.unsafeQueue.remove(stat)

        if len(self.safeQueue) > 0:
            self.lastMove = self.safeQueue.pop()
            self.uncovered += 1
            return Action(AI.Action.UNCOVER, self.lastMove[1], self.col - (self.lastMove[0]+1))
            #return Action(AI.Action.UNCOVER, 1, 2)


        #return Action(AI.Action.UNCOVER, 1, 1)


        return Action(AI.Action.LEAVE)

    # helperFunction
    def get_surrounding(self, x, y, mines):
        if mines == 0:
            for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]:
                x_row, y_col = i + x, j + y
                if 0 <= x_row < self.row and 0 <= y_col < self.col:
                    if self.state.boardState[x_row][y_col] == -2:
                        self.safeQueue.add((x_row, y_col))
        else:
            safe_condition = 0
            for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]:
                x_row, y_col = i + x, j + y
                if 0 <= x_row < self.row and 0 <= y_col < self.col:
                    if self.state.boardState[x_row][y_col] == -1:
                        safe_condition += 1
            # if safe block add all unknown block into safeQueue
            if safe_condition == mines:
                for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]:
                    x_row, y_col = i + x, j + y
                    if 0 <= x_row < self.row and 0 <= y_col < self.col:
                        if self.state.boardState[x_row][y_col] == -2:
                            self.safeQueue.add((x_row, y_col))
                return x, y

    def flag(self, x, y):
        lst = []
        uncover = 0
        number_of_mines = self.state.boardState[x][y]
        if (x == 0 and y == 0) or (x == 0 and y == self.col) or (y == 0 and x == self.row) or (x == self.row and y == self.col):
            adj = 3
        elif x == 0 or y == 0 or x == self.row or y == self.col:
            adj = 5
        else:
            adj = 8
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]:
            x_row, y_col = i + x, j + y
            if 0 <= x_row < self.row and 0 <= y_col < self.col:
                if self.state.boardState[x_row][y_col] != -2 and self.state.boardState[x_row][y_col] != -1:
                    uncover += 1
        if adj == uncover + number_of_mines: # this block can be solved
            ## Flag surroundings
            for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1)]:
                x_row, y_col = i + x, j + y
                if 0 <= x_row < self.row and 0 <= y_col < self.col:
                    if self.state.boardState[x_row][y_col] == -2:
                        self.state.update(x_row, y_col, -1)
                        #self.state.display()
            return x_row, y_col
        else:
            return -1, -1
                #self.safeQueue.add((x_row, y_col))


