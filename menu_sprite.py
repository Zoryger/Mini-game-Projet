# menu_sprite.py

import os
import sys
import pygame

SPRITE_SIZE = 48
SPRITES_COUNT = 5
SPRITES_FOLDER = "sprites"

FALLBACK_COLORS = [
    (220, 40, 40),
    (40, 120, 220),
    (40, 200, 120),
    (220, 180, 40),
    (160, 60, 200),
]


def load_animated_sprites():
    """
    Charge les sprites animés (sprite1a/sprite1b, etc.)
    Renvoie une liste de listes [[sprite1a, sprite1b], ...]
    """
    sprites = []
    for i in range(1, SPRITES_COUNT + 1):
        pair = []
        for suffix in ["a", "b"]:
            path = os.path.join(SPRITES_FOLDER, f"sprite{i}{suffix}.png")
            if os.path.isfile(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    img = pygame.transform.smoothscale(img, (SPRITE_SIZE, SPRITE_SIZE))
                    pair.append(img)
                except Exception as e:
                    print(f"Erreur chargement {path}: {e}")
        if not pair:
            # fallback si aucune image
            surf = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
            color = FALLBACK_COLORS[(i - 1) % len(FALLBACK_COLORS)]
            pygame.draw.rect(surf, color, (0, 0, SPRITE_SIZE, SPRITE_SIZE))
            pair = [surf, surf]
        # assure que chaque sprite a bien deux images
        if len(pair) == 1:
            pair.append(pair[0])
        sprites.append(pair)
    return sprites


def menu_select_sprite(screen, clock, sprites, win_width, win_height, fps=60):
    """
    Menu de sélection du sprite. On utilise la première image de chaque paire.
    """
    font = pygame.font.SysFont(None, 28)
    title = font.render(
        "Choisis ton sprite (clic / ← → + Entrée / 1-5)", True, (0, 0, 0)
    )

    selected = 0
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected + 1) % SPRITES_COUNT
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    selected = (selected - 1) % SPRITES_COUNT
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected
                elif event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2 and SPRITES_COUNT >= 2:
                    return 1
                elif event.key == pygame.K_3 and SPRITES_COUNT >= 3:
                    return 2
                elif event.key == pygame.K_4 and SPRITES_COUNT >= 4:
                    return 3
                elif event.key == pygame.K_5 and SPRITES_COUNT >= 5:
                    return 4
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                layout = menu_layout_positions((win_width, win_height))
                for idx, rect in enumerate(layout):
                    if rect.collidepoint(mx, my):
                        return idx

        screen.fill((240, 240, 240))
        screen.blit(title, (20, 20))

        layout = menu_layout_positions((win_width, win_height))
        for idx, rect in enumerate(layout):
            border_color = (0, 120, 0) if idx == selected else (80, 80, 80)
            pygame.draw.rect(screen, (230, 230, 230), rect.inflate(8, 8))
            pygame.draw.rect(screen, border_color, rect.inflate(8, 8), 3)
            sprite = sprites[idx][0]  # affiche toujours la première image dans le menu
            s_rect = sprite.get_rect(center=rect.center)
            screen.blit(sprite, s_rect)
            num_txt = font.render(str(idx + 1), True, (0, 0, 0))
            screen.blit(num_txt, (rect.left + 4, rect.top + 4))

        pygame.display.flip()


def menu_layout_positions(window_size):
    w, h = window_size
    margin = 20
    total_width = SPRITE_SIZE * SPRITES_COUNT + margin * (SPRITES_COUNT - 1)
    start_x = (w - total_width) // 2
    y = h // 2 - SPRITE_SIZE // 2
    rects = []
    for i in range(SPRITES_COUNT):
        rect = pygame.Rect(
            start_x + i * (SPRITE_SIZE + margin), y, SPRITE_SIZE, SPRITE_SIZE
        )
        rects.append(rect)
    return rects
