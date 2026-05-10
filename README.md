# 🎮 Othello — Projet IA (L3 S6)

Ce dépôt contient l'implémentation du jeu d'Othello réalisée dans le cadre du projet d'Intelligence Artificielle.

## 📋 Éléments du projet

Conformément aux consignes, ce projet inclut :
1. **Code source documenté** : Le code est commenté et structuré de manière modulaire dans le dossier `src/`.
2. **Script d'exécution (Makefile)** : Un fichier `Makefile` est fourni pour lancer le programme facilement.
3. **Instructions d'exécution** : Détaillées ci-dessous.
4. **Rapport de projet** : Le rapport détaillé au format PDF est inclus à la racine du projet.

## 🚀 Instructions d'exécution

Le projet est écrit en **Python 3** et ne nécessite aucune dépendance externe.

### Utilisation du Makefile

La méthode recommandée pour exécuter le projet est d'utiliser les commandes `make` suivantes :

*   **Lancer le jeu (Humain vs IA) :**
    ```bash
    make run
    ```
*   **Lancer le tournoi (IA vs IA) :**
    ```bash
    make tournoi
    ```
*   **Nettoyer les fichiers temporaires :**
    ```bash
    make clean
    ```

### Exécution manuelle

Si vous ne disposez pas de l'utilitaire `make`, vous pouvez lancer les scripts directement avec Python :

*   **Jeu principal :** `python3 main.py`
*   **Tournoi :** `python3 tournoi.py`

## 📁 Structure des fichiers

*   `main.py` : Point d'entrée pour jouer contre l'IA.
*   `tournoi.py` : Script automatisant les affrontements entre différentes configurations d'IA.
*   `src/` : Contient le moteur de jeu (`engine/`), l'algorithme Minimax (`ai/`) et l'interface (`ui/`).
*   `Makefile` : Script pour automatiser l'exécution.
*   `Rapport_Othello.pdf` : Rapport d'analyse et de résultats (à la racine).

---
*Projet réalisé par : Anis & Philippe*
