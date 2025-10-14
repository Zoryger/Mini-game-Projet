#!/usr/bin/env python3
"""
move_point_with_menu.py
- Menu initial pour choisir un sprite parmi 5 (clic ou flèches + Enter)
- Fenêtre de jeu (fond gris) avec le sprite sélectionné contrôlé par les flèches/WASD
- Utilise pygame
- Si ./sprites/sprite1.png ... sprite5.png existent, ils seront utilisés et redimensionnés.
  Sinon, des sprites de secours (surfaces colorées) seront créés automatiquement.
"""

import os
import sys
import pygame
from math import sqrt

# Configuration
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

BG_COLOR = (200, 200, 200)   # fond gris
POINT_RADIUS = 8
SPEED = 300  # pixels par seconde

SPRITE_SIZE = 48  # px affichés pour les sprites dans le jeu
SPRITES_COUNT = 5
SPRITES_FOLDER = "sprites"  # optionnel : placer sprite1.png..sprite5.png ici

# couleurs fallback si pas d'images
FALLBACK_COLORS = [
    (220, 40, 40),
    (40, 120, 220),
    (40, 200, 120),
    (220, 180, 40),
    (160, 60, 200),
]

def load_sprites():
    """Charge les images sprites si présentes sinon crée des surfaces fallback."""
    sprites = []
    for i in range(1, SPRITES_COUNT + 1):
        path = os.path.join(SPRITES_FOLDER, f"sprite{i}.png")
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (SPRITE_SIZE, SPRITE_SIZE))
                sprites.append(img)
                continue
            except Exception as e:
                print(f"Erreur chargement {path}: {e}. Utilisation d'un fallback.")
        # fallback : surface circulaire colorée avec un petit œil
        surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
        color = FALLBACK_COLORS[(i-1) % len(FALLBACK_COLORS)]
        pygame.draw.circle(surf, color, (SPRITE_SIZE//2, SPRITE_SIZE//2), SPRITE_SIZE//2)
        # petit "œil" pour donner du caractère
        pygame.draw.circle(surf, (255,255,255), (SPRITE_SIZE//2 + 8, SPRITE_SIZE//2 - 6), SPRITE_SIZE//8)
        pygame.draw.circle(surf, (0,0,0), (SPRITE_SIZE//2 + 8, SPRITE_SIZE//2 - 6), SPRITE_SIZE//16)
        sprites.append(surf)
    return sprites

def menu_select_sprite(screen, clock, sprites):
    """
    Affiche un menu simple avec les sprites et renvoie l'index sélectionné (0-based).
    Navigation : clic sur sprite, ou flèches gauche/droite + Enter, ou touches 1-5.
    """
    font = pygame.font.SysFont(None, 28)
    title = font.render("Choisis ton sprite (clic / ← → + Entrée / 1-5)", True, (0,0,0))

    selected = 0
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected + 1) % SPRITES_COUNT
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    selected = (selected - 1) % SPRITES_COUNT
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    return 0
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    if SPRITES_COUNT >= 2: return 1
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    if SPRITES_COUNT >= 3: return 2
                elif event.key in (pygame.K_4, pygame.K_KP4):
                    if SPRITES_COUNT >= 4: return 3
                elif event.key in (pygame.K_5, pygame.K_KP5):
                    if SPRITES_COUNT >= 5: return 4
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # calculer si clic sur l'un des sprites
                layout = menu_layout_positions(screen.get_size(), sprites)
                for idx, rect in enumerate(layout):
                    if rect.collidepoint(mx, my):
                        return idx

        # rendu menu
        screen.fill((240,240,240))
        screen.blit(title, (20, 20))

        layout = menu_layout_positions(screen.get_size(), sprites)
        # dessine cadres et sprites
        for idx, rect in enumerate(layout):
            border_color = (0, 120, 0) if idx == selected else (80, 80, 80)
            pygame.draw.rect(screen, (230,230,230), rect.inflate(8,8))
            pygame.draw.rect(screen, border_color, rect.inflate(8,8), 3)
            # centrer l'image dans rect
            sprite = sprites[idx]
            s_rect = sprite.get_rect(center=rect.center)
            screen.blit(sprite, s_rect)

            # numéro
            num_txt = font.render(str(idx+1), True, (0,0,0))
            screen.blit(num_txt, (rect.left + 4, rect.top + 4))

        # légende bas
        hint = "Utilise les flèches, clic ou 1-5. Entrée pour valider."
        hint_surf = font.render(hint, True, (60,60,60))
        screen.blit(hint_surf, (20, WIN_HEIGHT - 40))

        pygame.display.flip()

    return selected

def menu_layout_positions(window_size, sprites):
    """Retourne une liste de pygame.Rect pour positionner les sprites en ligne centrée."""
    w, h = window_size
    margin = 20
    total_width = SPRITE_SIZE * SPRITES_COUNT + margin * (SPRITES_COUNT - 1)
    start_x = (w - total_width) // 2
    y = h // 2 - SPRITE_SIZE // 2
    rects = []
    for i in range(SPRITES_COUNT):
        rect = pygame.Rect(start_x + i * (SPRITE_SIZE + margin), y, SPRITE_SIZE, SPRITE_SIZE)
        rects.append(rect)
    return rects

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Choisis ton sprite -> Jeu")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    # Charger sprites (ou fallback)
    sprites = load_sprites()

    # Menu : sélection du sprite
    chosen_index = menu_select_sprite(screen, clock, sprites)
    chosen_sprite = sprites[chosen_index]
    print(f"Sprite choisi: {chosen_index + 1}")

    # Position initiale (centre)
    x = WIN_WIDTH // 2
    y = WIN_HEIGHT // 2

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # touches maintenues
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

        if dx != 0 and dy != 0:
            # normaliser diagonale
            norm = 1 / sqrt(2)
            dx *= norm
            dy *= norm

        x += dx * SPEED * dt
        y += dy * SPEED * dt

        # garder dans la fenêtre en tenant compte de la taille du sprite
        half = SPRITE_SIZE // 2
        if x < half:
            x = half
        if x > WIN_WIDTH - half:
            x = WIN_WIDTH - half
        if y < half:
            y = half
        if y > WIN_HEIGHT - half:
            y = WIN_HEIGHT - half

        # rendu
        screen.fill(BG_COLOR)
        # blit du sprite centré sur (x,y)
        spr_rect = chosen_sprite.get_rect(center=(int(x), int(y)))
        screen.blit(chosen_sprite, spr_rect)

        # debug info en haut à gauche
        info = font.render(f"Sprite #{chosen_index+1}  Pos: ({int(x)},{int(y)})  FPS: {int(clock.get_fps())}", True, (0,0,0))
        screen.blit(info, (8, 8))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Crée le dossier sprites s'il n'existe pas (utile pour rappeler où placer les images)
    if not os.path.isdir(SPRITES_FOLDER):
        try:
            os.makedirs(SPRITES_FOLDER, exist_ok=True)
        except Exception:
            pass
    main()
