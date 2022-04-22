from colorsys import rgb_to_hls
from cmu_112_graphics import *
import random,math,colorsys
#quotations:
# <script src="https://gist.github.com/nthistle/52cc#
# 86190266fd5673b06ebc68377281.js"></script>
# roundHalfUp from 15-112
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
def sunSet(app):
    app.cloudList=[]
    if 390>  app.time %500 >=380:
        app.colorList = ['dark violet', 'SlateBlue1','light pink',
        'goldenrod','medium violet red','MediumOrchid4']
    elif 400>  app.time %500 >=390:
        app.colorList = ['SlateBlue1', 'SlateBlue2','SlateBlue3',
        'SlateBlue4','RoyalBlue1','RoyalBlue2','RoyalBlue3','RoyalBlue4',
        'MediumOrchid4','dark violet']
    elif 150>  app.time %500 :
        app.colorList = ['khaki', 'light yellow','LightBlue1',
        'goldenrod','medium violet red','peach puff']
    else:
        app.colorList = ['LightSky Blue1','SlateBlue1', 'SkyBlue2','thistle1',
        'LightSky Blue2','RoyalBlue1','RoyalBlue2','light yellow']
    k = 1.5
    for i in range(30,450,50):
        k+=.2
        rndInt = random.randint(0,len(app.colorList)-1)
        color = app.colorList[rndInt]
        app.cloudList.append((createRadius(cloud(app,i,k),
        withRadius = None),color))
        app.cloudList.append((createRadius(cloud(app,i,-k),
        withRadius = None),color))
        app.cloudList.append((createRadius(cloud(app,-i,k),
        withRadius = None),color))
        app.cloudList.append((createRadius(cloud(app,-i,-k),
        withRadius = None),color))
    app.cloudList=app.cloudList[::-1]
def distance(point1,point2):
    (x1, y1), (x2, y2) = point1,point2
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance
def cloud(app,dy,k):
    (x,y)=(app.width/2,app.height*3/5)
    interpointnum = abs(dy//20)
    dx = k*dy
    ddyList =[]
    for i in range(0,interpointnum+3):
        ddy = dy*i/(interpointnum+2)
        ddx = (1-ddy/dy)*dx
        if (ddx,ddy) not in ddyList:
            ddyList.append((x-dx+ddx,y-dy+ddy))
    ddyList = sorted(ddyList)
    return ddyList
def createRadius(ddyList,withRadius = None,i = None):
    if i == None:
        i = copy.deepcopy(ddyList)
    if withRadius == None:
        withRadius = []
        point1,point2 = ddyList[0],ddyList[1]
        d = distance(point1,point2)
        r1 = random.randrange(int(d)-5,int(d))
        withRadius.append(((point1),r1))
        ddyList = ddyList[1:]
        return createRadius(ddyList,withRadius,i)
    elif ddyList == []:
        return withRadius
    else:
        point = ddyList[0]
        prevPoint = withRadius[-1][0]
        prevR = withRadius[-1][1]
        d = distance(point,prevPoint)
        if int(abs(prevR-2*d))+1>= int(prevR+d):
            return None
        r = random.randrange(int(abs(prevR-2*d))+1,int(prevR+d))
        withRadius.append(((point),r))
        ddyList = ddyList[1:]
        result = createRadius(ddyList,withRadius,i)
        if result != None:
            return result
        else:
            if len(withRadius)<=2:
                withRadius =None
                ddyList = i
                return createRadius(ddyList,withRadius)
            p1,p2 = withRadius.pop(-1)[0],withRadius.pop(-2)[0]
            ddyList = [p1,p2]+ddyList
            return createRadius(ddyList,withRadius)
def drawCloud(app,canvas):
    for i in range(len(app.cloudList)):
        cloud = app.cloudList[i][0]
        color = app.cloudList[i][1]
        for circle in cloud:
            ((x1, y1),r1)= circle
            canvas.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,fill = color,width=0)







class JIMIBasic:
    def __init__(self,app,index):
        self.mazing = app.circleMazeList[index][1]
        self.maze = app.circleMazeList[index][0]
        self.mazeLength = self.mazing.length
        self.mazeWidth = self.mazing.width
        self.viewWidth = 5
        self.face = +1

        self.vanishingPoint = (app.width/2,app.height*3/5) #x,y
        self.centerx = self.vanishingPoint[0]
        self.centery = self.vanishingPoint[1]
        self.wallUpAngle = 30
        self.wallDownAngle = 25
        self.unitAngle = (180- 2*self.wallDownAngle)/(2*self.mazeWidth-1)/2
        self.lefty = app.height - self.vanishingPoint[1]       
        self.center = [0,self.viewWidth] 

        self.pathColor = 'gray45'
        self.wallColor = 'gray30'
        self.doorColor = 'light yellow'
        self.MarryColor = 'yellow'
        self.BenColor = ['orange','orange2']
        
class Wall:
    def __init__ (self,app):
        upAlpha,downAlpha = app.JM.wallUpAngle,app.JM.wallDownAngle
        self.LeftUp = (0, roundHalfUp(app.JM.centery -app.JM.centerx*
        math.tan(math.radians(upAlpha))))
        self.RightUp = (app.width,roundHalfUp(app.JM.centery - app.JM.centerx*
        math.tan(math.radians(upAlpha))))
        self.LeftDown = (0, roundHalfUp(app.JM.centery + app.JM.centerx*
        math.tan(math.radians(downAlpha))))
        self.RightDown = (app.width, roundHalfUp(app.JM.centery + app.JM.centerx*
        math.tan(math.radians(downAlpha))))
        #5 is a magic number
        self.middle = (app.JM.centerx,app.JM.centery-5)        
    def drawWallinAfternoon(self,app,canvas):
        canvas.create_polygon(self.LeftUp,self.middle,self.RightUp,
        self.RightDown,app.JM.vanishingPoint,self.LeftDown,fill = app.JM.wallColor)
class NodePosition:
    def __init__(self,app,node,direction):
        x = app.JM.center[1]
        if x < app.JM.viewWidth:
            if node[1]//(app.JM.viewWidth+1) != 0:
               x += app.JM.mazeLength
        self.y,self.x = node[0],(x - node[1])
        self.xy = (node[0],node[1])#in maze not in afternoon of Spring
        self.d = app.JM.lefty*(2**(self.x+1)-1)/(2**(app.JM.viewWidth+1)-1)
        self.theta = (self.y-(app.JM.mazeWidth-1)/2)*4*app.JM.unitAngle
        if direction == 'c': pass
        elif direction == 'nw':
            self.d *= 9/10
            self.theta += app.JM.unitAngle
        elif direction == 'ne':
            self.d *= 9/10
            self.theta -= app.JM.unitAngle
        elif direction == 'sw':
            self.d *= 11/10
            self.theta += app.JM.unitAngle
        elif direction == 'se':
            self.d *= 11/10
            self.theta -= app.JM.unitAngle
        self.position = getXYinRoad(app,self.d,self.theta)
class MarryinSpring:
    def __init__(self,app):
        node = app.MarryLocation[0]
        self.Marry = NodePosition(app,node,'c')
    def drawMarryinSpring(self,app,canvas):
        node = self.Marry
        drawRectangleinSpring(app,node,canvas,app.JM.MarryColor)
class Roads:
    def __init__(self,app,path):
        node1,node2 = (NodePosition(app,path[0],'c'),
                      NodePosition(app,path[1],'c'))
        self.nodes = (node1,node2)
        self.position = (node1.position,node2.position)
    def drawpolygram(self,app,canvas):
        (node1,node2) = self.nodes
        if node1.y == node2.y:
            if node1.x > node2.x:
                node1,node2 = node2,node1
            #node1 take nw,ne node2 take sw se
            node1nw = NodePosition(app,node1.xy,'nw')
            node1ne = NodePosition(app,node1.xy,'ne')
            node2sw = NodePosition(app,node2.xy,'sw')
            node2se = NodePosition(app,node2.xy,'se')
            canvas.create_polygon(node1nw.position,node1ne.position,
            node2se.position,node2sw.position,fill = app.JM.pathColor)
        elif node1.x == node2.x:
            if node1.y < node2.y:
                node1,node2 = node2,node1
            #node1 take nw,sw node2 take ne se
            node1nw = NodePosition(app,node1.xy,'nw')
            node1sw = NodePosition(app,node1.xy,'sw')
            node1ne = NodePosition(app,node1.xy,'ne')
            node1se = NodePosition(app,node1.xy,'se')
            node2ne = NodePosition(app,node2.xy,'ne')
            node2se = NodePosition(app,node2.xy,'se')
            node2nw = NodePosition(app,node2.xy,'nw')
            node2sw = NodePosition(app,node2.xy,'sw')
            color = app.JM.pathColor
            if node2.y == -1:
                node2ne.position = (node1ne.position[0],app.JM.vanishingPoint[1])
                node2se.position = (node1se.position[0],app.JM.vanishingPoint[1])
                color = app.JM.doorColor
                canvas.create_polygon(node1ne.position,node1se.position,
            node2se.position,node2ne.position,fill = color)
            elif node1.y == app.JM.mazeWidth:
                node1nw.position = (node2nw.position[0],app.JM.vanishingPoint[1])
                node1sw.position = (node2sw.position[0],app.JM.vanishingPoint[1])
                color = app.JM.doorColor
                canvas.create_polygon(node1nw.position,node1sw.position,
            node2sw.position,node2nw.position,fill = color)
                # print('hey, door here')
            else:
                canvas.create_polygon(node1nw.position,node1sw.position,
                node2se.position,node2ne.position,fill = color)
def paintTheNightWithStar(app):
    app.stars = []
    for i in range(100):
        radius = random.randrange(1,3)
        if radius == 3:
            radius = 2.5
        y = random.randrange(0,app.JM.vanishingPoint[1])
        x = random.randrange(0,app.width)
        app.stars.append((x,y,radius))
def startSky(app,canvas):
    app.JM.pathColor = 'gray45'
    app.JM.wallColor = 'gray30'
    app.JM.doorColor = 'light yellow'
    app.JM.MarryColor = 'yellow'
    canvas.create_rectangle(0,0,app.width,app.JM.vanishingPoint[1],
        fill = 'RoyalBlue4')
    canvas.create_rectangle(0,app.JM.vanishingPoint[1],
    app.width,app.height,fill = 'RoyalBlue3')
    for star in app.stars:
        (x,y,radius) = star
        canvas.create_oval(x-radius,y-radius,x+radius,y+radius,
        fill = 'light yellow')
        # canvas.create_oval(x-radius,2*app.JM.vanishingPoint[1]-(
        # y-radius),(x+radius),app.JM.vanishingPoint[1]*2-(y+radius),
        # fill = 'khaki')
def getXYinRoad(app,d,theta):
    x = d*math.tan(math.radians(theta))+app.JM.centerx
    y = app.JM.centery+d
    return (x,y)
def fourFacesDoor(node,direction,app,canvas,colors):
    color = colors[0]
    if 'se' in direction:
        color = colors[1]
    nodene = NodePosition(app,node,direction[0])
    nodese = NodePosition(app,node,direction[1])
    node1 = NodePosition(app,(nodene.xy[0],nodene.xy[1]+1),direction[0])
    node2 = NodePosition(app,(nodese.xy[0],nodese.xy[1]+1),direction[0])
    x1 = (nodene.position[0],node1.position[1])
    x2 = (nodese.position[0],node2.position[1])
    # x1 = (nodene.position[0],app.JM.vanishingPoint[1])
    # y1 = (nodese.position[0],app.JM.vanishingPoint[1])
    canvas.create_polygon(x1,x2,
    nodese.position,nodene.position,fill = color)
def drawRectangleinSpring(app,node,canvas,color):
    nodenw = NodePosition(app,node.xy,'nw')
    nodene = NodePosition(app,node.xy,'ne')
    nodesw = NodePosition(app,node.xy,'sw')
    nodese = NodePosition(app,node.xy,'se')
    canvas.create_polygon(nodenw.position,nodene.position,
        nodese.position,nodesw.position,fill = color)
def getViewofPath(app):
    app.seeMaze = []
    x,x2 = app.JM.center[1],app.JM.center[1]
    if x < app.JM.viewWidth:
        x2 = app.JM.mazeLength+x
    for edges in app.JM.maze:
        node1,node2 = edges[0],edges[1]
        if node1[1] > node2[1]:
            node1,node2 = node2,node1
        if ((node1[1] == 0 and node2[1]==app.JM.mazeLength-1)
        and app.JM.center[1]<app.JM.viewWidth):
            node2 = list(node2)
            node2[1] = -1
            node2 = (node2[0],node2[1])
        # print('node1x,node2x',node1x,node2x)
        if (((x >= node1[1] >=x - app.JM.face*app.JM.viewWidth) and 
            (x >= node2[1]>=x - app.JM.face*app.JM.viewWidth)) or 
            ((x2 >= node1[1]>=x2 - app.JM.face*app.JM.viewWidth) and 
            (x2 >= node2[1]>=x2 - app.JM.face*app.JM.viewWidth))):
            app.seeMaze.append(edges)
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
    return (maze,mazing)
############### GNERATE THE CIRCLE MAZE ###############
class mazeBasic:
    def __init__(self,layer):
        self.index = layer-1
        self.length =int(10*layer**(6/5)) #x
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
                        app.entrToTheWholeMaze = entrToTheWholeMaze
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
                    # app.me = nextEntrance
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
############### OTHER FEATURE CLASSES ###############
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
        if app.MarryLocation == app.key.location:
            app.getKey = True
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
                        app.MarryLocation = None
                        app.intoAfternoon = False
                        ######## THE WAY I STORE BEN'S LOCATION IS NOT EFFICIENT######
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
############### APP AND CONTROLLERS ###############
def appStarted(app,allLayers=5):
    ####### Maze Generation ########
    app.directions = {(1,0),(0,1),(-1,0),(0,-1)}
    app.margin = 10
    app.cellSize = 20
    app.wallWidth = 25 # app.width//(app.cellSize*2)
    app.wallLength = 20# app.height//(app.cellSize*2)
    app.normalMazeList = []
    for i in range(0,3):
        app.normalMazeList.append(createNormalMaze(app,i))
    # print(app.normalMazeList)
    app.allLayers = allLayers+1
    app.theWayOut = {} 
    app.circleMazeList = []
    app.interval = 10 #don't change
    for i in range(1,app.allLayers+1):
        app.circleMazeList.append(createCircleMaze(app,i)) 
    creatDoors(app)
    ####### FOLLOWING FEATURES ########
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
    #####other
    app.solutionMode = False
    app.getToTheKeyHole = False # the Game is over
    # help debugging print
    app.time =0
    app.intoAfternoon = False
    app.JM= JIMIBasic(app,app.MarryLocation[1])
    app.wallinAfternoon = Wall(app)
    app.roads = []
    getViewofPath(app)
    for path in app.seeMaze:
        app.roads.append(Roads(app,path))
    paintTheNightWithStar(app)
    sunSet(app)
    # print(app.theWayOut)
    # print(app.key.location)
    # app.image = app.loadImage('the secrect garden')
def keyPressedMarry(app,directionC,directionN):
    if not app.toOtherWalls:
        MarryMoveInCircle(app,directionC)
    else:
        MarryMove(app,directionN)
    pass
def keyPressed(app,event):
    if event.key == 'Up':
        directionC,directionN = (-1,0), (0,-1)
        keyPressedMarry(app,directionC,directionN)      
    elif event.key == 'Down':
        directionC,directionN = (1,0),(0,1) 
        keyPressedMarry(app,directionC,directionN)
    elif event.key == 'Left':
        directionC,directionN = (0,-1),(-1,0) 
        keyPressedMarry(app,directionC,directionN)
    elif event.key == 'Right':
        directionC,directionN = (0,1),(1,0)
        keyPressedMarry(app,directionC,directionN) 
    elif event.key == 'R':
        app.solutionMode = not app.solutionMode
    elif event.key == 'I':
        app.intoAfternoon = not app.intoAfternoon
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
        # print(app.JM.center)
def timerFired(app):
    app.time +=1
    if app.time%20 == 1:
        sunSet(app)
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
##################### VIEW #####################    
def drawLittleMarry(app,canvas):
    if not app.toOtherWalls:
        (n1,i) = app.MarryLocation
        maze,mazing = app.circleMazeList[i]
        color = 'yellow'
        drawCircleinCircleMaze(app,n1,mazing,canvas,color)
    else:
        # 10 here is a magic number, the radius
        n1 = app.MarryLocation
        radius = 10
        color = 'yellow'
        drawCircleinNormalMaze(app,n1,radius,canvas,color)
        pass
def drawCircleinNormalMaze(app,n1,radius,canvas,color):
    Ux = app.margin+n1[0]*app.cellSize*2-radius
    Uy = app.margin+n1[1]*app.cellSize*2-radius
    Lx = app.margin+n1[0]*app.cellSize*2+radius
    Ly = app.margin+n1[1]*app.cellSize*2+radius
    canvas.create_oval(Ux,Uy,Lx,Ly,fill = color)
def drawCircleinCircleMaze(app,n1,mazing,canvas,color):
    # 10 here is a magic number, the radius
    uy = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)-10
    ux = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)-10
    ly = ((n1[0]+mazing.layer+1)* math.cos(math.radians(n1[1]
        *mazing.angle))*app.interval + app.height//2)+10
    lx = ((n1[0]+mazing.layer+1)* math.sin(math.radians(n1[1]
        *mazing.angle))*app.interval + app.width//2)+10
    canvas.create_oval(ux,uy,lx,ly,fill = color)
    ########## board and final view ###########
def drawBoard(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = 'white')   
def drawPaths(app,canvas):
    # print(app.toOtherWalls)
    if app.toOtherWalls:
        maze = app.toOtherWalls[0]
        color = app.toOtherWalls[1].name
        for (n1,n2) in maze:
            Ux = app.margin+n1[0]*app.cellSize*2
            Uy = app.margin+n1[1]*app.cellSize*2
            Lx = app.margin+n2[0]*app.cellSize*2
            Ly = app.margin+n2[1]*app.cellSize*2
            canvas.create_line(Ux,Uy,Lx,Ly,fill = color,width = 3)
    else:
        for mazeL in app.circleMazeList:
            (maze,mazing) = mazeL
            # print(mazing.index)
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
                if app.solutionMode:
                    if (n1 in app.theWayOut[mazing.index] and
                        n2 in app.theWayOut[mazing.index]):
                       color = 'red'
                canvas.create_line(ux,uy,lx,ly,fill = color,width = 3)
                i+=1
def redrawAll(app,canvas):
    # if app.time <40:
    #     canvas.create_rectangle(0,0,app.width,app.height,fill 
    #                 = 'light yellow')   
    #     canvas.create_text(app.width//2,app.height//2,
    #         text = 'THE SECRET GARDEN',font = ('Times',24,'bold'),fill = 'green') 
    # elif app.time <60:
    #     canvas.create_rectangle(0,0,app.width,app.height,fill 
    #                 = 'light yellow')   
    #     canvas.create_text(app.width//2,app.height//2,
    #         text = 'THE ROBIN WHO SHOWS THE WAY',font = ('Times',24,'bold'),
    #         fill = 'Green') 
    # elif 60<=app.time <100:
    #     canvas.create_rectangle(0,0,app.width,app.height,fill 
    #                 = 'light yellow')   
    #     canvas.create_text(app.width//2,app.height//2,
    #         text = '''      Marry meets the robin and find out where the key is hiden
    #             Ben Weathestaff works in three other gardens
    # Can Marry find the key and open the door to the secrect garden?''',
    #         font = ('Times',24,'bold'),
    #         fill = 'Green') 
    if app.intoAfternoon:
        if app.time%500>=400:
            startSky(app,canvas)
        else:            
            drawCloud(app,canvas)
        app.wallinAfternoon.drawWallinAfternoon(app,canvas)
        for road in app.roadsinJM:
            road.drawpolygram(app,canvas)
        for robinC in app.robinsList:
            if robinC.robinLocation[1] == app.MarryLocation[1]:
                if (app.MarryLocation[0][1]-1<=robinC.robinLocation[0][1] 
                <= app.MarryLocation[0][1]+5):
                    robinC.drawRobininSpring(app,canvas)
        for ben in app.BenLocationList:
            if (type(ben.location[0])!=int and 
            ben.location[1]==app.MarryLocation[1]):
                if (app.MarryLocation[0][1]-1<=ben.location[0][1] 
                <= app.MarryLocation[0][1]+5):
                    ben.drawBeninJIMI(app,canvas)
        app.MarryinSpring.drawMarryinSpring(app,canvas)
        if (app.key.location[1]==app.MarryLocation[1] and app.key.show
        and not app.getKey):
            app.key.drawKeyinSpring(app,canvas)
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
            else:
                index = app.normalMazeList.index(app.toOtherWalls)
                for ben in app.BenLocationList:
                    if ben.where == index:
                        ben.drawBeninNormalMaze(app,canvas)
            drawLittleMarry(app,canvas)
runApp(width = 1000,height =800)