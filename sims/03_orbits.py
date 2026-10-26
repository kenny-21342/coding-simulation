"""
ORBITS
A star in the middle pulls on every planet with gravity.
Click and drag to throw a new planet: the arrow is its starting velocity.
Too slow and it crashes, too fast and it escapes. In between: an orbit.

Controls
  Click + drag  launch a planet (longer drag = faster)
  P             planets pull on each other on / off
  UP / DOWN     make the star heavier / lighter
  C             remove all planets
  R             start again
  F             fullscreen on / off
  ESC           quit
"""
import math
import random
import pygame

# ===================== PLAY WITH ME =====================
STAR_MASS = 4000         # how strongly the star pulls
GRAVITY_STRENGTH = 200   # the "G" in Newton's law F = G m1 m2 / r²
PLANETS_PULL_EACH_OTHER = False
START_PLANETS = 3        # planets placed in neat orbits at the start
TRAIL_LENGTH = 400       # how long the glowing trails are
LAUNCH_POWER = 1.5       # how much speed you get per pixel you drag
TIME_SPEED = 1.0         # 2.0 = double speed
STEPS_PER_FRAME = 8      # more steps = more accurate orbits (and slower)
# ========================================================

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbits")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)
CX, CY = WIDTH / 2, HEIGHT / 2
STAR_RADIUS = 26
messages = []            # (text, time left)


class Planet:
    def __init__(self, x, y, vx, vy, mass=None):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.mass = mass or random.uniform(1, 8)
        self.r = int(4 + self.mass)
        self.colour = pygame.Color(0)
        self.colour.hsva = (random.randint(150, 330), 60, 100, 100)
        self.trail = []


def circular_orbit(distance):
    """Speed needed for a perfect circle: v = sqrt(G M / r)"""
    angle = random.uniform(0, 2 * math.pi)
    v = math.sqrt(GRAVITY_STRENGTH * STAR_MASS / distance)
    x, y = CX + distance * math.cos(angle), CY + distance * math.sin(angle)
    return Planet(x, y, -v * math.sin(angle), v * math.cos(angle))


def start():
    return [circular_orbit(120 + i * 90) for i in range(START_PLANETS)]


def accelerations(planets):
    acc = []
    for p in planets:
        dx, dy = CX - p.x, CY - p.y
        r2 = dx * dx + dy * dy + 25
        r = math.sqrt(r2)
        a = GRAVITY_STRENGTH * STAR_MASS / r2
        ax, ay = a * dx / r, a * dy / r
        if PLANETS_PULL_EACH_OTHER:
            for q in planets:
                if q is p:
                    continue
                dx, dy = q.x - p.x, q.y - p.y
                r2 = dx * dx + dy * dy + 100
                r = math.sqrt(r2)
                a = GRAVITY_STRENGTH * q.mass * 20 / r2
                ax += a * dx / r
                ay += a * dy / r
        acc.append((ax, ay))
    return acc


def step(planets, dt):
    # "leapfrog" method: half kick, move, half kick (keeps orbits stable)
    acc = accelerations(planets)
    for p, (ax, ay) in zip(planets, acc):
        p.vx += ax * dt / 2
        p.vy += ay * dt / 2
        p.x += p.vx * dt
        p.y += p.vy * dt
    acc = accelerations(planets)
    for p, (ax, ay) in zip(planets, acc):
        p.vx += ax * dt / 2
        p.vy += ay * dt / 2


planets = start()
drag_start = None

running = True
while running:
    dt = clock.tick(60) / 1000 * TIME_SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag_start = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and drag_start:
            dx, dy = event.pos[0] - drag_start[0], event.pos[1] - drag_start[1]
            planets.append(Planet(drag_start[0], drag_start[1], dx * LAUNCH_POWER, dy * LAUNCH_POWER))
            drag_start = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                PLANETS_PULL_EACH_OTHER = not PLANETS_PULL_EACH_OTHER
            elif event.key == pygame.K_UP:
                STAR_MASS *= 1.2
            elif event.key == pygame.K_DOWN:
                STAR_MASS /= 1.2
            elif event.key == pygame.K_c:
                planets.clear()
            elif event.key == pygame.K_r:
                planets = start()
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    for _ in range(STEPS_PER_FRAME):
        step(planets, dt / STEPS_PER_FRAME)
    for p in planets[:]:
        p.trail.append((int(p.x), int(p.y)))
        p.trail = p.trail[-TRAIL_LENGTH:]
        if math.hypot(p.x - CX, p.y - CY) < STAR_RADIUS:
            planets.remove(p)
            messages.append(["A planet crashed into the star!", 2.5])
        elif math.hypot(p.x - CX, p.y - CY) > 3000:
            planets.remove(p)
            messages.append(["A planet escaped into space!", 2.5])

    screen.fill((6, 8, 18))
    for p in planets:
        if len(p.trail) > 1:
            pygame.draw.lines(screen, p.colour, False, p.trail, 1)
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.r)
    for glow in range(5, 0, -1):
        pygame.draw.circle(screen, (255, 160 + glow * 15, 40), (int(CX), int(CY)), STAR_RADIUS + glow * 4, 2)
    pygame.draw.circle(screen, (255, 230, 120), (int(CX), int(CY)), STAR_RADIUS)

    if drag_start:
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), drag_start, (mx, my), 2)
        pygame.draw.circle(screen, (255, 255, 255), drag_start, 6, 1)
        speed = math.hypot(mx - drag_start[0], my - drag_start[1]) * LAUNCH_POWER
        r = max(1, math.hypot(drag_start[0] - CX, drag_start[1] - CY))
        need = math.sqrt(GRAVITY_STRENGTH * STAR_MASS / r)
        screen.blit(font.render(f"speed {speed:.0f}  (circle needs {need:.0f}, escape needs {need * 1.414:.0f})",
                                True, (255, 255, 255)), (mx + 12, my + 12))

    screen.blit(big_font.render("Orbits", True, (255, 255, 255)), (24, 18))
    screen.blit(font.render(f"Planets: {len(planets)}   Star mass: {STAR_MASS:.0f}   "
                            f"Planets pull each other: {'ON' if PLANETS_PULL_EACH_OTHER else 'OFF'}",
                            True, (230, 230, 235)), (24, 60))
    y = 92
    for m in messages[:]:
        screen.blit(font.render(m[0], True, (255, 170, 120)), (24, y))
        y += 26
        m[1] -= dt
        if m[1] <= 0:
            messages.remove(m)
    screen.blit(font.render("Drag to launch   P planet gravity   UP/DOWN star mass   C clear   R reset   F fullscreen",
                            True, (140, 140, 150)), (24, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
