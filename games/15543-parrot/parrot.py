# **PARROT**

import pygame, sys, time
from random import random

WHITE = (255, 255, 255)
PARROT = (0x93, 0xDC, 0x69)

pygame.init()

screen = pygame.display.set_mode((320, 200))

petscii = pygame.font.Font("../C64_Pro_Mono-STYLE.ttf", 16)
instruct = pygame.font.Font("../C64_Pro-STYLE.ttf", 16)

def PRINT(text, x, y, color=WHITE):
	screen.blit(petscii.render(text, False, color), [16*x, 16*y])

def IPRINT(text, x, y):
	screen.blit(instruct.render(text, False, WHITE), [16*x, 16*y])
	
def PRINTR(text, x, y):
	text = "".join([chr(ord(i) + 0xE200) for i in text])
	PRINT(text, x, y)

score = 0
start_time = time.time()
letter = int(random()*26) + 65
last_answer = "none"
state = "waiting"

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if state == 'done': sys.exit()
			if state == 'playing':
				if event.key == letter or event.key - 0x20 == letter:
					last_answer = "right"
					score += 1
				else:
					last_answer = "wrong"
				if time.time() - start_time > 10:
					state = "done"
				else:
					letter = int(random()*26) + 65

			if state == 'waiting':
				state = 'playing'
	
	screen.fill((0, 0, 0))

	PRINT('    \uE2D1\uE220\uE220\uE220', 4, 1, PARROT)
	PRINT('   \uE2A9\uE220\uE220\uE220\uE220', 4, 2, PARROT)
	PRINT('   \uE0A1\uE220\uE220\uE220\uE220', 4, 3, PARROT)
	PRINT('    \uE220\uE220', 4, 4, PARROT)
	PRINTR('PARROT', 4, 6)

	IPRINT('Are you ready, parrot?', 0, 8)

	if state == "playing":
		PRINT(chr(letter), 2, 10)
		if last_answer == "right":
			PRINT('\uE1BA', 4, 10)
		if last_answer == "wrong":
			PRINT('\uE076', 4, 10)
	
	if state == "done":
		IPRINT("Final score: " + str(score), 2, 10)

	pygame.display.flip()
