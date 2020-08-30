import pygame
import math
from queue import PriorityQueue

# MAYBE TRY ADDING "TERRAIN NODES", SO MOVEMENT IS SLOWED IN CERTAIN NODES MAKING THEM LESS FAVORABLE
# THIS IS PRETTY ACHIEVEABLE BY ADDING H VALUES TO SPECIFC TYPES OF NODES

# setting resolution + name
displayWidth = 700
displayHeight = 700
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
# need double parenthases to work! nums are a tuple and function argument so it 2 sets
pygame.display.set_caption("A* Pathfinder Visualizationinator")

# setting colors and other variables
BLACK = (0, 0, 0)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINKISH = (255, 0, 127)
LIGHTBLUE = (0, 255, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()


# define a Node
# what does a node need to do?
# Works with Algorithm
# alright how do we do that
# It needs to know where it is (row column) for H score
# needs to know how wide it is to draw itself (set as 20 units in draw)
# total rows
# needs to know all of its neighbours for algorithm
# what node type(start, end, barrier, open/removed)
class Node:
    # the class is to store information like where it is, what row column position its in, etc (above)
    def __init__(self, row, column, width, totalRows):
        self.row = row
        self.column = column
        self.width = width
        self.totalRows = totalRows
        # width is the resolution width / number of rows(or columns), so multiplying gives us the x y
        self.x = row * width
        self.y = column * width
        self.neighbours = []
        self.color = WHITE

    def PositionofNode(self):
        return self.row, self.column

        # lets assign colors to the node types and list them
        # we need CLOSED nodes, NEIGHBOUR nodes, OPEN nodes, BARRIER nodes, START nodes, END nodes, FINAL nodes

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

        # colors a node

    def draw(self, gameDisp):
        pygame.draw.rect(gameDisp, self.color, (self.x, self.y, self.width, self.width))

        # making statements like this will help later with the algorithm, as instead of checking if a node is closed, we can instead check if closedNode == RED with isClosedNode
        # also we use == to check for equivalencies, and = for assignment, thus the distinct difference in = between our color and is function

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

    def reset(self):
        self.color = WHITE

        # for alg
        # SHOULD MAKE ALGORITHM PRIORITIZE DIAGONALS, IF NOT REEVALUATE
    def __lt__(self, other):
        return False
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


# The Heuristic score is the distance from the end node to the current node
# Ill set the length of a cube to be 1, so the formula D * Manhattan distance is just Manhattan Dist.
def H(current, end):
    xnodeC, ynodeC = current
    xnodeE, ynodeE = end
    dx = abs(xnodeC - xnodeE)
    dy = abs(ynodeC - ynodeE)
    return 1 * (dx + dy)


# G score is the distance from the start node to the current "open" node
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


# A* Algorithm full
def algorithm(draw, grid, start, end):
    count = 0
    open = PriorityQueue()  # pritority queue lets us put "sets" of information in a list and use them to order it, thus making it idea as we can order by fscore and the count
    open.put((0, count, start))
    openSetHash = {start}  
    parent = {}

    Gscore = {node: float("inf") for row in grid for node in row}
    Gscore[start] = 0
    Fscore = {node: float("inf") for row in grid for node in row}
    Fscore[start] = H(start.PositionofNode(), end.PositionofNode())

    # core loop
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
                # index x y pos in grid
                node = grid[gridx][gridy]
                if not start:
                    start = node
                    # start is stored as a class here, so we can call it with start.PositionofNode
                    start.colorStartNode()
                # theres nothing to catch if you try to override a start node with an endnode, maybe add one?
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


    pygame.quit()


# Drew a Grid
# pygame draws from the top left of the screen, so the top left most rectangle is 0,0, the bottom right is ((displayHeight,displayWidth))
# orignial grid function drew too many entities, this draws the lines instead of each box making it run a lot faster
def drawGrid(gameDisp, rows, dispWidth):
    nodeWidth = dispWidth // rows
    for i in range(rows):
        pygame.draw.line(gameDisp, GREY, (0, i * nodeWidth), (dispWidth, i * nodeWidth))
        for j in range(rows):
            pygame.draw.line(gameDisp, GREY, (j * nodeWidth, 0), (j * nodeWidth, dispWidth))


# this is to store Nodes inside the grid
def nodeGrid(rows, dispWidth):
    grid = []
    nodeWidth = dispWidth // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, nodeWidth, rows)
            grid[i].append(node)
    return grid


# draws colors
# this fills every frame so we can see updates
def fullDraw(gameDisp, grid, rows, dispWidth):
    gameDisplay.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(gameDisp)
    drawGrid(gameDisplay, rows, dispWidth)
    pygame.display.update()


# next we need to INPUT types of NODES
# we need mouse inputs
# mouse goes from 0,0 at top left to 700,700 at bottom right, each square is 20 long so lets translate it over
def mousePosition(x, y, nodeWid):
    gridx = math.floor(x / nodeWid)
    gridy = math.floor(y / nodeWid)
    return gridx, gridy


main(gameDisplay, displayWidth)
