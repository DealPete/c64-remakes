import pygame, sys, time
from random import random

pygame.init()

WHITE = (255, 255, 255)
TIME_LIMIT = 4

screen = pygame.display.set_mode((640,400))

instructions = pygame.font.Font("../../C64_Pro-STYLE.ttf", 16)
petscii = pygame.font.Font("../../C64_Pro_Mono-STYLE.ttf", 16)

state = {"turn": 0, "hits": 0}

def new_turn():
	state["diff"] = int(random()*10) + 1
	state["letter"] = int(random()*(26 - state["diff"])) + 65
	state["turn"] += 1
	state["start_time"] = time.clock()
	state["string"] = chr(state["letter"]) + '      ' + str(state["diff"])
	
new_turn()
success_msg = ""

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key > 0x60 and event.key < 0x7B: event.key -= 0x20
			if event.key == state["letter"] + state["diff"]:
				success_msg = "GOOD SHOT"
				state["hits"] += 1
			else:
				success_msg = "MISSED"
			new_turn()
	
	if time.clock() - state["start_time"] > TIME_LIMIT:
		success_msg = "MISSED"
		new_turn()

	whiteness = max(255 - int(150 * (time.clock() - state["start_time"])), 0)
	screen.fill((0, 0, 0))
	screen.blit(instructions.render("Press the right letter to hit the alien!", True, WHITE), [1, 1])
	screen.blit(instructions.render(str(state["hits"]) + " of " + str(state["turn"] - 1) + " slain!", True, WHITE), [1, 18])
	screen.blit(petscii.render(success_msg, False, (whiteness, whiteness, whiteness)), [240, 300])
	screen.blit(petscii.render(state["string"], False, WHITE), [240, 160])
	pygame.display.flip()
