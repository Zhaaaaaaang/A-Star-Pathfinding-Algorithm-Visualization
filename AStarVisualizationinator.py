import pygame
import math
from queue import PriorityQueue

displayWidth = 700
displayHeight = 700
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("A* Pathfinder Visualizationinator")

BLACK = (0, 0, 0)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINKISH = (255, 0, 127)
LIGHTBLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
FOREST = (0, 125, 0)

clock = pygame.time.Clock()

class Node:
    def __init__(self, row, column, width, totalRows):
        self.row = row
        self.column = column
        self.width = width
        self.totalRows = totalRows
        self.x = row * width
        self.y = column * width
        self.neighbours = []
        self.color = WHITE

    def PositionofNode(self):
        return self.row, self.column
    def colorClosedNode(self):
        self.color = RED
    def colorOpenNode(self):
        self.color = GREEN
    def colorNeighbourNode(self):
        self.color = YELLOW
    def colorBarrierNode(self):
        self.color = BLACK
    def colorStartNode(self):
        self.color = PINKISH
    def colorEndNode(self):
        self.color = LIGHTBLUE
    def colorFinalPathingNode(self):
        self.color = BLUE
    def colorForestNode(self):
        self.color = FOREST

    def draw(self, gameDisp):
        pygame.draw.rect(gameDisp, self.color, (self.x, self.y, self.width, self.width))
    def isClosedNode(self):
        return self.color == RED
    def isOpenNode(self):
        return self.color == GREEN
    def isNeighbourNode(self):
        return self.color == YELLOW
    def isBarrierNode(self):
        return self.color == BLACK
    def isStartNode(self):
        return self.color == PINKISH
    def isEndNode(self):
        return self.color == LIGHTBLUE
    def isFinalPathingNode(self):
        return self.color == BLUE
    def isForestNode(self):
        return self.color == FOREST
    def reset(self):
        self.color = WHITE

    def updateNeighbour(self, grid):
        self.neighbours = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.column].isBarrierNode():  # DOWN
            self.neighbours.append(grid[self.row + 1][self.column])
        if self.row > 0 and not grid[self.row - 1][self.column].isBarrierNode():  # UP
            self.neighbours.append(grid[self.row - 1][self.column])
        if self.column < self.totalRows - 1 and not grid[self.row][self.column + 1].isBarrierNode():  # RIGHT
            self.neighbours.append(grid[self.row][self.column + 1])
        if self.column > 0 and not grid[self.row][self.column - 1].isBarrierNode():  # LEFT
            self.neighbours.append(grid[self.row][self.column - 1])

def H(current, end):
    xnodeC, ynodeC = current
    xnodeE, ynodeE = end
    dx = abs(xnodeC - xnodeE)
    dy = abs(ynodeC - ynodeE)
    return 1 * (dx + dy)

def G(current, start):
    xnodeC, ynodeC = current
    xnodeS, ynodeS = start
    dx = abs(xnodeC - xnodeS)
    dy = abs(ynodeC - ynodeS)
    return 1 * (dx + dy)

def F(current, start, end):
    Fscore = H(current, end) + G(current, start)
    return Fscore

def reconstructPath(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.colorFinalPathingNode()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open = PriorityQueue()
    open.put((0, count, start))
    openSetHash = {start}
    parent = {}

    Gscore = {node: float("inf") for row in grid for node in row}
    Gscore[start] = 0
    Fscore = {node: float("inf") for row in grid for node in row}
    Fscore[start] = H(start.PositionofNode(), end.PositionofNode())

    while not open.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open.get()[2]
        openSetHash.remove(current)

        if current == end:
            reconstructPath(parent, end, draw)
            end.colorEndNode()
            return True

        for neighbour in current.neighbours:
            tempGscore = Gscore[current] + 1

            if tempGscore < Gscore[neighbour]:
                parent[neighbour] = current
                Gscore[neighbour] = tempGscore
                if neighbour.isForestNode():
                    Fscore[neighbour] = tempGscore + H(neighbour.PositionofNode(), end.PositionofNode()) + 10
                else:
                    Fscore[neighbour] = tempGscore + H(neighbour.PositionofNode(), end.PositionofNode())
                if neighbour not in openSetHash:
                    count += 1
                    open.put((Fscore[neighbour], count, neighbour))
                    openSetHash.add(neighbour)
                    neighbour.colorOpenNode()
        draw()

        if current != start:
            current.colorClosedNode()

    return None


def main(gameDisp, dispWidth):
    pygame.init()

    rowsInGrid = 35
    nodeWidth = dispWidth // rowsInGrid
    grid = nodeGrid(rowsInGrid, dispWidth)

    start = None
    end = None

    run = True

    while run:
        fullDraw(gameDisplay, grid, rowsInGrid, displayWidth)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # LM input
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                gridx, gridy = mousePosition(x, y, nodeWidth)
                node = grid[gridx][gridy]
                if not start:
                    start = node
                    start.colorStartNode()
                elif not end:
                    end = node
                    end.colorEndNode()

                elif node != end and node != start:
                    node.colorBarrierNode()
            # RM input
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                gridx1, gridy1 = mousePosition(x, y, nodeWidth)
                node = grid[gridx1][gridy1]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbour(grid)
                    algorithm(lambda: fullDraw(gameDisp, grid, rowsInGrid, dispWidth), grid, start, end)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = nodeGrid(rowsInGrid, displayWidth)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    x, y = pygame.mouse.get_pos()
                    gridx, gridy = mousePosition(x, y, nodeWidth)
                    forestNode = grid[gridx][gridy]
                    forestNode.colorForestNode()
    pygame.quit()

def drawGrid(gameDisp, rows, dispWidth):
    nodeWidth = dispWidth // rows
    for i in range(rows):
        pygame.draw.line(gameDisp, GREY, (0, i * nodeWidth), (dispWidth, i * nodeWidth))
        for j in range(rows):
            pygame.draw.line(gameDisp, GREY, (j * nodeWidth, 0), (j * nodeWidth, dispWidth))

def nodeGrid(rows, dispWidth):
    grid = []
    nodeWidth = dispWidth // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, nodeWidth, rows)
            grid[i].append(node)
    return grid


def fullDraw(gameDisp, grid, rows, dispWidth):
    gameDisplay.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(gameDisp)
    drawGrid(gameDisplay, rows, dispWidth)
    pygame.display.update()

def mousePosition(x, y, nodeWid):
    gridx = math.floor(x / nodeWid)
    gridy = math.floor(y / nodeWid)
    return gridx, gridy

main(gameDisplay, displayWidth)
