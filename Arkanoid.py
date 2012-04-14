#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import pygame, sys, os
	from pygame.locals import *
except ImportError:
	print ('Brak modulow')
	pygame.quit()
	sys.exit()

#dodanie dodatkowej sciezki do PYTHONPATH(lista katalogow gdzie ma szukać katalogow
sys.path.append(os.path.join(os.path.expanduser('~'), 'lib'))

from arkmod import *
	
for arg in sys.argv:
	if arg == '-h' or arg == '--help':
		help()
		sys.exit()



#inicjacja pygame
pygame.init()
mainClock = pygame.time.Clock()

#tworzenie okna
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT ), 0, 32)
pygame.display.set_caption('Arkanoid')

#ustawienie czcionki
basicFont = pygame.font.SysFont(None, 48)

#przygotowanie pilki i paletki
racket = pygame.Rect( int((WINDOWWIDTH / 2) - (racket_size / 2)), WINDOWHEIGHT - 25, racket_size , 15)

try:
	ballImage = pygame.image.load('ball.png')
except :
	ballImage = pygame.image.load(os.path.join(os.path.expanduser('~'), 'lib/ball.png'))
ballStretchedImage = pygame.transform.scale(ballImage, (ball_width, ball_heigth))

#przygotowanie okna
#wypelinj tlo okna na czarno
while True:
	windowSurface.fill(BLACK)

	#przygotuj gorne bloki
	blocks = resetBlocks()

	for b in blocks:
		pygame.draw.rect(windowSurface, WHITE, b)

	#narysuj paletke i pilke
	ball = { 'rect':pygame.Rect(int(racket.left + (racket_size)/2 - ball_width/2), racket.top - 21, ball_width, ball_heigth), 'dir':UPRIGHT }
	windowSurface.blit(ballStretchedImage, ball['rect'])
	pygame.draw.rect(windowSurface, RED, racket)

	#narysowanie obiektu Surface na okno
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				# zmiana zmienych klawiatury
				if event.key == K_LEFT or event.key == ord('a'):
					moveRight = False
					moveLeft = True
				if event.key == K_RIGHT or event.key == ord('d'):
					moveLeft = False
					moveRight = True
			if event.type == KEYUP:
				if event.key == K_SPACE:
					space_pressed = True
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_LEFT or event.key == ord('a'):
					moveLeft = False
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = False
					
	
		if space_pressed:
			space_pressed = False			
			break

		#poruszanie paletka
		if moveLeft and racket.left > 0:
			racket.left -= RACKETSPEED
			ball['rect'].left -= RACKETSPEED
		if moveRight and racket.right < WINDOWWIDTH:
			racket.right += RACKETSPEED
			ball['rect'].left += RACKETSPEED
	
		windowSurface.fill(BLACK)
		windowSurface.blit(ballStretchedImage, ball['rect'])
		pygame.draw.rect(windowSurface, RED, racket)
		for b in blocks:
			pygame.draw.rect(windowSurface, WHITE, b)
		pygame.display.update()
		mainClock.tick(40)

	#glowna petla
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				# zmiana zmienych klawiatury
				if event.key == K_LEFT or event.key == ord('a'):
					moveRight = False
					moveLeft = True
				if event.key == K_RIGHT or event.key == ord('d'):
					moveLeft = False
					moveRight = True
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_LEFT or event.key == ord('a'):
					moveLeft = False
				if event.key == K_RIGHT or event.key == ord('d'):
					moveRight = False
	
		#poruszanie paletka
		if moveLeft and racket.left > 0:
			racket.left -= RACKETSPEED
		if moveRight and racket.right < WINDOWWIDTH:
			racket.right += RACKETSPEED

		#poruszanie pilka
		if ball['dir'] == DOWNLEFT:
			ball['rect'].left -= BALLSPEED
			ball['rect'].top += BALLSPEED
		if ball['dir'] == DOWNRIGHT:
			ball['rect'].left += BALLSPEED
			ball['rect'].top += BALLSPEED
		if ball['dir'] == UPLEFT:
			ball['rect'].left -= BALLSPEED
			ball['rect'].top -= BALLSPEED
		if ball['dir'] == UPRIGHT:
			ball['rect'].left += BALLSPEED
			ball['rect'].top -= BALLSPEED

		# sprawdz czy pilka znajduje sie poza oknem
		if ball['rect'].top < 0:
			#pilka przekroczyla gorna strone okna
			if ball['dir'] == UPLEFT:
				ball['dir'] = DOWNLEFT
			if ball['dir'] == UPRIGHT:
				ball['dir'] = DOWNRIGHT
		if ball['rect'].left < 0:
			#pilka przekroczyla lewa strone okna
			if ball['dir'] == DOWNLEFT:
				ball['dir'] = DOWNRIGHT
			if ball['dir'] == UPLEFT:
				ball['dir'] = UPRIGHT
		if ball['rect'].right > WINDOWWIDTH:
			#pilka przekroczyla prawa strone okna
			if ball['dir'] == DOWNRIGHT:
				ball['dir'] = DOWNLEFT
			if ball['dir'] == UPRIGHT:
				ball['dir'] = UPLEFT
	
		#usuwanie blokow i zmiana kieunku pilki
		if ball['dir'] == UPRIGHT:
			for b in blocks[:]:
				if isPointInsideRect(ball['rect'].left, ball['rect'].top, b):
					blocks.remove(b)
					ball['dir'] = DOWNRIGHT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
				if isPointInsideRect(ball['rect'].right, ball['rect'].bottom, b):
					blocks.remove(b)
					ball['dir'] = UPLEFT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
		elif ball['dir'] == DOWNRIGHT:
			for b in blocks[:]:
				if isPointInsideRect(ball['rect'].right, ball['rect'].top, b):
					blocks.remove(b)
					ball['dir'] = DOWNLEFT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
				if isPointInsideRect(ball['rect'].left, ball['rect'].bottom, b):
					blocks.remove(b)
					ball['dir'] = UPRIGHT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
		elif ball['dir'] == DOWNLEFT:
			for b in blocks[:]:
				if isPointInsideRect(ball['rect'].left, ball['rect'].top, b):
					blocks.remove(b)
					ball['dir'] = DOWNRIGHT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
				if isPointInsideRect(ball['rect'].right, ball['rect'].bottom, b):
					blocks.remove(b)
					ball['dir'] = UPLEFT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
		elif ball['dir'] == UPLEFT:
			for b in blocks[:]:
				if isPointInsideRect(ball['rect'].right, ball['rect'].top, b):
					blocks.remove(b)
					ball['dir'] = DOWNLEFT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
				if isPointInsideRect(ball['rect'].left, ball['rect'].bottom, b):
					blocks.remove(b)
					ball['dir'] = UPRIGHT
					BALLSPEED += ACCELERATION
					SCORE += BALLSPEED
					break
	
		#odbicie pilki przez paletke
		if racket.colliderect(ball['rect']):
			if ball['dir'] == DOWNRIGHT:
				ball['dir'] = UPRIGHT
			if ball['dir'] == DOWNLEFT:
				ball['dir'] = UPLEFT
	
		#warunek przegranej gry
		#pilka przekroczyala dolna strone okna
		if ball['rect'].bottom > WINDOWHEIGHT:
			break
		
		windowSurface.fill(BLACK)
		windowSurface.blit(ballStretchedImage, ball['rect'])
		pygame.draw.rect(windowSurface, RED, racket)
		for b in blocks:
			pygame.draw.rect(windowSurface, WHITE, b)
		pygame.display.update()
		mainClock.tick(40)

	windowSurface.fill(BLACK)
	text = basicFont.render("Wynik: " + str(int(SCORE)), True, WHITE, BLACK)
	textRect = text.get_rect()
	textRect.centerx = windowSurface.get_rect().centerx
	textRect.centery = windowSurface.get_rect().centery
	windowSurface.blit(text, textRect)
	text= basicFont.render(u"Chcesz zagrać jeszcze raz (t/n)", True, WHITE, BLACK)
	textRect = text.get_rect()
	textRect.centerx = windowSurface.get_rect().centerx
	textRect.centery = windowSurface.get_rect().centery + 48
	windowSurface.blit(text, textRect)
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == ord('t'):
					yes_pressed = True
				if event.key == ord('n'):
					no_pressed = True
		if yes_pressed:
			yes_pressed = False
			break
		if no_pressed:
			pygame.quit()
			sys.exit()		
			
