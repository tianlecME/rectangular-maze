'''
This file includes the code for the Main view of the Maze
'''
from cmu_112_graphics import *
import random,math
import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
################## JIMI BASIC ##################
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
        if app.MarryLocation[1] == 0:
            self.wallColor = 'dark olive green'
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
            node1nw = NodePosition(app,node1.xy,'nw')
            node1ne = NodePosition(app,node1.xy,'ne')
            node2sw = NodePosition(app,node2.xy,'sw')
            node2se = NodePosition(app,node2.xy,'se')
            canvas.create_polygon(node1nw.position,node1ne.position,
            node2se.position,node2sw.position,fill = app.JM.pathColor)
        elif node1.x == node2.x:
            if node1.y < node2.y:
                node1,node2 = node2,node1
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
            else:
                canvas.create_polygon(node1nw.position,node1sw.position,
                node2se.position,node2ne.position,fill = color)   
    ############### DRAW THE ROAD ###############
'''
CODE NOTES
1) The road in JIMI view is one of the core parts of code:
    1.1 the connection of the end and start of each maze 
        - the user can return to the view they came in after traveled through the whole circle
        - the related codes are spread out
    1.2 the usage of vanishing point
    1.3 transition between different layers
 '''
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
        if (((x >= node1[1] >=x - app.JM.face*app.JM.viewWidth) and 
            (x >= node2[1]>=x - app.JM.face*app.JM.viewWidth)) or 
            ((x2 >= node1[1]>=x2 - app.JM.face*app.JM.viewWidth) and 
            (x2 >= node2[1]>=x2 - app.JM.face*app.JM.viewWidth))):
            app.seeMaze.append(edges)
class MarryinSpring:
    def __init__(self,app):
        node = app.MarryLocation[0]
        self.Marry = NodePosition(app,node,'c')
    def drawMarryinSpring(self,app,canvas):
        node = self.Marry
        drawRectangleinSpring(app,node,canvas,app.JM.MarryColor)
    ############### BACKGROUND IN JIMI ###############
    ############### CLOUDS ###############
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
        'goldenrod','DarkOrange1','peach puff']
    else:
        app.colorList = ['LightSky Blue1','SlateBlue1', 'SkyBlue2','thistle1',
        'LightSky Blue2','RoyalBlue1','RoyalBlue2','light yellow']
    k = 1.5
    for i in range(30,450,50):
        k+=.2
        rndInt = random.randint(0,len(app.colorList)-1)
        color = app.colorList[rndInt]
        (x,y)=(app.width/2,app.height*3/5)
        app.cloudList.append((createRadius(app,cloud(app,x,y,i,k),
        withRadius = None),color))
        app.cloudList.append((createRadius(app,cloud(app,x,y,i,-k),
        withRadius = None),color))
        app.cloudList.append((createRadius(app,cloud(app,x,y,-i,k),
        withRadius = None),color))
        app.cloudList.append((createRadius(app,cloud(app,x,y,-i,-k),
        withRadius = None),color))
    app.cloudList=app.cloudList[::-1]
def distance(point1,point2):
    (x1, y1), (x2, y2) = point1,point2
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance
def cloud(app,x,y,dy,k):
    interpointnum = abs(dy//20)
    dx = k*dy
    ddyList =[]
    for i in range(0,interpointnum+3):
        ddy = dy*i/(interpointnum+2)
        ddx = (1-ddy/dy)*dx
        if (ddx,ddy) not in ddyList:
            ddyList.append((x-dx+ddx,y-dy+ddy))
    ddyList = sorted(ddyList)
    app.ddyList = ddyList
    return ddyList
'''
CODE NOTES
1) Generating clouds is one of the core parts of code:
    1.1 createRadius uses backtracking and may crash from time to time,
        though the frequence is quite low so far
 '''
def createRadius(app,ddyList,withRadius = None):
    if withRadius == None:
        withRadius = []
        point1,point2 = ddyList[0],ddyList[1]
        d = distance(point1,point2)
        r1 = random.randrange(int(d)-5,int(d))
        withRadius.append(((point1),r1))
        ddyList = ddyList[1:]
        return createRadius(app,ddyList,withRadius)
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
        result = createRadius(app,ddyList,withRadius)
        if result != None:
            return result
        else:
            if len(withRadius)<=2:
                withRadius =None
                ddyList = app.ddyList
                return createRadius(app,ddyList,withRadius)
            p1,p2 = withRadius.pop(-1)[0],withRadius.pop(-2)[0]
            ddyList = [p1,p2]+ddyList
            return createRadius(app,ddyList,withRadius)
def drawCloud(app,canvas):
    for i in range(len(app.cloudList)):
        cloud = app.cloudList[i][0]
        color = app.cloudList[i][1]
        for circle in cloud:
            ((x1, y1),r1)= circle
            canvas.create_oval(x1-r1,y1-r1,x1+r1,y1+r1,fill = color,width=0)
    ############### PAINT THE SKY WITH STARS ###############
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
    if app.MarryLocation[1] == 0:
            app.JM.wallColor = 'dark olive green'
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