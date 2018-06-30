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
        pass
    
    def start(self):
        # initialize the game state
        width, height = self.boardSize
        game = Game(width, height)

        state = GAME_ONGOING
        while state == GAME_ONGOING:
            self.clearScreen()
            self.renderBoard(game.board)
            try:
                args = self.promptUser()
            except KeyboardInterrupt:
                state = GAME_QUIT
                print()
                break
            command = args[0].lower().strip()
            state = self.handleCommand(game, command, args[1:])
        
        self.clearScreen()
        self.renderBoard(game.board)
        
        # handle win or loss from game state
        if state == GAME_WIN:
            print("You win!")
            return
        
        if state == GAME_LOSE:
            print("BOOM... you lose!")
            return
        
        if state == GAME_QUIT:
            print("Goodbye, quitter.")
            return
    
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