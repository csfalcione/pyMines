from termcolor import colored #maybe for later
from definitions import *
from game import Game

class ConsoleInterface():

    def __init__(self, args, renderer):
        self.boardSize = DEFAULT_BOARD_SIZE
        self.parseConsoleArgs(args)

        self.renderBoard = renderer


    def parseConsoleArgs(self, args):
        pass
    
    def start(self):
        # initialize the game state
        width, height = self.boardSize
        game = Game(width, height)

        while True:
            self.renderBoard(game.board)
            args = self.promptUser()
            command = args[0]
            self.handleCommand(game, command, args[1:])

    
    
    def promptUser(self):
        return input(">").split()
    
    def handleCommand(self, game, command, params):
        pass