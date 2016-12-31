import sys
sys.path.append("..")

import time
from random import random
import pygame
from c64 import C64

pygame.init()
screen = pygame.display.set_mode((608, 592))
c64 = C64(screen)

pygame.display.set_caption("64 Potholes")

car = pygame.transform.scale(pygame.image.load('car.png'), (32, 32))
car = pygame.transform.flip(car, False, True)

grass = c64.SPRINT("\uE0a6"*11, c64.GREEN)
curbl = c64.SPRINT("\uE0bc", c64.YELLOW)
curbr = c64.SPRINT("\uE0be", c64.YELLOW)
pothole = c64.SPRINT("\uE071", c64.BLACK)

# left surface covers x=0 to x=192
# right surface covers x=416 to x=608
left = pygame.Surface((192, 608))
right = pygame.Surface((192, 608))
left.fill(c64.LIGHTGREY)
right.fill(c64.LIGHTGREY)

for i in range(38):
	left.blit(grass, [0, i*16])
	left.blit(curbl, [176, i*16])
	right.blit(grass, [16, i*16])
	right.blit(curbr, [0, i*16])

distance = nextpot = carX = potholes = score = hiscore = speed = state = gameTime = None

def add_pothole(y = 608):
	global potholes
	potholes.append([int(random()*208)+192, y])

def init_game():
	global distance, nextpot, carX, potholes, score, hiscore, speed, state, gameTime
	gameTime = time.time()
	distance = 0
	nextpot = 80
	carX = 300
	potholes = []
	score = 0
	hiscore = 0
	speed = 3
	state = "driving"
	for y in range(5):
		add_pothole(608 - y*80)

init_game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	key = pygame.key.get_pressed()

	if state=="crashed" and (key[pygame.K_RETURN] or key[pygame.K_SPACE]):
		init_game()

	if state=="driving":
		if key[pygame.K_LEFT]:
			carX -= 2
			if carX < 182:
				state = "crashed"
		if key[pygame.K_RIGHT]:
			carX += 2
			if carX > 394:
				state = "crashed"
		
		if nextpot <= 0:
			add_pothole()
			score += speed
			if hiscore < score: hiscore = score
			nextpot = 80

		nextpot -= speed
		distance += speed
		if time.time() - gameTime > 15:
			gameTime = time.time()
			speed += 1

	screen.fill(c64.LIGHTGREY)
	screen.blit(left, [0, -distance % 16 - 16])
	screen.blit(right, [416, -distance % 16 - 16])

	screen.blit(car, [carX, 10])

	if state == "crashed":
		c64.PRINT("Potholes - By Brent Kapilik", 7, 20, c64.BLACK)
		c64.PRINT("Remake by Peter Deal", 9, 21, c64.BLACK)
		c64.PRINT("Your score = " + str(score), 11, 23, c64.BLACK)
		c64.PRINT("  Hi score = " + str(hiscore), 11, 24, c64.BLACK)

	potholes = [[a,b] for [a,b] in potholes if b > -16]
	for hole in potholes:
		if hole[1] < 42 and hole[1] >=0:
			if hole[0] + 16 >= carX + 10 and hole[0] <= carX + 22:
				state = "crashed"
		if state == "driving":
			hole[1] -= speed
		if state != "crashed" or hole[1] < 50:
			screen.blit(pothole, hole)

	if state == "driving":
		c64.PRINT("SPEED: ", 2, 2, c64.BLACK)
		c64.PRINT(str(speed) + " MPH", 2, 3, c64.BLACK)

	pygame.display.flip()

