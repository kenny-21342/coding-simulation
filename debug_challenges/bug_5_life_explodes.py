"""
DEBUG CHALLENGE 5 (HARD): LIFE THAT NEVER DIES
What should happen: Conway's Game of Life. Live cells with 2 or 3 neighbours
survive, everything else dies, and dead cells with exactly 3 neighbours are born.
What actually happens: run it. Cells never die and the screen fills up.
There are no error messages. The bug is a very common Python mistake.
Find it and fix it. (Hint card in README.md)
"""
import random
import pygame

CELL = 14

pygame.init()
WIDTH, HEIGHT = 896, 602
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug 5: life that never dies")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
COLS, ROWS = WIDTH // CELL, HEIGHT // CELL
alive = {(c, r) for c in range(COLS) for r in range(ROWS) if random.random() < 0.15}


def count_neighbours(c, r):
    n = 0
    for dc in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if (dc or dr) and ((c + dc) % COLS, (r + dr) % ROWS) in alive:
                n += 1
    return n


running = True
while running:
    clock.tick(8)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            alive = {(c, r) for c in range(COLS) for r in range(ROWS) if random.random() < 0.15}

    new_alive = set()
    for c in range(COLS):
        for r in range(ROWS):
            n = count_neighbours(c, r)
            if (c, r) in alive:
                if n == 2 or 3:
                    new_alive.add((c, r))
            else:
                if n == 3:
                    new_alive.add((c, r))
    alive = new_alive

    screen.fill((8, 10, 18))
    for (c, r) in alive:
        pygame.draw.rect(screen, (90, 200, 255), (c * CELL + 1, r * CELL + 1, CELL - 2, CELL - 2))
    screen.blit(font.render(f"Alive: {len(alive)}   (R to restart)", True, (255, 255, 255)), (16, 12))
    pygame.display.flip()

pygame.quit()
