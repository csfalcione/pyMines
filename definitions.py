from termcolor import colored

DEFAULT_BOARD_SIZE = (6, 6)

BOMB_PROBABILITY = 0.15


CELL_NEUTRAL = 'neutral'
CELL_DETONATED = 'detonated'
CELL_UNCOVERED = 'uncovered'
CELL_MARKED = 'marked'
CELL_SUSPECTED = 'suspected'

DEFAULT_CELL_STATE = CELL_NEUTRAL

RENDER_NEUTRAL = '.'
RENDER_DETONATED = colored('X', 'red')
RENDER_MARKED = colored('!', 'yellow')
RENDER_SUSPECTED = colored('?', 'cyan')

COMMAND_UNCOVER = 'u'
COMMAND_MARK = 'm'
COMMAND_SUSPECT = 's'
COMMAND_QUIT = 'q'

GAME_WIN = 'win'
GAME_LOSE = 'lost'
GAME_QUIT = 'quit'
GAME_ONGOING = 'ongoing'