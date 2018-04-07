import Queue


#lop dai dien cho cac dinh trong do thi
class Node:
	__parent = None
	__name = ""
	__cost = 0
	
	def __init__(self,parent,name,cost):
		self.__parent = parent
		self.__name = name
		self.__cost = cost

	def getParent(self):
		return self.__parent

	def getName(self):
		return self.__name

	def getCost(self):
		return self.__cost
	
	def updateCost(self,cost):
	  self.__cost = cost
	 
	def updateParent(self,parent):
	  self.__parent = parent
		
#kiem tra dinh da duoc mo hay chua
def checkexist(name,list):
  for i in range(0,len(list)):
    if(name==list[i].getName()): return True
  return False
 
# mo file voi duong dan Link
# tra ve ma tran ke doc duoc tu file
# va ham heuristic  
def openFile(link):
	Reader = open(link,"r")
	if Reader is None: return
	n = int(Reader.readline().strip())
	[s,g] = Reader.readline().strip().split()
	matrix = []
	for i in range(n):
		edge = (Reader.readline().strip()).split()
		matrix.append(edge)
	heurictic = (Reader.readline().strip()).split()
	return [s,g,matrix,heurictic]

#chon gia tri so sanh de sap xep
# o day chon do dai quang duong
def chooseElemenForSort(node):
	return node.getCost()

# thuat toan DFS tim kiem theo chieu sau co tranh lap vo han
def DFS(Matrix, StartPoint, GoalPoint ):
	stack = [] # giu cac dinh cho duyet
	closed = [] # giu cac dinh da duyet roi
	goal = None
	s = Node(None,StartPoint,0) # khoi tao dinh bat dau
	stack.append(s)
	while(len(stack)>0): # thuc hien den khi khong con dinh de xet hoac tim thay goal
		p = stack.pop() # lay 1 dinh trong stack ra mo rong
		if(p.getName() in closed):
			continue
		closed.append(p.getName()) # danh dau dinh p da duoc xet
		if(p.getName() == GoalPoint):
			goal = p
			break # neu dinh lay ra la goal thi dung tim
		index = int(p.getName())
		l = len(Matrix[index]) # so dinh
		buf = [] # luu cac dinh mo rong tien cho viec sap xep theo cost de dua vao stack
		for i in range(l-1,-1,-1): # duyet n dinh
			cost = int(Matrix[index][i]) # cost tu dinh p den dinh i
			name = str(i)  #ten dinh dang set
			if(cost>0): # chi duyet cac dinh co duong di toi p
				if (name not in closed): # kiem tra dinh da duoc mo rong hay da duoc xet truoc do chua
				  node = Node(p,name,cost)
				  buf.append(node)
					
		buf.sort(reverse = True, key=chooseElemenForSort) # sap xep theo cost de dua vao stack
		for i in range(0,len(buf)):
		  stack.append(buf[i])

	return makeResultSequence(goal,closed)


#thuat toan tim kiem theo chieu rong
def BFS(Matrix, StartPoint, GoalPoint ):
	queue = [] # giu cac dinh cho duyet
	closed = [] # giu cac dinh da duyet roi
	goal = None
	s = Node(None,StartPoint,0) # khoi tao dinh bat dau
	queue.append(s)
	while(len(queue)>0): # thuc hien den khi khong con dinh de xet hoac tim thay goal
		p = queue.pop(0) # lay 1 dinh trong queue ra mo rong
		if(p.getName() in closed):
			continue
		closed.append(p.getName()) # danh dau dinh p da duoc xet
		if(p.getName() == GoalPoint):
			goal = p
			break # neu dinh lay ra la goal thi dung tim
		index = int(p.getName())
		l = len(Matrix[index]) # so dinh
		buf = [] # luu cac dinh mo rong tien cho viec sap xep theo cost de dua vao queue
		for i in range(0,l): # duyet n dinh
			cost = int(Matrix[index][i]) # cost tu dinh p den dinh i
			name = str(i)  #ten dinh dang set
			if(cost>0): # chi duyet cac dinh co duong di toi p
				if (name not in closed): # kiem tra dinh da duoc mo rong hay da duoc xet truoc do chua
				  node = Node(p,name,cost)
				  buf.append(node)
					
		buf.sort(key=chooseElemenForSort) # sap xep theo cost de dua vao queue
		for i in range(0,len(buf)):
		  queue.append(buf[i])
	
	return makeResultSequence(goal,closed)


# thuat toan tim kiem chi phi dong nhat
def UCS(Matrix,StartPoint,GoalPoint):
	heurictic = []
	for i in range(len(Matrix[0])):
		heurictic.append(0)
	return AStart(Matrix,heurictic,StartPoint,GoalPoint)


# tra ve chuoi ket qua gom 
# +duong di tu diem bat dau den dich
# +chi phi thuc hien
# +cac dinh da duyet qua

def makeResultSequence(goal,closed):
	DinhDuyet = []
	ret = []
	distance = []
	for i in closed:
	  DinhDuyet.append(i)

	if(goal is None): return[None,None,DinhDuyet]
	while(goal is not None):
		ret.append(goal.getName())
		if(goal.getParent() is not None):
			distance.append(goal.getCost())
		goal = goal.getParent()
	ret.reverse()
	distance.reverse()
	path = ret
	cost = str(sum(distance))
	return[path,cost,DinhDuyet]

# tao ket qua cho thuat toan A*
def makeResultSequenceAstart(goal,closed):
	DinhDuyet = []
	ret = []
	for i in range(len(closed)):
	  DinhDuyet.append(closed[i].getName())

	if(goal is None): return[None,None,DinhDuyet]
	
	cost = str(goal.getCost())
	while(goal is not None):
		ret.append(goal.getName())
		goal = goal.getParent()
		
	ret.reverse()
	path = ret
	return[path,cost,DinhDuyet]

#thuat toan greedy search
def GreedySearch(Matrix,heurictic,StartPoint,GoalPoint):
	opened = Queue.PriorityQueue(0)
	closed = []
	goal = None
	s = Node(None,StartPoint,0)
	opened.put((int(heurictic[int(StartPoint)]),s.getName(),s))
	while(not opened.empty()):
		p = opened.get()[2]
		if(p.getName() in closed):
			continue
		closed.append(p.getName())
		if(p.getName()==GoalPoint):
			goal = p
			break
		index = int(p.getName())
		l = len(Matrix[0])
		for i in range(0,l):
			cost = int(Matrix[index][i])
			childName = str(i) 
			if(cost>0):
				if(childName not in closed):
					h = int(heurictic[i])
					node = Node(p,childName,cost)
					opened.put((h,childName,node))
					
	return makeResultSequence(goal,closed)


def Test():
  Matrix = [['0','2','3','1','0','0','0'],['2','0','0','8','0','0','0'],['3','0','0','0','0','0','0'],['1','8','0','0','4','9','0'],['0','0','0','4','0','7','0'],['0','0','0','9','7','0','0']]
  heurictic = ['5','1','4','2','3','0','1']
  [p,c,closed] = AStart(Matrix,heurictic,'0','5')
  print(p)
  print(c)
  print(closed)

# chon gia tri de lay ra phan tu nho nhat
def getKey(x):
	return x[0]

#ham kiem tra dinh da ton tai cua thuat toan A*
# tra ra doi tuong Node neu no ton tai trong stack nguoc lai tra ve None
def checkexistAstart(name,stack):
	for i in range(0,len(stack)):
		if(stack[i][1].getName()==name):
			return stack[i]
	return None

#thuat toan A*
def key(x):
	return x[1].getCost()

def findMin(Opened):
	n = len(Opened)
	min = [Opened[0][0],int((Opened[0][1].getName())),Opened[0][1]]
	for i in range(1,n):
		if(min[0]<Opened[i][0]):
			continue
		else:
			if(min[0]>Opened[i][0]):
				min[0] = Opened[i][0]
				min[1] = int(Opened[i][1].getName())
				min[2] = Opened[i][1]
			else:
				if(min[1]>int(Opened[i][1].getName())):
					min[0] = Opened[i][0]
					min[1] = int(Opened[i][1].getName())
					min[2] = Opened[i][1]
	return [min[0],min[2]]					


def AStart(Matrix,heurictic,StartPoint,GoalPoint):
	Opened = [] # (h+g, data)
	explored = [] # luu cac dinh da duyet(neu co duong di qua dinh ton tai trong nay thi thay) 
	closed = [] # luu cac dinh da duyet qua
	goal = None
	s = Node(None,StartPoint,0)
	Opened.append([0,s]) # dua s vao tap mo rong
	while (len(Opened)>0):
		Tupe = findMin(Opened) # lay ra bo (f,Node) co f nho nhat
		Opened.remove(Tupe) #xoa Tupe khoi Opened
		p = Tupe[1] #lay ra Node de mo rong
		explored.append(Tupe) # dua explored vao bo nho
		closed.append(Tupe[1]) #dua Node P vao closed
		if(p.getName()==GoalPoint): # kiem tra la dich
			goal = p
			break
		index = int(p.getName())
		l = len(Matrix[0])
		for i in range(l-1,-1,-1): # duyet cac dinh ke dinh ke khi no cost >0
			cost = int(Matrix[index][i])
			childName = str(i) # ten dinh con mo rong
			if(cost>0):
				childTupe = checkexistAstart(childName,Opened)
				childTupeinClosed = checkexistAstart(childName,explored)
				if(childTupeinClosed is not None): # truong hop dinh da co trong closed
					if(childTupeinClosed[1].getCost()>p.getCost() + cost):
						explored.remove(childTupeinClosed)
						childTupeinClosed = None
				if(childTupe is not None): # neu dinh co trong open
					if (childTupe[1].getCost()>p.getCost() + cost):
						Opened.remove(childTupe)
						childTupe = None
				if(childTupe is None and childTupeinClosed is None):
				  f = p.getCost() + cost + int(heurictic[i])
				  node = Node(p,childName,p.getCost()+cost)
				  Opened.append([f,node])


	return makeResultSequenceAstart(goal,closed)

def writeFile(link,path,closed,cost):
	f = open(link,'w')
	if f is not None:
		if(path is None):
			f.write('No solution')
			return

		for i in range(len(closed)):
			x = closed[i]
			s = str(x)
			if(i!=len(closed)-1):
				s = s+" "
			else:
				s = s+'\n'
			f.write(s)
		for i in range(len(path)):
			x = path[i]
			s = str(x)
			if(i != len(path)-1):
				s = s+" "
			else:
				s = s+'\n'
			f.write(s)

def run(linkin, linkout):
	[s,g,matrix,heurictic] = openFile(linkin)
	[pathDFS,cosDFS,DinhDuyetDFS] = DFS(matrix,s,g)
	[pathBFS,cosBFS,DinhDuyetBFS] = BFS(matrix,s,g)
	[pathUCS,cosUCS,DinhDuyetUCS] = UCS(matrix,s,g)
	[pathGreedy,cosGreedy,DinhDuyetGreedy] = GreedySearch(matrix,heurictic,s,g)
	[pathAS,cosAS,DinhDuyetAS] = AStart(matrix,heurictic,s,g)
	writeFile(linkout+'\\'+'DFS.txt',pathDFS,DinhDuyetDFS,cosDFS)
	writeFile(linkout+'\\'+'BFS.txt',pathBFS,DinhDuyetBFS,cosBFS)
	writeFile(linkout+'\\'+'UCS.txt',pathUCS,DinhDuyetUCS,cosUCS)
	writeFile(linkout+'\\'+'Greedy.txt',pathGreedy,DinhDuyetGreedy,cosGreedy)
	writeFile(linkout+'\\'+'AStart.txt',pathAS,DinhDuyetAS,cosAS)






  







