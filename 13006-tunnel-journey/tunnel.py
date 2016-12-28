import c64, pygame, sys, math, time
from random import random
from collections import deque

size = (640, 592)

c64.init(size)
pygame.display.set_caption("Tunnel Journey")

ship = pygame.image.load('../00072-64-valley-of-death/ship.png')
ship_mask = pygame.mask.from_surface(ship)

walls = pygame.Surface(size, pygame.SRCALPHA)

state = {}

rocks = deque()

def next_left_edge():
	state['wavelength'] += random()*5 - 2.5 
	state['x'] += math.pi / state['wavelength'] 
	state['amplitude'] += 0.001
	state['offset'] += random()*0.5 - 0.25
	return int(state['amplitude'] * 
		(math.cos(state['x']) + math.sin(state['x'])) + state['offset'])

def start_game():
	rocks.clear()
	state['time'] = time.time()
	state['offset'] = 0
	state['speed'] = 3
	state['shipX'] = 304
	state['amplitude'] = 16
	state['x'] = 0
	state['wavelength'] = 592
	state['state'] = 'playing'

	walls.fill((0, 0, 0, 0))

	for i in range(592):
		left_edge = next_left_edge()
		pygame.draw.line(walls, c64.BROWN, (0, i), (240 + left_edge, i))
		pygame.draw.line(walls, c64.BROWN, (400 + left_edge, i), (639, i))

start_game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()

	key = pygame.key.get_pressed()

	if state['state'] == "crashed":
		if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
			start_game()

	if state['state'] == "playing":
		if time.time() - state['time'] > 10:
			state['time'] = time.time()
			state['speed'] += 1
		if key[pygame.K_LEFT]:
			state['shipX'] -= 2
		if key[pygame.K_RIGHT]:
			state['shipX'] += 2

	c64.screen.fill(c64.BLACK)
	c64.screen.blit(walls, [0, 0])
	c64.screen.blit(ship, [state['shipX'], 10])

	for rock in rocks:
		c64.screen.blit(rock[1], rock[0])
		if state['state'] == 'playing': rock[0][1] -= state['speed']
	
	if state['state'] == "playing":
		c64.PRINT("SPEED: ", 2, 2, c64.BLACK)
		c64.PRINT(str(state['speed']) + " MPH", 2, 3, c64.BLACK)

	if state['state'] == "crashed":
		c64.PRINT("You crashed!", 11, 23, c64.WHITE)
		c64.PRINT("Score = " + str(int(state['x'] * 100)), 11, 24, c64.WHITE)

	pygame.display.update()

	if state['state'] == "playing":
		tunnel_mask = pygame.mask.from_surface(walls)

		if tunnel_mask.overlap(ship_mask, (state['shipX'], 10)):
			state['state'] = 'crashed'

		for rock in rocks:
			if ship_mask.overlap(rock[2], (rock[0][0] - state['shipX'],
				rock[0][1] - 10)):
				state['state'] = 'crashed'
	
	if state['state'] == 'playing':
		walls.scroll(0, -state['speed'])
		
		for i in range(state['speed']):
			left_edge = next_left_edge()
			y = 592 - state['speed'] + i
			pygame.draw.line(walls, c64.BROWN, (0, y), (240 + left_edge, y))
			pygame.draw.line(walls, (0, 0, 0, 0), (241 + left_edge, y),
				(399 + left_edge, y))
			pygame.draw.line(walls, c64.BROWN, (400 + left_edge, y), (639, y))

		while len(rocks) > 0 and rocks[0][0][1] + 8 < 0:
			rocks.popleft()

		if (random()*8) < 1:
			rock = pygame.Surface((17, 17), pygame.SRCALPHA)
			location = [int(random()*624) + 8, 600]
			pygame.draw.circle(rock, c64.BROWN, (8, 8), 8)
			rocks.append([location, rock, pygame.mask.from_surface(rock)])
