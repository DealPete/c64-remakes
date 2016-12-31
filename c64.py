import pygame

class C64:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 170)
    BROWN = (102, 68, 0)
    CYAN = (170, 255, 255)
    DARKGREY = (51, 51, 51)
    GREEN = (0, 204, 85)
    GREY = (119, 119, 119)
    LIGHTGREEN = (170, 255, 102)
    LIGHTBLUE = (0, 136, 255)
    LIGHTGREY = (187, 187, 187)
    LIGHTRED = (255, 119, 119)
    ORANGE = (221, 136, 85)
    RED = (136, 0, 0)
    VIOLET = (204, 68, 204)
    WHITE = (255, 255, 255)
    YELLOW = (238, 238, 119)

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
