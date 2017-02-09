import pygame, sys, time
from random import random

pygame.init()

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((640,400))

instructions = pygame.font.Font("../../C64_Pro-STYLE.ttf", 16)
petscii = pygame.font.Font("../../C64_Pro_Mono-STYLE.ttf", 16)

status = "counting"
status_msg = ""
status_msg2 = ""
start_time = time.clock()
draw_time = int(random()*5) + 2

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if status == "ending": sys.exit()
			if not status == "drawn":
				status_msg = "You drew too early!"
				status_msg2 = "There is no honor in cheating."
			else:
				status_msg = "But you shoot first."
				status_msg2 = "You killed him."
			whiteness = 255
			status = "ending"

	counter = time.clock() - start_time

	if status == "drawing" and counter > draw_time + 10:
		status = "drawn"

	if status == "counting" and counter > 10:
		status = "drawing"

	if status == "counting":
		count_msg = str(min(int(counter), 9) + 1) + ".."
		whiteness = max(255 - int(150 * (counter % 1)), 0)

	if status == "drawn":
		whiteness = 255
		count_msg = "He draws..... "
		if counter > draw_time + 10.5:
			count_msg = "and shoots!"
			status_msg = "You are dead."
			status = "ending"

	screen.fill((0, 0, 0))
	screen.blit(instructions.render("You are back to back with the cowboy.", False, WHITE), [1, 1])
	screen.blit(instructions.render("Take ten paces and wait for him to draw.", False, WHITE), [1, 18])
	screen.blit(instructions.render("Press any key to shoot!", False, WHITE), [1, 35])
	screen.blit(instructions.render(status_msg, False, WHITE), [1, 300])
	screen.blit(instructions.render(status_msg2, False, WHITE), [1, 316])
	screen.blit(petscii.render(count_msg, False, (whiteness, whiteness, whiteness)), [240, 160])
	pygame.display.flip()
