from cmu_112_graphics import *
import random,math
# ###Globals
width = 10 #y
length =20 #x
interval = 20
nodes = [(i,j) for i in range(width) for j in range(length)]
directions = [(1,0),(0,1),(-1,0),(0,-1)]
class nodeClass:
    index = 0
    def __init__(self,node):
        self.yx = node
        self.index = nodeClass.index
        self.parent = nodeClass.index
        nodeClass.index += 1
nodesC = []
for n in nodes:
    m = nodeClass(n)
    nodesC.append(m)
# print(nodesC)


def checkLegalDirection(nodeC,direction):
    (y,x) = nodeC.yx
    (dy,dx) = direction
    if (0<= x+dx < length and 0<= y+dy < width):
        newNode = ((y+dy),(x+dx))
        index = nodes.index(newNode)
        return nodesC[index]
    return False
def neighborGeneration():
    neighbors = {}
    for n in nodesC:
        neighbors[n] = set()
        for d in directions:
            if checkLegalDirection(n,d):
                neighbors[n].add(checkLegalDirection(n,d))
    return neighbors
neighbors = neighborGeneration()
walls = [(n1,n2) for n1 in nodesC for n2 in neighbors[n1]]
# print(walls)
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
maze = []
def createRecMaze():
    randInU = random.randint(0,length-2)
    (nodeC1,nodeC2) = (nodesC[randInU],nodesC[randInU+1])
    walls.remove((nodeC1,nodeC2))
    unionParent(nodeC1,nodeC2)
    maze.append((nodeC1.yx,nodeC2.yx))
    randInL = random.randint(len(nodes)-2-length,len(nodes)-2)
    (nodeC3,nodeC4) = (nodesC[randInL],nodesC[randInL+1])
    walls.remove((nodeC3,nodeC4))
    unionParent(nodeC3,nodeC4)
    maze.append((nodeC3.yx,nodeC4.yx))
    counter = 2
    i,j =0,0
    while counter < len(nodes)-3:
        randI = random.randint(0,len(walls)-1)
        randEdge = walls.pop(randI)
        (nodeC1,nodeC2) = randEdge
        print(nodeC1.yx[0],nodeC2.yx[0])
        if nodeC1.yx[0] == nodeC2.yx[0] == 0:
            continue
        elif nodeC1.yx[0] == nodeC2.yx[0] == width-1:
            # print(nodeC1.yx[0],nodeC2.yx[0])
            continue
        if nodeC1.yx[0] == 0 or nodeC2.yx[0] == 0:
            i+=1
            if i>=length//2:
                counter+=1
                continue
        elif nodeC1.yx[0] == width-1 or nodeC2.yx[0] == width-1:
            j+=1
            if j>=length//2:
                counter+=1
                continue
        # counter+=1
        if findParentNode(nodeC1) != findParentNode(nodeC2):
            unionParent(nodeC1,nodeC2)
            maze.append((nodeC1.yx,nodeC2.yx))
            counter += 1
print(createRecMaze())
# print('union',maze)
for (nodeC1,nodeC2) in maze:
    print(nodeC1,nodeC2)
def appStarted(app):
    app.maze = maze
    # print(app.maze)
    app.cellSize = 20
    app.margin = 10
    app.timeFired = 10000
    app.mazeParent = []
def drawBoard(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = 'black')
def drawPaths(app,canvas):
    for (n1,n2) in app.maze:
        Uy = app.margin+n1[0]*app.cellSize*2
        Ux = app.margin+n1[1]*app.cellSize*2
        Ly = app.margin+n2[0]*app.cellSize*2
        Lx = app.margin+n2[1]*app.cellSize*2
        canvas.create_line(Ux,Uy,Lx,Ly,fill = 'white',width = 3)
def redrawAll(app,canvas):
    drawBoard(app,canvas)
    drawPaths(app,canvas)
runApp(width = 500,height =500)