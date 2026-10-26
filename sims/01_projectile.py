"""
PROJECTILE LAUNCHER
Fire a ball from a cannon. Change gravity, speed, angle and air resistance,
then compare where it lands with what the physics formula predicts.

Controls
  UP / DOWN     change the angle
  LEFT / RIGHT  change the launch speed
  SPACE         fire
  1 2 3 4       Earth, Moon, Mars, Jupiter gravity
  D             air resistance on / off
  C             clear the trails
  F             fullscreen on / off
  ESC           quit
"""
import math
import pygame

# ===================== PLAY WITH ME =====================
LAUNCH_SPEED = 25        # metres per second
LAUNCH_ANGLE = 45        # degrees above the ground
GRAVITY = 9.81           # metres per second squared (Earth = 9.81)
AIR_RESISTANCE = 0.02    # drag strength, try 0.0 to 0.1
DRAG_ON = False          # start with air resistance switched on?
PIXELS_PER_METRE = 12    # zoom: bigger number = everything looks bigger
TIME_SPEED = 1.0         # 2.0 = double speed, 0.5 = slow motion
BALL_RADIUS = 8          # pixels
TRAILS_TO_KEEP = 6       # how many old shots stay on screen
# ========================================================

PLANETS = {pygame.K_1: ("Earth", 9.81), pygame.K_2: ("Moon", 1.62),
           pygame.K_3: ("Mars", 3.71), pygame.K_4: ("Jupiter", 24.79)}
TRAIL_COLOURS = [(255, 120, 80), (255, 200, 60), (120, 220, 120),
                 (90, 180, 255), (200, 130, 255), (255, 110, 180)]

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Launcher")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)

GROUND_Y = HEIGHT - 70          # where the ground is drawn (pixels)
CANNON_X = 70                   # where the cannon sits (pixels)
planet_name = "Earth" if GRAVITY == 9.81 else "Custom"

shots = []                      # every shot: dict with position, velocity, trail
last_result = None


def to_screen(x_m, y_m):
    """Turn metres (from the cannon) into screen pixels."""
    return int(CANNON_X + x_m * PIXELS_PER_METRE), int(GROUND_Y - y_m * PIXELS_PER_METRE)


def fire():
    angle = math.radians(LAUNCH_ANGLE)
    return {"x": 0.0, "y": 0.0,
            "vx": LAUNCH_SPEED * math.cos(angle), "vy": LAUNCH_SPEED * math.sin(angle),
            "trail": [], "flying": True, "time": 0.0, "max_h": 0.0,
            "colour": TRAIL_COLOURS[len(shots) % len(TRAIL_COLOURS)],
            "speed": LAUNCH_SPEED, "angle": LAUNCH_ANGLE, "drag": DRAG_ON, "g": GRAVITY}


def predicted_range(speed, angle_deg, g):
    """The textbook formula (no air resistance): R = v² sin(2θ) / g"""
    return speed ** 2 * math.sin(math.radians(2 * angle_deg)) / g


def update(shot, dt):
    speed = math.hypot(shot["vx"], shot["vy"])
    ax, ay = 0.0, -shot["g"]
    if shot["drag"]:
        ax -= AIR_RESISTANCE * speed * shot["vx"]
        ay -= AIR_RESISTANCE * speed * shot["vy"]
    shot["vx"] += ax * dt
    shot["vy"] += ay * dt
    shot["x"] += shot["vx"] * dt
    shot["y"] += shot["vy"] * dt
    shot["time"] += dt
    shot["max_h"] = max(shot["max_h"], shot["y"])
    if shot["y"] <= 0 and shot["time"] > 0.05:      # hit the ground
        shot["y"] = 0
        shot["flying"] = False
    shot["trail"].append(to_screen(shot["x"], shot["y"]))


def draw_text(text, x, y, colour=(230, 230, 235), f=None):
    screen.blit((f or font).render(text, True, colour), (x, y))


running = True
while running:
    dt = clock.tick(60) / 1000 * TIME_SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                shots.append(fire())
                shots = shots[-TRAILS_TO_KEEP:]
            elif event.key == pygame.K_c:
                shots.clear()
                last_result = None
            elif event.key == pygame.K_d:
                DRAG_ON = not DRAG_ON
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            elif event.key in PLANETS:
                planet_name, GRAVITY = PLANETS[event.key]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        LAUNCH_ANGLE = min(89, LAUNCH_ANGLE + 30 * dt)
    if keys[pygame.K_DOWN]:
        LAUNCH_ANGLE = max(1, LAUNCH_ANGLE - 30 * dt)
    if keys[pygame.K_RIGHT]:
        LAUNCH_SPEED = min(80, LAUNCH_SPEED + 10 * dt)
    if keys[pygame.K_LEFT]:
        LAUNCH_SPEED = max(1, LAUNCH_SPEED - 10 * dt)

    for shot in shots:
        if shot["flying"]:
            for _ in range(4):                  # 4 small steps per frame = more accurate
                if shot["flying"]:
                    update(shot, dt / 4)
            if not shot["flying"]:
                last_result = shot

    # ---------- drawing ----------
    screen.fill((14, 16, 28))
    pygame.draw.rect(screen, (40, 70, 45), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    for m in range(0, int((WIDTH - CANNON_X) / PIXELS_PER_METRE) + 1, 10):   # distance markers
        sx, _ = to_screen(m, 0)
        pygame.draw.line(screen, (90, 120, 95), (sx, GROUND_Y), (sx, GROUND_Y + 10), 2)
        draw_text(f"{m} m", sx - 12, GROUND_Y + 14, (150, 180, 150))

    # predicted landing spot (no air resistance)
    pr = predicted_range(LAUNCH_SPEED, LAUNCH_ANGLE, GRAVITY)
    px, _ = to_screen(pr, 0)
    pygame.draw.polygon(screen, (255, 255, 255), [(px, GROUND_Y - 2), (px - 8, GROUND_Y - 16), (px + 8, GROUND_Y - 16)])

    for shot in shots:
        if len(shot["trail"]) > 1:
            pygame.draw.lines(screen, shot["colour"], False, shot["trail"], 2)
        pygame.draw.circle(screen, shot["colour"], to_screen(shot["x"], shot["y"]), BALL_RADIUS)

    # cannon barrel
    a = math.radians(LAUNCH_ANGLE)
    tip = (CANNON_X + 50 * math.cos(a), GROUND_Y - 50 * math.sin(a))
    pygame.draw.line(screen, (200, 200, 210), (CANNON_X, GROUND_Y), tip, 12)
    pygame.draw.circle(screen, (120, 120, 130), (CANNON_X, GROUND_Y), 18)

    draw_text("Projectile Launcher", 24, 18, (255, 255, 255), big_font)
    draw_text(f"Planet: {planet_name}   g = {GRAVITY:.2f} m/s²", 24, 60)
    draw_text(f"Angle: {LAUNCH_ANGLE:.0f}°   Speed: {LAUNCH_SPEED:.1f} m/s", 24, 88)
    draw_text(f"Air resistance: {'ON' if DRAG_ON else 'OFF'}", 24, 116,
              (255, 160, 120) if DRAG_ON else (160, 160, 170))
    draw_text(f"White arrow = formula says it lands at {pr:.1f} m (no air)", 24, 144, (200, 200, 210))
    if last_result:
        draw_text(f"Last shot landed at {last_result['x']:.1f} m, highest point {last_result['max_h']:.1f} m, "
                  f"flight time {last_result['time']:.2f} s", 24, 172, last_result["colour"])
    draw_text("SPACE fire   UP/DOWN angle   LEFT/RIGHT speed   1-4 planet   D air   C clear   F fullscreen",
              24, HEIGHT - 30, (140, 140, 150))
    pygame.display.flip()

pygame.quit()
