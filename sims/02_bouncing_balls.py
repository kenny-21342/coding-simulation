"""
BOUNCING BALLS
Balls fall, bounce and crash into each other. Watch the energy bar:
with BOUNCINESS below 1, energy is lost on every bounce.

Controls
  Click         add a ball where you click
  SPACE         shake the box (kick every ball upwards)
  G             gravity on / off
  UP / DOWN     more / less bouncy
  R             start again
  F             fullscreen on / off
  ESC           quit
"""
import math
import random
import pygame

# ===================== PLAY WITH ME =====================
NUMBER_OF_BALLS = 20
GRAVITY = 600            # pixels per second squared (try 0, 100, 2000)
BOUNCINESS = 0.85        # 1.0 = perfect bounce, 0.5 = loses half its speed
AIR_FRICTION = 0.0       # 0.0 = none, 0.5 = like moving through honey
MIN_RADIUS = 12          # pixels
MAX_RADIUS = 40          # pixels
BALLS_HIT_EACH_OTHER = True
SHAKE_STRENGTH = 700     # how hard SPACE kicks the balls
# ========================================================

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)
gravity_on = GRAVITY != 0
G = GRAVITY if GRAVITY != 0 else 600


class Ball:
    def __init__(self, x, y):
        self.r = random.randint(MIN_RADIUS, MAX_RADIUS)
        self.mass = self.r ** 2                      # bigger ball = heavier
        self.x, self.y = x, y
        self.vx = random.uniform(-250, 250)
        self.vy = random.uniform(-250, 50)
        self.colour = pygame.Color(0)
        self.colour.hsva = (random.randint(0, 359), 70, 100, 100)

    def move(self, dt):
        if gravity_on:
            self.vy += G * dt
        self.vx *= (1 - AIR_FRICTION * dt)
        self.vy *= (1 - AIR_FRICTION * dt)
        self.x += self.vx * dt
        self.y += self.vy * dt
        # walls: push the ball back inside, then flip and shrink its speed
        if self.x - self.r < 0:
            self.x = self.r
            self.vx = abs(self.vx) * BOUNCINESS
        if self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx = -abs(self.vx) * BOUNCINESS
        if self.y - self.r < 0:
            self.y = self.r
            self.vy = abs(self.vy) * BOUNCINESS
        if self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -abs(self.vy) * BOUNCINESS

    def energy(self):
        kinetic = 0.5 * self.mass * (self.vx ** 2 + self.vy ** 2)
        potential = self.mass * (G if gravity_on else 0) * (HEIGHT - self.y - self.r)
        return kinetic + potential


def collide(a, b):
    dx, dy = b.x - a.x, b.y - a.y
    dist = math.hypot(dx, dy)
    if dist == 0 or dist >= a.r + b.r:
        return
    nx, ny = dx / dist, dy / dist                    # direction from a to b
    overlap = a.r + b.r - dist                       # push them apart so they don't stick
    total = a.mass + b.mass
    a.x -= nx * overlap * b.mass / total
    a.y -= ny * overlap * b.mass / total
    b.x += nx * overlap * a.mass / total
    b.y += ny * overlap * a.mass / total
    closing = (a.vx - b.vx) * nx + (a.vy - b.vy) * ny
    if closing <= 0:                                 # already moving apart
        return
    impulse = (1 + BOUNCINESS) * closing / (1 / a.mass + 1 / b.mass)
    a.vx -= impulse / a.mass * nx
    a.vy -= impulse / a.mass * ny
    b.vx += impulse / b.mass * nx
    b.vy += impulse / b.mass * ny


def new_balls():
    return [Ball(random.uniform(MAX_RADIUS, WIDTH - MAX_RADIUS), random.uniform(MAX_RADIUS, HEIGHT / 2))
            for _ in range(NUMBER_OF_BALLS)]


balls = new_balls()
start_energy = sum(b.energy() for b in balls) or 1

running = True
while running:
    dt = min(clock.tick(60) / 1000, 1 / 30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(*event.pos))
            start_energy = sum(b.energy() for b in balls) or 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                for b in balls:
                    b.vy -= random.uniform(0.6, 1.0) * SHAKE_STRENGTH
                    b.vx += random.uniform(-0.5, 0.5) * SHAKE_STRENGTH
                start_energy = sum(b.energy() for b in balls) or 1
            elif event.key == pygame.K_g:
                gravity_on = not gravity_on
                start_energy = sum(b.energy() for b in balls) or 1
            elif event.key == pygame.K_UP:
                BOUNCINESS = min(1.0, round(BOUNCINESS + 0.05, 2))
            elif event.key == pygame.K_DOWN:
                BOUNCINESS = max(0.0, round(BOUNCINESS - 0.05, 2))
            elif event.key == pygame.K_r:
                balls = new_balls()
                start_energy = sum(b.energy() for b in balls) or 1
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    for _ in range(2):                               # two half-steps per frame = fewer missed hits
        for b in balls:
            b.move(dt / 2)
        if BALLS_HIT_EACH_OTHER:
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    collide(balls[i], balls[j])

    screen.fill((14, 16, 28))
    for b in balls:
        pygame.draw.circle(screen, b.colour, (int(b.x), int(b.y)), b.r)
    energy_left = sum(b.energy() for b in balls) / start_energy
    bar_w = 300
    pygame.draw.rect(screen, (60, 60, 70), (24, 110, bar_w, 18))
    pygame.draw.rect(screen, (255, 200, 60), (24, 110, int(bar_w * max(0, min(1, energy_left))), 18))
    screen.blit(big_font.render("Bouncing Balls", True, (255, 255, 255)), (24, 18))
    screen.blit(font.render(f"Balls: {len(balls)}   Bounciness: {BOUNCINESS:.2f}   "
                            f"Gravity: {'ON' if gravity_on else 'OFF'}", True, (230, 230, 235)), (24, 60))
    screen.blit(font.render(f"Energy left: {energy_left * 100:.0f}%", True, (255, 200, 60)), (24, 82))
    screen.blit(font.render("Click add ball   SPACE shake   G gravity   UP/DOWN bounciness   R reset   F fullscreen",
                            True, (140, 140, 150)), (24, HEIGHT - 30))
    pygame.display.flip()

pygame.quit()
