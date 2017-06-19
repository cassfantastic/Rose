import tools
import pygame as pg

white = (0xFF,0xFF,0xFF)
black = (0,0,0)
red = (255,0,0)
skyblue = (0x99,0xDD,0xEE)
sqrt2 = 1.4142135623730951

@tools.chainable
def setalpha(image): image.set_colorkey(skyblue)

def loadimage(path):
	try: return setalpha(pg.image.load(path))
	except pg.error: return loadimage("C:/Bee/dev/Rose/missing.bmp")