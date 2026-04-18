"""
Module board.py — Logique du plateau de jeu Othello.

Contient la classe Board qui gère :
- L'état du plateau 8x8
- La validation des coups
- L'application des coups et le retournement des pions
- Le calcul des scores
"""

import copy


class Board:
    """Représente le plateau de jeu Othello 8x8."""

    VIDE = 0
    NOIR = 1
    BLANC = -1

    DIRECTIONS = [
        (0, 1), (1, 0), (0, -1), (-1, 0),
        (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    def __init__(self):
        """Initialise un plateau 8x8 avec les 4 pions centraux."""
        self.board = [[self.VIDE for _ in range(8)] for _ in range(8)]
        self.turn = self.NOIR  # Le noir commence toujours
        self._init_board()

    def _init_board(self):
        """Place les 4 pions initiaux au centre du plateau."""
        self.board[3][3] = self.BLANC
        self.board[4][4] = self.BLANC
        self.board[3][4] = self.NOIR
        self.board[4][3] = self.NOIR

    def display(self):
        """Affichage du plateau dans la console."""
        symbols = {self.VIDE: '.', self.NOIR: 'N', self.BLANC: 'B'}
        print("  0 1 2 3 4 5 6 7")
        for y in range(8):
            line = f"{y} "
            for x in range(8):
                line += symbols[self.board[y][x]] + " "
            print(line)

    def is_valid_move(self, x, y, player):
        """Vérifie si un coup est légal pour le joueur donné."""
        if self.board[y][x] != self.VIDE:
            return False

        for dx, dy in self.DIRECTIONS:
            if self._check_direction(x, y, dx, dy, player):
                return True
        return False

    def _check_direction(self, x, y, dx, dy, player):
        """Vérifie si une direction permet de capturer des pions adverses."""
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < 8 and 0 <= ny < 8:
            cell = self.board[ny][nx]

            if cell == self.VIDE:
                return False

            if cell == player:
                return found_opponent

            found_opponent = True
            nx, ny = nx + dx, ny + dy

        return False

    def apply_move(self, x, y, player):
        """Applique un coup : pose le pion et retourne les pions encadrés."""
        self.board[y][x] = player

        for dx, dy in self.DIRECTIONS:
            pions_a_retourner = []
            nx, ny = x + dx, y + dy

            while 0 <= nx < 8 and 0 <= ny < 8:
                cell = self.board[ny][nx]

                if cell == self.VIDE:
                    break
                elif cell != player:
                    pions_a_retourner.append((nx, ny))
                elif cell == player:
                    for rx, ry in pions_a_retourner:
                        self.board[ry][rx] = player
                    break

                nx += dx
                ny += dy

    def has_valid_move(self, player):
        """Vérifie si le joueur a au moins un coup possible."""
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y, player):
                    return True
        return False

    def get_valid_moves(self, player):
        """Retourne la liste de tous les coups légaux [(x, y), ...]."""
        moves = []
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        return moves

    def get_score(self):
        """Renvoie le score (Noirs, Blancs)."""
        black_score = sum(row.count(self.NOIR) for row in self.board)
        white_score = sum(row.count(self.BLANC) for row in self.board)
        return black_score, white_score

    def copy(self):
        """Retourne une copie profonde du plateau."""
        return copy.deepcopy(self)

    def simulate_move(self, x, y, player):
        """Retourne une copie du plateau après avoir joué le coup."""
        new_board = self.copy()
        new_board.apply_move(x, y, player)
        return new_board
