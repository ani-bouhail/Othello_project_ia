"""
Module minimax.py — Algorithmes Minimax pour l'IA Othello.

Contient :
- Les fonctions d'évaluation heuristique (3 niveaux)
- L'algorithme Minimax classique
- L'algorithme Minimax avec élagage alpha-bêta
"""

# ─────────────────────────────────────────────
#  Compteur de nœuds
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
#  Fonctions d'évaluation
#  Convention : score > 0 => avantage Noir
# ─────────────────────────────────────────────

def evaluate_pions(board):
    """Heuristique 1 : différence de pions."""
    black, white = board.get_score()
    total = black + white
    if total == 0:
        return 0
    return 100 * (black - white) / total


def evaluate_mobilite(board):
    """Heuristique 2 : différence de mobilité."""
    black_moves = len(board.get_valid_moves(1))
    white_moves = len(board.get_valid_moves(-1))
    total = black_moves + white_moves
    if total == 0:
        return 0
    return 100 * (black_moves - white_moves) / total


_WEIGHTS = [
    [100, -20, 10,  5,  5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10,   -2,  1,  1,  1,  1,  -2,  10],
    [5,    -2,  1,  0,  0,  1,  -2,   5],
    [5,    -2,  1,  0,  0,  1,  -2,   5],
    [10,   -2,  1,  1,  1,  1,  -2,  10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10,  5,  5, 10, -20, 100],
]


def evaluate_positionnelle(board):
    """Heuristique 3 : contrôle positionnel du plateau."""
    score = 0
    for y in range(8):
        for x in range(8):
            if board.board[y][x] == 1:
                score += _WEIGHTS[y][x]
            elif board.board[y][x] == -1:
                score -= _WEIGHTS[y][x]
    return score


def _score_for_player(board, eval_fn, root_player):
    """
    Convertit un score 'positif = avantage Noir'
    en score 'positif = avantage pour root_player'.
    """
    raw_score = eval_fn(board)
    return raw_score if root_player == 1 else -raw_score


# ─────────────────────────────────────────────
#  Minimax classique
# ─────────────────────────────────────────────

def minimax(board, depth, player, eval_fn=evaluate_pions, root_player=None):
    """
    Minimax classique.

    Args:
        board: plateau courant
        depth: profondeur restante
        player: joueur courant (1 = Noir, -1 = Blanc)
        eval_fn: heuristique à utiliser
        root_player: joueur de la racine (celui pour qui on cherche le meilleur coup)

    Returns:
        (meilleur_score, meilleur_coup)
    """
    _increment_counter()

    if root_player is None:
        root_player = player

    moves = board.get_valid_moves(player)

    # Cas terminal
    if depth == 0 or (not moves and not board.get_valid_moves(-player)):
        return _score_for_player(board, eval_fn, root_player), None

    # Si le joueur courant ne peut pas jouer, il passe
    if not moves:
        return minimax(board, depth - 1, -player, eval_fn, root_player)

    best_move = None

    # Le joueur racine maximise, l'adversaire minimise
    if player == root_player:
        best_score = float("-inf")
        for x, y in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax(new_board, depth - 1, -player, eval_fn, root_player)
            if score > best_score:
                best_score = score
                best_move = (x, y)
        return best_score, best_move

    else:
        best_score = float("inf")
        for x, y in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax(new_board, depth - 1, -player, eval_fn, root_player)
            if score < best_score:
                best_score = score
                best_move = (x, y)
        return best_score, best_move


# ─────────────────────────────────────────────
#  Minimax avec élagage alpha-bêta
# ─────────────────────────────────────────────

def minimax_alphabeta(
    board,
    depth,
    player,
    alpha=float("-inf"),
    beta=float("inf"),
    eval_fn=evaluate_pions,
    root_player=None
):
    """
    Minimax avec élagage alpha-bêta.

    Args:
        board: plateau courant
        depth: profondeur restante
        player: joueur courant (1 = Noir, -1 = Blanc)
        alpha: borne inférieure
        beta: borne supérieure
        eval_fn: heuristique à utiliser
        root_player: joueur de la racine

    Returns:
        (meilleur_score, meilleur_coup)
    """
    _increment_counter()

    if root_player is None:
        root_player = player

    moves = board.get_valid_moves(player)

    # Cas terminal
    if depth == 0 or (not moves and not board.get_valid_moves(-player)):
        return _score_for_player(board, eval_fn, root_player), None

    # Passe
    if not moves:
        return minimax_alphabeta(
            board,
            depth - 1,
            -player,
            alpha,
            beta,
            eval_fn,
            root_player
        )

    best_move = None

    # Le joueur racine maximise
    if player == root_player:
        best_score = float("-inf")
        for x, y in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax_alphabeta(
                new_board,
                depth - 1,
                -player,
                alpha,
                beta,
                eval_fn,
                root_player
            )

            if score > best_score:
                best_score = score
                best_move = (x, y)

            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score, best_move

    # L'adversaire minimise
    else:
        best_score = float("inf")
        for x, y in moves:
            new_board = board.simulate_move(x, y, player)
            score, _ = minimax_alphabeta(
                new_board,
                depth - 1,
                -player,
                alpha,
                beta,
                eval_fn,
                root_player
            )

            if score < best_score:
                best_score = score
                best_move = (x, y)

            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return best_score, best_move