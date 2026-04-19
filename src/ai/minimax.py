"""
Module minimax.py — Algorithmes Minimax pour l'IA Othello.

Contient :
- La fonction d'évaluation heuristique
- L'algorithme Minimax classique
- L'algorithme Minimax avec élagage alpha-bêta
"""


# ─────────────────────────────────────────────
#  Compteur de nœuds (pour mesurer la performance)
# ─────────────────────────────────────────────

_node_counter = 0


def reset_counter():
    """Remet le compteur de nœuds explorés à zéro."""
    global _node_counter
    _node_counter = 0


def get_counter():
    """Retourne le nombre de nœuds explorés depuis le dernier reset."""
    return _node_counter


def _increment_counter():
    """Incrémente le compteur de nœuds."""
    global _node_counter
    _node_counter += 1


# ─────────────────────────────────────────────
#  Fonction d'évaluation
# ─────────────────────────────────────────────

def evaluate(board):
    """
    Évaluation heuristique du plateau.
    Score positif = avantage pour les Noirs.
    Score négatif = avantage pour les Blancs.
    """
    black, white = board.get_score()
    return black - white


# ─────────────────────────────────────────────
#  Minimax classique (sans élagage)
# ─────────────────────────────────────────────

def minimax(board, depth, player):
    """
    Algorithme Minimax classique (sans élagage).

    Explore TOUS les nœuds de l'arbre de jeu jusqu'à la profondeur donnée.
    Sert de référence pour mesurer le gain de l'élagage alpha-bêta.

    Args:
        board: instance de Board (plateau de jeu)
        depth: profondeur de recherche restante
        player: 1 (Noir = MAX) ou -1 (Blanc = MIN)

    Returns:
        (meilleur_score, meilleur_coup)
    """
    _increment_counter()

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


# ─────────────────────────────────────────────
#  Minimax avec élagage Alpha-Bêta
# ─────────────────────────────────────────────

def minimax_alphabeta(board, depth, player, alpha=float('-inf'), beta=float('+inf')):
    """
    Algorithme Minimax avec élagage alpha-bêta.

    Principe de l'élagage :
    - alpha = meilleur score garanti pour MAX (borne inférieure)
    - beta  = meilleur score garanti pour MIN (borne supérieure)

    Si à un moment alpha >= beta, on sait que la branche courante ne sera
    jamais choisie par le parent, donc on la COUPE (= élagage).

    Résultat identique au Minimax classique, mais explore beaucoup moins
    de nœuds car les branches inutiles sont élaguées.

    Args:
        board: instance de Board (plateau de jeu)
        depth: profondeur de recherche restante
        player: 1 (Noir = MAX) ou -1 (Blanc = MIN)
        alpha: meilleur score garanti pour MAX (initialement -∞)
        beta: meilleur score garanti pour MIN (initialement +∞)

    Returns:
        (meilleur_score, meilleur_coup)
    """
    _increment_counter()

    moves = board.get_valid_moves(player)

    # Cas terminal : profondeur 0 ou fin de partie (aucun joueur ne peut jouer)
    if depth == 0 or (not moves and not board.get_valid_moves(-player)):
        return evaluate(board), None

    # Si le joueur courant n'a pas de coup, il passe son tour
    if not moves:
        score, _ = minimax_alphabeta(board, depth - 1, -player, alpha, beta)
        return score, None

    best_move = None

    if player == 1:  # MAX (Noir) — cherche à MAXIMISER le score
        best_score = float('-inf')
        for (x, y) in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax_alphabeta(new_board, depth - 1, -player, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = (x, y)

            # Mise à jour d'alpha (meilleur garanti pour MAX)
            alpha = max(alpha, best_score)

            # ÉLAGAGE : si alpha >= beta, MIN ne choisira jamais cette branche
            # car MAX a déjà une meilleure option ailleurs
            if alpha >= beta:
                break  # Coupure bêta (on élague les frères restants)

        return best_score, best_move

    else:  # MIN (Blanc) — cherche à MINIMISER le score
        best_score = float('+inf')
        for (x, y) in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax_alphabeta(new_board, depth - 1, -player, alpha, beta)

            if score < best_score:
                best_score = score
                best_move = (x, y)

            # Mise à jour de bêta (meilleur garanti pour MIN)
            beta = min(beta, best_score)

            # ÉLAGAGE : si alpha >= beta, MAX ne choisira jamais cette branche
            # car MIN a déjà une meilleure option ailleurs
            if alpha >= beta:
                break  # Coupure alpha (on élague les frères restants)

        return best_score, best_move
