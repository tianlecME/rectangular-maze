###create the doors
from cmu_112_graphics import *
import random,math
# ###Globals
# generate maze(layer):
# mazeBasic(layer)

class mazeBasic:
    def __init__(self,layer):
        self.mazeIndex = layer
        self.length =int(10*layer**(6/5)) #x
        self.angle = 360/self.length
        self.width = 8 #y 
        self.layer = (layer-1)*self.width
        self.nodes = [(i,j) for i in range(self.width) 
                     for j in range(self.length)]

class nodeClass:
    index = 0
    def __init__(self,node):
        self.yx = node
        self.index = nodeClass.index
        self.parent = nodeClass.index
        nodeClass.index += 1

def getNodesC(app,mazing):
    nodesC = []
    for n in mazing.nodes:
        m = nodeClass(n)
        nodesC.append(m)
    app.nodesC = nodesC
def checkLegalDirection(app,mazing,nodeC,direction):
    (y,x) = nodeC.yx
    (dy,dx) = direction
    if (0<= x+dx < mazing.length and 
        0<= y+dy < mazing.width):
        newNode = ((y+dy),(x+dx))
        index = mazing.nodes.index(newNode)
        return app.nodesC[index]
    return False
def neighborGeneration(app,mazing):
    neighbors = {}
    for n in app.nodesC:
        neighbors[n] = set()
        for d in app.directions:
            if checkLegalDirection(app,mazing, n,d):
                neighbors[n].add(checkLegalDirection(
                                app,mazing,n,d))
        if n.yx[1] == 0:
            index = mazing.nodes.index((n.yx[0],mazing.length-1))
            # print(app.nodesC[index])
            neighbors[n].add(app.nodesC[index])
    app.neighbors = neighbors

def findParentNode(nodeC):
    #baseCase: the node is the root of paths
    if type(nodeC.parent) == int:
        # nodeC.parent = nodeC
        return nodeC
    else:
        #recursion #remember the self.parent should always be a nodeC
        parentNode = findParentNode(nodeC.parent)
        nodeC.parent = parentNode
        return parentNode
def unionParent(nodeC1,nodeC2):
    parent1 = findParentNode(nodeC1)
    parent2 = findParentNode(nodeC2)
    parent1.parent = parent2

def createRecMaze(app,mazing,maze):
    while len(maze) < len(mazing.nodes)-1:
        randI = random.randint(0,len(app.walls)-1)
        randEdge = app.walls.pop(randI)
        (nodeC1,nodeC2) = randEdge
        if findParentNode(nodeC1) != findParentNode(nodeC2):
            unionParent(nodeC1,nodeC2)
            maze.append((nodeC1.yx,nodeC2.yx))
    return maze

def createMaze(app,layer):
    mazing = mazeBasic(layer)
    getNodesC(app,mazing)
    neighborGeneration(app,mazing)
    app.walls = [(n1,n2) for n1 in app.nodesC 
                for n2 in app.neighbors[n1]]
    maze = []
    createRecMaze(app,mazing,maze)
    return (maze, mazing)

def creatDoors(app):              
    for (n1,n2) in app.mazeList[0][0]:
        exit = 0
        if (n1[0] == 0 and exit == 0):
            nNew = (n1[0]-1,n1[1])
            app.mazeList[0][0].append((n1,nNew))
            app.origin = app.mazeList[0][0][-1][-1]
            for layerIndex in range(0,app.allLayers):
                path = findTheWayOut(app,layerIndex,path=None)
                # this exit is the entrance of next maze
                if path == None:
                    app.mazeList[0][0].remove((n1,nNew))
                else:
                    if layerIndex == app.allLayers-1:
                        currentExit = path[-1][1]
                        entrToTheWholeMaze = (path[-1][0]+1,path[-1][1])
                        app.mazeList[layerIndex][0].append(
                                (currentExit,entrToTheWholeMaze))
                        continue
                    currentLayerMaze = app.mazeList[layerIndex]
                    currentAngle=currentLayerMaze[1].angle
                    nextLayerMaze = app.mazeList[layerIndex+1]
                    nextAngle=nextLayerMaze[1].angle
                    # print(currentAngle,nextAngle)
                    x = int(path[-1][1]*currentAngle//nextAngle)
                    # currentExit = (0,path[-1][1])
                    nextEntrance = (0,x)
                    pathToEntrace = (-1,x)
                    app.me = nextEntrance
                    app.mazeList[layerIndex+1][0].append(
                                (pathToEntrace,nextEntrance))
                    # print((currentExit,nextEntrance))
            exit += 1
            break
        
def findTheWayOut(app,i,path):
    maze,mazing = app.mazeList[i]
    if path == None:
        if i ==0:
            path = [maze[-1][1]]
        else:
            path = [app.me]
    previousMe = path[-1]
    if  previousMe[0] == 7:
        return path
    else:
        neighbors = []
        for (dy,dx) in app.directions:
            newPosition = (previousMe[0]+dy,previousMe[1]+dx)
            neighbors.append(newPosition)
        if previousMe[1]==0:
            neighbors.append((previousMe[0],mazing.length-1))
        elif previousMe[1]==mazing.length-1:
            neighbors.append((previousMe[0],0))
        # print(neighbors)
        for position in neighbors:
            if position in path:
                continue
            newMe = position
            if ((previousMe,newMe) in maze or
                (newMe,previousMe) in maze):
                path.append(newMe)
                result = findTheWayOut(app,i,path)
                if result == None:
                    path.remove(newMe)
                else:
                    return result
    return None

def appStarted(app,allLayers=4):
    app.allLayers = allLayers
    app.gates = {} 
    app.mazeList = []
    app.interval = 10 #don't change
    app.directions = {(1,0),(0,1),(-1,0),(0,-1)}
    app.origin = [0,0]
    app.me = [0,0]
    for i in range(1,app.allLayers+1):
        app.mazeList.append(createMaze(app,i)) 
    creatDoors(app)
def drawBoard(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = 'white')
def drawPaths(app,canvas):
    for mazeL in app.mazeList:
        (maze,mazing) = mazeL
        i = 0
        while i < len(maze):
            (n1,n2) = maze[i]
            uy = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
                *mazing.angle))*app.interval + app.height//2)
            ux = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
                *mazing.angle))*app.interval + app.width//2)
            ly = ((n2[0]+mazing.layer+1)* math.cos(math.radians(n2[1]
                *mazing.angle))*app.interval + app.height//2)
            lx = ((n2[0]+mazing.layer+1)* math.sin(math.radians(n2[1]
                *mazing.angle))*app.interval + app.width//2)
            color = 'cyan'
            if i == len(maze)-1:
                color = 'red'
            canvas.create_line(ux,uy,lx,ly,fill = color,width = 3)
            i+=1
def redrawAll(app,canvas):
    drawBoard(app,canvas)
    # for i in range(1,8*(app.allLayers+1),8):
    #     i-=1
    #     # canvas.create_oval(app.width//2-i*app.interval,app.height//2
    #     #                 -i*app.interval,app.width//2+i*app.interval,
    #     #                 app.height//2 + i*app.interval,width = 3 )
    drawPaths(app,canvas)
runApp(width = 500,height =500)