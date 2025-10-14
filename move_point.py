#!/usr/bin/env python3
"""
move_point.py
Mini-application pygame :
- fenêtre avec fond gris
- point rouge contrôlé par les flèches directionnelles
- movement lisse avec gestion du maintien des touches
"""

import pygame
import sys

# Configuration
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

BG_COLOR = (200, 200, 200)   # fond gris
POINT_COLOR = (220, 40, 40)  # rouge
POINT_RADIUS = 8
SPEED = 300  # pixels par seconde

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Point contrôlé - flèches")
    clock = pygame.time.Clock()

    # Position initiale (centre)
    x = WIN_WIDTH // 2
    y = WIN_HEIGHT // 2

    running = True
    while running:
        # dt en secondes (pour mouvement indépendant du framerate)
        dt = clock.tick(FPS) / 1000.0

        # Événements (fermeture fenêtre, pressions de touches non-maintien)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Gestion des touches maintenues (déplacement fluide)
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Normaliser mouvement diagonal (éviter vitesse > SPEED en diagonale)
        if dx != 0 and dy != 0:
            # facteur 1/sqrt(2)
            from math import sqrt
            norm = 1 / sqrt(2)
            dx *= norm
            dy *= norm

        # Appliquer le déplacement en fonction de la vitesse et dt
        x += dx * SPEED * dt
        y += dy * SPEED * dt

        # Garder le point dans la fenêtre (bordures)
        if x < POINT_RADIUS:
            x = POINT_RADIUS
        if x > WIN_WIDTH - POINT_RADIUS:
            x = WIN_WIDTH - POINT_RADIUS
        if y < POINT_RADIUS:
            y = POINT_RADIUS
        if y > WIN_HEIGHT - POINT_RADIUS:
            y = WIN_HEIGHT - POINT_RADIUS

        # Rendu
        screen.fill(BG_COLOR)
        pygame.draw.circle(screen, POINT_COLOR, (int(x), int(y)), POINT_RADIUS)

        # Optionnel : affiche la position et FPS en haut (debug)
        font = pygame.font.SysFont(None, 20)
        info = font.render(f"Pos: ({int(x)},{int(y)})  FPS: {int(clock.get_fps())}", True, (0,0,0))
        screen.blit(info, (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
