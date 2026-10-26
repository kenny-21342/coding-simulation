"""
DEBUG CHALLENGE 1: THE BALL FALLS UP
What should happen: the ball drops and bounces on the floor.
What actually happens: run it and see.
Find the ONE line that is wrong and fix it. (Hint card in README.md)
"""
import pygame

GRAVITY = 800            # pixels per second squared
BOUNCINESS = 0.8

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug 1: the ball falls up")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

x, y = WIDTH / 2, 100
vy = 0.0
radius = 25

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            y, vy = 100, 0.0

    # On a screen, y gets BIGGER as you go DOWN.
    vy -= GRAVITY * dt
    y += vy * dt

    if y + radius > HEIGHT:              # hit the floor
        y = HEIGHT - radius
        vy = -vy * BOUNCINESS

    screen.fill((14, 16, 28))
    pygame.draw.circle(screen, (255, 160, 80), (int(x), int(y)), radius)
    screen.blit(font.render(f"y = {y:.0f}   speed = {vy:.0f}   (R to restart)", True, (230, 230, 235)), (20, 20))
    pygame.display.flip()

pygame.quit()
