import pygame
import math
from queue import PriorityQueue


#pygame.init() is pretty self explanitory

    #setting resolution + name
displayWidth = 900
displayHeight = 700
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
        #need double parenthases to work! the two nums are a tuple so it need one set of (), and a function argument so it needs the second set
pygame.display.set_caption("A* Pathfinder Visualizationinator")

BLACK = (0,0,0)
WHITE = (255,255,255)

fpsclock = pygame.time.Clock()

#define a Node
#what does a node need to do?
    #Works with Algorithm
        #alright how do we do that
            #It needs to know where it is (row column) for H score
            #needs to know how wide it is to dram itself
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
    def PositionofNode:




#crash function methinks
def main():
    pygame.init()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
           #print(event) right here will show you every event that happens to the program, mouse movements resizing, exiting, etc
        gameDisplay.fill(WHITE)
        #fps setter
        pygame.display.update()
        fpsclock.tick
'''
    def makeGrid(rows,width):
        grid = []
        #// means floor division, quotients are rounded down
        gap = width // rows
        #This is a Multidimensional List! for loop in for loop
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                #Node = (i, j, gap, rows)
        return grid
'''

main()