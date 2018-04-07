#########################################################################
#------------------------------------------------------------------------
#------------------------------FIT-HCMUS---------------------------------
#---------------------------Tran Chi Khang-------------------------------
#------------------------------1512237-----------------------------------
#----------------------------DA-CSTTNT-PHAN 2-----------------------------------

import math
import sys
import pyglet
SIZE_BLOCK = 8*sys.getsizeof(int(0))
DOMAIN_X = 10000
DOMAIN_Y = 10000
HORIZONTAL = 0
VERTICAL = 1

#create Map
#dat vat can cho map theo chieu ngang
def CreateMapHor(obstacles,MyMap):
	for obt in obstacles:
		xm = obt.getminx()
		xma = obt.getmaxx()
		ym = obt.getminy()
		yma= obt.getmaxy()
		for i in range(ym,yma+1):
			for j in range(xm,xma+1):
				if(obt.PIP((j,i))):
					Set(j,i,MyMap)
#dat vat can theo chieu doc
def createMapVer(obstacles,MyMap):
	for obt in obstacles:
		xm = obt.getminx()
		xma = obt.getmaxx()
		ym = obt.getminy()
		yma= obt.getmaxy()
		for i in range(ym,yma+1):
			for j in range(xm,xma+1):
				if(obt.PIP((j,i))):
					Set(i,j,MyMap)

def creater(x):
  return 0
#khoi tao map
def initMap(width,height):
  MyMap = []
  for i in range(0,height):
    add = map(creater,range(0,width))
    MyMap.append(add)
  
  return MyMap
# dat diem x,y la vat can vao map
def Set(x,y,MyMap):
  block_pos = x/SIZE_BLOCK
  pos = x%SIZE_BLOCK
  sh=int(1)
  sh = sh<<pos
  MyMap[y][block_pos] = MyMap[y][block_pos]|sh
#kiem tra diem x,y co nam trong Mymap
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

#---------JUMP POINT SEARCH IMPLEMENTATION---------------------
# danh gia heuristic 
def myheuristic(start,end):
	x,y = start
	x1,y1 = end
	ax,ay = x1-x,y1-y
	h = math.sqrt(ax*ax+ay*ay)
	return h
#ham do theo chieu ngang cuaJPS
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
#ham do theo chieu doc cua JPS
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
#ham do cheo cua JPS
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
#khoi tao nut bat dau
def init(s,g,Opened):
	x,y =s
	for i in [-1,0,1]:
		for j in [-1,0,1]:
			if(i!=0 or j!=0):
				n = Node(None,x,y,i,j,0,myheuristic(s,g))
				Opened.append(n)
#tra gia tri cho viec lay min
def getkey(x):
	return x.f
#kiem tra co chua Node a trong list
def have(a,List):
	for i in List:
		if(a.x==i.x and a.y==i.y and a.dx==i.dx and a.dy==i.dy):
			return i
	return None
#chen vao tap mo rong cua JPS
def addToOPend(Opened,closed,add):
	if(add is None):
		return
	for a in add:

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
# trien khai thuat toan JPS
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
#chuyen cac diem nhay thanh duong di tu start den goal (dung cho ban do luoi)
def makeResultGrid(path):
	ret = []
	if(path is not None):
		for i in range(0,len(path)-1):
			p1 = path[i]
			p2 = path[i+1]
			dx,dy = p2[0]-p1[0],p2[1]-p1[1]
			daudx = 1
			daudy = 1
			if(dx<0):
				daudx = -1
			if(dy<0):
				daudy = -1
			if(dx==0):
				dy = int(dy/dy)
			elif(dy==0):
				dx = int(dx/dx)
			else:
				dx = int(dx/dx)
				dy = int(dy/dy)
			dx*=daudx
			dy*=daudy
			while(p1[0]!=p2[0] or p1[1]!=p2[1]):
				ret.append(p1)
				p1 = [p1[0]+dx,p1[1]+dy]
			if(i==len(path)-2):
				ret.append(p2)

	return ret
#tao ket qua tra ve gom cac diem nhay va so o di chuyen
def makeResult(target):
	if(target==None):
		return [None,None]
	path = []
	cost = 0
	while(target is not None):
		path.append([target.x,target.y])
		target = target.parent
	path.reverse()
	for i in range(0,len(path)-1):
		p1 = path[i]
		p2 = path[i+1]
		cost += math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
	return [path,cost]
 # cua so do hoa hien thi cho truong hop ve graphics
class StaticPathFindingWindow(pyglet.window.Window):

	def __init__(self,start,end,obstacles):
		super(StaticPathFindingWindow,self).__init__(visible=False)
		self.set_size(600,600)
		self.camx,self.camy = start
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
		if(self.path is None):
			label = pyglet.text.Label('No SoLuTion', 
									   font_name='Times New Roman', 
                          			   font_size=36,
                          			   x=self.camx+300, y=self.camy+300)
			label.draw()
		
		for obstacle in self.obstacles:
			polygon = obstacle.get()
			n = len(polygon)
			for i in range(0,n,2):
				polygon[i] -= self.camx
				polygon[i+1]-= self.camy
			n=n/2
			pyglet.graphics.draw(n, pyglet.gl.GL_POLYGON,('v2i', polygon))

		green =(0,255,0,0,255,0)
		red = (255,0,0,255,0,0)
		blue = (0,0,255,0,0,255)
		xs,ys = self.start
		xe,ye = self.end
		xs -=self.camx
		ys -= self.camy
		xe -= self.camx
		ye -= self.camy
		pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xs-3,ys-3,xs+3,ys-3,xs+3,ys+3,xs-3,ys+3)),('c3B',(0,0,255,0,0,255,0,0,255,0,0,255)))
		pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xe-3,ye-3,xe+3,ye-3,xe+3,ye+3,xe-3,ye+3)),('c3B',(255,0,0,255,0,0,255,0,0,255,0,0)))
		if(self.path is not None):
			s = self.path[0]
			for i in range(1,len(self.path)):
			    color = green
			    if(i==1):
				    color = blue
			    if(i==len(self.path)-1):
				    color = red
			    x,y = s
			    x-=self.camx
			    y-=self.camy
			    x2,y2 = self.path[i]
			    x2 = x2-self.camx
			    y2 = y2-self.camy
			    pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(x,y,x2,y2)),('c3B',color))
			    s = self.path[i]


	def run(self):
		self.set_visible()
		pyglet.app.run()
# cua so do hoa ve duoi dang o luoi
class StaticPathFindingWindowonGrid(pyglet.window.Window):

	def __init__(self,start,end,obstaclesObj):
		super(StaticPathFindingWindowonGrid,self).__init__(visible=False)
		self.set_size(600,600)
		self.camx,self.camy = start
		self.cell = 10
		self.widthdraw = 600/self.cell
		self.heightdraw = 600/self.cell
		self.obstacles = []
		for obt in obstaclesObj:
			self.obstacles.append(obt.getPoints())

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
		createMapVer(obstaclesObj,self.VerMap)
		CreateMapHor(obstaclesObj,self.HorMap)
		self.path,self.dist = JPS(self.start,self.end,self.VerMap,self.HorMap)
		self.path = makeResultGrid(self.path)
		pyglet.clock.schedule_interval(self.update, 1.0/24.0)
	
	def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
		if buttons & pyglet.window.mouse.LEFT:
			self.camx -= dx
    		self.camy -= dy

	def update(self,dt):
		pass

	def on_draw(self):
		self.clear()
		if(self.path is None):
			label = pyglet.text.Label('No SoLuTion', 
									   font_name='Times New Roman', 
                          			   font_size=36,
                          			   x=self.camx+300, y=self.camy+300)
			label.draw()
		
		for i in range(self.heightdraw):
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(0,i*self.cell,self.width,i*self.cell)))
		for i in range(self.widthdraw):
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(i*self.cell,0,i*self.cell,self.height)))

		for obt in self.obstacles:
			n = len(obt)
			for point in obt:
				x,y = point
				x = x-self.camx + int(self.width/(2*self.cell))
				y = y-self.camy + int(self.height/(2*self.cell))
				if(x<0 or x>self.widthdraw or y<0 or y>self.heightdraw):
					continue

				x = x*self.cell
				y = y*self.cell
				pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i',(x,y,x+self.cell,y,x+self.cell,y+self.cell,x,y+self.cell)))

		green = (0,255,0,0,255,0,0,255,0,0,255,0)
		red = (255,0,0,255,0,0,255,0,0,255,0,0)
		blue = (0,0,255,0,0,255,0,0,255,0,0,255)
		xs,ys =self.start
		xe,ye = self.end
		xs = xs-self.camx+int(self.width/(2*self.cell))
		ys = ys-self.camy+int(self.height/(2*self.cell))
		xs*=self.cell
		ys*=self.cell
		xe = xe-self.camx+int(self.width/(2*self.cell))
		ye = ye-self.camy+int(self.height/(2*self.cell))
		xe*=self.cell
		ye*=self.cell
		pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xs,ys+1,xs-1+self.cell,ys+1,xs-1+self.cell,ys+self.cell,xs,ys+self.cell)),('c3B',blue))
		pyglet.graphics.draw(4,pyglet.gl.GL_POLYGON,('v2i',(xe,ye+1,xe-1+self.cell,ye+1,xe-1+self.cell,ye+self.cell,xe,ye+self.cell)),('c3B',red))
		if(self.path is not None):
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

	def on_close(self):
		self.close()

#----------------LOP QUAN LY VAT CAN----------------------
def getxforobt(x):
	return x[0]

def getyforobt(x):
	return x[1]

class Obstacle:
	def __init__(self,polygon):
		self.polygon = polygon
	# kiem tra point trong polygon
	def PIP(self,point):
		algle = 0.0
		n = len(self.polygon)
		x,y = point
		px1,py1 = self.polygon[0]
		for i in range(n):
			px2,py2 = self.polygon[(i+1)%n]
			if(x==px1 and y==py1 or x==px2 and y==py2):
				return True
			ax = px1-x
			ay = py1-y
			bx = px2-x
			by = py2-y
			multi = ax*bx+ay*by
			multidist = math.sqrt(ax*ax+ay*ay)*math.sqrt(bx*bx+by*by)
			Cos = multi/multidist
			if(Cos>1.0):
			  Cos = 1.0
			
			if(Cos<=-1.0):
				return True
			
			algle += math.acos(Cos)
			px1,py1 = px2,py2
    
		if(math.fabs(algle - 2*math.pi)<0.00001): return True
		return False
	#dich chuyen polygon
	def change(self,hx,hy,direction,x,y):
		n = len(self.polygon)

		temp = []
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if(self.PIP((x+j,y+i))):
					temp.append((x+j,y+i))
		for i in range(n):
			self.polygon[i][0]+=hx
			self.polygon[i][1]+=hy
		if (self.PIP((x,y))):
			for p in temp:
				dx,dy = p[0]-x,p[1]-y
				direction[dx+1][dy+1] = False


	#tra ve tap cac diem
	def get(self):
		ret = []
		for i in self.polygon:
			ret.append(i[0])
			ret.append(i[1])
		return ret

	def getminx(self):
		x = min(self.polygon,key=getxforobt)
		return x[0]
	def getmaxx(self):
		x = max(self.polygon,key=getxforobt)
		return x[0]
	def getminy(self):
		y = min(self.polygon,key=getyforobt)
		return y[1]
	def getmaxy(self):
		y = max(self.polygon,key=getyforobt)
		return y[1]
	# tra ve cac diem trong polygon
	def getPoints(self):
		ret = []
		xm = self.getminx()
		xmax = self.getmaxx()
		ym = self.getminy()
		ymax= self.getmaxy()
		for i in range(ym,ymax+1):
			for j in range(xm,xmax+1):
				if(self.PIP((j,i))):
					ret.append([j,i])
		return ret
#---------------PHAN XU LY REAL TIME----------------------
class RealTimeAStart:
	def __init__(self,StartPoint,GoalPoint):
		self.currenPoint = StartPoint
		self.GoalPoint = GoalPoint
		self.explored = {}
	#tra ve cac neighbour
	def generate(self,obstacles,direction):
		ret = []
		for i in [-1,0,1]:
			for j in [-1,0,1]:
				if(direction[i+1][j+1]):
					flag = True
					for a in range(len(obstacles)):
					  if(obstacles[a].PIP((self.currenPoint[0]+j,self.currenPoint[1]+i))):
							flag = False
							break
					
					if(flag):
					  	ret.append((self.currenPoint[0]+j,self.currenPoint[1]+i))
		return ret
	#do khoang cach p1 p2
	def distances(self,p1,p2):
		x1,y1 = p1
		x2,y2 = p2
		dist = (x2-x1)**2 + (y2-y1)**2
		return math.sqrt(dist) 

	#dich chuyen den buoc moi
	def Run(self,obstacles,direction):
		if(self.currenPoint[0]==self.GoalPoint[0] and self.currenPoint[1]==self.GoalPoint[1]):
			return

		GP = self.generate(obstacles,direction)
		n = len(GP)
		if(n==0):
			return

		fmin = self.distances(GP[0],self.currenPoint)
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
			f = self.distances(GP[i],self.currenPoint) + h
			if f<fmin:
				fsecondmin = fmin
				fmin = f
				nextx,nexty = GP[i]

		CurName = str(self.currenPoint) 
		if(CurName in self.explored):
			hc = self.explored[CurName]
			self.explored[CurName] = hc + fsecondmin
		else:
			self.explored[CurName] = fsecondmin

		self.currenPoint = (nextx,nexty)

	# tra ve diem hien tai
	def getCurrentPoint(self):
		return self.currenPoint
#cua so do hoa ve graphics
class RealTimeMyWindow(pyglet.window.Window):

    def __init__(self,RTA,obstacles,speed,Range,dx,dy,StartPoint,GoalPoint):
             super(RealTimeMyWindow,self).__init__(visible = False)
             self.camx = 300 # tam camera 
             self.camy = 300 # tam camere
             self.set_size(600,600)
             self.RTA = RTA
             self.obstacles = obstacles
             self.NumChageStep = 1
             self.Range = Range
             self.count = int(Range/2)
             self.xState, self.yState = RTA.getCurrentPoint()
             self.camx = self.xState
             self.camy = self.yState
             self.direction = [[True,True,True],[True,True,True],[True,True,True]]
             self.GoalPoint = GoalPoint
             self.StartPoint = StartPoint
             self.dx = dx
             self.dy = dy
             pyglet.clock.schedule_interval(self.update, 1.0/speed)

    def on_draw(self):
            self.clear()
            #draw obtacles
            for obstacle in self.obstacles:
            	polygon = obstacle.get()
            	n = len(polygon)
            	for i in range(0,n,2):
            		polygon[i] -= self.camx
            		polygon[i+1]-= self.camy
            	n=n/2
            	pyglet.graphics.draw(n, pyglet.gl.GL_POLYGON,('v2i', polygon))
			#draw current point
            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i',(self.GoalPoint[0]-5-self.camx,
            													 self.GoalPoint[1]-5-self.camy,
            													 self.GoalPoint[0]-5-self.camx,
            													 self.GoalPoint[1]+5-self.camy,
            													 self.GoalPoint[0]+5-self.camx,
            													 self.GoalPoint[1]+5-self.camy,
            													 self.GoalPoint[0]+5-self.camx,
            													 self.GoalPoint[1]-5-self.camy)),('c3B',(0,255,0,0,255,0,0,255,0,0,255,0)))

            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i', (self.StartPoint[0]-5-self.camx,
            													 self.StartPoint[1]-5-self.camy,
            													 self.StartPoint[0]-5-self.camx,
            													 self.StartPoint[1]+5-self.camy,
            													 self.StartPoint[0]+5-self.camx,
            													 self.StartPoint[1]+5-self.camy,
            													 self.StartPoint[0]+5-self.camx,
            													 self.StartPoint[1]-5-self.camy)),('c3B',(255,0,0,255,0,0,255,0,0,255,0,0)))
            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i', (self.xState-5-self.camx,
            													  self.yState-5-self.camy,
            													  self.xState-5-self.camx,
            													  self.yState+5-self.camy,
            													  self.xState+5-self.camx,
            													  self.yState+5-self.camy,
            													  self.xState+5-self.camx,
            													  self.yState-5-self.camy)),('c3B',(0,0,255,0,0,255,0,0,255,0,0,255)))

    def update(self,dt):
    	#update obtacle's moving
        if(self.count==self.Range):
        	self.NumChageStep *= -1
        	self.count = 0	

        for i in [0,1,2]:
        	for j in [0,1,2]:
        		self.direction[i][j] = True
        self.direction[1][1] = False
        for obt in self.obstacles:
        	obt.change(self.NumChageStep*self.dx,self.NumChageStep*self.dy,self.direction,self.xState,self.yState)
        #update currentPoint
        self.RTA.Run(self.obstacles,self.direction)
        self.xState,self.yState = self.RTA.getCurrentPoint()
        self.count = self.count+1

    def on_mouse_press(self,x, y, button, modifiers):
    	if button & pyglet.window.mouse.RIGHT:
			dx = x-300
			dy = y-300
			self.camx += dx
			self.camy += dy

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
    	if buttons & pyglet.window.mouse.LEFT:
    		self.camx -= dx
    		self.camy -= dy
    def run(self):
    	self.set_visible()
    	pyglet.app.run()
# cua so do hoa ve duoi dang o luoi
class RealTimeMyWindowOnGrid(pyglet.window.Window):

    def __init__(self,obstaclesObj,speed,dx,dy,Range,StartPoint,GoalPoint):
             super(RealTimeMyWindowOnGrid,self).__init__(visible = False)
             self.cell = 10
             self.camx = int((600/self.cell)/2)
             self.camy = int((600/self.cell)/2)
             self.heightdraw = int(600/self.cell)
             self.widthdraw = int(600/self.cell)
             self.set_size(600,600)
             self.obstaclesObj = obstaclesObj
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
            	pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(0,i*self.cell,self.width,i*self.cell)))

            for i in range(self.widthdraw):
				pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(i*self.cell,0,i*self.cell,self.height)))

            for obt in self.obstaclesObj:
		        for point in obt.getPoints():
				    x,y = point
				    x = x-self.camx + int(self.width/(2*self.cell))
				    y = y-self.camy + int(self.height/(2*self.cell))
				    if(x<0 or x>self.widthdraw or y<0 or y>self.heightdraw):
				    	continue

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
        	for obt in self.obstaclesObj:
        		obt.change(self.NumChageStepdx,self.NumChageStepdy,self.direction,self.xState,self.yState)
        
        #update currentPoint
        	self.RTA.Run(self.obstaclesObj,self.direction)
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
#--------------------CAC HAM XU LY--------------------
# mo file voi link
def openFile(link):
	Reader = open(link,"r")
	if Reader is None: return[None,None,None,None,None]
	[Domx,Domy] = Reader.readline().strip().split()
	global DOMAIN_X 
	global DOMAIN_Y
	DOMAIN_X = int(Domx)
	DOMAIN_Y = int(Domy)
	n = int(Reader.readline().strip())
	[xs,ys] = Reader.readline().strip().split()
	[xg,yg] = Reader.readline().strip().split()
	[sdx,sdy] =  Reader.readline().strip().split()
	[sspeed,sRange] = Reader.readline().strip().split()
	s = [int(xs),int(ys)]
	g = [int(xg),int(yg)]
	dx =int(sdx)
	dy =int(sdy)
	speed = int(sspeed)
	Range = int(sRange)
	obstacles = []
	for i in range(n):
		edge = (Reader.readline().strip()).split()
		obstacle = []
		for j in range(0,len(edge),2):
			obstacle.append([int(edge[j]),int(edge[j+1])])

		obstaclesObj = Obstacle(obstacle)
		obstacles.append(obstaclesObj)
	return [s,g,dx,dy,obstacles,speed,Range]
#------------------chay chuong trinh voi file cho truoc 
# chay chuong trinh bang file
def findPathWithFile(Link):
	s,g,dx,dy,obstaclesObj,speed,Range = openFile(Link)
	if(s is None or g is None or dx is None or dy is None or obstaclesObj is None):
		print('Read Error!!!')
		return
	Win = StaticPathFindingWindow(s,g,obstaclesObj)
	Win.run()
	RTA = RealTimeAStart(s,g)
	RWin = RealTimeMyWindow(RTA,obstaclesObj,speed,Range,dx,dy,s,g)
	RWin.run()
#------------------ chay chuong trinh bang tay, tao vat can tren map truoc khi chay-------------
#chay chuong trinh  duoi dang o luoi
def findPathWithFile_Grid(Link):
	s,g,dx,dy,obstaclesObj,speed,Range = openFile(Link)
	if(s is None or g is None or dx is None or dy is None or obstaclesObj is None):
		print('Read Error!!!')
		return
	Win = StaticPathFindingWindowonGrid(s,g,obstaclesObj)
	Win.run()
	RWin = RealTimeMyWindowOnGrid(obstaclesObj,speed,dx,dy,Range,s,g)
	RWin.run()