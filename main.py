import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 1020))

columns = 10
rows = 20
cell_size = 50
grid = [[0 for _ in range(10)] for _ in range(20)]
score = 0  # Score initialisé

T_SHAPE = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0]
]

L_SHAPE = [
    [1, 0],
    [1, 0],
    [1, 1]
]

J_SHAPE = [
    [0, 1],
    [0, 1],
    [1, 1]
]

I_SHAPE = [
    [1],
    [1],
    [1],
    [1]
]

O_SHAPE = [
    [1, 1],
    [1, 1]
]

S_SHAPE = [
    [0, 1, 1],
    [1, 1, 0]
]

Z_SHAPE = [
    [1, 1, 0],
    [0, 1, 1]
]

SHAPES = [T_SHAPE, L_SHAPE, J_SHAPE, I_SHAPE, O_SHAPE, S_SHAPE, Z_SHAPE]


def clear_full_rows(grid):
    full_rows = [row for row in range(len(grid)) if all(grid[row])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [0] * len(grid[0]))
    return len(full_rows)  # Nombre de lignes supprimées


class Tetris:
    def __init__(self, shape, x, y, grid_width, grid_height):
        self.shape = shape
        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height

    def valid_pos(self, mx=0, my=0):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:
                    new_x = self.x + col + mx
                    new_y = self.y + row + my
                    if new_x < 0 or new_x >= self.grid_width or new_y >= self.grid_height:
                        return False
                    if new_y >= 0 and grid[new_y][new_x] == 1:
                        return False
        return True

    def draw(self, screen, cell_size):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     ((self.x + col) * cell_size,
                                      (self.y + row) * cell_size,
                                      cell_size,
                                      cell_size))

    def move_down(self, grid):
        if self.valid_pos(my=1):
            self.y += 1
        else:
            self.lock_piece(grid)

    def move_left(self):
        if self.valid_pos(mx=-1):
            self.x -= 1

    def move_right(self):
        if self.valid_pos(mx=1):
            self.x += 1

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def rotate(self):
        """Fait tourner la pièce si possible"""
        new_shape = self.rotate_shape(self.shape)
        old_shape = self.shape
        self.shape = new_shape
        if not self.valid_pos():
            self.shape = old_shape

    def lock_piece(self, grid):
        """Fixe la pièce et génère une nouvelle pièce"""
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:
                    grid[self.y + row][self.x + col] = 1


def draw_next_piece(screen, next_tetrimino, cell_size):
    x = 600  # Position X pour l'affichage de la prochaine pièce (à droite)
    y = 100  # Position Y pour l'affichage de la prochaine pièce (en haut)
    for row in range(len(next_tetrimino.shape)):
        for col in range(len(next_tetrimino.shape[row])):
            if next_tetrimino.shape[row][col] == 1:
                pygame.draw.rect(screen, (255, 0, 0),
                                 (x + col * cell_size,
                                  y + row * cell_size,
                                  cell_size, cell_size))


tetris = Tetris(random.choice(SHAPES), 4, 0, columns, rows)
next_tetrimino = Tetris(random.choice(SHAPES), 4, 0, columns, rows)

fall_speed = 500
last_fall_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
while running:
    screen.fill("black")

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (600, 10))

    for row in range(20):
        for col in range(10):
            x = col * cell_size
            y = row * cell_size
            color = (96, 96, 96)
            if grid[row][col] == 1:
                color = (0, 255, 255)
                pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(
                    screen, color, (x, y, cell_size, cell_size), 1)

    current_time = pygame.time.get_ticks()
    if current_time - last_fall_time > fall_speed:
        tetris.move_down(grid)
        last_fall_time = current_time

    if not tetris.valid_pos(my=1):
        tetris.lock_piece(grid)
        tetris = next_tetrimino
        next_tetrimino = Tetris(random.choice(SHAPES), 4, 0, columns, rows)
        score += clear_full_rows(grid) * 100

    tetris.draw(screen, cell_size)
    # Afficher la prochaine pièce
    draw_next_piece(screen, next_tetrimino, cell_size)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move_left()
            elif event.key == pygame.K_RIGHT:
                tetris.move_right()
            elif event.key == pygame.K_DOWN:
                tetris.move_down(grid)
            elif event.key == pygame.K_UP:
                tetris.rotate()

    clock.tick(60)

pygame.quit()
