"""
Module console.py — Interface console pour le jeu Othello.

Gère l'interaction avec le joueur humain via le terminal :
- Choix du mode de jeu
- Saisie des coups
- Affichage des résultats
"""

from src.engine.board import Board
from src.ai.minimax import minimax


def choose_game_mode():
    """Demande au joueur de choisir le mode de jeu."""
    print("=== OTHELLO ===")
    print("1. Joueur vs Joueur")
    print("2. Joueur vs IA")
    while True:
        mode = input("Choisissez un mode (1 ou 2) : ").strip()
        if mode in ("1", "2"):
            return mode
        print("Choix invalide, entrez 1 ou 2.")


def choose_ia_camp():
    """Demande au joueur quel camp joue l'IA."""
    print("L'IA joue quel camp ?")
    print("1. Noir (commence en premier)")
    print("2. Blanc")
    while True:
        camp = input("Choisissez (1 ou 2) : ").strip()
        if camp in ("1", "2"):
            return Board.NOIR if camp == "1" else Board.BLANC
        print("Choix invalide.")


def get_player_name(turn, mode, ia_player):
    """Retourne le nom affiché du joueur courant."""
    if turn == Board.NOIR:
        if mode == "2" and ia_player == Board.NOIR:
            return "Noir (IA)"
        return "Noir (Humain)"
    else:
        if mode == "2" and ia_player == Board.BLANC:
            return "Blanc (IA)"
        return "Blanc (Humain)"


def human_turn(game, player_name):
    """Gère le tour d'un joueur humain."""
    while True:
        try:
            user_input = input(f"Entrez x,y pour {player_name} (ex: 3,2) : ")
            x, y = map(int, user_input.split(","))
            if not (0 <= x < 8 and 0 <= y < 8):
                print("Coordonnées hors du plateau !")
                continue
            if game.is_valid_move(x, y, game.turn):
                game.apply_move(x, y, game.turn)
                game.turn *= -1
                break
            else:
                print("Coup invalide (ne retourne aucun pion adverse). Réessayez.")
        except ValueError:
            print("Format invalide. Entrez deux chiffres séparés par une virgule.")


def ia_turn(game, ia_player, depth):
    """Gère le tour de l'IA."""
    print("L'IA réfléchit...")
    _, best_move = minimax(game, depth, ia_player)
    if best_move:
        x, y = best_move
        print(f"L'IA joue en {x},{y}")
        game.apply_move(x, y, game.turn)
        game.turn *= -1


def display_results(game):
    """Affiche les résultats de la partie."""
    print("\n--- RÉSULTATS ---")
    game.display()
    black, white = game.get_score()
    print(f"Score Final -> Noir: {black} | Blanc: {white}")
    if black > white:
        print("Victoire des NOIRS !")
    elif white > black:
        print("Victoire des BLANCS !")
    else:
        print("ÉGALITÉ PARFAITE !")


def run():
    """Point d'entrée principal du jeu en mode console."""
    game = Board()
    consecutive_passes = 0
    DEPTH = 3

    mode = choose_game_mode()

    if mode == "2":
        ia_player = choose_ia_camp()
    else:
        ia_player = None

    while True:
        game.display()
        player_name = get_player_name(game.turn, mode, ia_player)
        print(f"--- Tour de {player_name} ---")

        if not game.has_valid_move(game.turn):
            print(f"Aucun coup possible pour {player_name} ! Il passe son tour.")
            consecutive_passes += 1
            if consecutive_passes >= 2:
                print("Aucun joueur ne peut plus bouger. Fin de la partie !")
                break
            game.turn *= -1
            continue
        else:
            consecutive_passes = 0

        if mode == "2" and game.turn == ia_player:
            ia_turn(game, ia_player, DEPTH)
        else:
            human_turn(game, player_name)

    display_results(game)
