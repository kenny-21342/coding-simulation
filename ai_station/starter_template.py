"""
STARTER TEMPLATE
An empty simulation that already runs. Use it two ways:
  1. Write your own: fill in the three TODO parts.
  2. With AI: paste this file into the AI and ask it to fill in the TODOs for your idea.
"""
import math
import random
import pygame

# ===================== PLAY WITH ME =====================
GRAVITY = 500            # pixels per second squared
# TODO 1: add your own numbers here
# ========================================================

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

# TODO 2: set up your objects (position, velocity, size ...)
x, y = WIDTH / 2, 100.0
vx, vy = 0.0, 0.0

running = True
while running:
    dt = clock.tick(60) / 1000                 # seconds since the last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # TODO 3: the physics. Change velocity, then change position.
    vy += GRAVITY * dt
    x += vx * dt
    y += vy * dt
    if y > HEIGHT - 20:
        y, vy = HEIGHT - 20, -vy * 0.8

    screen.fill((14, 16, 28))
    pygame.draw.circle(screen, (255, 160, 80), (int(x), int(y)), 20)
    screen.blit(font.render(f"y = {y:.0f}   vy = {vy:.0f}", True, (230, 230, 235)), (20, 20))
    pygame.display.flip()

pygame.quit()
