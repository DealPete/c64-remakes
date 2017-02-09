import sys
sys.path.append('../..')
from random import random

BOARD_HEIGHT = 35

import pygame
pygame.init()
screen = pygame.display.set_mode((192, BOARD_HEIGHT*16 + 48))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
FPS = 60

from c64 import C64

c64 = C64(screen)

class Tetromino:
    colors = [c64.BLACK, c64.BROWN, c64.CYAN, c64.DARKGREY,
              c64.LIGHTRED, c64.GREEN, c64.GREY, c64.LIGHTGREEN,
              c64.LIGHTGREY, c64.ORANGE, c64.RED, c64.VIOLET,
              c64.WHITE, c64.YELLOW]

    I = [[[0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0]],
         [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0]],
         [[0, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 1, 0, 0],
          [0, 1, 0, 0]],
         [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]]

    J = [[[1, 0, 0], [1, 1, 1], [0, 0, 0]],
         [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
         [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
         [[0, 1, 0], [0, 1, 0], [1, 1, 0]]]

    L = [[[0, 0, 1], [1, 1, 1], [0, 0, 0]],
         [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
         [[1, 1, 0], [0, 1, 0], [0, 1, 0]]]

    O = [[[1, 1], [1, 1]],
         [[1, 1], [1, 1]],
         [[1, 1], [1, 1]],
         [[1, 1], [1, 1]]]
    
    S = [[[0, 1, 1], [1, 1, 0], [0, 0, 0]],
         [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
         [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
         [[1, 0, 0], [1, 1, 0], [0, 1, 0]]]

    T = [[[0, 1, 0], [1, 1, 1], [0, 0, 0]],
         [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
         [[0, 0, 0], [1, 1, 1], [0, 1, 0]],
         [[0, 1, 0], [1, 1, 0], [0, 1, 0]]]

    Z = [[[1, 1, 0], [0, 1, 1], [0, 0, 0]],
         [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
         [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [1, 1, 0], [1, 0, 0]]] 

    def __init__(self):
        block = int(random()*7)
        self.color = self.colors[int(random()*len(self.colors))]
        if block == 0:
            self.size = 4
            self.numforms = 4
            self.forms = self.I
        elif block == 1:
            self.size = 3
            self.forms = self.J
        elif block == 2:
            self.size = 3
            self.forms = self.L
        elif block == 3:
            self.size = 2
            self.forms = self.O
        elif block == 4:
            self.size = 3
            self.forms = self.S
        elif block == 5:
            self.size = 3
            self.forms = self.T
        elif block == 6:
            self.size = 3
            self.forms = self.Z

class game_state:
    def __init__(self):
        self.start_game()

    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.timer = 0
        self.frames_per_move = 30
        self.board = [[c64.BLUE] * 10 for y in range(BOARD_HEIGHT)]
        self.add_new_piece()

    def add_new_piece(self):
        self.piece = Tetromino()
        self.form = int(random()*4)
        self.X = int(random()*(10 - self.piece.size + 1))
        self.Y = -1

state = game_state()

def valid(bx, by, form):
    for i in range(state.piece.size):
        for j in range(state.piece.size):
            if form[i][j] == 1:
                x = j + bx
                if x < 0 or x >= 10:
                    return False
                y = i + by
                if y >= 0:
                    if y >= BOARD_HEIGHT or state.board[y][x] != c64.BLUE:
                        return False
    return True

def get_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if state.state == "playing":
                if event.key == pygame.K_LEFT:
                    if valid(state.X - 1, state.Y, state.piece.forms[state.form]):
                        state.X -= 1
                if event.key == pygame.K_RIGHT:
                    if valid(state.X + 1, state.Y, state.piece.forms[state.form]):
                        state.X += 1
                if event.key == pygame.K_SPACE:
                    new_form = state.form - 1
                    if new_form < 0: new_form = 3
                    if valid(state.X, state.Y, state.piece.forms[new_form]):
                        state.form = new_form
                if event.key == pygame.K_DOWN:
                    state.state = "falling"
            if state.state == "lost":
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    state.start_game()

def update_world():
    def remove_finished_lines():
        for y in range(BOARD_HEIGHT):
            if all([block != c64.BLUE for block in state.board[y]]):
                for row in range(y-1, 0, -1):
                    state.board[row + 1] = state.board[row][:]
                state.board[0] = [c64.BLUE] * 10
                state.score += 10

    def place_tile():
        for i in range(state.piece.size):
            for j in range(state.piece.size):
                if state.piece.forms[state.form][i][j] == 1 and i + state.Y >= 0:
                    state.board[i + state.Y][j + state.X] = state.piece.color
        state.score += 1
        remove_finished_lines()
        state.add_new_piece()
        if valid(state.X, state.Y, state.piece.forms[state.form]):
            state.state = "playing"
        else:
            state.state = "lost"

    if state.state != "lost":
        state.timer += 1
        if state.timer % state.frames_per_move == 0 or state.state == "falling":
            if valid(state.X, state.Y + 1, state.piece.forms[state.form]):
                state.Y += 1
            else:
                place_tile()

def draw_screen():
    pygame.draw.rect(screen, c64.LIGHTBLUE, (0, 0, 192, 16*BOARD_HEIGHT + 32))
    pygame.draw.rect(screen, c64.BLUE, (16, 16, 160, 16*BOARD_HEIGHT))
    pygame.draw.rect(screen, c64.BLACK, (0, 16*BOARD_HEIGHT + 32, 192, 16))
    scoreX = 1
    if state.score < 10: scoreX = 2
    c64.PRINT("SCORE: " + str(state.score), scoreX, BOARD_HEIGHT + 2)
    for x in range(10):
        for y in range(BOARD_HEIGHT):
            if state.board[y][x] != c64.BLUE:
                c64.PRINT("\uE220", x + 1, y + 1, state.board[y][x])
    for i in range(state.piece.size):
        if state.Y + i >= 0:
            for j in range(state.piece.size):
                if state.piece.forms[state.form][i][j] == 1:
                    c64.PRINT("\uE220", state.X + j + 1,
                        state.Y + i + 1, state.piece.color)
    pygame.display.update()

while True:
    clock.tick(FPS)
    draw_screen()
    get_input()
    update_world()

