import pyglet

class createMap(pyglet.window.Window):
	def __init__(self,link,ob):
		super(createMap,self).__init__(600,600)
		self.obstacle = []
		self.cell = 10
		self.camx = 0
		self.camy = 0
		self.heightdraw = int(self.height/self.cell)
		self.widthdraw = int(self.width/self.cell)
		self.link = link
		self.ob = ob
		pyglet.clock.schedule_interval(self.update, 1.0/24.0)
		pyglet.app.run()

	def check(self,x,y):
		for ob in self.obstacle:
			xp,yp = ob
			if(x==xp and y==yp):
				self.obstacle.remove(ob)
				return True
		return False

	def on_mouse_press(self,x, y, button, modifiers):
	    if button & pyglet.window.mouse.RIGHT:
		    dx = int(x/self.cell) + self.camx 
		    dy = int(y/self.cell) + self.camy
		    print(dx,dy)
		    if(not self.check(dx,dy)):
		    	self.obstacle.append([dx,dy])

	def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
		if buttons & pyglet.window.mouse.LEFT:
			self.camx -= dx
			self.camy -= dy

	def on_draw(self):
		self.clear()
		for i in range(self.heightdraw):
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(0,i*self.cell,600,i*self.cell)))
		for i in range(self.widthdraw):
			pyglet.graphics.draw(2,pyglet.gl.GL_LINES,('v2i',(i*self.cell,0,i*self.cell,600)))

		for obt in self.obstacle:
			x,y = obt
			x = x-self.camx 
			y = y-self.camy
			x = x*self.cell
			y = y*self.cell
			pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,('v2i',(x,y,x+self.cell,y,x+self.cell,y+self.cell,x,y+self.cell)))

	def update(self,dt):
		pass

	def on_close(self):
		self.luu()
		self.add()
		self.close()
		print('passed')
	
	def luu(self):
		if self.link is None:
			return
		f = open(self.link,'w')
		if f is not None:
			for p in self.obstacle:
				x,y = p
				s = str(x)+" "+str(y)+" "
				f.write(s)
			f.close()
	def add(self):
		for p in self.obstacle:
			self.ob.append(p)

def run():
	ob = []
	cr = createMap(None,ob)
	

