"""
PENDULUM PAINTING (HARMONOGRAPH)
Two swinging pendulums move a pen: one pushes it left-right, one up-down.
Each swing slowly dies away, so the pen spirals inwards and draws a pattern.
This is the same physics as the pendulum painting event and the Lissajous
figures on the oscilloscope.

Controls
  SPACE         new random pattern
  1 2 3 4 5     ready-made patterns
  R             redraw the current pattern
  S             save the picture as a PNG next to this file
  UP / DOWN     draw faster / slower
  F             fullscreen on / off
  ESC           quit
"""
import math
import os
import random
import pygame

# ===================== PLAY WITH ME =====================
# Each pendulum: frequency (swings per second), phase (starting point, 0 to 6.28),
# damping (how fast it dies away: 0 = never stops, 0.1 = stops quickly)
FREQ_X = 2.00
FREQ_Y = 3.01            # try a ratio close to a simple fraction: 2 and 3, 3 and 4 ...
PHASE_X = 0.0
PHASE_Y = 1.57
DAMPING_X = 0.02 
DAMPING_Y = 0.02 
# A second, smaller pendulum adds to each direction (set its size to 0 to switch it off)
FREQ_X2 = 3.00
FREQ_Y2 = 2.00
SIZE_2 = 0.35            # 0.0 to 1.0, size compared with the main pendulum
DRAW_SPEED = 1.0         # 1.0 = real time, 3.0 = three times faster
LINE_WIDTH = 2
COLOUR_CHANGE = True     # rainbow pen? False = white pen
# ========================================================

PRESETS = {
    pygame.K_1: (2.00, 3.01, 0.0, 1.57, 3.00, 2.00, 0.00),   # simple Lissajous knot
    pygame.K_2: (3.00, 4.01, 0.0, 1.57, 4.00, 3.00, 0.30),
    pygame.K_3: (2.01, 2.00, 0.0, 1.57, 6.00, 6.01, 0.40),   # nearly equal = rotating ellipse
    pygame.K_4: (5.00, 4.00, 0.3, 0.0, 1.00, 1.01, 0.50),
    pygame.K_5: (1.00, 1.00, 0.0, 1.57, 7.00, 7.02, 0.60),
}

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Painting")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)
canvas = pygame.Surface((WIDTH, HEIGHT))
CX, CY = WIDTH / 2 + 120, HEIGHT / 2
SCALE = HEIGHT * 0.42 / (1 + SIZE_2 if SIZE_2 > 0 else 1)
saved_message = 0.0


def pen_position(t):
    dx, dy = math.exp(-DAMPING_X * t), math.exp(-DAMPING_Y * t)
    x = dx * (math.sin(2 * math.pi * FREQ_X * t + PHASE_X) + SIZE_2 * math.sin(2 * math.pi * FREQ_X2 * t))
    y = dy * (math.sin(2 * math.pi * FREQ_Y * t + PHASE_Y) + SIZE_2 * math.sin(2 * math.pi * FREQ_Y2 * t + 0.7))
    return CX + x * SCALE, CY + y * SCALE


def restart():
    global t, last_point, SCALE
    SCALE = HEIGHT * 0.42 / (1 + SIZE_2)
    canvas.fill((10, 10, 18))
    t = 0.0
    last_point = pen_position(0)


restart()
running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                a, b = random.randint(1, 5), random.randint(1, 5)
                FREQ_X, FREQ_Y = a + random.choice([0, 0.01, 0.02]), b + random.choice([0, 0.01])
                FREQ_X2, FREQ_Y2 = random.randint(1, 7), random.randint(1, 7)
                PHASE_X, PHASE_Y = random.uniform(0, 6.28), random.uniform(0, 6.28)
                SIZE_2 = random.choice([0, 0.2, 0.35, 0.5])
                restart()
            elif event.key in PRESETS:
                FREQ_X, FREQ_Y, PHASE_X, PHASE_Y, FREQ_X2, FREQ_Y2, SIZE_2 = PRESETS[event.key]
                restart()
            elif event.key == pygame.K_r:
                restart()
            elif event.key == pygame.K_s:
                name = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    f"pendulum_painting_{pygame.time.get_ticks()}.png")
                pygame.image.save(canvas, name)
                saved_message = 3.0
            elif event.key == pygame.K_UP:
                DRAW_SPEED = min(10, DRAW_SPEED * 1.5)
            elif event.key == pygame.K_DOWN:
                DRAW_SPEED = max(0.2, DRAW_SPEED / 1.5)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    # draw many tiny line pieces this frame
    pieces = 60
    if math.exp(-min(DAMPING_X, DAMPING_Y) * t) > 0.02:       # stop when the swing has died away
        for _ in range(pieces):
            t += DRAW_SPEED * dt / pieces
            point = pen_position(t)
            colour = pygame.Color(0)
            if COLOUR_CHANGE:
                colour.hsva = ((t * 6) % 360, 70, 100, 100)
            else:
                colour = pygame.Color(235, 235, 240)
            pygame.draw.line(canvas, colour, last_point, point, LINE_WIDTH)
            last_point = point

    screen.blit(canvas, (0, 0))
    pygame.draw.circle(screen, (255, 255, 255), (int(last_point[0]), int(last_point[1])), 5)
    screen.blit(big_font.render("Pendulum Painting", True, (255, 255, 255)), (24, 18))
    lines = [f"Left-right swing: {FREQ_X:.2f} Hz", f"Up-down swing:   {FREQ_Y:.2f} Hz",
             f"Ratio: {FREQ_X / FREQ_Y:.3f}", f"Second pendulum: {FREQ_X2:.0f} / {FREQ_Y2:.0f} Hz, size {SIZE_2:.2f}",
             f"Swing left: {math.exp(-DAMPING_X * t) * 100:.0f}%"]
    for i, text in enumerate(lines):
        screen.blit(font.render(text, True, (220, 220, 230)), (24, 64 + i * 28))
    if saved_message > 0:
        screen.blit(font.render("Saved! The PNG is in the sims folder.", True, (120, 230, 140)), (24, 220))
        saved_message -= dt
    screen.blit(font.render("SPACE random   1-5 presets   R redraw   S save   UP/DOWN speed   F fullscreen",
                            True, (140, 140, 150)), (24, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
