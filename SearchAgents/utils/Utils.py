import random
from tkinter import *
import copy
import numpy as np

piecesDimensions = [
    (8, 3),
    (5, 1),
    (2, 2),
    (1, 1),
    (9, 4),
    (6, 2),
    (4, 3),
    (5, 7),
    (3, 2),
    (4, 2),
]

def generateRandomPieces(piecesDimensions):
    pieces = []
    for dimensions in piecesDimensions:
        pieces.append( RectangularPiece((random.randint(0, 9), random.randint(0, 9)), 1, Rotation(random.randint(0, 1)), dimensions) )
    return pieces

class Rotation:
    def __init__(self, rotation = 0):
        self.rotation = rotation

    def __str__(self):
        if (self.rotation == 0):
            return "Horizontal"
        else:
            return "Vertical"

class RectangularPiece:
    def __init__(self, coordinates, sheet, rotation, dimensions):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.sheet = sheet
        self.rotation = rotation
        if self.rotation.rotation == 0:
            self.width = dimensions[0]
            self.height = dimensions[1]
        else:
            self.width = dimensions[1]
            self.height = dimensions[0]
        self.area = self.width * self.height

    def getProperties(self, gridCoordinates, cellSize):
        x = gridCoordinates[0] + (self.x * cellSize)
        y = gridCoordinates[1] + (self.y * cellSize)
        width = self.width * cellSize
        height = self.height * cellSize
        return ( x, y, x + width, y + height )

    def canMoveUp(self):
        return self.y > 0

    def moveUp(self):
        if self.canMoveUp():
            self.y -= 1

    def canMoveDown(self):
        return self.y < 9

    def moveDown(self):
        if self.canMoveDown():
            self.y += 1

    def canMoveLeft(self):
        return self.x > 0

    def moveLeft(self):
        if self.canMoveLeft():
            self.x -= 1

    def canMoveRight(self):
        return self.x < 9

    def moveRight(self):
        if self.canMoveRight():
            self.x += 1

    def rotate(self):
        reg = self.height
        self.height = self.width
        self.width = reg
        self.rotation.rotation = (self.rotation.rotation + 1) % 2

    def canMovePreviousSheet(self):
        return self.sheet > 1

    def movePreviousSheet(self):
        if self.canMovePreviousSheet():
            self.sheet -= 1
    
    def moveNextSheet(self):
        self.sheet += 1
        
class BasicState:
    def __init__(self, pieces):
        self.pieces = pieces

    def getAsMatrix(self):
        sheets = []
        for i in range(0, self.f()):
            sheets.append(np.zeros((10, 10)))

        for piece in self.pieces:
            for x in range(piece.x, min(piece.x + piece.width, 10)):
                for y in range(piece.y, min(piece.y + piece.height, 10)):
                    sheets[piece.sheet - 1][x][y] += 1
        return sheets

    # Number of sheets
    def f(self):
        numOfSheets = 1
        for piece in self.pieces:
            numOfSheets = max(numOfSheets, piece.sheet)
        return numOfSheets

    # Count of overlaps
    def g(self):
        sheets = self.getAsMatrix()

        overlaps = 0
        for sheet in sheets:
            for row in sheet:
                for cell in row:
                    if cell > 0:
                        overlaps += (cell - 1)
        return overlaps

    # Pieces out of sheet
    def h(self): 
        cellsOutOfSheet = 0
        for piece in self.pieces:
            maxX = piece.width + piece.x
            maxY = piece.height + piece.y

            cellsInsideTheSheet = (min(10, maxX) - piece.x) * (min(10, maxY) - piece.y)

            cellsOutOfSheet += piece.area - cellsInsideTheSheet
        return cellsOutOfSheet

    # White spaces
    def i (self):
        sheets = self.getAsMatrix()

        whiteSpaces = 0
        for sheet in sheets:
            for idxr, row in enumerate(sheet):
                for idxc, cell in enumerate(row):
                    if cell == 0:
                        whiteSpaces += (18 - ((idxr + idxc))) / 10
        return whiteSpaces

class State(BasicState):
    def getRandomNeighbor(self):
        state = State(copy.deepcopy(self.pieces))
        piece = state.pieces[random.randint(0, 9)]
        action = random.randint(0, 6)
        if action == 0:
            piece.moveUp()
        elif action == 1:
            piece.moveLeft()
        elif action == 2:
            piece.moveRight()
        elif action == 3:
            piece.moveDown()
        elif action == 4:
            piece.rotate()
        elif action == 5:
            piece.movePreviousSheet()
        else:
            piece.moveNextSheet()
        return state

    def findNeighbors(self):
        neighbors = []
        for idx, piece in enumerate(self.pieces):
            if piece.canMoveUp():
                newState = State(copy.deepcopy(self.pieces))
                newState.pieces[idx].moveUp()
                neighbors.append(newState)
            if piece.canMoveLeft():
                newState = State(copy.deepcopy(self.pieces))
                newState.pieces[idx].moveLeft()
                neighbors.append(newState)
            if piece.canMoveDown():
                newState = State(copy.deepcopy(self.pieces))
                newState.pieces[idx].moveDown()
                neighbors.append(newState)
            if piece.canMoveRight():
                newState = State(copy.deepcopy(self.pieces))
                newState.pieces[idx].moveRight()
                neighbors.append(newState)
            if piece.canMovePreviousSheet():
                newState = State(copy.deepcopy(self.pieces))
                newState.pieces[idx].movePreviousSheet()
                neighbors.append(newState)
            newState = State(copy.deepcopy(self.pieces))
            newState.pieces[idx].moveNextSheet()
            neighbors.append(newState)
            newState = State(copy.deepcopy(self.pieces))
            newState.pieces[idx].rotate()
            neighbors.append(newState)
        return neighbors

    def heuristic(self):
        return (self.f() ** 3) + ((self.g() + self.h()) ** 2) + self.i()

class Chromosome(BasicState):
    def fitness(self):
        pass

class Drawer:
    def __init__(self, cellSize = 50):
        self.cellSize = cellSize
        self.sheetSize = cellSize * 10
        self.canvas = Canvas(width=(32 * cellSize), height=(21.5 * cellSize), background='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.colors = [
            '#0000FF',
            '#FF7F50',
            '#DC143C',
            '#8B008B',
            '#228B22',
            '#808000',
            '#D3D3D3',
            '#B8860B',
            '#FF00FF',
            '#FFD700'
        ]

    def draw(self, state):
        # Draw sheets
        sheetsPerRow = 3
        sheets = []
        for idx in range (0, state.f()):
            sheetCoordinates = (
                ((self.cellSize / 2) * ((idx % sheetsPerRow) + 1)) + (self.sheetSize * (idx % sheetsPerRow)),
                ((self.cellSize / 2) * (int(idx / sheetsPerRow) + 1) + self.sheetSize * int(idx / sheetsPerRow))
            )
            self.canvas.create_rectangle(
                sheetCoordinates[0],
                sheetCoordinates[1],
                sheetCoordinates[0] + self.sheetSize,
                sheetCoordinates[1] + self.sheetSize,
                outline='#000000',
                width=3
            )
            sheets.append(sheetCoordinates)

        # Draw pieces
        for index, piece in enumerate(state.pieces):
            self.canvas.create_rectangle(
                piece.getProperties(sheets[piece.sheet - 1], self.cellSize),
                fill=self.colors[index]
            )
        mainloop()