import tools
import math
import random
import pygame as pg
from Rose import controls
from Rose import util

def classmaker(name,bases,dict):
	newclass = type(name,bases,dict)
	newclass.group = pg.sprite.Group()
	newclass.subclasses = set()
	for i in bases: addsubclass(newclass,i)
	return newclass

def addsubclass(newclass,superclass):
	if hasattr(superclass,"subclasses"):
		for i in superclass.__bases__: addsubclass(newclass,i)
		superclass.subclasses.add(newclass)

class Entity(pg.sprite.Sprite,metaclass=classmaker):
	image = util.loadimage("images/entity.bmp")
	basetimeout = 60
	def __init__(self,game):
		super().__init__()
		self.game = game
		self.screen = game.screen
		self.controls = game.controls
		self.rect = self.image.get_rect()
		self.rect.center = self.screen.get_rect().center
		self.timeout = self.basetimeout
		self.group.add(self)
	@classmethod
	def updateall(cls):
		for i in cls.subclasses: i.group.update()
	@classmethod
	def drawall(cls,screen):
		for i in cls.subclasses: i.group.draw(screen)
	def check(self):
		if not self.rect.colliderect(self.screen.get_rect()):
			if self.timeout > 0: self.timeout -= 1
			else: self.kill()
		else: self.timeout = self.basetimeout
	def collide(self,other): return pg.sprite.collide_rect(self,other)
	__and__ = collide
	def collideall(self,otherclass): return [i for i in otherclass.group if self & i]
	def collidesubclasses(self,otherclass): return self.collideall(otherclass) + [i for c in otherclass.subclasses for i in c.group if self & i]

class Player(Entity,metaclass=classmaker):
	image = util.loadimage("images/player.bmp")
	basespeed = 5
	def __init__(self,game):
		super().__init__(game)
		self.controls.addconstant(("up","down","left","right"),self.move)
		self.controls.addinstant("dev1",lambda _:AutoOrbitGun(self))
		self.controls.addinstant("dev2",lambda _:RecoilOrbitGun(self))
		self.controls.addinstant("dev3",lambda _:GliderEnemy(self.game))
		#GunMaker(self,(0,-22))
		#EnemyMaker(self,(-12,-6))
		#MachineGun(self,(24,10))
		#MachineGun(self,(-24,10))
	def directspeed(self): return self.basespeed
	def diagonalspeed(self): return self.directspeed() / util.sqrt2
	def move(self,keys):
		xv = keys[self.controls["right"]] - keys[self.controls["left"]]
		yv = keys[self.controls["down"]] - keys[self.controls["up"]]
		if xv and yv: speed = self.diagonalspeed()
		else: speed = self.directspeed()
		self.rect.move_ip(speed*xv,speed*yv)
		self.rect.clamp_ip(self.screen.get_rect())
	def addautogun(self,_): AutoOrbitGun(self)
	def addrecoilgun(self,_): RecoilOrbitGun(self)

class Bullet(Entity,metaclass=classmaker):
	def __init__(self,gun):
		super().__init__(gun.player.game)
		self.gun = gun
		self.player = gun.player
		self.rect.center = gun.rect.center
	def update(self): self.move()
	def move(self):
		self.rect.move_ip(0,-self.basespeed)
		self.check()
	def hit(self): self.kill()

class AngleBullet(Bullet,metaclass=classmaker):
	def __init__(self,gun):
		super().__init__(gun)
		self.xv, self.yv = tools.circleposition(-self.angle,self.speed)
		self.x, self.y = self.rect.topleft
	def move(self):
		self.x += self.xv
		self.y += self.yv
		self.rect.topleft = (self.x,self.y)
		self.check()

class PistolBullet(Bullet,metaclass=classmaker):
	image = util.loadimage("images/pistolbullet.bmp")
	damage = 10
	basespeed = 10

class MachineBullet(AngleBullet,metaclass=classmaker):
	image = util.loadimage("images/machinebullet.bmp")
	damage = 1
	speed = 5
	spread = math.radians(10)
	midangle = math.radians(90)
	maxangle = midangle + spread
	minangle = midangle - spread
	def __init__(self,gun):
		self.angle = random.uniform(self.minangle,self.maxangle)
		super().__init__(gun)

class RecoilOrbitBullet(AngleBullet,metaclass=classmaker):
	image = util.loadimage("images/machinebullet.bmp")
	damage = 3
	speed = 10
	def __init__(self,gun):
		self.angle = math.pi/2 - gun.angle
		super().__init__(gun)

class AutoOrbitBullet(Bullet,metaclass=classmaker):
	image = util.loadimage("images/machinebullet.bmp")
	damage = 1
	basespeed = 7

class Gun(Entity,metaclass=classmaker):
	def __init__(self,player,offset):
		super().__init__(player.game)
		self.player = player
		self.offset = offset
		self.firestate = 0
		self.controls.addconstant("shoot",self.shoot)
		self.move()
	def update(self):
		if self.firestate > 0: self.firestate -= 1
		if self.firestate < 0: self.firestate = 0
		self.move()
	def shoot(self,_=None):
		if self.firestate <= 0:
			self.bullettype(self)
			self.firestate = self.firerate
			return True
		else: return False
	def kill(self):
		super().kill()
		self.controls.removeconstant(self.shoot)
	def move(self): self.rect.center = tools.addlists(self.player.rect.center,self.offset)

class PistolGun(Gun,metaclass=classmaker):
	image = util.loadimage("images/pistolgun.bmp")
	firerate = 15
	bullettype = PistolBullet

class MachineGun(Gun,metaclass=classmaker):
	image = util.loadimage("images/machinegun.bmp")
	firerate = 3
	bullettype = MachineBullet

class OrbitGun(Gun,metaclass=classmaker):
	def __init__(self,player):
		self.angle = 0
		super().__init__(player,(0,0))
		self.reassignangles()
	def move(self):
		self.angle += self.av
		self.angle %= 2*math.pi
		self.rect.center = tools.addlists(self.player.rect.center,tools.circleposition(self.angle,self.radius))
	@classmethod
	def reassignangles(cls):
		for i in enumerate(cls.group): i[1].assignangle(i[0])
	def assignangle(self,n): self.angle = 2*math.pi*(n/len(self.group))
	def kill(self):
		super().kill()
		self.reassignangles()

class AutoOrbitGun(OrbitGun,metaclass=classmaker):
	image = util.loadimage("images/machinegun.bmp")
	firerate = 7
	av = math.radians(3)
	radius = 50
	bullettype = AutoOrbitBullet

class RecoilOrbitGun(OrbitGun,metaclass=classmaker):
	image = util.loadimage("images/recoilorbitgun.bmp")
	firerate = 2
	aa = math.radians(0.15)
	maxav = math.radians(9)
	radius = 70
	bullettype = RecoilOrbitBullet
	def __init__(self,player):
		self.angle = 0
		self.av = 0
		super().__init__(player)
		self.accelerating = False
	def update(self):
		super().update()
		if not self.accelerating:
			self.av -= self.aa
			if self.av < 0: self.av = 0
		self.accelerating = False
	def shoot(self,_=None):
		self.accelerating = True
		if super().shoot():
			self.av += self.aa
			if self.av > self.maxav: self.av = self.maxav
			return True
		else: return False
	@classmethod
	def reassignangles(cls):
		av = sum(i.av for i in cls.group) / len(cls.group)
		for i in enumerate(cls.group):
			i[1].assignangle(i[0])
			i[1].av = av
	def assignangle(self,n):
		super().assignangle(n)
		self.av = 0

class Enemy(Entity,metaclass=classmaker):
	basetimeout = 120
	def update(self):
		self.collide()
		if self.health <= 0: self.destroy()
		self.move()
	def move(self):
		self.rect.move_ip(0,self.basespeed)
		self.check()
	def collide(self):
		for i in self.collidesubclasses(Bullet):
			self.health -= i.damage
			i.hit()
	def destroy(self):
		for i in range(20): EnemySpark(self)
		self.kill()

class GliderEnemy(Enemy,metaclass=classmaker):
	image = util.loadimage("images/gliderenemy.bmp")
	basespeed = 3
	health = 3
	def __init__(self,game,x=None):
		super().__init__(game)
		if x == None: self.rect.left = random.randint(0,game.screenwidth-self.image.get_width())
		else: self.rect.left = x
		self.rect.bottom = -60

class Particle(Entity,metaclass=classmaker):
	def __init__(self,origin):
		super().__init__(origin.game)
		self.health = random.randint(5,10)
		self.speed = random.randint(3,7)
		self.angle = random.uniform(0,2*math.pi)
		self.x, self.y = origin.rect.center
		self.xv,self.yv = tools.circleposition(self.angle,self.speed)
	def update(self):
		self.health -= 1
		if self.health <= 0: self.kill()
		self.move()
	def move(self):
		self.x += self.xv
		self.y += self.yv
		self.xv *= 0.8
		self.yv *= 0.8
		self.rect.topleft = (self.x,self.y)
		self.check()

class EnemySpark(Particle,metaclass=classmaker):
	image = util.loadimage("images/enemyspark.bmp")