from termcolor import colored #maybe for later
from definitions import *


def renderBoard(board):
    height, width = len(board), len(board[0])
    columnWidth = max( len(getColumnDisplay(width)), len(getRowDisplay(height)) )


    padder = getPadder(columnWidth)
    renderHeader(width, padder)
    for idx, row in enumerate(board):
        renderRow(idx, row, padder)
    
    print()

def renderHeader(width, padder):
    header = padder("") + " "
    columns = range(width)
    columns = map( getColumnDisplay, columns )
    columns = map( padder, columns )
    header += " ".join(columns)
    header = colored(header, 'green')
    print(header)

def renderRow( index, cells, padder):
    start = colored(padder( getRowDisplay(index) ), 'green') + " "

    rest = map(renderCell, cells)
    rest = map(padder, rest)
    row = start + " ".join(rest)

    print(row)


def renderCell(cell):
    return renderMap[cell.state](cell)

def renderUncovered(cell):
    count = cell.getNeighborCount()
    if count == 0:
        return " "
    return str(count)

def getPadder( targetLen):
    def padder(string):
        return padString(string, targetLen)
    return padder

def padString( string, targetLen):
    delta = targetLen - len(string)
    return " " * delta + string

def getColumnDisplay(index):
    return getRowDisplay(index)

def getRowDisplay( index):
    return str(index + 1)

renderMap = {
    CELL_NEUTRAL: lambda cell: RENDER_NEUTRAL,
    CELL_DETONATED: lambda cell: RENDER_DETONATED,
    CELL_MARKED: lambda cell: RENDER_MARKED,
    CELL_SUSPECTED: lambda cell: RENDER_SUSPECTED,
    CELL_UNCOVERED: renderUncovered
}