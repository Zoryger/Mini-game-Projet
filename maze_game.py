import pygame
import sys
from math import sqrt
from maze_generator import generate_maze
from menu_sprite import load_animated_sprites, menu_select_sprite

# --- CONFIG ---
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60

TILE_SIZE = 32
MAZE_WIDTH = 20
MAZE_HEIGHT = 20
MAZE_SEED = 12345

BG_COLOR = (200, 200, 200)
WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (240, 220, 180)
EXIT_COLOR = (0, 200, 0)

SPEED = 200  # pixels / seconde
ANIMATION_SPEED = 0.5  # secondes par frame (2 FPS)


# --- GAME ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Labyrinthe - Trouve la sortie!")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # --- Sprite Selection ---
    sprites = load_animated_sprites()
    chosen_index = menu_select_sprite(screen, clock, sprites, WIN_WIDTH, WIN_HEIGHT)
    player_frames = sprites[chosen_index]  # [sprite_a, sprite_b]
    current_frame = 0
    sprite_timer = 0

    # --- Maze Generation ---
    maze, (start_x, start_y), (exit_x, exit_y) = generate_maze(
        MAZE_WIDTH, MAZE_HEIGHT, MAZE_SEED
    )
    x = start_x * TILE_SIZE + TILE_SIZE // 2
    y = start_y * TILE_SIZE + TILE_SIZE // 2

    timer_start = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (
            keys[pygame.K_UP] or keys[pygame.K_w]
        )

        if dx != 0 and dy != 0:
            norm = 1 / sqrt(2)
            dx *= norm
            dy *= norm

        # --- Collision ---
        new_x = x + dx * SPEED * dt
        new_y = y + dy * SPEED * dt
        if is_wall(maze, new_x, y) == 0:
            x = new_x
        if is_wall(maze, x, new_y) == 0:
            y = new_y

        # --- Animation du sprite ---
        moving = dx != 0 or dy != 0
        if moving:
            sprite_timer += dt
            if sprite_timer >= ANIMATION_SPEED:
                sprite_timer -= ANIMATION_SPEED
                current_frame = (current_frame + 1) % 2
        player_sprite = player_frames[current_frame]

        # --- Vérifie la sortie ---
        if int(x // TILE_SIZE) == exit_x and int(y // TILE_SIZE) == exit_y:
            total_time = (pygame.time.get_ticks() - timer_start) // 1000
            print(f"🎉 Victoire en {total_time} secondes !")
            running = False

        # --- Scroll centré ---
        camera_x = x - WIN_WIDTH // 2
        camera_y = y - WIN_HEIGHT // 2

        render(
            screen,
            maze,
            x,
            y,
            camera_x,
            camera_y,
            player_sprite,
            font,
            timer_start,
            exit_x,
            exit_y,
        )

    pygame.quit()
    sys.exit()


def is_wall(maze, x, y):
    grid_x = int(x // TILE_SIZE)
    grid_y = int(y // TILE_SIZE)
    if 0 <= grid_x < len(maze[0]) and 0 <= grid_y < len(maze):
        return maze[grid_y][grid_x]
    return 1


def render(
    screen,
    maze,
    player_x,
    player_y,
    camera_x,
    camera_y,
    sprite,
    font,
    timer_start,
    exit_x,
    exit_y,
):
    screen.fill(BG_COLOR)

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            tile = maze[row][col]
            draw_x = col * TILE_SIZE - camera_x
            draw_y = row * TILE_SIZE - camera_y
            color = WALL_COLOR if tile == 1 else FLOOR_COLOR
            pygame.draw.rect(screen, color, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))

    # Dessine la sortie
    pygame.draw.rect(
        screen,
        EXIT_COLOR,
        (
            exit_x * TILE_SIZE - camera_x,
            exit_y * TILE_SIZE - camera_y,
            TILE_SIZE,
            TILE_SIZE,
        ),
    )

    # Dessine le joueur
    spr_rect = sprite.get_rect(
        center=(int(player_x - camera_x), int(player_y - camera_y))
    )
    screen.blit(sprite, spr_rect)

    # Timer
    elapsed = (pygame.time.get_ticks() - timer_start) // 1000
    timer_text = font.render(f"Temps: {elapsed} s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()


if __name__ == "__main__":
    main()
