import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 1100))

columns = 10
rows = 20
cell_size = 50
grid = [[0 for _ in range(10)] for _ in range(20)]

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


class Tetris:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y

    def draw(self, screen, cell_size):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] == 1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     ((self.x + col) * cell_size, (self.y + row) * cell_size, cell_size, cell_size))

    def move_down(self):
        self.y += 1

    def rotate(self):
        a = [list(row) for row in zip(*self.shape)]
        b = [row[::-1] for row in a]
        self.shape = b

tetrimino = Tetris(L_SHAPE, 4, 0)

fall_speed = 500
last_fall_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True
while running:
    # poll for events

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for row in range(20):
        for col in range(10):
            x = col * cell_size
            y = row * cell_size
            color = (0, 0, 0)
            if grid[row][col] == 1:
                color = (0, 255, 255)
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size), 1)

    current_time = pygame.time.get_ticks()
    if current_time - last_fall_time > fall_speed:
        tetrimino.move_down()  # Descendre la pièce
        # Mettre à jour le temps du dernier déplacement vers le bas
        last_fall_time = current_time

    tetrimino.draw(screen, cell_size)

    pygame.display.flip()

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetrimino.x -= 1
            elif event.key == pygame.K_RIGHT:
                tetrimino.x += 1
            elif event.key == pygame.K_DOWN:
                tetrimino.move_down()
            elif event.key == pygame.K_UP:
                tetrimino.rotate()
    clock.tick(60)

pygame.quit()
