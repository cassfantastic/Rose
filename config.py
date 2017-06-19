import pygame
from tools import *
from .utilities import *

screenwidth = 640
screenheight = 480
background = white

class Input:
	width = 200
	height = 20
	def __init__(self,label,command):
		self.label = label
		self.command = command
		self.keyvalue = 0
		self.keyname = ""
		self.saved = True
		self.color = black
		self.rect = pygame.Rect(0,0,self.width,self.height)
	def draw(self):
		pygame.draw.rect(screen,self.color,self.rect,1)
		pygame.draw.line(screen,self.color,self.rect.midtop,self.rect.move(0,-1).midbottom,1)
		textimage = font.render(self.label,True,self.color)
		screen.blit(textimage,self.rect.move(4,3))
	@chainable
	def move(self,x,y): self.rect.topleft = (x,y)

def update():
	for e in pygame.event.get(): handle(e)
	screen.fill(background)
	for i in inputs: i.draw()
	pygame.display.flip()

def handle(e): pass

def run():
	global running, screen, inputs, font

	pygame.init()
	pygame.font.init()
	Icon = pygame.image.load("player.bmp")
	pygame.display.set_icon(Icon)
	pygame.display.set_caption("Rose configuration")
	screen = pygame.display.set_mode((screenwidth,screenheight))
	font = pygame.font.Font(None,20)

	upinput = Input("Move up","up").move(20,20)
	inputs = [upinput]

	running = True
	while running: update()
	pygame.quit()

if __name__ == "__main__": run()