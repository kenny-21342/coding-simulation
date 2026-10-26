"""
SPOTLIGHT SIMULATION LAUNCHER
Run this file to get a menu of every simulation. Press a number or click one.
Close a simulation (ESC) and you come back here.
"""
import os
import subprocess
import sys
import pygame

HERE = os.path.dirname(os.path.abspath(__file__))
SIMS = [
    ("01_projectile.py", "Projectile Launcher", "Fire a cannon on Earth, the Moon, Mars or Jupiter"),
    ("02_bouncing_balls.py", "Bouncing Balls", "Collisions, bounciness and where the energy goes"),
    ("03_orbits.py", "Orbits", "Throw planets around a star with gravity"),
    ("04_pendulum_painting.py", "Pendulum Painting", "Two pendulums draw a picture (harmonograph)"),
    ("05_resonance_string.py", "Resonance on a String", "Find the frequencies that make a string swing"),
    ("06_game_of_life.py", "Game of Life", "Three rules, endless patterns: a CS classic"),
]

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics and CS in the Spotlight: Simulations")
title_font = pygame.font.SysFont("arial", 46, bold=True)
name_font = pygame.font.SysFont("arial", 30, bold=True)
font = pygame.font.SysFont("arial", 22)
clock = pygame.time.Clock()


def run(index):
    path = os.path.join(HERE, "sims", SIMS[index][0])
    pygame.display.iconify()
    subprocess.run([sys.executable, path], cwd=os.path.join(HERE, "sims"))
    pygame.display.set_mode((WIDTH, HEIGHT))


def rows():
    top = 190
    return [pygame.Rect(80, top + i * 78, WIDTH - 160, 66) for i in range(len(SIMS))]


running = True
while running:
    hover = None
    mouse = pygame.mouse.get_pos()
    for i, rect in enumerate(rows()):
        if rect.collidepoint(mouse):
            hover = i
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif pygame.K_1 <= event.key <= pygame.K_9 and event.key - pygame.K_1 < len(SIMS):
                run(event.key - pygame.K_1)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
        elif event.type == pygame.MOUSEBUTTONDOWN and hover is not None:
            run(hover)

    screen.fill((14, 16, 28))
    pygame.draw.rect(screen, (240, 240, 245), (80, 60, WIDTH - 160, 10))
    screen.blit(title_font.render("Simulations: code and play", True, (255, 255, 255)), (80, 86))
    screen.blit(font.render("Pick one, play with it, then open its file and change the numbers under PLAY WITH ME.",
                            True, (170, 170, 185)), (80, 146))
    for i, rect in enumerate(rows()):
        pygame.draw.rect(screen, (40, 44, 66) if i == hover else (24, 27, 42), rect, border_radius=10)
        screen.blit(name_font.render(f"{i + 1}   {SIMS[i][1]}", True, (255, 255, 255)), (rect.x + 20, rect.y + 6))
        screen.blit(font.render(SIMS[i][2], True, (170, 170, 185)), (rect.x + 64, rect.y + 38))
    screen.blit(font.render("Press 1 to 6 or click   ESC quit   Inside a simulation, ESC comes back here",
                            True, (120, 120, 135)), (80, HEIGHT - 40))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
