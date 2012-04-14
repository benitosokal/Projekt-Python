#arkmod.py

try:
	import pygame, sys, os
	from pygame.locals import *
except ImportError:
	print ('Brak modulow')
	pygame.quit()
	sys.exit()

blocks_width = 30 
blocks_heigth = 20
ball_width = 20
ball_heigth = 20
racket_size = 80
RACKETSPEED = 15
BALLSPEED = 4
ACCELERATION = 0.05
SCORE = 0

# ustawienie kierunkow poruszania sie
DOWNLEFT = 1
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

#defincja kolorow
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)

#przygotowanie zmiennych do poruszania sie
moveLeft = False
moveRight = False
space_pressed = False
yes_pressed = False
no_pressed = False

def help():
	try:
		f = open('help_arkanoid.txt', 'r')
	except IOError:
		try:
			f = open(os.path.join(os.path.expanduser('~'), 'lib/help_arkanoid.txt'), 'r')
		except IOError:
			print ("Nie moge znalezc pliku z pomoca")
			sys.exit()
	print (f.read())
	f.close()

def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def resetBlocks():
	b = []
	for x in range(19):
		for y in range(10):
			b.append(pygame.Rect( x * blocks_width + x + 26 , y * blocks_heigth + y + 40 , blocks_width, blocks_heigth))
	return b
