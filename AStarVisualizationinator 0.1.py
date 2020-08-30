import pygame
import math
from queue import PriorityQueue

                #MAYBE TRY ADDING "TERRAIN NODES", SO MOVEMENT IS SLOWED IN CERTAIN NODES MAKING THEM LESS FAVORABLE
                        #THIS IS PRETTY ACHIEVEABLE BY ADDING H VALUES TO SPECIFC TYPES OF NODES

    #setting resolution + name
displayWidth = 700
displayHeight = 700
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
        #need double parenthases to work! the two nums are a tuple so it need one set of (), and a function argument so it needs the second set
pygame.display.set_caption("A* Pathfinder Visualizationinator")

    #setting colors and other variables
BLACK = (0,0,0)
GREY = (90,90,90)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
PINKISH = (255,0,127)
LIGHTBLUE = (0,255,255)
YELLOW = (255,255,0)


fpsclock = pygame.time.Clock()

#define a Node
#what does a node need to do?
    #Works with Algorithm
        #alright how do we do that
            #It needs to know where it is (row column) for H score
            #needs to know how wide it is to draw itself (set as 20 units in draw)
            #total rows
            #needs to know all of its neighbours for algorithm
            #what node type(start, end, barrier, open/removed)
class Node:
        #the class is to store information like where it is, what row column position its in, etc (above)
    def __init__(self, row, column, width, totalRows):
        self.row = row
        self.column = column
        self.width = width
        self.totalRows = totalRows
            #width is the resolution width / number of rows(or columns), so multiplying gives us the x y
        self.x = row * width
        self.y = column * width
        self.neighbours = []
        self.color = WHITE
    def PositionofNode(self):
        return self.row, self.column

    #lets assign colors to the node types and list them
    #we need CLOSED nodes, NEIGHBOUR nodes, OPEN nodes, BARRIER nodes, START nodes, END nodes, FINAL nodes
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

#colors a node
    def draw(self, gameDisp):
        pygame.draw.rect(gameDisp, self.color, (self.x, self.y, self.width, self.width))

    #making statements like this will help later with the algorithm, as instead of checking if a node is closed, we can instead check if closedNode == RED with isClosedNode
    #also we use == to check for equivalencies, and = for assignment, thus the distinct difference in = between our color and is function
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
        self.color == WHITE


        #now its important for us to update the rectangles and also compare F scores (G score plus H score)
#  def updateNeighbours:



        #lets make the H score function
# The Heuristic score is the distance from the end node to the current node
    #Ill set the length of a cube to be 1, so the formula D * Manhattan distance is just Manhattan Dist.
def H(Node1, Node2):
    xnode1, ynode1 = Node1
    xnode2, ynode2 = Node2
    dx = abs(xnode1 - xnode2)
    dy = abs(ynode1 - ynode2)
    return 1 * (dx + dy)



        #crash function methinks
def main():
    pygame.init()
    crashed = False
    while not crashed:
        fullDraw(gameDisplay, nodeGrid(35, displayWidth), 35, displayWidth)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        #print(event) right here will show you every event that happens to the program, mouse movements resizing, exiting, etc
        #fps setter
        pygame.display.update()
        fpsclock.tick

#Drew a Grid
# pygame draws from the top left of the screen, so the top left most rectangle is 0,0, the bottom right is ((displayHeight,displayWidth))
def drawGrid(rows, dispWidth):
    nodeWidth = dispWidth // rows
    for i in range(dispWidth):
        for j in range(dispWidth):
            rect = pygame.Rect(i*nodeWidth, j*nodeWidth, nodeWidth, nodeWidth)
            pygame.draw.rect(gameDisplay, GREY, rect, 1)
#this is to store Nodes inside the grid
def nodeGrid(rows, dispWidth):
    nodeGrid = []
    nodeWidth = dispWidth // rows
    for k in range(rows):
        nodeGrid.append([])
        for l in range(rows):
            gridNode = Node(k, l, nodeWidth, rows)
            nodeGrid[k].append(gridNode)
    return nodeGrid
#draws colors
#this fills every frame so we can see updates
def fullDraw(gameDisp, grid, rows, dispWidth):
    gameDisplay.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(gameDisp)
    drawGrid(rows, dispWidth)
    pygame.display.update()

#next we need to INPUT types of NODES





main()