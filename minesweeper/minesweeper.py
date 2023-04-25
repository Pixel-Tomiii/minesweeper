import pygame
import random

import time

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

    
class Level():
    def __init__(self, width, height, world, overlay):
        self.width = width
        self.height = height
        self.world = world
        self.overlay = overlay

    def is_mine(self, x, y):
        return self.world[y][x] == -1


def create_level(width, height, mines):
    # Create board of zeros.
    level = [[0 for _ in range(width)] for __ in range(height)]
    overlay = [[0 for _ in range(width)] for __ in range(height)]

    positions = set()

    for y in range(height):
        for x in range(width):
            positions.add((x, y))

    positions = list(positions)

    # Place mines.
    for _ in range(mines):
        index = random.randint(0, len(positions) - 1)
        x, y = positions.pop(index)
        level[y][x] = -1

        for y_off in range(-1, 2):
            for x_off in range(-1, 2):
                if y_off == 0 and y_off == x_off:
                    continue
                if not 0 <= y + y_off < height:
                    continue
                if not 0 <= x + x_off < width:
                    continue
                if level[y + y_off][x + x_off] != -1:
                    level[y + y_off][x + x_off] += 1

    return Level(width, height, level, overlay)


def get_revealed(level, x, y):
    visited = set()
    to_check = set([(x, y)])

    while len(to_check) > 0:
        x, y = to_check.pop()      
        visited.add((x, y))

        if level.world[y][x] != 0:
            continue

        for y_off in range(-1, 2):
            if not 0 <= y + y_off < level.height:
                continue
            for x_off in range(-1, 2):
                if not 0 <= x + x_off < level.width:
                    continue
                
                next_pos = (x + x_off, y + y_off)
                if next_pos in visited:
                    continue
                if next_pos in to_check:
                    continue
                to_check.add(next_pos)
    return list(visited)


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


def check_won(level):
    for y, row in enumerate(level.overlay):
        for x, val in enumerate(row):
            if val != -1 and level.world[y][x] != -1:
                return False
    return True


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
                    val = level.overlay[y][x]
                    if val == 0:
                        level.overlay[y][x] = 1
                    if val == 1:
                        level.overlay[y][x] = 0

        window.blit(draw_board(level, TILE_SIZE), (0, 0))
        pygame.display.update()
        
    return False if lost else won


level = create_level(WIDTH, HEIGHT, MINES)
result = run_game(level)

if result != None:
    print("won" if result else "lost")
    time.sleep(3)
    
pygame.quit()
