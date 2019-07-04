import csv, sys
sys.path.append('../..')
from random import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 30
INFO_WIDTH = 18
INFO_HEIGHT = BOARD_HEIGHT
FPS = 60

import pygame
pygame.init()
screen = pygame.display.set_mode((16*BOARD_WIDTH + INFO_WIDTH*16 + 48,
    BOARD_HEIGHT*16 + 32))
pygame.display.set_caption("Polytris")
clock = pygame.time.Clock()

from c64 import C64

c64 = C64(screen)

BACKGROUND_COLOR = c64.BLACK

class Polyomino:
    colors = [c64.BLUE, c64.BROWN, c64.CYAN, c64.DARKGREY,
              c64.LIGHTRED, c64.GREEN, c64.GREY, c64.LIGHTGREEN,
              c64.LIGHTGREY, c64.ORANGE, c64.RED, c64.VIOLET,
              c64.WHITE, c64.YELLOW]

    I1 = [[1]]

    I2 = [[0, 1],
          [0, 1]]

    I3 = [[0, 1, 0],
          [0, 1, 0],
          [0, 1, 0]]

    L3 = [[1, 0],
          [1, 1]]

    I4 = [[0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0]]

    J4 = [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]]

    L4 = [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]]

    O4 = [[1, 1],
          [1, 1]]

    S4 = [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]]

    T4 = [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]]

    Z4 = [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]]

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

    variants = [(I1, 1), (I2, 2), (I3, 3), (L3, 2), (I4, 4), (J4, 3),
                (L4, 3), (O4, 2), (S4, 3), (T4, 3), (Z4, 3), (F, 3),
                (FR, 3), (I, 5), (J, 4), (L, 4), (N, 4),
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
            rotation.append([])
            for j in range(size):
                rotation[i].append(form[j][size - 1 - i])
        return rotation
        
    def rotate_right(form, size):
        rotation = []
        for i in range(size):
            rotation.append([])
            for j in range(size):
                rotation[i].append(form[size - 1 - j][i])
        return rotation
    
    def flip_horizontal(form, size):
        rotation = []
        for i in range(size):
            rotation.append([])
            for j in reversed(range(size)):
                rotation[i].append(form[i][j])
        return rotation

    def flip_vertical(form, size):
        rotation = []
        for i in range(size):
            rotation.append(form[size - i - 1])
        return rotation
    
    def mutate_piece(state, mutation):
        mutated = mutation(state.piece.form, state.piece.size)
        if valid(state.X, state.Y, mutated):
            state.piece.form = mutated
    
    def drop_piece(state):
        while (valid(state.X, state.Y + 1, state.piece.form)):
            state.Y += 1


    def __init__(self):
        block = int(random()*len(self.variants))
        self.color = self.colors[int(random()*len(self.colors))]
        self.size = self.variants[block][1]
        self.form = self.variants[block][0]

class game_state:
    def __init__(self):
        scorefile = open("hiscores.csv", "r")
        reader = csv.reader(scorefile, dialect = csv.unix_dialect)
        self.hiscores = []
        for row in reader:
            self.hiscores.append(row)
        scorefile.close()
        self.start_game()

    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.timer = 0
        self.frames_per_move = 30
        self.board = [[BACKGROUND_COLOR] * BOARD_WIDTH for y in range(BOARD_HEIGHT)]
        self.next_piece = Polyomino()
        self.add_next_piece()

    def add_next_piece(self):
        self.piece = self.next_piece
        self.next_piece = Polyomino()
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
                if event.key == pygame.K_z:
                    Polyomino.mutate_piece(state, Polyomino.rotate_left)
                if event.key == pygame.K_x:
                    Polyomino.mutate_piece(state, Polyomino.rotate_right)
                if event.key == pygame.K_c:
                    Polyomino.mutate_piece(state, Polyomino.flip_horizontal)
                if event.key == pygame.K_v:
                    Polyomino.mutate_piece(state, Polyomino.flip_vertical)
                if event.key == pygame.K_DOWN:
                    state.state = "falling"
                if event.key == pygame.K_UP:
                    Polyomino.drop_piece(state)
            elif state.state == "paused":
                if event.key == pygame.K_p:
                    state.state = "playing"
            elif state.state == "entering high score":
                if event.key == pygame.K_BACKSPACE and state.cursorpos > 0:
                    state.cursorpos -= 1
                    state.hiscores[state.scorepos][0] = \
                        state.hiscores[state.scorepos][0][:state.cursorpos]
                elif event.key == pygame.K_RETURN:
                    scorefile = open("hiscores.csv", "w")
                    writer = csv.writer(scorefile, dialect = csv.unix_dialect)
                    for row in state.hiscores:
                        writer.writerow(row)
                    scorefile.close()
                    state.start_game()
                elif (event.unicode.isalpha() or event.key == pygame.K_SPACE) \
                    and state.cursorpos < INFO_WIDTH - 3 - len(str(state.score)):
                    state.hiscores[state.scorepos][0] = \
                        state.hiscores[state.scorepos][0][:state.cursorpos] \
                        + event.unicode
                    state.cursorpos += 1
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
            state.add_next_piece()
        else:
            scorepos = -1
            for i in range(len(state.hiscores)):
                if state.score > int(state.hiscores[len(state.hiscores) - i - 1][1]):
                    scorepos = len(state.hiscores) - i - 1
            if scorepos == -1 and len(state.hiscores) < INFO_HEIGHT - 13:
                scorepos = len(state.hiscores)
            if scorepos == -1:
                state.state = "lost"
            else:
                state.state = "entering high score"
                state.scorepos = scorepos
                state.cursorpos = 0
                state.hiscores = state.hiscores[:scorepos] \
                    + [["", str(state.score)]] + state.hiscores[scorepos:]

    if state.state == "playing" or state.state == "falling":
        state.timer += 1
        if state.timer % state.frames_per_move == 0 or state.state == "falling":
            if valid(state.X, state.Y + 1, state.piece.form):
                state.Y += 1
            else:
                place_tile()

def draw_screen():
    def draw_tile(piece, x, y):
        for i in range(piece.size):
            if y + i >= 0:
                for j in range(piece.size):
                    if piece.form[i][j] == 1:
                        c64.PRINT("\uE220", x + j + 1, y + i + 1, piece.color)

    pygame.draw.rect(screen, c64.LIGHTBLUE, (0, 0, 16*BOARD_WIDTH + 48 + 16*INFO_WIDTH, 16*BOARD_HEIGHT + 32))
    pygame.draw.rect(screen, BACKGROUND_COLOR, (16, 16, 16*BOARD_WIDTH + 16*INFO_WIDTH + 16, 16*BOARD_HEIGHT))
    pygame.draw.rect(screen, c64.LIGHTBLUE, (16*BOARD_WIDTH + 16, 16, 16, 16*BOARD_HEIGHT))
    if state.state != "entering high score":
        draw_tile(state.next_piece,
            BOARD_WIDTH + 3 + int((5 - state.next_piece.size)/2),
            2 + int((5 - state.next_piece.size)/2))
        scoreX = 12 - int(len(str(state.score))/2)
        c64.PRINT("SCORE: ", 9 + BOARD_WIDTH + 2, 4)
        c64.PRINT(str(state.score), scoreX + BOARD_WIDTH + 2, 5)
    else:
        c64.PRINT("Congratulations!", BOARD_WIDTH + 3, 4)
        c64.PRINT("Enter your score", BOARD_WIDTH + 3, 5)
    c64.PRINT("HIGH SCORES:", BOARD_WIDTH + 3, 11)
    for i in range(min(BOARD_HEIGHT - 13, len(state.hiscores))):
        c64.PRINT(state.hiscores[i][0], BOARD_WIDTH + 3, 13 + i)
        score = state.hiscores[i][1]
        c64.PRINT(score, BOARD_WIDTH + INFO_WIDTH - len(score) + 1, 13 + i)
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if state.board[y][x] != BACKGROUND_COLOR:
                c64.PRINT("\uE220", x + 1, y + 1, state.board[y][x])
    draw_tile(state.piece, state.X, state.Y)
    pygame.display.update()

while True:
    clock.tick(FPS)
    draw_screen()
    get_input()
    update_world()
