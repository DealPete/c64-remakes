import pygame, sys, time
from random import random

pygame.init()

shifts = {'1': 0x21,
          '2': 0x40,
          '3': 0x23,
		  '4': 0x24,
		  '5': 0x25,
		  '6': 0x5E,
		  '7': 0x26,
		  '8': 0x2A,
		  '9': 0x28,
		  '0': 0x29,
		  '-': 0x5F,
		  '=': 0x2B,
		  '[': 0x7B,
		  ']': 0x7D,
		  '\\': 0x7C,
		  ';': 0x3A,
		  '\'': 0x22,
		  ',': 0x3C,
		  '.': 0x3E,
		  '/': 0x3F,
		  '`': 0x7E}

for i in range(0x61, 0x7B):
	shifts[chr(i)] = i - 0x20

WHITE = (255, 255, 255)
TIME_LIMIT = 1

screen = pygame.display.set_mode((640,400))

instructions = pygame.font.Font("../C64_Pro-STYLE.ttf", 16)
petscii = pygame.font.Font("../C64_Pro_Mono-STYLE.ttf", 16)

state = {"turn": 0, "hits": 0}

def new_turn():
	state["x"] = int(random()*620) + 2
	state["y"] = int(random()*320) + 40 
	state["robot"] = int(random()*93) + 33
	state["turn"] += 1
	state["start_time"] = time.clock()
	state["string"] = chr
	
new_turn()
success_msg = ""

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key > 0x20 and event.key < 0x7F:
				if pygame.key.get_mods() & pygame.KMOD_SHIFT:
					key_pressed = shifts[pygame.key.name(event.key)]
				else:
					key_pressed = event.key
				if key_pressed == state["robot"]:
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
	screen.blit(instructions.render("Press the right key to hit the alien!", True, WHITE), [1, 1])
	screen.blit(instructions.render(str(state["hits"]) + " of " + str(state["turn"] - 1) + " destroyed!", True, WHITE), [1, 18])
	screen.blit(petscii.render(chr(state["robot"]), False, WHITE), [state["x"], state["y"]])
	screen.blit(petscii.render(success_msg, False, (whiteness, whiteness, whiteness)), [240, 380])
	pygame.display.flip()
