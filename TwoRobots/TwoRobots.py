import math
import string
import random
import time

# The next few lines are for reading the parameters of the file which are needed

# This way way make the global tupple start = (robot's row at start , robot's column at start)
# The global tupple gridSize = (number of rows , number of columns)
# The global tupple goal = (goal's row, goal's column)
# The global List of tupples positionsAvailable which denotes the legal robot positions
# The global List of tupples obstaclePositions


#Opening File
f = open('test.txt','r+')


#Read Grid Size
line = f.readline()
gridSize = line.strip().split( )
gridSize = [int(gridSize[i]) for i in range(len(gridSize))]
gridSize.reverse()  #for (row,col) format
gridSize = tuple(gridSize)
print "Grid Size : ", gridSize


#Read Starting Position
line = f.readline()
start = line.strip().split( )
start = [int(start[i]) for i in range(len(start))]
start.reverse()  #for (row,col) format
start = tuple(start)
print "Starting position : ", start


#Read Goal Position
line = f.readline()
goal = line.strip().split( )
goal = [int(goal[i]) for i in range(len(goal))]
goal.reverse()  #for (row,col) format
goal = tuple(goal)
print "Goal position : ", goal


#Read Available Positions and ObstaclePositions
positionsAvailable = []
obstaclePositions = []
for row in range(gridSize[0]):
    line = f.readline()
    symbols = line.strip()
    for col in range(len(symbols)):
        if symbols[col] == 'O':
            positionsAvailable.append((row,col))
        else:
            obstaclePositions.append((row,col))
            
f.close()



def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class Node:
    def __init__(self, position, costToNode):
        self.position = position
        self.costToNode = costToNode
        #self.costToGoal = 1/(dist(self.position , goal)+1)
        self.costToGoal = dist(self.position , goal)
        self.nodeCost = self.costToNode + self.costToGoal

    def successors(self):
        listOfSuccessors = []
        for i in [-1,1]:
            if (self.position[0]+i,self.position[1]) in positionsAvailable:
                listOfSuccessors.append(Node((self.position[0]+i,self.position[1]),self.costToNode+1))
            if (self.position[0],self.position[1]+i) in positionsAvailable:
                listOfSuccessors.append(Node((self.position[0],self.position[1]+i),self.costToNode+1))
        return listOfSuccessors

#the following global variable was used to count the number of the nodes we expand

COUNT = 0

def AlphaStar(Start,Goal):
    global COUNT
    #initializations
    bestScore = float('Inf') #No Score Yet
    worstNodeScore = 0
    N = Node(Start,0)
    CLOSE = set([])
    ListOfPaths = [[N]]
    GoalNodeReached = False

    while (True) :
        if len(ListOfPaths)==0:
            return []
        bestPath = ListOfPaths.pop(0)
        parent = bestPath[-1]
        if bestPath[-1].position not in CLOSE:
            CLOSE.add(bestPath[-1].position)
            for child in parent.successors():
                pathToAppend = list(bestPath) #for mutation avoidance
                pathToAppend.append(child)
                ListOfPaths.append(pathToAppend)
            ListOfPaths = sorted(ListOfPaths, key=lambda path: path[-1].nodeCost)
            bestPath = ListOfPaths[0]
        if (bestPath[-1].position == Goal):
            COUNT += len(CLOSE)
            return bestPath

robot1pos = start
robot2pos = goal
print "**********************"
print "        START "
print "**********************"
print "Position of Robot 2 : " ,robot2pos
print "Position of Robot 1 : " ,robot1pos

#Uncomment the following line and the last ones to count the time
#needed for the algorithm. You should also comment the print lines
#in the wile loop.

Begin = time.time()

COUNT2 = 0

while robot1pos != robot2pos:
    robot2node = Node(robot2pos,0)
    robot2successors  = robot2node.successors()
    robot2node = random.choice(robot2successors)
    robot2pos = robot2node.position
    if robot2pos == robot1pos:
        break
    Solution = AlphaStar(robot1pos,robot2pos)
    COUNT2 += 1
    if len(Solution)< 4:
        robot1node = Solution[-1]
        robot1pos = robot1node.position
    else :
        robot1node = Solution[3]
        robot1pos = robot1node.position

        print
        print "Position of Robot 2 : " ,robot2pos
        print "Position of Robot 1 : " ,robot1pos

print 
print "Position of Robot 2 : " ,robot2pos
print "Position of Robot 1 : " ,robot1pos

print "**********************"
print "        FINISH "
print "**********************"

Stop = time.time()

print "Number of Nodes Expanded : ", COUNT
print "Time Needed : " , Stop-Begin
print "Number of Times A* Run : ", COUNT2
print "Average Nodes Expanded per Step : ", COUNT/COUNT2
print "Average time for each A* : ", (Stop-Begin)/COUNT2
