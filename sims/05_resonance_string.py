"""
RESONANCE ON A STRING
The left end of a string is wiggled up and down. At most frequencies the
string just shivers. At special frequencies (the harmonics) the waves line up
and the string swings hugely: that is resonance. Count the nodes (still points).

The string is set up so its first harmonic is exactly 1 Hz.
Harmonic n is at n Hz: 1, 2, 3, 4 ...

Controls
  UP / DOWN       frequency up / down by 0.05 Hz
  RIGHT / LEFT    frequency up / down by 0.01 Hz (fine tuning)
  1 to 6          jump straight to harmonic 1 to 6
  SPACE           pause the wiggling (watch the string ring by itself)
  R               calm the string down
  F               fullscreen on / off
  ESC             quit
"""
import math
import pygame

# ===================== PLAY WITH ME =====================
DRIVE_FREQUENCY = 0.70   # Hz: how fast the left end wiggles (start off-resonance)
DRIVE_SIZE = 0.004       # how far the left end moves (tiny!)
WAVE_SPEED = 2.0         # metres per second; harmonic 1 = WAVE_SPEED / (2 x LENGTH)
STRING_LENGTH = 1.0      # metres
DAMPING = 0.15            # energy loss: 0 = none (it grows forever!), 1 = very floppy
POINTS = 160             # how many pieces the string is made of
TIME_SPEED = 1.0
# ========================================================

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Resonance on a String")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)

dx = STRING_LENGTH / POINTS
dt_max = 0.9 * dx / WAVE_SPEED          # small enough for the maths to stay stable
u = [0.0] * (POINTS + 1)                # height of each point now
u_old = [0.0] * (POINTS + 1)            # height one step ago
t = 0.0
driving = True
peak_history = []


def first_harmonic():
    return WAVE_SPEED / (2 * STRING_LENGTH)


def step(dt):
    """Wave equation: acceleration = speed² x curvature, minus damping."""
    global u, u_old, t
    c2 = (WAVE_SPEED * dt / dx) ** 2
    damp = DAMPING * dt
    new = [0.0] * (POINTS + 1)
    for i in range(1, POINTS):
        curvature = u[i + 1] - 2 * u[i] + u[i - 1]
        new[i] = (2 * u[i] - (1 - damp) * u_old[i] + c2 * curvature) / (1 + damp)
    t += dt
    new[0] = DRIVE_SIZE * math.sin(2 * math.pi * DRIVE_FREQUENCY * t) if driving else 0.0
    new[POINTS] = 0.0                    # the right end is tied down
    u_old, u = u, new


running = True
while running:
    frame = clock.tick(60) / 1000 * TIME_SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                DRIVE_FREQUENCY = round(DRIVE_FREQUENCY + 0.05, 2)
            elif event.key == pygame.K_DOWN:
                DRIVE_FREQUENCY = max(0.05, round(DRIVE_FREQUENCY - 0.05, 2))
            elif event.key == pygame.K_RIGHT:
                DRIVE_FREQUENCY = round(DRIVE_FREQUENCY + 0.01, 2)
            elif event.key == pygame.K_LEFT:
                DRIVE_FREQUENCY = max(0.01, round(DRIVE_FREQUENCY - 0.01, 2))
            elif pygame.K_1 <= event.key <= pygame.K_6:
                DRIVE_FREQUENCY = round((event.key - pygame.K_0) * first_harmonic(), 2)
            elif event.key == pygame.K_SPACE:
                driving = not driving
            elif event.key == pygame.K_r:
                u = [0.0] * (POINTS + 1)
                u_old = [0.0] * (POINTS + 1)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    steps = max(1, math.ceil(frame / dt_max))
    for _ in range(steps):
        step(frame / steps)

    peak = max(abs(v) for v in u)
    peak_history = (peak_history + [peak])[-240:]
    swing = max(peak_history)

    screen.fill((14, 16, 28))
    left, right, mid = 120, WIDTH - 120, HEIGHT / 2 + 40
    scale = 260 / max(0.08, swing)       # zoom out automatically when it swings a lot
    scale = min(scale, 6000)
    pts = [(left + (right - left) * i / POINTS, mid - u[i] * scale) for i in range(POINTS + 1)]
    pygame.draw.line(screen, (50, 55, 75), (left, mid), (right, mid), 1)
    pygame.draw.lines(screen, (90, 200, 255), False, pts, 4)
    pygame.draw.rect(screen, (255, 160, 80), (left - 30, pts[0][1] - 20, 24, 40))    # the wiggler
    pygame.draw.rect(screen, (160, 160, 170), (right + 6, mid - 40, 18, 80))         # the wall

    n_near = max(1, round(DRIVE_FREQUENCY / first_harmonic()))
    target = n_near * first_harmonic()
    off_by = DRIVE_FREQUENCY - target
    on_resonance = abs(off_by) < 0.03
    screen.blit(big_font.render("Resonance on a String", True, (255, 255, 255)), (24, 18))
    screen.blit(font.render(f"Wiggle frequency: {DRIVE_FREQUENCY:.2f} Hz    "
                            f"Nearest harmonic: n = {n_near} at {target:.2f} Hz", True, (230, 230, 235)), (24, 60))
    status = "RESONANCE!" if on_resonance else f"off by {off_by:+.2f} Hz"
    screen.blit(big_font.render(status, True, (255, 200, 60) if on_resonance else (160, 160, 170)), (24, 92))
    bar = min(1.0, swing / 0.06)
    pygame.draw.rect(screen, (60, 60, 70), (24, 136, 320, 16))
    pygame.draw.rect(screen, (255, 200, 60), (24, 136, int(320 * bar), 16))
    screen.blit(font.render(f"Swing size (the wiggler moves only {DRIVE_SIZE * 100:.1f} cm)", True, (200, 200, 210)),
                (356, 131))
    if not driving:
        screen.blit(font.render("Wiggler paused: the string keeps ringing until damping stops it",
                                True, (255, 160, 120)), (24, 164))
    screen.blit(font.render("UP/DOWN 0.05 Hz   LEFT/RIGHT 0.01 Hz   1-6 harmonics   SPACE pause   R calm   F fullscreen",
                            True, (140, 140, 150)), (24, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
