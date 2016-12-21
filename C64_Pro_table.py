import pygame, sys

WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((1024, 464))

petscii = pygame.font.Font("C64_Pro_Mono-STYLE.ttf", 16)

screen.fill((0, 0, 0))

for i in range(0xFF):
	screen.blit(petscii.render(chr(i + 0xE000), False, WHITE), [16*(i % 64), 16 * (i // 64)])
	screen.blit(petscii.render(chr(i + 0xE100), False, WHITE), [16*(i % 64), 80 + 16 * (i // 64)])
	screen.blit(petscii.render(chr(i + 0xE200), False, WHITE), [16*(i % 64), 160 + 16 * (i // 64)])
	screen.blit(petscii.render(chr(i + 0xE300), False, WHITE), [16*(i % 64), 240 + 16 * (i // 64)])
	screen.blit(petscii.render(chr(i + 0xEE00), False, WHITE), [16*(i % 64), 320 + 16 * (i // 64)])
	screen.blit(petscii.render(chr(i + 0xEF00), False, WHITE), [16*(i % 64), 400 + 16 * (i // 64)])
pygame.display.flip()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
