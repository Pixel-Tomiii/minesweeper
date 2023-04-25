import pygame
import random

import time
from level import *

EASY = 1
MEDIUM = 2
HARD = 3

# Constans.
WIDTH = 20
HEIGHT = 30
DIFFICULTY = HARD
MINES = int((0.05 + (0.05 * DIFFICULTY)) * WIDTH * HEIGHT)
NUM_REVEALED_TEXTURES = 10
NUM_OVERLAY_TEXTURES = 2
TILE_SIZE = 24

# Create window
width = WIDTH * TILE_SIZE
height = HEIGHT * TILE_SIZE
pygame.init()
window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, 16)

# Textures
revealed_textures = [0 for _ in range(NUM_REVEALED_TEXTURES)]
overlay_textures = [0 for _ in range(NUM_OVERLAY_TEXTURES)]

for i in range(NUM_REVEALED_TEXTURES):
    revealed_textures[i] = pygame.image.load(f"revealed/{i}.png").convert()
for i in range(NUM_OVERLAY_TEXTURES):
    overlay_textures[i] = pygame.image.load(f"overlay/{i}.png").convert()


def draw_board(level, tile_size):
    board_width = level.width * tile_size
    board_height = level.height * tile_size
    board = pygame.Surface((board_width, board_height))

    for y, row in enumerate(level.world):
        for x, val in enumerate(row):
            render_x = x * tile_size
            render_y = y * tile_size

            texture = revealed_textures[val] if level.overlay[y][x] == -1 else overlay_textures[level.overlay[y][x]]

            board.blit(
                pygame.transform.scale(texture, (tile_size, tile_size)),
                (render_x, render_y)
                )
    return board

def run_game(level):
    won = False
    lost = False
    
    while not (won or lost):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            # Click on tile.
            if event.type == pygame.MOUSEBUTTONDOWN:
                LEFT_CLICK = 1
                RIGHT_CLICK = 3

                x = event.pos[0] // TILE_SIZE
                y = event.pos[1] // TILE_SIZE

                # Reveal square
                if event.button == LEFT_CLICK:
                    level.moves += 1
                    reveal = get_revealed(level, x, y)
                    for x, y in reveal:
                        level.overlay[y][x] = -1

                    # Lost
                    if level.world[y][x] == -1:
                        for y, row in enumerate(level.world):
                            for x, val in enumerate(row):
                                if val == -1:
                                    level.overlay[y][x] = -1
                        lost = True

                    won = check_won(level)

                # Place flag
                elif event.button == RIGHT_CLICK:
                    level.moves += 1
                    val = level.overlay[y][x]
                    if val == 0:
                        level.overlay[y][x] = 1
                    if val == 1:
                        level.overlay[y][x] = 0

        window.blit(draw_board(level, TILE_SIZE), (0, 0))
        pygame.display.update()
        
    return False if lost else won


level = create_level(WIDTH, HEIGHT, "EASY", [])
result = run_game(level)

if result != None:
    print("won" if result else "lost")
    print("moves:", level.moves)
    time.sleep(3)
    
pygame.quit()
