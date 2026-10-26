"""
GAME OF LIFE (John Conway, 1970)
Every square is a cell that is alive or dead. Each step, every cell looks at
its 8 neighbours:
  - a dead cell with exactly 3 live neighbours is BORN
  - a live cell with 2 or 3 live neighbours SURVIVES
  - every other cell dies (loneliness or overcrowding)
Three tiny rules, endless patterns. Change the rules below and see what happens!

Controls
  Click / drag   draw live cells (right-click or shift-drag to erase)
  SPACE          pause / play
  N              one step (while paused)
  R              random world
  C              clear
  G              add a glider gun
  UP / DOWN      faster / slower
  F              fullscreen on / off
  ESC            quit
"""
import random
import pygame

# ===================== PLAY WITH ME =====================
CELL_SIZE = 12           # pixels per cell (smaller = bigger world)
BORN_WITH = {3}          # neighbours needed to be born. HighLife: {3, 6}. Seeds: {2}
SURVIVE_WITH = {2, 3}    # neighbours needed to survive. Seeds: set()  (empty)
STEPS_PER_SECOND = 10
RANDOM_FILL = 0.25       # how full a random world is (0.0 to 1.0)
WRAP_AROUND = True       # cells leaving one edge come back on the other
# ========================================================

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 30, bold=True)
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

GLIDER_GUN = ["........................O...........",
              "......................O.O...........",
              "............OO......OO............OO",
              "...........O...O....OO............OO",
              "OO........O.....O...OO..............",
              "OO........O...O.OO....O.O...........",
              "..........O.....O.......O...........",
              "...........O...O....................",
              "............OO......................"]

alive = {}               # (col, row) -> age in steps


def randomise():
    return {(c, r): 0 for c in range(COLS) for r in range(ROWS) if random.random() < RANDOM_FILL}


def next_generation(cells):
    counts = {}
    for (c, r) in cells:
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if dc == 0 and dr == 0:
                    continue
                nc, nr = c + dc, r + dr
                if WRAP_AROUND:
                    nc, nr = nc % COLS, nr % ROWS
                elif not (0 <= nc < COLS and 0 <= nr < ROWS):
                    continue
                counts[(nc, nr)] = counts.get((nc, nr), 0) + 1
    new = {}
    for cell, n in counts.items():
        if cell in cells and n in SURVIVE_WITH:
            new[cell] = cells[cell] + 1
        elif cell not in cells and n in BORN_WITH:
            new[cell] = 0
    return new


def add_gun(left, top):
    for r, line in enumerate(GLIDER_GUN):
        for c, ch in enumerate(line):
            if ch == "O":
                alive[((left + c) % COLS, (top + r) % ROWS)] = 0


alive = randomise()
paused = False
generation = 0
timer = 0.0

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
                paused = not paused
            elif event.key == pygame.K_n and paused:
                alive = next_generation(alive)
                generation += 1
            elif event.key == pygame.K_r:
                alive, generation = randomise(), 0
            elif event.key == pygame.K_c:
                alive, generation = {}, 0
            elif event.key == pygame.K_g:
                add_gun(random.randint(0, max(0, COLS - 40)), random.randint(0, max(0, ROWS - 12)))
            elif event.key == pygame.K_UP:
                STEPS_PER_SECOND = min(60, STEPS_PER_SECOND + 2)
            elif event.key == pygame.K_DOWN:
                STEPS_PER_SECOND = max(1, STEPS_PER_SECOND - 2)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()

    buttons = pygame.mouse.get_pressed()
    if buttons[0] or buttons[2]:
        mx, my = pygame.mouse.get_pos()
        cell = (mx // CELL_SIZE, my // CELL_SIZE)
        erase = buttons[2] or pygame.key.get_mods() & pygame.KMOD_SHIFT
        if erase:
            alive.pop(cell, None)
        else:
            alive[cell] = 0

    if not paused:
        timer += dt
        while timer >= 1 / STEPS_PER_SECOND:
            alive = next_generation(alive)
            generation += 1
            timer -= 1 / STEPS_PER_SECOND

    screen.fill((8, 10, 18))
    for (c, r), age in alive.items():
        colour = pygame.Color(0)
        colour.hsva = ((190 + age * 4) % 360, 70, 100, 100)    # young = blue, old = pink/yellow
        pygame.draw.rect(screen, colour, (c * CELL_SIZE + 1, r * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    panel = pygame.Surface((560, 118), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 170))
    screen.blit(panel, (12, 10))
    screen.blit(big_font.render("Game of Life", True, (255, 255, 255)), (24, 16))
    rule = f"B{''.join(map(str, sorted(BORN_WITH)))}/S{''.join(map(str, sorted(SURVIVE_WITH)))}"
    screen.blit(font.render(f"Generation {generation}   Alive: {len(alive)}   Rule: {rule}   "
                            f"{'PAUSED' if paused else f'{STEPS_PER_SECOND} steps/s'}", True, (230, 230, 235)), (24, 56))
    screen.blit(font.render("Click draw   SPACE pause   N step   R random   C clear   G glider gun",
                            True, (160, 160, 170)), (24, 86))
    pygame.display.flip()

pygame.quit()
