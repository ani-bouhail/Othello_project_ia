class Othello:
    def __init__(self):
        # 0 = vide, 1 = Noir, -1 = Blanc
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.turn = 1  # Le noir commence toujours
        self._init_board()

    def _init_board(self):
        # Placement des 4 pions centraux
        self.board[3][3] = -1
        self.board[4][4] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1

    def display(self):
        # Affichage simple dans la console
        symbols = {0: '.', 1: 'N', -1: 'B'}
        print("  0 1 2 3 4 5 6 7")
        for y in range(8):
            line = f"{y} "
            for x in range(8):
                line += symbols[self.board[y][x]] + " "
            print(line)



    def is_valid_move(self, x, y, player):
        # Si la case n'est pas vide, c'est interdit
        if self.board[y][x] != 0:
            return False
        
        # Liste des directions (dx, dy)
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
        
        for dx, dy in directions:
            if self.check_direction(x, y, dx, dy, player):
                return True # Un seul sandwich suffit pour que le coup soit légal
        return False

    def check_direction(self, x, y, dx, dy, player):
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < 8 and 0 <= ny < 8:
            cell = self.board[ny][nx]

            if cell == 0:
                return False  # case vide :

            if cell == player:
                return found_opponent  # notre pion 

            # cell est forcément un pion adverse ici
            found_opponent = True
            nx, ny = nx + dx, ny + dy

        return False  # bord du plateau atteint sans refermer le sandwich

    def apply_move(self, x, y, player):
        # 1. On pose le pion
        self.board[y][x] = player
        
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
        
        # 2. On vérifie toutes les directions pour retourner les pions
        for dx, dy in directions:
            pions_a_retourner = [] # Liste temporaire pour cette direction
            
            nx, ny = x + dx, y + dy
            
            # On avance dans la direction
            while 0 <= nx < 8 and 0 <= ny < 8:
                cell = self.board[ny][nx]
                
                if cell == 0:
                    # Case vide : la ligne est brisée, on ne retourne rien ici
                    break 
                
                elif cell != player:
                    # Pions adverses : on les ajoute à la liste temporaire
                    pions_a_retourner.append((nx, ny))
                
                elif cell == player:
                    # On retrouve notre couleur 
                    # On retourne effectivement tous les pions mémorisés
                    for rx, ry in pions_a_retourner:
                        self.board[ry][rx] = player
                    break # On a fini pour cette direction
                
                nx += dx
                ny += dy

    def has_valid_move(self, player):
        """Vérifie si le joueur a au moins un coup possible sur le plateau."""
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y, player):
                    return True
        return False

    def get_score(self):
        """Renvoie le score (Noirs, Blancs)."""
        black_score = sum(row.count(1) for row in self.board)
        white_score = sum(row.count(-1) for row in self.board)
        return black_score, white_score
    
    def get_valid_moves(self, player):
        """Retourne la liste de tous les coups légaux [(x, y), ...]"""
        moves = []
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y, player):
                    moves.append((x, y))
        return moves

    def simulate_move(self, x, y, player):
        """Retourne une copie du jeu après avoir joué le coup (sans modifier le vrai plateau)"""
        import copy
        new_game = copy.deepcopy(self)
        new_game.apply_move(x, y, player)
        return new_game
    
    def evaluate(self):
        """Score heuristique : différence de pions (positif = bon pour Noir)"""
        black, white = self.get_score()
        return black - white


    
    def minimax(self, depth, player):
        """
        Retourne (meilleur_score, meilleur_coup).
        player = 1 (Noir = MAX), player = -1 (Blanc = MIN)
        """
        moves = self.get_valid_moves(player)

        # Cas terminal : profondeur 0 ou aucun coup possible pour les deux joueurs
        if depth == 0 or (not moves and not self.get_valid_moves(-player)):
            return self.evaluate(), None

        # Si le joueur courant n'a pas de coup, il passe
        if not moves:
            score, _ = self.minimax(depth - 1, -player)
            return score, None

        best_move = None

        if player == 1:  # MAX (Noir)
            best_score = float('-inf')
            for (x, y) in moves:
                new_game = self.simulate_move(x, y, player)
                score, _ = new_game.minimax(depth - 1, -player)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
            return best_score, best_move

        else:  # MIN (Blanc)
            best_score = float('+inf')
            for (x, y) in moves:
                new_game = self.simulate_move(x, y, player)
                score, _ = new_game.minimax(depth - 1, -player)
                if score < best_score:
                    best_score = score
                    best_move = (x, y)
            return best_score, best_move



import src.ai.minimax as mm

# ─────────────────────────────────────────────
#  Configuration des niveaux de difficulté
# ─────────────────────────────────────────────

NIVEAUX = {
    "1": {"nom": "Facile",  "eval_fn": mm.evaluate_pions,          "depth": 2},
    "2": {"nom": "Moyen",   "eval_fn": mm.evaluate_mobilite,       "depth": 4},
    "3": {"nom": "Fort",    "eval_fn": mm.evaluate_positionnelle,   "depth": 6},
}

if __name__ == "__main__":
    game = Othello()
    consecutive_passes = 0

    print("=== OTHELLO ===")
    print("1. Joueur vs Joueur")
    print("2. Joueur vs IA")
    while True:
        mode = input("Choisissez un mode (1 ou 2) : ").strip()
        if mode in ("1", "2"):
            break
        print("Choix invalide.")

    if mode == "2":
        print("\nQuel camp joue l'IA ?")
        print("1. Noir (commence en premier)")
        print("2. Blanc")
        while True:
            camp = input("Choisissez (1 ou 2) : ").strip()
            if camp in ("1", "2"):
                break
            print("Choix invalide.")
        IA_PLAYER = 1 if camp == "1" else -1

        print("\nNiveau de difficulté de l'IA :")
        print("1. Facile  (différence de pions,  profondeur 2)")
        print("2. Moyen   (mobilité,              profondeur 4)")
        print("3. Fort    (contrôle des coins,    profondeur 6)")
        while True:
            niveau = input("Choisissez (1, 2 ou 3) : ").strip()
            if niveau in NIVEAUX:
                break
            print("Choix invalide.")

        config = NIVEAUX[niveau]
        print(f"\n→ IA niveau {config['nom']} sélectionnée.\n")
    else:
        IA_PLAYER = None
        config = None

    # ─────────────────────────────────────────────
    #  Boucle de jeu
    # ─────────────────────────────────────────────

    while True:
        game.display()

        if game.turn == 1:
            player_name = "Noir (IA)" if (mode == "2" and IA_PLAYER == 1) else "Noir (Humain)"
        else:
            player_name = "Blanc (IA)" if (mode == "2" and IA_PLAYER == -1) else "Blanc (Humain)"

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

        # Tour de l'IA
        if mode == "2" and game.turn == IA_PLAYER:
            print("L'IA réfléchit...")
            mm.reset_counter()
            _, best_move = mm.minimax_alphabeta(
                game,
                depth=config["depth"],
                player=game.turn,
                eval_fn=config["eval_fn"]
            )
            print(f"Nœuds explorés : {mm.get_counter()}")
            if best_move:
                x, y = best_move
                print(f"L'IA joue en {x},{y}")
                game.apply_move(x, y, game.turn)
                game.turn *= -1

        # Tour du joueur humain
        else:
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
                        print("Coup invalide. Réessayez.")
                except ValueError:
                    print("Format invalide. Entrez deux chiffres séparés par une virgule.")

    print("\n--- RÉSULTATS ---")
    game.display()
    black, white = game.get_score()
    print(f"Score Final -> Noir: {black} | Blanc: {white}")
    if black > white:   print("Victoire des NOIRS !")
    elif white > black: print("Victoire des BLANCS !")
    else:               print("ÉGALITÉ PARFAITE !")