"""
tournoi.py — Tournoi automatique entre les IA Othello.

Fait s'affronter chaque couple d'IA dans N parties.
Enregistre les résultats dans results.csv pour le rapport.

Usage :
    python tournoi.py
    python tournoi.py --parties 100
"""

import argparse
import csv
import time
from Othello import Othello
import src.ai.minimax as mm

# ─────────────────────────────────────────────
#  Définition des IA
# ─────────────────────────────────────────────

IA_CONFIGS = [
    {"nom": "Facile",  "eval_fn": mm.evaluate_pions,           "depth": 2},
    {"nom": "Moyen",   "eval_fn": mm.evaluate_mobilite,        "depth": 4},
    {"nom": "Fort",    "eval_fn": mm.evaluate_positionnelle,   "depth": 5},
]


# ─────────────────────────────────────────────
#  Jouer une partie IA vs IA
# ─────────────────────────────────────────────

def play_game(ia_noir, ia_blanc):
    """
    Joue une partie complète entre deux IA.
    ia_noir joue les Noirs (commence), ia_blanc joue les Blancs.

    Returns:
        1  si les Noirs gagnent
        -1 si les Blancs gagnent
        0  en cas d'égalité
    """
    game = Othello()
    consecutive_passes = 0

    while True:
        if not game.has_valid_move(game.turn):
            consecutive_passes += 1
            if consecutive_passes >= 2:
                break
            game.turn *= -1
            continue
        else:
            consecutive_passes = 0

        # Choisir la bonne IA selon le tour
        if game.turn == 1:
            ia = ia_noir
        else:
            ia = ia_blanc

        _, best_move = mm.minimax_alphabeta(
            game,
            depth=ia["depth"],
            player=game.turn,
            eval_fn=ia["eval_fn"]
        )

        if best_move:
            game.apply_move(best_move[0], best_move[1], game.turn)

        game.turn *= -1

    black, white = game.get_score()
    if black > white:   return 1
    elif white > black: return -1
    else:               return 0


# ─────────────────────────────────────────────
#  Tournoi complet
# ─────────────────────────────────────────────

def run_tournament(n_parties=50):
    """
    Fait s'affronter chaque couple d'IA dans n_parties parties.
    Chaque matchup est joué dans les deux sens (A vs B et B vs A)
    pour mesurer l'avantage du premier joueur.
    """
    resultats = []

    # Générer tous les couples (i, j) avec i < j
    matchups = [
        (IA_CONFIGS[i], IA_CONFIGS[j])
        for i in range(len(IA_CONFIGS))
        for j in range(i + 1, len(IA_CONFIGS))
    ]

    total = len(matchups) * 2 * n_parties
    fait  = 0

    for ia1, ia2 in matchups:
        for ia_noir, ia_blanc in [(ia1, ia2), (ia2, ia1)]:
            wins_noir = wins_blanc = nuls = 0
            debut = time.time()

            for i in range(n_parties):
                resultat = play_game(ia_noir, ia_blanc)
                if resultat == 1:    wins_noir += 1
                elif resultat == -1: wins_blanc += 1
                else:                nuls += 1

                fait += 1
                print(f"\r[{fait}/{total}] {ia_noir['nom']} (N) vs {ia_blanc['nom']} (B) "
                      f"— partie {i+1}/{n_parties}", end="", flush=True)

            duree = time.time() - debut
            print()  # saut de ligne après la progression

            resultats.append({
                "noir":         ia_noir["nom"],
                "blanc":        ia_blanc["nom"],
                "victoires_N":  wins_noir,
                "victoires_B":  wins_blanc,
                "nuls":         nuls,
                "total":        n_parties,
                "taux_N_%":     round(100 * wins_noir  / n_parties, 1),
                "taux_B_%":     round(100 * wins_blanc / n_parties, 1),
                "taux_nul_%":   round(100 * nuls        / n_parties, 1),
                "duree_s":      round(duree, 1),
            })

    return resultats


# ─────────────────────────────────────────────
#  Affichage et export CSV
# ─────────────────────────────────────────────

def afficher_resultats(resultats):
    print("\n" + "=" * 70)
    print(f"{'Noir':<10} {'Blanc':<10} {'V.Noir':>7} {'V.Blanc':>8} {'Nuls':>6} {'%N':>6} {'%B':>6} {'Durée':>8}")
    print("=" * 70)
    for r in resultats:
        print(f"{r['noir']:<10} {r['blanc']:<10} "
              f"{r['victoires_N']:>7} {r['victoires_B']:>8} {r['nuls']:>6} "
              f"{r['taux_N_%']:>5}% {r['taux_B_%']:>5}% "
              f"{r['duree_s']:>6}s")
    print("=" * 70)


def exporter_csv(resultats, fichier="results.csv"):
    colonnes = ["noir", "blanc", "victoires_N", "victoires_B", "nuls",
                "total", "taux_N_%", "taux_B_%", "taux_nul_%", "duree_s"]
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(resultats)
    print(f"\n→ Résultats exportés dans '{fichier}'")


# ─────────────────────────────────────────────
#  Point d'entrée
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tournoi Othello entre IA")
    parser.add_argument("--parties", type=int, default=50,
                        help="Nombre de parties par couple (défaut : 50)")
    args = parser.parse_args()

    print(f"=== TOURNOI OTHELLO — {args.parties} parties par couple ===\n")
    resultats = run_tournament(n_parties=args.parties)
    afficher_resultats(resultats)
    exporter_csv(resultats)