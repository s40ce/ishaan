import pygame
import sys
import random
import time

# Grid settings
ROWS, COLS = 20, 20
CELL_SIZE = 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Blue Cell (Flash Red)")
clock = pygame.time.Clock()

# Blue cell
blue_cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

# Red flash tracking
flashing_cell = None
flash_timer = 0  # In milliseconds

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = WHITE

            if (row, col) == blue_cell:
                color = BLUE
            elif (row, col) == flashing_cell:
                color = RED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def get_cell_from_mouse(pos):
    x, y = pos
    return (y // CELL_SIZE, x // CELL_SIZE)

# Main loop
while True:
    dt = clock.tick(60)  # Milliseconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_cell_from_mouse(pygame.mouse.get_pos())

            if clicked == blue_cell:
                # Move blue cell to new spot
                while True:
                    new_cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
                    if new_cell != blue_cell:
                        blue_cell = new_cell
                        break
            else:
                # Flash red cell for 200 ms
                flashing_cell = clicked
                flash_timer = 200

    # Handle red flash timer
    if flash_timer > 0:
        flash_timer -= dt
        if flash_timer <= 0:
            flashing_cell = None

    draw_grid()
    pygame.display.flip()
