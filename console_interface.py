from termcolor import colored #maybe for later
from definitions import *
from game import Game
from os import system

class ConsoleInterface():

    def __init__(self, args, renderer):
        self.boardSize = DEFAULT_BOARD_SIZE
        self.parseConsoleArgs(args)

        self.renderBoard = renderer

        self.commandHandlers = {
            COMMAND_UNCOVER: self.handleUncover,
            COMMAND_MARK: self.handleMark,
            COMMAND_SUSPECT: self.handleSuspect,
            COMMAND_QUIT: self.handleQuit
        }


    def parseConsoleArgs(self, args):
        if args[0] in ['-h', '--help']:
            print(self.helpText())
            exit()
        if len(args) != 2:
            return
        try:
            result = tuple( map(int, args) )
            if any( map(lambda x: x <= 0, result) ):
                raise ValueError
            self.boardSize = result
        except ValueError:
            print("Please enter two positive integers for board sizes")
            exit(1)
    
    def start(self):
        # initialize the game state
        width, height = self.boardSize
        game = Game(width, height)

        state = GAME_ONGOING
        while state == GAME_ONGOING:
            self.refreshScreen(game)
            try:
                args = self.promptUser()
            except KeyboardInterrupt:
                state = GAME_QUIT
                print()
                break
            command = args[0].lower().strip()
            state = self.handleCommand(game, command, args[1:])
        
        self.refreshScreen(game)
        
        # handle win or loss from game state
        if state == GAME_WIN:
            print( colored("You win!", 'green', None, ['underline']) )
            return
        
        if state == GAME_LOSE:
            print( colored("BOOM!", 'red', None, ['bold']) )
            return
        
        if state == GAME_QUIT:
            print("Goodbye, quitter.")
            return
    
    def refreshScreen(self, game):
        self.clearScreen()
        print(self.commandHelpText())
        self.renderBoard(game.board)
    
    def clearScreen(self):
        system("clear||cls")
    
    
    def promptUser(self):
        return input(">").split()
    
    def handleCommand(self, game, command, params):
        if command not in self.commandHandlers:
            print("Command not found")
        handler = self.commandHandlers[command]
        return handler(game, params)

    def handleUncover(this, game, params):
        for col, row in this.parseCoordinates(params):
            cell = game.getCell(row, col)
            cell.uncover()
            if cell.state == CELL_DETONATED:
                return GAME_LOSE
        
        if this.didWin(game):
            return GAME_WIN
        
        return GAME_ONGOING
    
    def handleMark(self, game, params):
        for col, row in self.parseCoordinates(params):
            cell = game.getCell(row, col)
            cell.mark()
        
        if self.didWin(game):
            return GAME_WIN

        return GAME_ONGOING
    
    def handleSuspect(self, game, params):
        for col, row in self.parseCoordinates(params):
            cell = game.getCell(row, col)
            cell.suspect()

        return GAME_ONGOING
    
    def handleQuit(self, game, params):
        return GAME_QUIT
    
    def didWin(self, game):
        def mapFunc(cell):
            if cell.isBomb:
                return cell.state == CELL_MARKED
            return cell.state == CELL_UNCOVERED
        return all(map(mapFunc, game.getCells()))
    
    def parseCoordinates(self, params):
        if len(params) == 0:
            print("Please specify coordinates.")
            self.printCoordinateHelp()
            return
        if len(params) % 2 == 1:
            self.printCoordinateHelp()
            return
        try:
            parsed = list(map(lambda x: int(x) - 1, params))
            if any(map(lambda x: x < 0, parsed)):
                self.printCoordinateHelp()
                return
            for left in range(0, len(parsed), 2):
                yield parsed[left], parsed[left + 1]
            
        except ValueError:
            self.printCoordinateHelp()
            return
        
    
    def printCoordinateHelp(self):
        print("Coordinates are pairs of non-negative integers.")
    
    def helpText(self):
        return \
"""
Terminal Minesweeper
    usage: python pyMines.py [width height]

note: commands can be followed by arbitrarily many coordinates.
    ex: 'u 1 1 1 2 1 3' uncovers cells (1, 1), (1, 2), (1, 3)
"""
    
    def commandHelpText(self):
        return colored("Commands:", attrs=['underline']) + \
"""
  {}: u <x> <y>
  {}:    m <x> <y>
  {}: s <x> <y>
  {}:    q
""".format(*map(lambda x: colored(x, 'cyan'), ['uncover', 'mark', 'suspect', 'quit']))