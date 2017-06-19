from functools import reduce
from math import cos,sin

def flip(f):
	def g(x,y,*args): return f(y,x,*args)
	return g

def multimap(fs,xs): return reduce(flip(map),fs,xs)

def chainable(f):
	def g(*args,**kwargs):
		f(*args,**kwargs)
		return f.__self__ if hasattr(f,"__self__") else args[0]
	return g

def anysum(xs): return sum(xs[1:],xs[0])

def addlists(*xss): return type(xss[0])((anysum(xs) for xs in zip(*xss)))

def flipdict(d): return {v:k for k,v in d}

def capitalizefirst(s): return s[0].upper() + s[1:]

def circleposition(angle,radius=1): return (radius*cos(angle),radius*sin(angle))