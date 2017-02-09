import sys
sys.path.append('../..')
from random import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 30

import pygame
pygame.init()
screen = pygame.display.set_mode((16*BOARD_WIDTH + 32,
    BOARD_HEIGHT*16 + 48))
pygame.display.set_caption("Pentris")
clock = pygame.time.Clock()
FPS = 60

from c64 import C64

BACKGROUND_COLOR = C64.BLACK
c64 = C64(screen)

class Pentomino:
    colors = [c64.BLUE, c64.BROWN, c64.CYAN, c64.DARKGREY,
              c64.LIGHTRED, c64.GREEN, c64.GREY, c64.LIGHTGREEN,
              c64.LIGHTGREY, c64.ORANGE, c64.RED, c64.VIOLET,
              c64.WHITE, c64.YELLOW]

    F = [[0, 1, 1],
         [1, 1, 0],
         [0, 1, 0]]

    FR = [[1, 1, 0],
          [0, 1, 1],
          [0, 1, 0]]

    I = [[0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0]]

    J = [[0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 1, 1, 0]]

    L = [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0]]

    N = [[0, 0, 1, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]

    NR = [[0, 1, 0, 0],
          [0, 1, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0]]

    P = [[0, 1, 0],
         [1, 1, 0],
         [1, 1, 0]]

    PR = [[0, 1, 0],
          [0, 1, 1],
          [0, 1, 1]]

    T = [[1, 1, 1],
         [0, 1, 0],
         [0, 1, 0]]

    U = [[1, 0, 1],
         [1, 1, 1],
         [0, 0, 0]]

    V = [[1, 0, 0],
         [1, 0, 0],
         [1, 1, 1]]

    W = [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 1]]

    X = [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]]

    Y = [[0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]]

    YR = [[0, 0, 1, 0],
          [0, 1, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0]]

    Z = [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 1]]

    ZR = [[0, 1, 1],
          [0, 1, 0],
          [1, 1, 0]]

    variants = [(F, 3), (FR, 3), (I, 5), (J, 4), (L, 4), (N, 4),
                (NR, 4), (P, 3), (PR, 3), (T, 3), (U, 3), (V, 3),
                (W, 3), (X, 3), (Y, 4), (YR, 4), (Z, 3), (ZR, 3)]

    def transpose(form, size):
        transposition = []
        for i in range(size):
            transposition.append([])
            for j in range(size):
                transposition[i].append(form[j][i])
        return transposition
                
    def rotate_left(form, size):
        rotation = []
        for i in range(size):
            rotation.append(form[size - 1 - i][:])
        return Pentomino.transpose(rotation, size)
        
    def rotate_right(form, size):
        rotation = []
        for i in range(size):
            rotation.append([])
            for j in range(size):
                rotation[i].append(form[size - 1 - j][i])
        return rotation


    def __init__(self):
        block = int(random()*len(self.variants))
        self.color = self.colors[int(random()*len(self.colors))]
        self.size = self.variants[block][1]
        self.form = self.variants[block][0]

class game_state:
    def __init__(self):
        self.start_game()

    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.timer = 0
        self.frames_per_move = 30
        self.board = [[BACKGROUND_COLOR] * BOARD_WIDTH for y in range(BOARD_HEIGHT)]
        self.add_new_piece()

    def add_new_piece(self):
        self.piece = Pentomino()
        self.X = int(random()*(BOARD_WIDTH - self.piece.size + 1))
        self.Y = 2 - self.piece.size 

state = game_state()

def valid(bx, by, form):
    for i in range(state.piece.size):
        for j in range(state.piece.size):
            if form[i][j] == 1:
                x = j + bx
                if x < 0 or x >= BOARD_WIDTH:
                    return False
                y = i + by
                if y >= 0:
                    if y >= BOARD_HEIGHT or state.board[y][x] != BACKGROUND_COLOR:
                        return False
    return True

def get_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN \
            and state.state == "falling":
            state.state = "playing"
        if event.type == pygame.KEYDOWN:
            if state.state == "playing":
                if event.key == pygame.K_p:
                    state.state = "paused"
                if event.key == pygame.K_LEFT:
                    if valid(state.X - 1, state.Y, state.piece.form):
                        state.X -= 1
                if event.key == pygame.K_RIGHT:
                    if valid(state.X + 1, state.Y, state.piece.form):
                        state.X += 1
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    new_form = Pentomino.rotate_right(state.piece.form,
                        state.piece.size)
                    if valid(state.X, state.Y, new_form):
                        state.piece.form = new_form
                if event.key == pygame.K_DOWN:
                    state.state = "falling"
            elif state.state == "paused":
                if event.key == pygame.K_p:
                    state.state = "playing"
            elif state.state == "lost":
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    state.start_game()

def update_world():
    def remove_finished_lines():
        for y in range(BOARD_HEIGHT):
            if all([block != BACKGROUND_COLOR for block in state.board[y]]):
                for row in range(y-1, 0, -1):
                    state.board[row + 1] = state.board[row][:]
                state.board[0] = [BACKGROUND_COLOR] * BOARD_WIDTH
                state.score += 10

    def place_tile():
        for i in range(state.piece.size):
            for j in range(state.piece.size):
                if state.piece.form[i][j] == 1 and i + state.Y >= 0:
                    state.board[i + state.Y][j + state.X] = state.piece.color
        state.score += 1
        remove_finished_lines()
        if all([x == BACKGROUND_COLOR for x in state.board[0]]):
            state.state = "playing"
            state.add_new_piece()
        else:
            state.state = "lost"

    if state.state == "playing" or state.state == "falling":
        state.timer += 1
        if state.timer % state.frames_per_move == 0 or state.state == "falling":
            if valid(state.X, state.Y + 1, state.piece.form):
                state.Y += 1
            else:
                place_tile()

def draw_screen():
    pygame.draw.rect(screen, c64.LIGHTBLUE, (0, 0, 16*BOARD_WIDTH + 32, 16*BOARD_HEIGHT + 32))
    pygame.draw.rect(screen, c64.BLACK, (16, 16, 16*BOARD_WIDTH, 16*BOARD_HEIGHT))
    pygame.draw.rect(screen, c64.BLACK, (0, 16*BOARD_HEIGHT + 32, 16*BOARD_WIDTH + 32, 16))
    scoreX = 1
    if state.score < 10: scoreX = 2
    c64.PRINT("SCORE: " + str(state.score), scoreX, BOARD_HEIGHT + 2)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if state.board[y][x] != BACKGROUND_COLOR:
                c64.PRINT("\uE220", x + 1, y + 1, state.board[y][x])
    for i in range(state.piece.size):
        if state.Y + i >= 0:
            for j in range(state.piece.size):
                if state.piece.form[i][j] == 1:
                    c64.PRINT("\uE220", state.X + j + 1,
                        state.Y + i + 1, state.piece.color)
    pygame.display.update()

while True:
    clock.tick(FPS)
    draw_screen()
    get_input()
    update_world()

