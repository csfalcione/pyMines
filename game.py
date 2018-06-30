from itertools import product
from random import Random
from definitions import *

rand = Random()

class Game():

    def __init__(self, width, height):
        self.board = self.makeBoard(width, height)

    def makeBoard(self, width, height):
        return Board(width, height)


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
            isNotSelf = i != row and j != col
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

    def __init__(self, hasBomb, state, neighborIter):
        self.hasBomb = hasBomb
        self.neighborIter = neighborIter
        self.state = state
    
    
    def getNeighborCount(self):
        filterFunc = lambda cell: cell.hasBomb
        neighbors = self.neighborIter()
        neighbors = filter(filterFunc, neighbors)
        return len( list(neighbors) )
    
