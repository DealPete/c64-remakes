import pygame, sys, time
from random import random

pygame.init()

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((640,400))

instructions = pygame.font.Font("../C64_Pro-STYLE.ttf", 16)
petscii = pygame.font.Font("../C64_Pro_Mono-STYLE.ttf", 16)

keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

playing = True
state = {"turn": 0, "hits": 0}

def new_turn():
	soldiers = ''
	traitor = int(random()*9) + 1
	for i in range(1, 10):
		if i == traitor:
			soldiers += "O"
		else:
			soldiers += "."
	state["soldiers"] = soldiers
	state["traitor"] = traitor
	state["turn"] += 1
	state["start_time"] = time.clock()
	
new_turn()
success_msg = ""

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN and pygame.key.name(event.key) in keys:
			if int(pygame.key.name(event.key)) == state["traitor"]:
				success_msg = "GOOD SHOT"
				state["hits"] += 1
			else:
				success_msg = "MISSED"
			new_turn()
	
	if time.clock() - state["start_time"] > 2:
		success_msg = "MISSED"
		new_turn()

	whiteness = max(255 - int(250 * (time.clock() - state["start_time"])), 0)
	screen.fill((0, 0, 0))
	screen.blit(instructions.render("Press the number keys to fire at the traitor!", True, WHITE), [1, 1])
	screen.blit(instructions.render(str(state["hits"]) + " of " + str(state["turn"] - 1) + " slain!", True, WHITE), [1, 17])
	screen.blit(petscii.render(success_msg, False, (whiteness, whiteness, whiteness)), [240, 300])
	screen.blit(petscii.render(state["soldiers"], False, WHITE), [240, 160])
	pygame.display.flip()
