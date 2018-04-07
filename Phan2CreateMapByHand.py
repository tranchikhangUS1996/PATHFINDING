import math
import sys
import pyglet
import CreateMapByHand
SIZE_BLOCK = 8*sys.getsizeof(int(0))
DOMAIN_X = 10000
DOMAIN_Y = 10000
HORIZONTAL = 0
VERTICAL = 1

#create Map
def CreateMapHor(Polygons,MyMap):
  for poly in Polygons:
    for p in poly:
      x,y = p
      Set(x,y,MyMap)

def createMapVer(Polygons,MyMap):
  for poly in Polygons:
    for p in poly:
      x,y = p
      Set(y,x,MyMap)

def creater(x):
  return 0

def initMap(width,height):
  MyMap = []
  for i in range(0,height):
    add = map(creater,range(0,width))
    MyMap.append(add)
  
  return MyMap

def Set(x,y,MyMap):
  block_pos = x/SIZE_BLOCK
  pos = x%SIZE_BLOCK
  sh=int(1)
  sh = sh<<pos
  MyMap[y][block_pos] = MyMap[y][block_pos]|sh

def see(x,y,MyMap,Type):
  if(Type==VERTICAL):
  	if(x<0 or x>DOMAIN_Y or y<0 or y>DOMAIN_X):
  		return True
  if(Type==HORIZONTAL):
  	if(x<0 or x>DOMAIN_X or y<0 or y>DOMAIN_Y):
  		return True

  block_pos = x/SIZE_BLOCK
  pos = x%SIZE_BLOCK
  temp = MyMap[y][block_pos]
  if(temp==0): return False
  ret = (temp>>pos)&1
  if(ret==1): return True
  return False



 #Class 
class Node:
	def __init__(self,parent,x,y,dx,dy,g,f):
		self.parent = parent
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.g = g
		self.f = f

#---------UMP POINT SEARCH IMPLEMENTATION---------------------

def search_horizontal(HorMap,current,dx,g,dist):
	#print('her cur ',current)
	x0,y0 = current
	node = []
	while(True):
		x1 = x0+dx
		x2 = x1+dx 
		# if (x,y) is obtacles
		if(see(x1,y0,HorMap,HORIZONTAL)):
			return None
		#outside area
		if(x1<0 or x1>DOMAIN_X or y0<0 or y0>DOMAIN_Y):
			return None

		if(x1 == g[0] and y0 == g[1]):
			return [(Node(None,x1,y0,0,0,dist+1,0))]

		block_pos = int(x1/SIZE_BLOCK)
		blockup = 0
		blockdown = 0
		if(y0+1<=DOMAIN_Y): 
			blockup = HorMap[y0+1][block_pos]

		block = HorMap[y0][block_pos]

		if(y0-1>=0):
			blockdown = HorMap[y0-1][block_pos]

		if(blockdown==0 and blockup==0 and block==0 and (int(g[0]/SIZE_BLOCK) != block_pos or math.fabs(g[1]-y0)>1)):
			if(dx>0):
				x0 = block_pos*SIZE_BLOCK + SIZE_BLOCK-1
			else:
				x0 = block_pos*SIZE_BLOCK
			#print('hor x0 sau cap nhat',dx,x0)
			dist+=(x0-x1-1)*dx
		
		else:
		# check forced neighbours
			if(see(x1,y0-1,HorMap,HORIZONTAL) and not see(x2,y0-1,HorMap,HORIZONTAL)):
				node.append(Node(None,x1,y0,dx,-1,dist+1,0))
			if(see(x1,y0+1,HorMap,HORIZONTAL) and not see(x2,y0+1,HorMap,HORIZONTAL)):
				node.append(Node(None,x1,y0,dx,1,dist+1,0))
			if(len(node)>0):
				node.append(Node(None,x1,y0,dx,0,dist+1,0))
				return node

			x0 = x1
			dist+=1

	return None

def search_vertical(VerMap,current,dy,g,dist):
	#print('ver current ',current)
	x0,y0 = current
	node = []
	while(True):	
		y1 = y0+dy
		y2 = y1+dy

		#check outside area
		if(x0<0 or x0>DOMAIN_X or y1<0 or y1>DOMAIN_Y):
			return None
		#check obtacle
		if(see(y1,x0,VerMap,VERTICAL)):
			return None
		#check goal
		if(x0==g[0] and y1==g[1]):
			return [Node(None,x0,y1,0,0,dist+1,0)]

		block_pos = int(y1/SIZE_BLOCK)
		blockup = 0
		blockdown = 0
		if(x0+1<=DOMAIN_X): 
			blockup = VerMap[x0+1][block_pos]

		block = VerMap[x0][block_pos]

		if(x0-1>=0):
			blockdown = VerMap[x0-1][block_pos]

		#print('ver',x0,y1,dy,block_pos,SIZE_BLOCK,block,blockdown,blockup)

		if(blockdown == 0 and blockup ==0 and block == 0 and (int(g[1]/SIZE_BLOCK) != block_pos or math.fabs(g[0]-x0)>1)):
			if(dy>0):
				y0 = block_pos*SIZE_BLOCK + SIZE_BLOCK-1
			else:
				y0 = block_pos*SIZE_BLOCK

			#print('ver y0 sau cap nhat',dy,y0)
			dist+=(y0-y1-1)*dy

		else:
			if(see(y1,x0-1,VerMap,VERTICAL) and not see(y2,x0-1,VerMap,VERTICAL)):
				node.append(Node(None,x0,y1,-1,dy,dist+1,0))
			if(see(y1,x0+1,VerMap,VERTICAL) and not see(y2,x0+1,VerMap,VERTICAL)):
				node.append(Node(None,x0,y1,1,dy,dist+1,0))
			if(len(node)>0):
				node.append(Node(None,x0,y1,0,dy,dist+1,0))
				return node

			dist+=1
			y0 = y1
	return None

def search_diagonal(VerMap,HorMap,current,dx,dy,g,dist):
	x0,y0 = current
	while(True):
		x= x0 + dx
		y= y0 + dy
		if(see(x,y,HorMap,HORIZONTAL)):
			return None
		if(x<0 or x>DOMAIN_X or y<0 or y>DOMAIN_Y):
			return None

		if(x==g[0] and y==g[1]):
			return [Node(None,x,y,0,0,dist+1,0)]

		node = []
		if(see(x-dx,y,HorMap,HORIZONTAL) and not see(x-dx,y+dy,HorMap,HORIZONTAL)):
			node.append(Node(None,x,y,-dx,dy,dist+1,0))

		if(see(x,y-dy,HorMap,HORIZONTAL) and not see(x+dx,y-dy,HorMap,HORIZONTAL)):
			node.append(Node(None,x,y,dx,-dy,dist+1,0))
		hdone,vdone = False,False
		if(len(node)==0):
			subnode = search_horizontal(HorMap,(x,y),dx,g,dist+1)
			hdone = True
			if(subnode is not None and len(subnode)>0):
				pd = Node(None,x,y,dx,0,dist+1,0)
				node.append(pd)
				for s in subnode:
					s.parent=pd
					node.append(s)
		if(len(node)==0):
			subnode = search_vertical(VerMap,(x,y),dy,g,dist+1)
			vdone = True
			if(subnode is not None and len(subnode)>0):
				pd = Node(None,x,y,0,dy,dist+1,0)
				node.append(pd)
				for s in subnode:
					s.parent = pd
					node.append(s)
		if(len(node)>0):
			if(not hdone):
				node.append(Node(None,x,y,dx,0,dist+1,0))
			if(not vdone):
				node.append(Node(None,x,y,0,dy,dist+1,0))
			node.append(Node(None,x,y,dx,dy,dist+1,0))
			return node
		dist+=1
		x0,y0 = x,y
	return None

def init(s,g,Opened):
	x,y =s
	for i in [-1,0,1]:
		for j in [-1,0,1]:
			if(i!=0 or j!=0):
				n = Node(None,x,y,i,j,0,myheuristic(s,g))
				Opened.append(n)

def getkey(x):
	return x.f

def have(a,List):
	for i in List:
		if(a.x==i.x and a.y==i.y and a.dx==i.dx and a.dy==i.dy):
			return i
	return None

def addToOPend(Opened,closed,add):
	if(add is None):
		return
	for a in add:
		#print('add ',a.x,a.y,a.dx,a.dy)
		#Opened.append(a)
		InOpen = have(a,Opened)
		InClosed = have(a,closed)
		if(InClosed is not None):
			if(a.g < InClosed.g):
				closed.remove(InClosed)
				InClosed =None
		if(InOpen is not None):
			if(a.g<InOpen.g):
				Opened.remove(InOpen)
				InOpen = None
		if(InOpen is None and InClosed is None):
			Opened.append(a)

def JPS(s,g,VerMap,HorMap):
	Opened = []
	closed = []
	goal = None
	init(s,g,Opened)
	while(len(Opened)>0):
		#print(len(Opened))
		p = min(Opened,key=getkey)
		Opened.remove(p)
		closed.append(p)
		if(p.x==g[0] and p.y==g[1]):
			goal = p
			break
		if(p.dx==0):
			#print('p ',p.x,p.y,p.dx,p.dy)
			myadd = search_vertical(VerMap,(p.x,p.y),p.dy,g,p.g)
			if(myadd is not None):
				for a in myadd:
					if a.parent==None:
						a.parent = p
					a.f = a.g + myheuristic((a.x,a.y),g)

			addToOPend(Opened,closed,myadd)
		if(p.dy==0):
			#print('p ',p.x,p.y,p.dx,p.dy)
			myadd = search_horizontal(HorMap,(p.x,p.y),p.dx,g,p.g)
			if(myadd is not None):
				for a in myadd:
					if a.parent==None:
						a.parent = p
					a.f = a.g + myheuristic((a.x,a.y),g)

			addToOPend(Opened,closed,myadd)
		if(p.dx!=0 and p.dy!=0):
			#print('p ',p.x,p.y,p.dx,p.dy)
			myadd = search_diagonal(VerMap,HorMap,(p.x,p.y),p.dx,p.dy,g,p.g)
			if(myadd is not None):
				#print('loi ',len(myadd))
				for a in myadd:
					if a.parent==None:
						a.parent = p
					a.f = a.g + myheuristic((a.x,a.y),g)

			addToOPend(Opened,closed,myadd)


	return makeResult(goal)

def makeResult(target):
	if(target==None):
		return [None,None]
	path = []
	cost = target.g
	while(target is not None):
		parent = target.parent
		if(parent is None):
			path.append((target.x,target.y))
			break

		dx,dy = -parent.dx,-parent.dy
		x,y = target.x,target.y
		#print('target ',x,y,parent.x,parent.y)
		while(x!=parent.x or y!=parent.y):
			path.append((x,y))
			x+=dx
			y+=dy
		target = parent
	path.reverse()
	return [path,cost]

def myheuristic(start,end):
	x,y = start
	x1,y1 = end
	ax,ay = x1-x,y1-y
	h = math.sqrt(ax*ax+ay*ay)
	return h

class StaticPathFindingWindow(pyglet.window.Window):

	def __init__(self,start,end,obstacles):
		super(StaticPathFindingWindow,self).__init__(visible=False)
		self.set_size(600,600)
		self.camx,self.camy = start
		self.cell = 10
		self.widthdraw = 600/self.cell
		self.heightdraw = 600/self.cell
		self.obstacles = obstacles
		mywidth = int(DOMAIN_X/SIZE_BLOCK)
		if(DOMAIN_X%SIZE_BLOCK!=0):
			mywidth+=1
		myheight = int(DOMAIN_Y/SIZE_BLOCK)
		if(DOMAIN_Y%SIZE_BLOCK!=0):
			myheight+=1
		self.start = start
		self.end = end
		self.VerMap = initMap(myheight,DOMAIN_X+1)
		self.HorMap = initMap(mywidth,DOMAIN_Y+1)
		createMapVer(obstacles,self.VerMap)
		CreateMapHor(obstacles,self.HorMap)
		self.path,self.dist = JPS(self.start,self.end,self.VerMap,self.HorMap)
		pyglet.clock.schedule_interval(self.update, 1.0/24.0)
	
	def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
		if buttons & pyglet.window.mouse.LEFT:
			self.camx -= dx
    		self.camy -= dy

	def update(self,dt):
		pass

	def on_draw(self):
		self.clear()
		if(self.path==None):
			label = pyglet.text.Label('No SoLuTion', 
									   font_name='Times New Roman', 
                          			   font_size=36,
                          			   x=self.camx+300, y=self.camy+300)
			label.draw()
		else:
			for i in range(self.heightdraw):
				pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(0,i*self.cell,600,i*self.cell)))
			for i in range(self.widthdraw):
				pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(i*self.cell,0,i*self.cell,600)))

			for obt in self.obstacles:
				n = len(obt)
				for point in obt:
					x,y = point
					x = x-self.camx + int(self.width/(2*self.cell))
					y = y-self.camy + int(self.height/(2*self.cell))
					x = x*self.cell
					y = y*self.cell
					pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i',(x,y,x+self.cell,y,x+self.cell,y+self.cell,x,y+self.cell)))

			green = (0,255,0,0,255,0,0,255,0,0,255,0)
			red = (255,0,0,255,0,0,255,0,0,255,0,0)
			blue = (0,0,255,0,0,255,0,0,255,0,0,255)
			for i in range(len(self.path)):
				color = green
				if(i==0):
					color = blue
				if(i==len(self.path)-1):
					color = red

				x2,y2 = self.path[i]
				x2 = x2-self.camx+int(self.width/(2*self.cell))
				y2 = y2-self.camy+int(self.height/(2*self.cell))
				x2 = x2*self.cell
				y2 = y2*self.cell
				pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(x2,y2+1,x2-1+self.cell,y2+1,x2-1+self.cell,y2+self.cell,x2,y2+self.cell)),('c3B',color))

	def run(self):
		self.set_visible()
		pyglet.app.run()

def runStatic(s,g,domx,domy):
	global DOMAIN_X
	global DOMAIN_Y
	DOMAIN_X = domx
	DOMAIN_Y = domy
	obtacles = []
	creater = CreateMapByHand.createMap(None,obtacles)
	obtacle = [obtacles]
	print('please wait')
	FS = StaticPathFindingWindow(s,g,obtacle)
	FS.run()

class RealTimeAStart:
	def __init__(self,StartPoint,GoalPoint):
		self.currentPoint = StartPoint
		self.GoalPoint = GoalPoint
		self.explored = {}

	def checkObstacles(self,point,obstacles):
		x,y = point
		for obt in obstacles:
			for p in obt:
				xp,yp = p
				if(xp==x and yp==y):
					return True
		return False

	def generate(self,obstacles,direction):
		ret = []
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if(direction[i+1][j+1]):
					if(not self.checkObstacles((self.currentPoint[0]+j,self.currentPoint[1]+i),obstacles)):
						ret.append((self.currentPoint[0]+j,self.currentPoint[1]+i))

		return ret

	def distances(self,p1,p2):
		x1,y1 = p1
		x2,y2 = p2
		dist = (x2-x1)**2 + (y2-y1)**2
		return math.sqrt(dist) 

	def Run(self,obstacles,direction):
		if(self.currentPoint[0]==self.GoalPoint[0] and self.currentPoint[1]==self.GoalPoint[1]):
			return

		GP = self.generate(obstacles,direction)
		n = len(GP)
		if(n==0):
			return

		fmin = self.distances(GP[0],self.currentPoint)
		if(str(GP[0]) in self.explored):
			fmin += self.explored[str(GP[0])]

		else:
			fmin += self.distances(GP[0],self.GoalPoint)

		fsecondmin = fmin
		nextx,nexty = GP[0]

		for i in range(1,n):
			name = str(GP[i])
			h = self.distances(GP[i],self.GoalPoint)
			if(name in self.explored):
				h = self.explored[name]
			f = self.distances(GP[i],self.currentPoint) + h
			if f<=fmin:
				fsecondmin = fmin
				fmin = f
				nextx,nexty = GP[i]

		CurName = str(self.currentPoint) 
		self.explored[CurName] = fsecondmin
		#if(CurName in self.explored):
			#hc = self.explored[CurName]
			#self.explored[CurName] = fsecondmin
		#else:
			#self.explored[CurName] = fsecondmin

		self.currentPoint = (nextx,nexty)

	def getCurrentPoint(self):
		return self.currentPoint

class RealTimeMyWindow(pyglet.window.Window):

    def __init__(self,obstacles,speed,dx,dy,Range,StartPoint,GoalPoint):
             super(RealTimeMyWindow,self).__init__(visible = False)
             self.cell = 10
             self.camx = int((600/self.cell)/2)
             self.camy = int((600/self.cell)/2)
             self.heightdraw = int(600/self.cell)
             self.widthdraw = int(600/self.cell)
             self.set_size(600,600)
             self.obstacles = obstacles
             self.GoalPoint = GoalPoint
             self.StartPoint = StartPoint
             self.direction = [[True,True,True],[True,True,True],[True,True,True]]
             self.RTA = RealTimeAStart(self.StartPoint,self.GoalPoint)
             self.NumChageStepdx = dx
             self.NumChageStepdy = dy
             self.Range = Range
             self.count = int(Range/2)
             self.xState, self.yState = self.RTA.getCurrentPoint()
             pyglet.clock.schedule_interval(self.update, 1.0/speed)

    def on_draw(self):
            self.clear()
            #draw obtacles
            for i in range(self.heightdraw):
            	pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(0,i*self.cell,600,i*self.cell)))

            for i in range(self.widthdraw):
				pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(i*self.cell,0,i*self.cell,600)))

            for obt in self.obstacles:
		        n = len(obt)
		        for point in obt:
				    x,y = point
				    x = x-self.camx + int(self.width/(2*self.cell))
				    y = y-self.camy + int(self.height/(2*self.cell))
				    x = x*self.cell
				    y = y*self.cell
				    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i',(x,y,x+self.cell,y,x+self.cell,y+self.cell,x,y+self.cell)))

			#draw current point
			green = (0,255,0,0,255,0,0,255,0,0,255,0)
			red = 	(255,0,0,255,0,0,255,0,0,255,0,0)
			blue =  (0,0,255,0,0,255,0,0,255,0,0,255)
            x2,y2 = self.xState,self.yState
            x2 = x2-self.camx+int(self.width/(2*self.cell))
            y2 = y2-self.camy+int(self.height/(2*self.cell))
            x2 = x2*self.cell
            y2 = y2*self.cell
            pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(x2,y2+1,x2-1+self.cell,y2+1,x2-1+self.cell,y2+self.cell,x2,y2+self.cell)),('c3B',green))
            xg,yg = self.GoalPoint
            xg = xg-self.camx + int(self.width/(2*self.cell))
            yg = yg-self.camy+int(self.height/(2*self.cell))
            xg*=self.cell
            yg*=self.cell
            pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xg,yg+1,xg-1+self.cell,yg+1,xg-1+self.cell,yg+self.cell,xg,yg+self.cell)),('c3B',red))
            xs,ys = self.StartPoint
            xs = xs-self.camx + int(self.width/(2*self.cell))
            ys = ys-self.camy+int(self.height/(2*self.cell))
            xs*=self.cell
            ys*=self.cell
            pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xs,ys+1,xs-1+self.cell,ys+1,xs-1+self.cell,ys+self.cell,xs,ys+self.cell)),('c3B',blue))


    def update(self,dt):
    	if(self.xState != self.GoalPoint[0] or self.yState!=self.GoalPoint[1]):
    	#update obtacle's moving
        	if(self.count==self.Range):
        		self.NumChageStepdx *= -1
        		self.NumChageStepdy *= -1
        		self.count = 0	

        	for i in [0,1,2]:
        		for j in [0,1,2]:
        			self.direction[i][j] = True


        	self.direction[1][1] = False
        	for obt in self.obstacles:
        		self.changeObtacles(self.NumChageStepdx,self.NumChageStepdy,obt)
        
        #update currentPoint
        	self.RTA.Run(self.obstacles,self.direction)
        	self.xState,self.yState = self.RTA.getCurrentPoint()
        	self.count = self.count+1

    def changeObtacles(self,dx,dy,obt):
    	temp = []
    	flag = False
    	for p in obt:
    		x,y = p
    		if(math.sqrt((x-self.xState)**2 + (y-self.yState)**2)<1.5):
    			temp.append((x,y))

    		p[0]+=dx
    		p[1]+=dy
    		if(p[0]==self.xState and p[1]==self.yState):
    			flag = True

    	if(flag):
    		self.direction[-dy+1][-dx+1] = False
    		for i in temp:
    			xi,yi= i
    			dxi = xi-self.xState+1
    			dyi = yi- self.yState+1
    			self.direction[dyi][dxi] = False


    def on_mouse_press(self,x, y, button, modifiers):
    	if button & pyglet.window.mouse.RIGHT:
			dx = int(x/self.cell) - int(self.width/(2*self.cell))
			dy = int(y/self.cell) - int(self.height/(2*self.cell))
			self.camx += dx
			self.camy += dy

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
    	if buttons & pyglet.window.mouse.LEFT:
    		self.camx -= dx
    		self.camy -= dy
    def run(self):
    	self.set_visible()
    	pyglet.app.run()
    def on_close(self):
    	self.close()

def run_real_time(S,G,Range,Speed,Dx,Dy,domx,domy):
	global DOMAIN_X
	global DOMAIN_Y
	DOMAIN_X = domx
	DOMAIN_Y = domy	
	obtacles = []
	creater = CreateMapByHand.createMap(None,obtacles)
	obtacle = [obtacles]
	print('please wait')
	RTW = RealTimeMyWindow(obtacle,Speed,Dx,Dy,Range,S,G)
	RTW.run()