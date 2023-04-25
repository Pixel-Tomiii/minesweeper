from random import randint

DIFFICULTIES = {"EASY": 1,
                "MEDIUM": 2,
                "HARD": 3}

EMPTY = 0
MINE = -1
REVEALED = -1

class Level():
    """Defines certain members about a game of minesweeper"""
    def __init__(self, width, height, world, difficulty):
        self.width = width
        self.height = height
        self.world = world
        self.overlay = [[0 for _ in range(width)] for __ in range(height)]
        self.moves = 0
        self.difficulty = DIFFICULTIES[difficulty]

    def reset_overlay(self):
        self.overlay = [[0 for _ in range(width)] for __ in range(height)]
        self.moves = 0

    def get(self, pos):
        return self.world[pos[1]][pos[0]]


def create_level(width, height, difficulty, safezone):
    """Generate a level with the given properites."""
    world = [[0 for _ in range(width)] for __ in range(height)]
    mines = int((0.05 + (0.05 * DIFFICULTIES[difficulty]) * width * height))

    # Creating list of available positions for mines
    positions = set()
    for y in range(height):
        for x in range(width):
            positions.add((x, y))
    positions = list(positions.difference(set(safezone)))

    # Spawning mines
    for _ in range(mines):
        index = randint(0, len(positions) - 1)
        x, y = positions.pop(index)
        world[y][x] = MINE

        # Add 1 to surrounding tile values.
        for y_off in range(-1, 2):
            new_y = y + y_off
            # y value in grid
            if not (0 <= new_y < height):
                continue
            
            for x_off in range(-1, 2):
                new_x = x + x_off
                # x value in grid
                if not (0 <= new_x < width):
                    continue  

                if world[new_y][new_x] != MINE:
                    world[new_y][new_x] += 1
                    
    return Level(width, height, world, difficulty)


def check_won(level):
    """Checks to see if a level is won. A level is won if all non mine
    tiles are revealed. Returns True if won.
    """
    for y, row in enumerate(level.overlay):
        for x, val in enumerate(row):
            if val != REVEALED and level.get((x, y)) != MINE:
                return False
    return True


def get_revealed(level, x, y):
    """Returns a list of all the tiles that were revealed based on the
    tile that was selected.
    """
    visited = set()
    to_check = set([(x, y)])

    # Loop while there are still tiles to check.
    while len(to_check) > 0:
        x, y = pos = to_check.pop()
        visited.add(pos)

        # Stop on tiles that aren't empty 
        if level.get(pos) != EMPTY:
            continue

        # Get neighbors.
        for y_off in range(-1, 2):
            new_y = y + y_off
            if not (0 <= new_y < level.height):
                continue

            for x_off in range(-1, 2):
                new_x = x + x_off
                if not (0 <= new_x < level.width):
                    continue

                # Add neighbor to be checked
                next_pos = (new_x, new_y)
                if next_pos in visited:
                    continue
                if next_pos in to_check:
                    continue
                to_check.add(next_pos)
    return list(visited)
