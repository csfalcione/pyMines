from termcolor import colored

DEFAULT_BOARD_SIZE = (8, 8)

BOMB_PROBABILITY = 0.20


CELL_NEUTRAL = 'neutral'
CELL_DETONATED = 'detonated'
CELL_UNCOVERED = 'uncovered'
CELL_MARKED = 'marked'
CELL_SUSPECTED = 'suspected'

DEFAULT_CELL_STATE = CELL_UNCOVERED

RENDER_NEUTRAL = '.'
RENDER_DETONATED = colored('X', 'red')
RENDER_MARKED = colored('!', 'yellow')
RENDER_SUSPECTED = colored('?', 'cyan')