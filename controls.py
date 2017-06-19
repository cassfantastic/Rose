import tools
import pygame as pg

class Controls:
	def __init__(self,game):
		self.game = game
		self.constantkeys = {"up":pg.K_w,"down":pg.K_s,"left":pg.K_a,"right":pg.K_d,"shoot":pg.K_SPACE}
		self.constantmap = {}
		self.instantkeys = {"switch":pg.K_LSHIFT,"quit":pg.K_ESCAPE,"dev1":pg.K_1,"dev2":pg.K_2,"dev3":pg.K_3}
		self.instantmap = {}
	def __getitem__(self,key):
		if key in self.constantkeys: return self.constantkeys[key]
		elif key in self.instantkeys: return self.instantkeys[key]
		else: raise KeyError(f"Key {key} not found in controls.")
	def addconstant(self,key,handler):
		if isinstance(key,int): self.addtoconstantmap(key,handler)
		elif isinstance(key,str): self.addtoconstantmap(self.constantkeys[key],handler)
		elif hasattr(key,"__iter__"):
			for i in key: self.addconstant(i,handler)
	def addinstant(self,key,handler):
		if isinstance(key,int): self.addtoinstantmap(key,handler)
		elif isinstance(key,str): self.addtoinstantmap(self.instantkeys[key],handler)
		elif hasattr(key,"__iter__"):
			for i in key: self.addinstant(i,handler)
	def addtoconstantmap(self,key,handler):
		if key in self.constantmap: self.constantmap[key].append(handler)
		else: self.constantmap[key] = [handler]
	def addtoinstantmap(self,key,handler):
		if key in self.instantmap: self.instantmap[key].append(handler)
		else: self.instantmap[key] = [handler]
	def removeconstant(self,handler):
		for i in self.constantmap.values():
			if handler in i: i.remove(handler)
	def removeinstant(self,handler):
		for i in self.instantmap.values():
			if handler in i: i.remove(handler)
	def handle(self):
		self.handleinstant()
		self.handleconstant()
	def handleinstant(self):
		for e in pg.event.get(): self.handleevent(e)
	def handleevent(self,e):
		if e.type == pg.KEYDOWN:
			if e.key in self.instantmap:
				for f in self.instantmap[e.key]: f(e.key)
		elif e.type == pg.QUIT: self.game.quit()
	def handleconstant(self):
		pg.event.pump()
		keys = pg.key.get_pressed()
		handlers = {f for k in self.constantmap for f in self.constantmap[k] if keys[k]}
		for f in handlers: f(keys)