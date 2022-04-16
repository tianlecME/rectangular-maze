from cmu_112_graphics import *
import random,math
#quotations:
# the idea of initializing parent to an int 
# and the idea of set union root parent 
# is quote from # <script src="https://gist.
# github.com/nthistle/52cc
# 86190266fd5673b06ebc68377281.js"></script>
# roundHalfUp is quoted from 15-112
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

############### GNERATE THE MAZE ###############
class mazeBasic:
    def __init__(self,layer):
        self.mazeIndex = layer
        self.length =int(10*layer**(6/5)) #x
        self.angle = 360/self.length
        self.width = 6 #y 
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
def neighborGeneration(app,mazing): #set
    neighbors = {}
    for n in app.nodesC:
        neighbors[n] = set()
        for d in app.directions:
            if checkLegalDirection(app,mazing, n,d):
                neighbors[n].add(checkLegalDirection(
                                app,mazing,n,d))
        if n.yx[1] == 0:
            index = mazing.nodes.index((n.yx[0],mazing.length-1))
            neighbors[n].add(app.nodesC[index])
    app.neighbors = neighbors
def neighborGinList(app,node,mazing): #yx
    previousMe = node
    neighbors = []
    for (dy,dx) in app.directions:
        newPosition = (previousMe[0]+dy,previousMe[1]+dx)
        neighbors.append(newPosition)
    if previousMe[1]==0:
        neighbors.append((previousMe[0],mazing.length-1))
    elif previousMe[1]==mazing.length-1:
        neighbors.append((previousMe[0],0))
    return neighbors
def findParentNode(nodeC):
    if type(nodeC.parent) == int:
        return nodeC
    else:
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

############### GNERATE THE GATES ###############
def creatDoors(app):              
    for (n1,n2) in app.mazeList[0][0]:
        exit = 0
        if (n1[0] == 0 and exit == 0):
            nNew = (n1[0]-1,n1[1])
            app.mazeList[0][0].append((n1,nNew))
            app.mazeList[0][1].nodes.append(nNew)
            app.origin = app.mazeList[0][0][-1][-1]
            nextEntrance = (0,0)
            for layerIndex in range(0,app.allLayers):
                path = findTheWayOut(app,nextEntrance,layerIndex,path=None)
                # this exit is the entrance of next maze
                if path == None:
                    app.mazeList[0][0].remove((n1,nNew))
                else:
                    if layerIndex == app.allLayers-1:
                        currentExit = path[-1]
                        entrToTheWholeMaze = (path[-1][0]+1,path[-1][1])
                        app.mazeList[layerIndex][0].append(
                                (currentExit,entrToTheWholeMaze))
                        app.mazeList[layerIndex][1].nodes.append(
                                    entrToTheWholeMaze)
                        app.entrToTheWholeMaze = entrToTheWholeMaze
                        path.append(entrToTheWholeMaze)
                        app.theWayOut[layerIndex] = path
                        continue
                    currentLayerMaze = app.mazeList[layerIndex]
                    currentAngle=currentLayerMaze[1].angle
                    nextLayerMaze = app.mazeList[layerIndex+1]
                    nextAngle=nextLayerMaze[1].angle
                    x = roundHalfUp(path[-1][1]*currentAngle/nextAngle)
                    # currentExit = (0,path[-1][1])
                    nextEntrance = (0,x)
                    pathToEntrace = (-1,x)
                    # app.me = nextEntrance
                    app.mazeList[layerIndex+1][0].append(
                                (pathToEntrace,nextEntrance))
                    app.mazeList[layerIndex+1][1].nodes.append(
                                                    pathToEntrace)
                app.theWayOut[layerIndex] = path
            exit += 1
            break
        
def findTheWayOut(app,nextEntrance,i,path):
    maze,mazing = app.mazeList[i]
    if path == None:
        if i ==0:
            path = [maze[-1][1]]
        else:
            path = [(-1,nextEntrance[1]),nextEntrance]
    previousMe = path[-1]
    if  previousMe[0] == mazing.width-1:
        return path
    else:
        neighbors = neighborGinList(app,previousMe,mazing)
        for position in neighbors:
            if position in path:
                continue
            newMe = position
            if ((previousMe,newMe) in maze or
                (newMe,previousMe) in maze):
                path.append(newMe)
                result = findTheWayOut(app,nextEntrance,i,path)
                if result == None:
                    path.remove(newMe)
                else:
                    return result
    return None
############### OTHER FEATURE CLASSES ###############
class robin:
    def __init__(self):
        self.robinPath = [((-2,0),-1)]
        self.robinLocation = None
        self.robinPathLibry = {}
        self.robinDisappear = False
    def drawRobin(self,app,canvas):
        n1= self.robinLocation[0]
        i = self.robinLocation[1]
        maze,mazing = app.mazeList[i]
        color = 'green'
        drawCircle(app,n1,mazing,canvas,color)
class key:
    def __init__(self,app):
        self.show = False
        self.find = False
        randLayer = random.randint(1,app.allLayers-1) 
        randLocation = random.randint(0,
                app.mazeList[randLayer][1].length-1)
        location = app.mazeList[randLayer][0][randLocation][0]
        self.location = (location,randLayer)
    def drawKey(self,app,canvas):
        if self.show:
            n1= self.location[0]
            i = self.location[1]
            maze,mazing = app.mazeList[i]
            color = 'purple'
            drawCircle(app,n1,mazing,canvas,color)
############### APP AND CONTROLLERS ###############
def appStarted(app,allLayers=5):
    ####### Maze Generation ########
    app.allLayers = allLayers+1
    app.theWayOut = {} 
    app.mazeList = []
    app.interval = 10 #don't change
    app.directions = {(1,0),(0,1),(-1,0),(0,-1)}
    for i in range(1,app.allLayers+1):
        app.mazeList.append(createMaze(app,i)) 
    creatDoors(app)
    app.MarryMeetRobin = 0
    app.MarryLocation = (app.entrToTheWholeMaze,app.allLayers-1) 
    rfootPrint = robin()
    app.robinsList = [rfootPrint]
    robinAutoMove(app,rfootPrint)
    app.getToTheKeyHole = False
    app.key = key(app)
    # help debugging print
    print(app.theWayOut)
    print(app.key.location)
    # add a function that combines all the layers in to one list of positions

def keyPressed(app,event):
    if event.key == 'Up':
        direction = (-1,0)
        MarryMove(app,direction)
    elif event.key == 'Down':
        direction = (1,0)
        MarryMove(app,direction)
    elif event.key == 'Left':
        direction = (0,-1)
        MarryMove(app,direction)
    elif event.key == 'Right':
        direction = (0,1)
        MarryMove(app,direction)
    pass
def MarryMove(app,direction):
    (location,i) = app.MarryLocation
    maze,mazing = app.mazeList[i]
    newy,newx = (location[0]+direction[0],
                   location[1]+direction[1])
    if newx == -1: newx = mazing.length-1
    elif newx == mazing.length: newx = 0
    newLocation = (newy,newx)
    if ((location,newLocation) in maze or 
        (newLocation,location) in maze):
        if i > 0 and newLocation == app.theWayOut[i][0]:
            app.MarryLocation = (app.theWayOut[i-1][-1],i-1)
        elif i <app.allLayers-1 and newLocation == app.theWayOut[i][-1]:
                    app.MarryLocation = (app.theWayOut[i+1][0],i+1)
        else:
            app.MarryLocation = (newLocation,i)
def robinAutoMove(app,robi):
    if robi.robinLocation == None:
        while True:
            randLayer = random.randint(app.allLayers-2,app.allLayers-1) 
            randLocation = random.randint(0,
                    app.mazeList[randLayer][1].length-1)
            location = app.mazeList[randLayer][0][randLocation][0]
            if (location,randLayer) != app.MarryLocation:
                robi.robinLocation = (location,randLayer)
                robi.robinPath.append(robi.robinLocation)
                break
    else:
        (location,i) = robi.robinLocation
        if i == 0:
            robi.robinDisappear = True
        maze,mazing = app.mazeList[i]
        if robi.robinLocation in robi.robinPathLibry:
            if robi.robinPathLibry[robi.robinLocation] == {}:
                robi.robinPath.remove(robi.robinLocation)
                oldLocation = robi.robinLocation
                robi.robinLocation = robi.robinPath[-1]
                robi.robinPathLibry[robi.robinLocation].pop(oldLocation)
            else:
                #find the direction that has the minimum index
                min = 10**8
                nextMove = None
                for position in robi.robinPathLibry[robi.robinLocation]:
                    index = robi.robinPathLibry[robi.robinLocation][position]
                    if index < min:
                        min = index
                        if nextMove != app.MarryLocation:
                            nextMove = position
                if i > 0 and nextMove[0] == app.theWayOut[i][0]:
                    nextMove = (app.theWayOut[i-1][-1],i-1)
                    robi.robinLocation = nextMove
                    robi.robinPath.append(nextMove)
                    # print('to lower level')
                elif i <app.allLayers-1 and nextMove[0] == app.theWayOut[i][-1]:
                    nextMove = (app.theWayOut[i+1][0],i+1)
                    robi.robinLocation = nextMove
                    robi.robinPath.append(nextMove)
                else:
                    robi.robinPath.append(nextMove)
                    currentStep = len(robi.robinPath)
                    robi.robinPathLibry[robi.robinLocation][nextMove]=currentStep
                    robi.robinLocation = nextMove
        else: 
            # robi.robinLocation not in robi.robinPathLibry
            robi.robinPathLibry[robi.robinLocation] = {}
            neighbors = neighborGinList(app,location,mazing)
            for paths in maze:
                if location in paths:
                    if paths[0] ==location:
                        possibleMove = (paths[1],i) 
                        #location,layer,index of the last visited
                    else: possibleMove = (paths[0],i)
                    if possibleMove[0] in neighbors:
                        step = 0
                        if possibleMove == robi.robinPath[-2]:
#### step = 1
                            step = 2
                        robi.robinPathLibry[(location,i)][possibleMove]=step
def timerFired(app):
    ranInt = random.randint(0,50)
    if ranInt == 0 and len(app.robinsList)<=app.allLayers//3:
        rfootPrint = robin()
        app.robinsList.append(rfootPrint)
        robinAutoMove(app,rfootPrint)
    elif ranInt ==1:
        randInt = random.randint(0,len(app.robinsList)-1)
        app.robinsList[randInt] = robin()
    for i in range(len(app.robinsList)):
        robi = app.robinsList[i]
        if robi.robinLocation == app.MarryLocation:
            app.MarryMeetRobin += 1
            if app.MarryMeetRobin >= 1:
                app.key.show = True
            while True:
                app.robinsList[i] = robin()
                if robi.robinLocation != app.MarryMeetRobin:
                    robinAutoMove(app,app.robinsList[i])
                    break
        robinAutoMove(app,robi)
############### VIEW ###############        
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
            if i == len(maze)-1 or i == len(maze)-2:
                color = 'red'
            canvas.create_line(ux,uy,lx,ly,fill = color,width = 3)
            i+=1
def drawLittleMarry(app,canvas):
    (n1,i) = app.MarryLocation
    maze,mazing = app.mazeList[i]
    color = 'yellow'
    drawCircle(app,n1,mazing,canvas,color)

def drawCircle(app,n1,mazing,canvas,color):
    uy = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)-10
    ux = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)-10
    ly = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)+10
    lx = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)+10
    canvas.create_oval(ux,uy,lx,ly,fill = color)
def redrawAll(app,canvas):
    drawBoard(app,canvas)
    # for i in range(1,6*(app.allLayers+1),6):
    #     i-=1
    #     canvas.create_oval(app.width//2-i*app.interval,app.height//2
    #                     -i*app.interval,app.width//2+i*app.interval,
    #                     app.height//2 + i*app.interval,width = 3 )
    drawPaths(app,canvas)
    drawLittleMarry(app,canvas)
    for robi in app.robinsList:
        if not robi.robinDisappear:
            robi.drawRobin(app,canvas)
    app.key.drawKey(app,canvas)
runApp(width = 1000,height =1000)