import pygame

class C64:
	BLACK = (0, 0, 0)
	BROWN = (102, 68, 0)
	GREEN = (0, 204, 85)
	GREY3 = (187, 187, 187)
	YELLOW = (238, 238, 119)
	WHITE = (255, 255, 255)

	def __init__(self, screen):
		self.screen = screen
		self.petscii = pygame.font.Font("../C64_Pro_Mono-STYLE.ttf", 16)
		self.variable_width_petscii = pygame.font.Font("../C64_Pro-STYLE.ttf", 16)

	def SPRINT(self, text, color=WHITE):
		return self.petscii.render(text, False, color)

	def PRINT(self, text, x, y, color=WHITE, screen=None):
		if screen == None:
			target = self.screen
		else:
			target = screen
		surface = self.petscii.render(text, False, color)
		target.blit(surface, [16*x, 16*y])

	def VPRINT(self, text, x, y, color=WHITE, screen=None):
		if screen == None:
			target = self.screen
		else:
			target = screen
		surface = self.variable_width_petscii.render(text, False, color)
		target.blit(surface, [16*x, 16*y])
		
	def PRINTR(text, x, y, color=WHITE):
		text = "".join([chr(ord(i) + 0xE200) for i in text])
		return PRINT(text, x, y, color)
