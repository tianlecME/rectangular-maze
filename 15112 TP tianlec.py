'''
No modules, pictures, music are used.
Four core parts of code are highlighted in CODE NOTES comments
including those in JIMI part.

The structure of this file:
1) Kruskal logic
2) General Maze generation
3) Circle Maze generation
4) Core elements of the maze:
    5.1 Robin
    5.2 Key
    5.3 Ben Weatherstaff
    5.4 Marry
5) General Maze Background
6) Instruction page Background
7) AppStarted, keyPressed and TimerFired
8) View

All parts and subparts are separated by comments

Counterintuitive Things in this game:
1) As it is a circle, up and down keys can be strange

quotations:
1) <script src="https://gist.github.com/nthistle/52cc#
  86190266fd5673b06ebc68377281.js"></script>
2) roundHalfUp from 15-112
3) topic inspired by Frances Hodgson Burnett's The Secret Garden
4) JIMI view inspired by Jimmy Liao's One More Day With You
'''
from cmu_112_graphics import *
from JIMI import *
import random,math
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

############### KRUSKAL LOGIC ###############
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
def neighborGeneration(app,mazing,isDoor): #set
    neighbors = {}
    for n in app.nodesC:
        neighbors[n] = set()
        for d in app.directions:
            if checkLegalDirection(app,mazing, n,d):
                neighbors[n].add(checkLegalDirection(
                                app,mazing,n,d))
        if isDoor and n.yx[1] == 0:
            index = mazing.nodes.index((n.yx[0],mazing.length-1))
            neighbors[n].add(app.nodesC[index])
    app.neighbors = neighbors
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
def createRecMaze(app,nodes,maze):
    while len(maze) < len(nodes)-1:
        randI = random.randint(0,len(app.walls)-1)
        randEdge = app.walls.pop(randI)
        (nodeC1,nodeC2) = randEdge
        if findParentNode(nodeC1) != findParentNode(nodeC2):
            unionParent(nodeC1,nodeC2)
            maze.append((nodeC1.yx,nodeC2.yx))
    return maze

############### GNERATE NORMAL MAZES ###############
class normalMazeBasic:
    def __init__(self,app,i):
        if i ==0:self.name = 'green'# 'kitchen garden'
        if i ==1:self.name = 'gold'# 'orchard'
        if i ==2:self.name = 'pink1'# 'flower garden'
        self.width = app.wallWidth
        self.length =app.wallLength
        self.nodes = [(i,j) for i in range(self.width) 
                     for j in range(self.length)]
def createNormalMaze(app,i):
    mazing = normalMazeBasic(app,i)
    getNodesC(app,mazing)
    neighborGeneration(app,mazing, False)
    app.walls = [(n1,n2) for n1 in app.nodesC 
                for n2 in app.neighbors[n1]]
    maze = []
    createRecMaze(app,mazing.nodes,maze)
    # magic number here
    y = app.height*1//3
    x =app.height*1//4
    randint = random.randint(0,1)
    if randint == "1":
        app.sunAndMoon.append(sunAndMoon(app,y,x,'sun'))
    else:
        app.sunAndMoon.append(sunAndMoon(app,y,x,'moon'))
    return (maze,mazing)

############### GNERATE THE CIRCLE MAZE ###############
'''
CODE NOTES
1) The circle maze consists of several layers:
    1.1 each layer has different number of nodes 
        - to make the node distance between layers roughly the same
    1.2 gates are generated between layers using backtracking
2) The user is initialized at the entrance to the whole maze
 '''
class mazeBasic:
    def __init__(self,layer):
        self.index = layer-1
        self.length =int(12*layer**(6/5)) #x
        self.angle = 360/self.length
        self.width = 8 #y 
        self.layer = (layer-1)*self.width
        self.nodes = [(i,j) for i in range(self.width) 
                     for j in range(self.length)]
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
def createCircleMaze(app,layer):
    mazing = mazeBasic(layer)
    getNodesC(app,mazing)
    neighborGeneration(app,mazing, True)
    app.walls = [(n1,n2) for n1 in app.nodesC 
                for n2 in app.neighbors[n1]]
    maze = []
    createRecMaze(app,mazing.nodes,maze)
    return (maze, mazing)
    ############### GNERATE THE GATES ###############
def creatDoors(app):              
    for (n1,n2) in app.circleMazeList[0][0]:
        exit = 0
        if (n1[0] == 0 and exit == 0):
            nNew = (n1[0]-1,n1[1])
            app.circleMazeList[0][0].append((n1,nNew))
            app.circleMazeList[0][1].nodes.append(nNew)
            app.origin = app.circleMazeList[0][0][-1][-1]
            nextEntrance = (0,0)
            for layerIndex in range(0,app.allLayers):
                mazing = app.circleMazeList[layerIndex][1]
                path = findTheWayOut(app,nextEntrance,layerIndex,path=None)
                # this exit is the entrance of next maze
                if path == None:
                    app.circleMazeList[0][0].remove((n1,nNew))
                else:
                    if layerIndex == app.allLayers-1:
                        currentExit = path[-1]
                        entrToTheWholeMaze = (path[-1][0]+1,path[-1][1])
                        app.circleMazeList[layerIndex][0].append(
                                (currentExit,entrToTheWholeMaze))
                        app.circleMazeList[layerIndex][1].nodes.append(
                                    entrToTheWholeMaze)
                        app.entrToTheWholeMaze = (path[-1][0],path[-1][1])
                        path.append(entrToTheWholeMaze)
                        app.theWayOut[layerIndex] = path
                        continue
                    currentLayerMaze = app.circleMazeList[layerIndex]
                    currentAngle=currentLayerMaze[1].angle
                    nextLayerMaze = app.circleMazeList[layerIndex+1]
                    nextAngle=nextLayerMaze[1].angle
                    x = roundHalfUp(path[-1][1]*currentAngle/nextAngle)
                    currentExit = (mazing.width,path[-1][1])
                    nextEntrance = (0,x)
                    pathToEntrace = (-1,x)
                    app.circleMazeList[layerIndex][0].append(
                                (currentExit,path[-1]))
                    app.circleMazeList[layerIndex][1].nodes.append(
                                                    currentExit)
                    app.circleMazeList[layerIndex+1][0].append(
                                (pathToEntrace,nextEntrance))
                    app.circleMazeList[layerIndex+1][1].nodes.append(
                                                    pathToEntrace)
                app.theWayOut[layerIndex] = path
            exit += 1
            break  
def findTheWayOut(app,nextEntrance,i,path):
    maze,mazing = app.circleMazeList[i]
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
################ MAZE ELEMENTS ##################
####### ROBIN WHO SHOWS THE WAY #######
class robin:
    def __init__(self):
        self.robinPath = [((-2,0),-1)]
        self.robinLocation = None
        self.robinPathLibry = {}
        self.robinDisappear = False
    def drawRobin(self,app,canvas):
        n1= self.robinLocation[0]
        i = self.robinLocation[1]
        maze,mazing = app.circleMazeList[i]
        color = 'green'
        drawCircleinCircleMaze(app,n1,mazing,canvas,color)
    def drawRobininSpring(self,app,canvas):
        node = self.robinLocation[0]
        drawRectangleinSpring(app,NodePosition(app,node,'c'),canvas,'green')
'''
CODE NOTES
1) robinAutoMove is one of the core parts of code:
    1.1 as the robin does not need to "win the game", there is no base case
        where the function would return. Thus, I decide to use nested dictionary 
        to record the index of the neighbors of robin's present location.
        - the main idea is make the robin move smartly in the maze,
            and won't be trapped at some point
    1.2 step = 2 is for no reason, just because it crashed once at step = 1 but 
        haven't crash since I change it to 2
 '''
def robinAutoMove(app,robi):
    if robi.robinLocation == None:
        while True:
            randLayer = random.randint(app.allLayers-2,app.allLayers-1) 
            randLocation = random.randint(0,
                    app.circleMazeList[randLayer][1].length-1)
            location = app.circleMazeList[randLayer][0][randLocation][0]
            if (location,randLayer) != app.MarryLocation:
                robi.robinLocation = (location,randLayer)
                robi.robinPath.append(robi.robinLocation)
                break
    else:
        (location,i) = robi.robinLocation
        if i == 0:
            robi.robinDisappear = True
        maze,mazing = app.circleMazeList[i]
        if robi.robinLocation in robi.robinPathLibry:
            if robi.robinPathLibry[robi.robinLocation] == {}:
                robi.robinPath.remove(robi.robinLocation)
                oldLocation = robi.robinLocation
                robi.robinLocation = robi.robinPath[-1]
                robi.robinPathLibry[robi.robinLocation].pop(oldLocation)
            else:
                #find the direction that has the minimum index
                min = 10**8 #magic number
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
                    # print('to upper level')
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
    ####### THE KEY THAT HAS BEEN BURRIED FOR TEN YEARS #######                       
class key:
    def __init__(self,app):
        self.show = False
        while True:
            randLayer = random.randint(1,app.allLayers-1) 
            randLocation = random.randint(0,
                    app.circleMazeList[randLayer][1].length-1)
            location = app.circleMazeList[randLayer][0][randLocation][0]
            if (location,randLayer) not in app.BenLocationList:
                self.location = (location,randLayer)
                break
    def drawKey(self,app,canvas):
        if not app.getKey:
            if self.show:
                n1= self.location[0]
                i = self.location[1]
                maze,mazing = app.circleMazeList[i]
                color = 'purple'
                drawCircleinCircleMaze(app,n1,mazing,canvas,color)
    def drawKeyinSpring(self,app,canvas):
        node = NodePosition(app,self.location[0],'c')
        drawRectangleinSpring(app,node,canvas,'purple')
    ####### BenWeathestaff, WHO IS HALF BAD AS HE LOOKS #######
class BenWeathestaff:
    def __init__(self,app,where):
        self.where = where
        self.visited = False
        if where == 'Door':
            randLayer = random.randint(1,app.allLayers-1) 
            randLocation = random.randint(0,
                    app.circleMazeList[randLayer][1].length-1)
            location = app.circleMazeList[randLayer][0][randLocation][0]
            self.location = (location,randLayer)
        else:
            randLocation = random.randint(0,
                    len(app.toOtherWalls[0])-1)
            self.location = app.toOtherWalls[0][randLocation][0]
    def drawBeninCircleMaze(self,app,canvas):
        n1= self.location[0]
        i = self.location[1]
        maze,mazing = app.circleMazeList[i]
        color = 'orange'
        drawCircleinCircleMaze(app,n1,mazing,canvas,color) 
    def drawBeninNormalMaze(self,app,canvas):
        n1 = self.location
        radius = 10
        color = 'orange'
        drawCircleinNormalMaze(app,n1,radius,canvas,color) 
    def drawBeninJIMI(self,app,canvas):
        node = self.location[0]
        for direction in [('ne','nw'),('se','sw'),('ne','se'),('nw','sw')]:
            fourFacesDoor(node,direction,app,canvas,app.JM.BenColor)         
    ############## MISTRESS MARRY, QUITE CONTRARY ##############  
def MarryMove(app,direction):
    if app.MarryLocation == None:
        app.MarryLocation = app.toOtherWalls[0][0][0]
    else:
        location = app.MarryLocation
        index = app.normalMazeList.index(app.toOtherWalls)
        for ben in app.BenLocationList:
            if ben.where == index:
                benPosition = ben.location
        newy,newx = (location[0]+direction[0],
                    location[1]+direction[1])
        newLocation = (newy,newx)
        if ((location,newLocation) in app.toOtherWalls[0] or 
            (newLocation,location) in app.toOtherWalls[0]):
            app.MarryLocation = newLocation
        if app.MarryLocation == benPosition:
            app.toOtherWalls = False
            app.MarryLocation = app.MarryReturn
            app.intoAfternoon = True
def MarryMoveInCircle(app,direction):
    if app.MarryLocation == None:
        app.MarryLocation = (app.entrToTheWholeMaze,app.allLayers-1)
    else:
        (location,i) = app.MarryLocation
        maze,mazing = app.circleMazeList[i]
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
        if app.MarryLocation == app.key.location and not app.getKey:
            app.keyGetText = True
            app.keyGetTime = app.time
        if (app.MarryLocation == (app.theWayOut[0][0],0)
            and app.getKey == True):
            app.intoAfternoon = False
            app.getToTheKeyHole = True
        for Ben in app.BenLocationList:
            if Ben.where == 'Door':
                if Ben.visited == False:
                    if app.MarryLocation == Ben.location:
                        app.MarryReturn = Ben.location
                        Ben.visited = True
                        randIndex = random.randint(0,len(app.normalMazeList)-1)
                        app.toOtherWalls = app.normalMazeList[randIndex]
                        createRoseWall(app)
                        app.MarryLocation = None
                        app.intoAfternoon = False
                        while True:
                            alreadyHaveBen = False
                            for ben in app.BenLocationList:
                                if ben.where == randIndex:
                                    alreadyHaveBen = True
                            if alreadyHaveBen == True:
                                break
                            app.BenLocationList.append(BenWeathestaff(app,randIndex))
                            break
                        MarryMove(app,(0,0))
    #################INTO OTHER GARDENS ################
def initializeGround(app):
    colorList = ['coral4','saddle brown','tomato4','burlywood4',
                'DarkGoldenrod4','bisque4','dim gray']
    for r in range(app.rows//2,app.rows):
        for c in range(app.cols):
            app.Cboard[r][c] = colorList[random.randint(0,6)] 
class sunAndMoon:
    def __init__(self,app,y,x,name):
        self.position = (y,x)
        self.name = name
        if name == 'sun':
            self.colorList = ['khaki','pale goldenrod','light yellow'] 
        elif name == 'moon':
            self.colorList = ['gray86','gray90','gray99'] 
        self.list =[]
        for i in range(0,3):
            (x1,y1)=(app.width//2*(i+1)//3,app.height//2*(i+1)//3)
            ddyList = cloud(app,x1,y1,app.height//2*(i+1)//3,-4)
            self.list.append((createRadius(app,ddyList),self.colorList[i]))
    def drawSun(self,app,canvas):
        for i in range(len(self.list)):
            clouds = self.list[i][0]
            color = self.list[i][1]
            for circle in clouds:
                ((x1, y1),r1)= circle
                if y1+r1>app.height//2:
                    continue
                canvas.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,fill = color,width=0)
    ################### INSTRUCTION ROSES #####################
class rose:
    def __init__(self,app,position,age = 1):
        self.position = position
        self.age = age
        self.petalnumber = 5
        self.disappear = False
        self.roseColor = [('orchid1','orchid2','orchid3'),
        ('VioletRed1','VioletRed2','VioletRed3'),('purple1','purple2','purple3')]
        self.createFlower()
    def createFlower(self):
        self.petalList = []
        if self.age > 2.5:
            self.disappear = True
        (y,x) = self.position
        randint = random.randint(0,len(self.roseColor)-1)
        colorList = self.roseColor[randint]
        k = self.petalnumber
        radius = 8+k
        for i in range(0,k+1):
            randint = random.randint(0,len(colorList)-1)
            color = colorList[randint]
            dx = radius*math.cos(math.radians(i/k*360))
            dy = radius*math.sin(math.radians(i/k*360))
            x,y = x+dx,y+dy
            r = random.randint(int(2*self.age),int(4*self.age*1.5))
            self.petalList.append(((x,y),r,color))
    def drawRose(self,canvas):
        if not self.disappear:
            for petal in self.petalList:
                ((x1, y1),r1,color)= petal
                canvas.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,fill = color,width=0)
def createRoseWall(app):
    app.roseList = []
    while len(app.roseList) <= 20:
        randint1 = random.randint(0,app.width-1)
        randint2 = random.randint(-app.height//2,app.height//3)
        position = (randint2,randint1)
        app.roseList.append(rose(app,position))
############### APP AND CONTROLLERS ###############
def appStarted(app,allLayers=3):
    ####### Maze Generation ########
    app.directions = {(1,0),(0,1),(-1,0),(0,-1)}
    app.margin = 10
    app.cellSize = 20
    app.wallWidth = (app.width)//(app.cellSize*2)
    app.wallLength = (app.height//2)//(app.cellSize*2)
    app.rows = app.wallLength*4
    app.cols = app.wallWidth*2
    app.Cboard = [['DarkSeaGreen3']*app.cols for i in range(app.rows)]
    app.ground = [['saddle brown']*app.cols for i in range(app.rows//2)]
    app.roseList =[]
    app.sunAndMoon = []
    app.normalMazeList = []
    for i in range(0,3):
        app.normalMazeList.append(createNormalMaze(app,i))
    app.allLayers = allLayers+1
    app.theWayOut = {} 
    app.circleMazeList = []
    app.interval = 10 #dmagic number, the distance between lines
    for i in range(1,app.allLayers+1):
        app.circleMazeList.append(createCircleMaze(app,i)) 
    creatDoors(app)
    createRoseWall(app)
    ####### FOLLOWING FEATURES ########
    ############Marry
    app.MarryMeetRobin = 0
    app.MarryLocation = None 
    MarryMoveInCircle(app,(0,0))
    ############robin
    rfootPrint = robin()
    app.robinsList = [rfootPrint]
    robinAutoMove(app,rfootPrint)
    ############Ben
    app.toOtherWalls = False
    app.BenLocationList =[]
    app.BenPlaces = app.allLayers-2
    for i in range(0,app.BenPlaces):
        app.BenLocationList.append(BenWeathestaff(app,'Door'))
    ############key
    app.getKey = False
    app.key = key(app)
    ##########JM
    app.JM= JIMIBasic(app,app.MarryLocation[1])
    app.wallinAfternoon = Wall(app)
    app.roads = []
    #####other
    app.solutionMode = False
    app.getToTheKeyHole = False # the Game is over
    app.keyShownText = False
    app.keyGetText = False
    app.intoAfternoon = False
    app.instruction = False
    app.time =0
    ##########Initialization functions
    getViewofPath(app)
    for path in app.seeMaze:
        app.roads.append(Roads(app,path))
    paintTheNightWithStar(app)
    sunSet(app)
    initializeGround(app)
#NEED BETTER NAME, a wraper for Marry move
def keyPressedMarry(app,directionC,directionN):
    if not app.toOtherWalls:
        MarryMoveInCircle(app,directionC)
    else:
        MarryMove(app,directionN)
    pass
def keyPressed(app,event):
    if event.key == 'Up':
        directionC,directionN = (0,1), (0,-1)
        keyPressedMarry(app,directionC,directionN)      
    elif event.key == 'Down':
        directionC,directionN = (0,-1),(0,1) 
        keyPressedMarry(app,directionC,directionN)
    elif event.key == 'Left':
        directionC,directionN = (-1,0),(-1,0) 
        keyPressedMarry(app,directionC,directionN)
    elif event.key == 'Right':
        directionC,directionN = (1,0),(1,0)
        keyPressedMarry(app,directionC,directionN) 
    elif event.key == 'R':
        app.solutionMode = not app.solutionMode
    elif event.key == 'I'and not app.toOtherWalls:
        app.intoAfternoon = not app.intoAfternoon
    elif event.key == 'N':
        app.instruction = not app.instruction
    elif event.key == 'G':
        appStarted(app,allLayers=3)
    if not app.toOtherWalls:
        app.JM= JIMIBasic(app,app.MarryLocation[1])
        app.wallinAfternoon = Wall(app)
        app.JM.center[1] = app.MarryLocation[0][1]+ app.JM.viewWidth-1
        app.JM.center[1] %= (app.JM.mazeLength)
        if app.JM.center[1] == 0:
            app.JM.center[1] = app.JM.mazeLength
        app.roadsinJM = []
        getViewofPath(app)
        for path in app.seeMaze:
            app.roadsinJM.append(Roads(app,path))
        app.MarryinSpring = MarryinSpring(app)
# timerfired is not organized
def timerFired(app):
    app.time += 1
    if app.time<160:
        app.instruction = True
    elif app.time == 160:
        app.instruction = False
    if app.time%5==1 and app.intoAfternoon:
        paintTheNightWithStar(app)
    if app.time%20 == 1 and app.intoAfternoon:
        sunSet(app)
    ranInt = random.randint(0,50)
    if ranInt == 0 and len(app.robinsList)<=5: # for testing reason set to 5
        # <=app.allLayers//3
        rfootPrint = robin()
        app.robinsList.append(rfootPrint)
        robinAutoMove(app,rfootPrint)
    elif ranInt ==1:
        randint = random.randint(0,len(app.robinsList)-1)
        app.robinsList[randint] = robin()
    for i in range(len(app.robinsList)):
        robi = app.robinsList[i]
        if robi.robinLocation == app.MarryLocation:
            app.MarryMeetRobin += 1
            if app.MarryMeetRobin >= 1 and not app.key.show:
                app.keyShownText = True
                app.keyShownTime = app.time
            while True:
                app.robinsList[i] = robin()
                if robi.robinLocation != app.MarryMeetRobin:
                    robinAutoMove(app,app.robinsList[i])
                    break
        robinAutoMove(app,robi)
    if app.instruction:
        for rose in app.roseList:
            randInt = random.randint(0,3)
            if randInt == 0:
                rose.position = (rose.position[0]+10,rose.position[1])
                if rose.position[0]>app.height:
                    createRoseWall(app)
            elif randInt == 1:
                rose.position = (rose.position[0]+5,rose.position[1])
                rose.age += .01
            rose.createFlower()
    if app.keyShownText and not app.key.show:
        if app.time >= app.keyShownTime+10:
            app.keyShownText = False
            app.key.show = True
    elif app.keyGetText and not app.getKey:
        if app.time >= app.keyGetTime+10:
            app.keyGetText = False
            app.getKey = True
        
##################### VIEW ##################### 
def getCellBound(app,row,col):
    Ux = col*app.cellSize
    Uy = row*app.cellSize
    Lx = (col+1)*app.cellSize
    Ly = (row+1)*app.cellSize
    return (Ux,Uy,Lx,Ly)
def drawCell(app,canvas,row,col,color):
    Ux,Uy,Lx,Ly = getCellBound(app,row,col)
    canvas.create_rectangle(Ux,Uy,Lx,Ly,fill =color,
                            outline='white', width=0.1)   
def drawCBoard(app,canvas):
    for r in range(app.rows):
        for c in range(app.cols):
            color = app.Cboard[r][c]
            drawCell(app,canvas,r,c,color)
def drawLittleMarry(app,canvas):
    if not app.toOtherWalls:
        (n1,i) = app.MarryLocation
        maze,mazing = app.circleMazeList[i]
        color = 'yellow'
        drawCircleinCircleMaze(app,n1,mazing,canvas,color)
    else:
        # 10 here is the radius
        n1 = app.MarryLocation
        radius = 10
        color = 'yellow'
        drawCircleinNormalMaze(app,n1,radius,canvas,color)
        pass
def drawCircleinNormalMaze(app,n1,radius,canvas,color):
    Ux = app.cellSize+n1[0]*app.cellSize*2-radius
    Uy = app.cellSize+n1[1]*app.cellSize*2-radius+app.height//2
    Lx = app.cellSize+n1[0]*app.cellSize*2+radius
    Ly = app.cellSize+n1[1]*app.cellSize*2+radius+app.height//2
    canvas.create_oval(Ux,Uy,Lx,Ly,fill = color)
def drawCircleinCircleMaze(app,n1,mazing,canvas,color):
    # 10 here the radius
    # 20 is the size of the text
    uy = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)-10 +20
    ux = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)-10
    ly = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)+10 +20
    lx = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)+10
    canvas.create_oval(ux,uy,lx,ly,fill = color)
    ########## board and final view ###########
def drawBoard(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = 'dark olive green')   
def drawPaths(app,canvas):
    if app.toOtherWalls:
        maze = app.toOtherWalls[0]
        color = app.toOtherWalls[1].name
        for (n1,n2) in maze:
            Ux = n1[0]*app.cellSize*2+app.cellSize
            Uy = n1[1]*app.cellSize*2+app.cellSize+app.height//2
            Lx = n2[0]*app.cellSize*2+app.cellSize
            Ly = n2[1]*app.cellSize*2+app.cellSize+app.height//2
            canvas.create_line(Ux,Uy,Lx,Ly,fill = color,width = 3)
    else:
        for mazeL in app.circleMazeList:
            (maze,mazing) = mazeL
            i = 0
            while i < len(maze):
                (n1,n2) = maze[i]
                # 20 is the size of the text
                uy = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
                    *mazing.angle))*app.interval + app.height//2+20)
                ux = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
                    *mazing.angle))*app.interval + app.width//2)
                ly = ((n2[0]+mazing.layer+1)* math.cos(math.radians(n2[1]
                    *mazing.angle))*app.interval + app.height//2+20)
                lx = ((n2[0]+mazing.layer+1)* math.sin(math.radians(n2[1]
                    *mazing.angle))*app.interval + app.width//2)
                color = 'light yellow'
                if app.solutionMode:
                    if (n1 in app.theWayOut[mazing.index] and
                        n2 in app.theWayOut[mazing.index]):
                       color = 'red'
                canvas.create_line(ux,uy,lx,ly,fill = color,width = 3)
                i+=1
def redrawAll(app,canvas):
    if app.time <80:
        canvas.create_rectangle(0,0,app.width,app.height,fill 
                    = 'light yellow')   
        canvas.create_text(app.width//2,app.height//2,
            text = '''THE SECRET GARDEN
            THE ROBIN WHO SHOWS THE WAY''',font = ('Times',24,'bold'),fill = 'green') 
    elif app.instruction:
        canvas.create_rectangle(0,0,app.width,app.height,fill = 'misty rose',width=0)
        for rose in app.roseList:
            rose.drawRose(canvas)
        canvas.create_text(app.width//2,app.height//2,text = '''\
                                                        The Secret Garden:
                A garden that has slept for ten years, Nobody has entered it since.
        The door to the garden is right at the middle of the maze. But where is the key?

                         The Key that has been Burried for TEN Years: \
(Purple block/Dot)
                    The key is burried and will not be shown on the maze at first.
                                Marry needs to find the key to open the door.

                                     Mistress Marry, Quite Contrary: \
(Yellow block/Dot)
        You can move Marry. Notice: The direction is anticlockwise in the cycle maze.

                                         Robin Who Shows the Way: \
(Green block/Dot)
        You can not control the Robins and they will fly away when you try to catch them.
            However to find the burried key, you need to meet the Robin at least once
                                                (be at the same position) 

                                       The leader of Ben Weatherstaff: \
(Orange block/Dot)
            Ben WeatherStaff works in the garden, he puts his leader everywhere. 
                             When your road is blocked by one ofhis leaders, 
                                      you will enter other gardens he works in.
        ''',font = ('Times',18,'bold'),fill = 'dark slate blue')
        canvas.create_text(app.width//6,app.height*7//8,text = '''
Press 'R' to show solution mode
Press 'I' to open or close the map of the maze
Press 'N' to open or close the instruction
Press 'G' to restart the game''',
font = ('Times',12,'bold'),fill = 'VioletRed4')
    elif app.intoAfternoon:
        if app.time%500>=400:
            startSky(app,canvas)
        else:            
            drawCloud(app,canvas)
        app.wallinAfternoon.drawWallinAfternoon(app,canvas)
        for road in app.roadsinJM:
            road.drawpolygram(app,canvas)
        for robinC in app.robinsList:
            if (robinC.robinLocation[0][0] == -1 or 
                    robinC.robinLocation[0][0] == app.JM.mazeWidth):
                continue
            if robinC.robinLocation[1] == app.MarryLocation[1]:
                if (app.MarryLocation[0][1]-1<=robinC.robinLocation[0][1] 
                <= app.MarryLocation[0][1]+app.JM.viewWidth):
                    robinC.drawRobininSpring(app,canvas)
        for ben in app.BenLocationList:
            if (type(ben.location[0])!=int and 
            ben.location[1]==app.MarryLocation[1]):
                if (app.MarryLocation[0][1]-1<=ben.location[0][1] 
                <= app.MarryLocation[0][1]+app.JM.viewWidth):
                    ben.drawBeninJIMI(app,canvas)
        if (app.MarryLocation[0][0] == -1 or 
            app.MarryLocation[0][0] == app.JM.mazeWidth):
            pass
        else:
            app.MarryinSpring.drawMarryinSpring(app,canvas)
        if (app.key.location[1]==app.MarryLocation[1] and app.key.show
        and not app.getKey):
            app.key.drawKeyinSpring(app,canvas)
        if app.keyShownText:
            canvas.create_text(app.width//2-50,app.height//2,text = '''
                The Robin has shown you the location of the key!
                        Open the Map and see where it is!''', anchor = 'c',
                font = ('Times',25,'bold'),fill = 'gold')
        elif app.keyGetText:
            canvas.create_text(app.width//2-50,app.height//2,text = '''
                         Congratulations you have get key!
                                Now lets head to the door!''', anchor = 'c',
                font = ('Times',25,'bold'),fill = 'gold')
    else:
        drawBoard(app,canvas)
        drawPaths(app,canvas)
        if app.getToTheKeyHole == True:
            canvas.create_rectangle(0,0,app.width,app.height,fill 
                    = 'light yellow')   
            canvas.create_text(app.width//2,app.height//2,
                text = 'THE DOOR OPENS...' ,font = ('Times',24,'bold'),fill = 'green')  
        else:
            if not app.toOtherWalls:
                for robi in app.robinsList:
                    if not robi.robinDisappear:
                        robi.drawRobin(app,canvas)
                app.key.drawKey(app,canvas)
                for ben in app.BenLocationList:
                    if ben.where == 'Door':
                        ben.drawBeninCircleMaze(app,canvas)
                # the number here is hardcode
                canvas.create_text(app.width//2-50,app.height*1//22,text = '''
                Map of The Secret Garden''', anchor = 'c',
                font = ('Times',25,'bold'),fill = 'VioletRed4')
            else:
                # not adjusted to change in app size
                index = app.normalMazeList.index(app.toOtherWalls)
                drawCBoard(app,canvas)
                backgroundColor = 'DarkSeaGreen3'
                canvas.create_rectangle(0,0,app.width,app.height//2,fill = backgroundColor,width=0)
                sunAndMoon = app.sunAndMoon[index]
                sunAndMoon.drawSun(app,canvas)
                drawPaths(app,canvas)
                for ben in app.BenLocationList:
                    if ben.where == index:
                        ben.drawBeninNormalMaze(app,canvas)
            drawLittleMarry(app,canvas)
runApp(width = 1200,height =800)