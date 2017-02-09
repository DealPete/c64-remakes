# LETTER CATCHER - CHING KO
# Remake by Peter Deal

import pygame, sys, time
from random import random

pygame.init()

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((640,400))

gameoverscii = pygame.font.Font("../../C64_Pro-STYLE.ttf", 16)
petscii = pygame.font.Font("../../C64_Pro_Mono-STYLE.ttf", 16)

clock = pygame.time.Clock()

state = {}
score = 0
speed = 1
FPS = 60

status = "playing"

def new_turn():
    state['x'] = int(random()*620) + 2
    state['y'] = 400
    state['letter'] = int(random()*26) + 0x41

new_turn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if status == "lost": sys.exit()
            if event.key == state['letter'] or event.key - 0x20 == state['letter']:
                score += 1
                if score % 5 == 0: speed += 1
                new_turn()
    
    state['y'] -= speed
    if state['y'] < 1:
        status = "lost"

    screen.fill((0, 0, 0))
    if status == "lost":
        screen.blit(gameoverscii.render("You let one slip through... game over", False, WHITE), [16*5, 16*12])
    screen.blit(petscii.render(str(score), False, WHITE), [16*20, 0])
    screen.blit(petscii.render(chr(state["letter"]), False, WHITE), [state["x"], state["y"]])
    clock.tick(FPS)
    pygame.display.flip()
