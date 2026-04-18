"""
Module minimax.py — Algorithme Minimax pour l'IA Othello.

Contient :
- La fonction d'évaluation heuristique
- L'algorithme Minimax (à améliorer avec alpha-bêta)
"""


def evaluate(board):
    """
    Évaluation heuristique du plateau.
    Score positif = avantage pour les Noirs.
    Score négatif = avantage pour les Blancs.
    """
    black, white = board.get_score()
    return black - white


def minimax(board, depth, player):
    """
    Algorithme Minimax classique.

    Args:
        board: instance de Board (plateau de jeu)
        depth: profondeur de recherche restante
        player: 1 (Noir = MAX) ou -1 (Blanc = MIN)

    Returns:
        (meilleur_score, meilleur_coup)
    """
    moves = board.get_valid_moves(player)

    # Cas terminal : profondeur 0 ou fin de partie
    if depth == 0 or (not moves and not board.get_valid_moves(-player)):
        return evaluate(board), None

    # Si le joueur courant n'a pas de coup, il passe son tour
    if not moves:
        score, _ = minimax(board, depth - 1, -player)
        return score, None

    best_move = None

    if player == 1:  # MAX (Noir)
        best_score = float('-inf')
        for (x, y) in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax(new_board, depth - 1, -player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_score, best_move

    else:  # MIN (Blanc)
        best_score = float('+inf')
        for (x, y) in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax(new_board, depth - 1, -player)
            if score < best_score:
                best_score = score
                best_move = (x, y)
        return best_score, best_move
