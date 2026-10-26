"""
DEBUG CHALLENGE 2: THE STICKY WALL
What should happen: the ball bounces around inside the window forever.
What actually happens: run it and watch the right-hand wall.
Find the ONE line that is wrong and fix it. (Hint card in README.md)
"""
import pygame

BOUNCINESS = 1.0

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug 2: the sticky wall")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

x, y = 200.0, 300.0
vx, vy = 350.0, 220.0
radius = 25

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            x, y, vx, vy = 200.0, 300.0, 350.0, 220.0

    x += vx * dt
    y += vy * dt

    if x - radius < 0:                   # left wall
        x = radius
        vx = -vx * BOUNCINESS
    if x + radius > WIDTH:               # right wall
        x = WIDTH - radius
        vx = vx * BOUNCINESS
    if y - radius < 0:                   # ceiling
        y = radius
        vy = -vy * BOUNCINESS
    if y + radius > HEIGHT:              # floor
        y = HEIGHT - radius
        vy = -vy * BOUNCINESS

    screen.fill((14, 16, 28))
    pygame.draw.circle(screen, (90, 200, 255), (int(x), int(y)), radius)
    screen.blit(font.render(f"x = {x:.0f}   vx = {vx:.0f}   (R to restart)", True, (230, 230, 235)), (20, 20))
    pygame.display.flip()

pygame.quit()
