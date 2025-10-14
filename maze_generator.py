# maze_generator.py
import random


def generate_maze(width, height, seed=12345):
    """
    Génère un labyrinthe parfait (1 entrée, 1 sortie, sans boucles)
    en utilisant un algorithme DFS (backtracking).
    width et height correspondent au nombre de cases en largeur / hauteur.
    """

    random.seed(seed)

    # On crée une grille pleine de murs (1 = mur, 0 = chemin)
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        """
        Creuse les couloirs récursivement.
        """
        # Marquer comme chemin
        maze[y][x] = 0

        # Ordre aléatoire des directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                # Creuse le mur entre les deux cellules
                maze[y + dy][x + dx] = 0
                carve(nx, ny)

    # Point de départ (entrée du labyrinthe)
    start_x, start_y = 0, 0  # en haut à gauche
    maze[start_y][start_x] = 0
    carve(start_x, start_y)

    # Définir la sortie : en bas à droite
    maze[height - 1][width - 1] = 0
    # Assure qu'au moins une case autour est libre pour que le joueur puisse entrer
    if maze[height - 2][width - 1] == 1:
        maze[height - 2][width - 1] = 0
    if maze[height - 1][width - 2] == 1:
        maze[height - 1][width - 2] = 0

    return maze, (start_x, start_y), (width - 1, height - 1)
