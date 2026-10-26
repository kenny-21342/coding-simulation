"""
DEBUG CHALLENGE 4: THE CRASH
What should happen: press SPACE and the rocket launches upwards.
What actually happens: press SPACE. The program crashes!
Read the red error message (the "traceback"): it tells you the line number
and what went wrong. Fix it. (Hint card in README.md)
"""
import pygame

THRUST = 900             # upward push, pixels per second squared
GRAVITY = 400

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug 4: the crash")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)

y = HEIGHT - 80.0
velocity = 0.0
engine_on = False

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            engine_on = not engine_on
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            y, velocity, engine_on = HEIGHT - 80.0, 0.0, False

    if engine_on:
        velocty -= THRUST * dt
    velocity += GRAVITY * dt
    y += velocity * dt
    if y > HEIGHT - 80:
        y, velocity = HEIGHT - 80.0, 0.0
    y = max(0, y)

    screen.fill((14, 16, 28))
    pygame.draw.polygon(screen, (230, 230, 240), [(450, y - 40), (430, y + 20), (470, y + 20)])
    if engine_on:
        pygame.draw.polygon(screen, (255, 140, 40), [(435, y + 20), (465, y + 20), (450, y + 55)])
    screen.blit(font.render("SPACE engine on/off   R restart", True, (230, 230, 235)), (20, 20))
    pygame.display.flip()

pygame.quit()
