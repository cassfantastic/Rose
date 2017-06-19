from traceback import print_exc
from Rose import game
from Rose import entities
from Rose import controls
from Rose import util

def run(): return game.Game().loop()

if __name__ == "__main__":
	try: run()
	except Exception as e:
		print_exc()
		input("Waiting.")