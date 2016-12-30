import pygame

def init(size):
	global screen, petscii, variable_width_petscii
	pygame.init()
	screen = pygame.display.set_mode(size)
	petscii = pygame.font.Font("../C64_Pro_Mono-STYLE.ttf", 16)
	variable_width_petscii = pygame.font.Font("../C64_Pro-STYLE.ttf", 16)

BLACK = (0, 0, 0)
BROWN = (102, 68, 0)
GREEN = (0, 204, 85)
GREY3 = (187, 187, 187)
YELLOW = (238, 238, 119)
WHITE = (255, 255, 255)


def SPRINT(text, color=WHITE):
	return petscii.render(text, False, color)

def PRINT(text, x, y, color=WHITE):
	surface = petscii.render(text, False, color)
	screen.blit(surface, [16*x, 16*y])

def VPRINT(text, x, y, color=WHITE):
	surface = variable_width_petscii.render(text, False, color)
	screen.blit(surface, [16*x, 16*y])
	
def PRINTR(text, x, y, color=WHITE):
	text = "".join([chr(ord(i) + 0xE200) for i in text])
	return PRINT(text, x, y, color)
