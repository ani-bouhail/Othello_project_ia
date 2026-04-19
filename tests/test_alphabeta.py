"""
Script de test — Comparaison Minimax vs Minimax Alpha-Bêta.

Ce script compare les deux algorithmes sur plusieurs profondeurs
pour montrer le gain de performance de l'élagage alpha-bêta.

Usage:
    python tests/test_alphabeta.py
"""

import sys
import os
import time

# Ajouter la racine du projet au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine.board import Board
from src.ai.minimax import minimax, minimax_alphabeta, reset_counter, get_counter


def separator():
    print("─" * 70)


def test_meme_resultat():
    """
    TEST 1 : Vérifier que les deux algorithmes retournent le même résultat.
    
    C'est le test le plus important : alpha-bêta est une OPTIMISATION
    de minimax, donc il DOIT donner le même score et le même coup.
    """
    print("\n🧪 TEST 1 : Vérification que les résultats sont identiques")
    separator()

    board = Board()
    profondeurs = [1, 2, 3, 4, 5]

    tous_ok = True
    for depth in profondeurs:
        # Minimax classique
        reset_counter()
        score_mm, coup_mm = minimax(board, depth, Board.NOIR)

        # Alpha-Bêta
        reset_counter()
        score_ab, coup_ab = minimax_alphabeta(board, depth, Board.NOIR)

        match = (score_mm == score_ab and coup_mm == coup_ab)
        status = "✅" if match else "❌"
        
        if not match:
            tous_ok = False

        print(f"  Profondeur {depth} : Minimax = (score={score_mm}, coup={coup_mm}) | "
              f"Alpha-Bêta = (score={score_ab}, coup={coup_ab}) {status}")

    separator()
    if tous_ok:
        print("  ✅ SUCCÈS : Les deux algorithmes donnent toujours le même résultat !")
    else:
        print("  ❌ ÉCHEC : Résultats différents détectés !")

    return tous_ok


def test_performance():
    """
    TEST 2 : Comparer le nombre de nœuds explorés et le temps d'exécution.
    
    Alpha-bêta doit explorer significativement moins de nœuds que minimax
    tout en trouvant le même résultat.
    """
    print("\n📊 TEST 2 : Comparaison de performance (nœuds explorés + temps)")
    separator()

    board = Board()
    profondeurs = [1, 2, 3, 4, 5]

    print(f"  {'Prof.':<7} {'Minimax':>12} {'Alpha-Bêta':>12} {'Nœuds élagués':>15} {'Gain':>8} {'T. Minimax':>12} {'T. Alpha-B':>12} {'Speedup':>9}")
    separator()

    for depth in profondeurs:
        # Minimax classique
        reset_counter()
        t1 = time.perf_counter()
        minimax(board, depth, Board.NOIR)
        t_mm = time.perf_counter() - t1
        nodes_mm = get_counter()

        # Alpha-Bêta
        reset_counter()
        t2 = time.perf_counter()
        minimax_alphabeta(board, depth, Board.NOIR)
        t_ab = time.perf_counter() - t2
        nodes_ab = get_counter()

        # Calculs
        elagued = nodes_mm - nodes_ab
        gain_pct = (elagued / nodes_mm * 100) if nodes_mm > 0 else 0
        speedup = t_mm / t_ab if t_ab > 0 else float('inf')

        print(f"  {depth:<7} {nodes_mm:>12,} {nodes_ab:>12,} {elagued:>15,} {gain_pct:>7.1f}% {t_mm:>11.4f}s {t_ab:>11.4f}s {speedup:>8.1f}x")

    separator()
    print("  → Plus le % de gain est élevé, plus alpha-bêta élague de branches inutiles.")
    print("  → Le speedup montre combien de fois alpha-bêta est plus rapide.")


def test_en_cours_de_partie():
    """
    TEST 3 : Tester les algorithmes après quelques coups joués.
    
    L'élagage alpha-bêta est souvent encore plus efficace en milieu
    de partie quand il y a plus de pions et plus de contraintes.
    """
    print("\n🎮 TEST 3 : Performance en milieu de partie (après 6 coups)")
    separator()

    board = Board()

    # Jouer quelques coups pour atteindre un milieu de partie
    coups_joues = []
    player = Board.NOIR
    for _ in range(6):
        moves = board.get_valid_moves(player)
        if moves:
            x, y = moves[0]  # Jouer le premier coup disponible
            board.apply_move(x, y, player)
            coups_joues.append((x, y, "N" if player == 1 else "B"))
        player *= -1

    print("  Coups joués :", " → ".join(f"({x},{y}){c}" for x, y, c in coups_joues))
    print()
    board.display()
    print()

    black, white = board.get_score()
    print(f"  Score actuel : Noir={black}, Blanc={white}")
    print()

    # Comparer sur profondeur 4 et 5
    for depth in [4, 5]:
        reset_counter()
        t1 = time.perf_counter()
        score_mm, coup_mm = minimax(board, depth, Board.NOIR)
        t_mm = time.perf_counter() - t1
        nodes_mm = get_counter()

        reset_counter()
        t2 = time.perf_counter()
        score_ab, coup_ab = minimax_alphabeta(board, depth, Board.NOIR)
        t_ab = time.perf_counter() - t2
        nodes_ab = get_counter()

        gain = (nodes_mm - nodes_ab) / nodes_mm * 100 if nodes_mm > 0 else 0
        speedup = t_mm / t_ab if t_ab > 0 else float('inf')
        match = "✅" if score_mm == score_ab else "❌"

        print(f"  Profondeur {depth} :")
        print(f"    Minimax     → {nodes_mm:>10,} nœuds | {t_mm:.4f}s | coup={coup_mm} score={score_mm}")
        print(f"    Alpha-Bêta  → {nodes_ab:>10,} nœuds | {t_ab:.4f}s | coup={coup_ab} score={score_ab}")
        print(f"    Gain : {gain:.1f}% de nœuds élagués, speedup {speedup:.1f}x {match}")
        print()


def test_profondeur_elevee():
    """
    TEST 4 : Montrer qu'alpha-bêta permet d'atteindre des profondeurs
    inaccessibles pour le minimax classique dans un temps raisonnable.
    """
    print("\n⚡ TEST 4 : Profondeur élevée (alpha-bêta uniquement)")
    separator()
    print("  Minimax classique serait trop lent à profondeur 6+.")
    print("  On teste alpha-bêta seul pour voir jusqu'où on peut aller.\n")

    board = Board()

    for depth in [5, 6, 7]:
        reset_counter()
        t = time.perf_counter()
        score, coup = minimax_alphabeta(board, depth, Board.NOIR)
        elapsed = time.perf_counter() - t
        nodes = get_counter()

        print(f"  Profondeur {depth} : {nodes:>12,} nœuds | {elapsed:>8.3f}s | coup={coup} score={score}")

        if elapsed > 30:
            print(f"  ⚠️  Trop lent à profondeur {depth}, arrêt des tests.")
            break

    separator()
    print("  → Alpha-bêta permet d'explorer des profondeurs plus grandes")
    print("    dans un temps raisonnable grâce à l'élagage.")


# ──────────────────────────────────────────────────────────────
#  Exécution
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("   🔬 COMPARAISON : MINIMAX vs MINIMAX + ÉLAGAGE ALPHA-BÊTA")
    print("=" * 70)

    test_meme_resultat()
    test_performance()
    test_en_cours_de_partie()
    test_profondeur_elevee()

    print("\n" + "=" * 70)
    print("   ✅ Tous les tests sont terminés !")
    print("=" * 70)
