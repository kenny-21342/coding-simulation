"""
DEBUG CHALLENGE 3: THE WONKY CANNON
What should happen: the cannon fires at the angle shown on screen.
What actually happens: press SPACE a few times, change the angle with UP/DOWN,
and compare where the ball goes with where the barrel points.
Find the bug and fix it. (Hint card in README.md)
"""
import math
import pygame

ANGLE = 45               # degrees
SPEED = 600              # pixels per second
GRAVITY = 500

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debug 3: the wonky cannon")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
GROUND = HEIGHT - 50
ball = None

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ANGLE = min(85, ANGLE + 5)
            if event.key == pygame.K_DOWN:
                ANGLE = max(5, ANGLE - 5)
            if event.key == pygame.K_SPACE:
                vx = SPEED * math.cos(ANGLE)
                vy = -SPEED * math.sin(ANGLE)
                ball = [60.0, float(GROUND), vx, vy]

    if ball:
        ball[3] += GRAVITY * dt
        ball[0] += ball[2] * dt
        ball[1] += ball[3] * dt
        if ball[1] > GROUND:
            ball[1] = GROUND
            ball[2] = ball[3] = 0

    screen.fill((14, 16, 28))
    pygame.draw.rect(screen, (40, 70, 45), (0, GROUND, WIDTH, HEIGHT - GROUND))
    a = math.radians(ANGLE)
    pygame.draw.line(screen, (200, 200, 210), (60, GROUND), (60 + 50 * math.cos(a), GROUND - 50 * math.sin(a)), 10)
    if ball:
        pygame.draw.circle(screen, (255, 200, 60), (int(ball[0]), int(ball[1])), 10)
    screen.blit(font.render(f"Angle = {ANGLE}°   SPACE fire   UP/DOWN angle", True, (230, 230, 235)), (20, 20))
    pygame.display.flip()

pygame.quit()
