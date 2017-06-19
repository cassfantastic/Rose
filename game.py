import pygame as pg
from traceback import print_exc
from Rose import entities
from Rose import controls
from Rose import util

class Game:
	framerate = 30
	framedelay = 1000 // framerate
	screenwidth = 640
	screenheight = 480
	def __init__(self):
		self.prepinit()
		self.createinit()
	def prepinit(self):
		pg.init()
		pg.display.set_icon(entities.Player.image)
		pg.display.set_caption("Rose")
	def createinit(self):
		self.clock = pg.time.Clock()
		self.controls = controls.Controls(self)
		self.screen = pg.display.set_mode((self.screenwidth,self.screenheight))
		self.running = True
		entities.Player(self)
	def update(self):
		self.controls.handle()
		if self.running:
			entities.Entity.updateall()
			self.draw()
	def draw(self):
		self.screen.fill(util.black)
		entities.Entity.drawall(self.screen)
		pg.display.flip()
	def quit(self):
		self.running = False
		for i in entities.Entity.subclasses:
			i.group.empty()
	def loop(self):
		while self.running:
			self.update()
			self.clock.tick(self.framerate)
		pg.quit()
		return self