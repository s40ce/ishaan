import pygame
import random
import time
from math import log2

# --- Config ---
WIDTH, HEIGHT = 600, 640
ROWS, COLS = 20, 20
GRID_SIZE = WIDTH // COLS
TEXT_AREA = 40
MAX_TIME = 60  # Countdown time in seconds

# --- Colors ---
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Click Game")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# --- Game State ---
blue_cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
flashing_cell = None
flash_timer = 0
Sc = 0  # Correct clicks
Si = 0  # Incorrect clicks
start_time = time.time()

# --- Functions ---
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE + TEXT_AREA, GRID_SIZE, GRID_SIZE)
            color = WHITE
            if (row, col) == blue_cell:
                color = BLUE
            if (row, col) == flashing_cell and flash_timer > 0:
                color = RED
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

def draw_info(time_left, bitrate):
    score_text = font.render(f"Score: {Sc}", True, BLACK)
    miss_text = font.render(f"Misses: {Si}", True, BLACK)
    time_text = font.render(f"Time Left: {int(time_left)}s", True, BLACK)
    bitrate_text = font.render(f"B: {bitrate:.2f} bps", True, BLACK)

    screen.blit(score_text, (10, 5))
    screen.blit(miss_text, (140, 5))
    screen.blit(time_text, (260, 5))
    screen.blit(bitrate_text, (400, 5))

def get_cell_from_mouse(pos):
    x, y = pos
    if y < TEXT_AREA:
        return (-1, -1)
    col = x // GRID_SIZE
    row = (y - TEXT_AREA) // GRID_SIZE
    return (row, col)

# --- Main Loop ---
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Update time & state
    time_left = max(0, MAX_TIME - (time.time() - start_time))
    game_active = time_left > 0

    # Calculate bitrate
    N = ROWS * COLS  # total symbols
    elapsed = MAX_TIME - time_left
    bitrate = max(0, log2(N - 1) * (Sc - Si) / (elapsed if elapsed > 0 else 1e-5))

    # Stop blue cell if game over
    if not game_active:
        blue_cell = None

    # Handle flashing red cell timer
    if flash_timer > 0:
        flash_timer -= clock.get_time()
    else:
        flashing_cell = None

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and game_active:
            clicked = get_cell_from_mouse(pygame.mouse.get_pos())

            if 0 <= clicked[0] < ROWS and 0 <= clicked[1] < COLS:
                if clicked == blue_cell:
                    Sc += 1
                    while True:
                        new_cell = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
                        if new_cell != blue_cell:
                            blue_cell = new_cell
                            break
                else:
                    Si += 1
                    flashing_cell = clicked
                    flash_timer = 200

    # Draw
    draw_grid()
    draw_info(time_left, bitrate)

    if not game_active:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 70, TEXT_AREA // 2 - 10))

    pygame.display.flip()

pygame.quit()
