# 🎮 Othello — Projet IA (L3 S6)

Conception d'un jeu stratégique humain vs IA en Python, avec 3 niveaux de difficulté basés sur Minimax + élagage alpha-bêta, puis organisation de tournois automatisés entre les IA avec un rapport.

## 👥 Équipe

| Membre   | Branche Git  |
|----------|-------------|
| Anis     | `anis`      |
| Philippe | `philippe`  |

## 📁 Structure du projet

```
Othello_project_ia/
├── main.py                  # Point d'entrée principal
├── src/
│   ├── engine/              # Moteur de jeu
│   │   ├── __init__.py
│   │   └── board.py         # Plateau, règles, validation des coups
│   ├── ai/                  # Intelligence artificielle
│   │   ├── __init__.py
│   │   └── minimax.py       # Algorithme Minimax (+ alpha-bêta à venir)
│   └── ui/                  # Interfaces utilisateur
│       ├── __init__.py
│       └── console.py       # Interface console (terminal)
├── tests/                   # Tests unitaires
├── docs/                    # Documentation et sujet
│   └── sujet_projet.pdf
├── Othello.py               # [LEGACY] Ancien fichier monolithique
└── README.md
```

## 🚀 Lancer le jeu

```bash
python main.py
```

## 🔀 Workflow Git

- **`main`** : Branche stable, code validé et fusionné
- **`anis`** : Branche de développement d'Anis
- **`philippe`** : Branche de développement de Philippe

### Commandes utiles

```bash
# Aller sur sa branche
git checkout anis       # ou: git checkout philippe

# Récupérer les dernières modifications
git pull origin main

# Pousser son travail
git push origin anis    # ou: git push origin philippe
```

## 📋 TODO

- [ ] Implémenter l'élagage alpha-bêta
- [ ] Ajouter 3 niveaux de difficulté
- [ ] Organiser les tournois IA vs IA
- [ ] Rédiger le rapport
