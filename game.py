from itertools import product
from random import Random
from definitions import *

rand = Random()

class Game():

    def __init__(self, width, height):
        self.board = self.makeBoard(width, height)

    def makeBoard(self, width, height):
        return Board(width, height)

    def getCells(self):
        for row in self.board:
            for cell in row:
                yield cell
    
    def getCell(self, row, col):
        return self.board[row][col]

class Board():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [ [self.makeCell(row, col) for col in range(width)] for row in range(height)]

    def __getitem__(self, key):
        return self.board[key]

    def __len__(self):
        return len(self.board)
    
    def makeCell(self, row, col):
        def filterFunc(coord):
            i, j = coord
            isNotSelf = not (i == row and j == col)
            isInBounds = i >= 0 and i < self.height and \
                         j >= 0 and j < self.width
            return isNotSelf and isInBounds

        def neighborIter():
            vertical = range(row - 1, row + 2)
            horizontal = range(col - 1, col + 2)

            neighbors = product(vertical, horizontal)
            neighbors = filter(filterFunc, neighbors)
            neighbors = map(lambda coord: self.board[coord[0]][coord[1]], neighbors)
            return neighbors
        
        return Cell(self.getHasBomb(BOMB_PROBABILITY), self.getDefaultState(), neighborIter)
        
    
    def getHasBomb(self, bombProb):
        return rand.random() <= bombProb
    
    def getDefaultState(self):
        return DEFAULT_CELL_STATE


class Cell():

    def __init__(self, isBomb, state, neighborIter):
        self.isBomb = isBomb
        self.neighborIter = neighborIter
        self.state = state
    
    
    def getNeighborCount(self):
        filterFunc = lambda cell: cell.isBomb
        neighbors = self.neighborIter()
        neighbors = filter(filterFunc, neighbors)
        return len( list(neighbors) )
    
    def uncover(self):
        if self.isBomb:
            self.state = CELL_DETONATED
            return
        self.state = CELL_UNCOVERED

        if self.getNeighborCount() > 0:
            return

        for neighbor in self.neighborIter():
            if neighbor.isBomb == False and neighbor.state == CELL_NEUTRAL:
                neighbor.uncover()
    
    def mark(self):
        if not self.canTransistion():
            raise ValueError("cannot mark an uncovered cell")
        self.state = CELL_MARKED
    
    def suspect(self):
        if not self.canTransistion():
            raise ValueError("cannot suspect an uncovered cell")
        self.state = CELL_SUSPECTED
    
    def canTransistion(self):
        return self.state not in [CELL_DETONATED, CELL_UNCOVERED]
