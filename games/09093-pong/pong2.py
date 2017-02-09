import pygame, sys

WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode([480, 400])
petscii = pygame.font.Font("../../C64_Pro_Mono-STYLE.ttf", 16)
clock = pygame.time.Clock()

paddleY = 100
points = 0
ballX = 10
ballY = 10
sX = 2
sY = 2
FPS = 60

while True:
	Alive = True
	while Alive:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and paddleY > 0: paddleY -= 2
		if key[pygame.K_DOWN] and paddleY < 352: paddleY += 2

		if ballX < 16 and sX < 0 and ballY + 16 >= paddleY and ballY <= paddleY + 48:
				points += 1
				sX = points + 1
				if sY < 0:
					sY = -(points + 1)
				else:
					sY = points + 1

		if sX + ballX < 0:
			Alive = False
		if sX + ballX > 464:
			sX = -sX
		if sY + ballY > 384:
			sY = -sY
		if sY + ballY < 0:
			sY = -sY

		ballX += sX
		ballY += sY

		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, WHITE, [0, paddleY, 16, 48])
		pygame.draw.rect(screen, WHITE, [ballX, ballY, 16, 16])
		screen.blit(petscii.render(str(points), False, WHITE), [232, 0])
		clock.tick(FPS)
		pygame.display.flip()
	
	paddleY = 100
	points = 0
	ballX = 10
	ballY = 10
	sX = 2
	sY = 2


