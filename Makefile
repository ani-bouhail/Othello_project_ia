# Makefile pour le projet Othello

# Variables
PYTHON = python3
MAIN = main.py
TOURNOI = tournoi.py

.PHONY: help run tournoi clean

help:
	@echo "Options disponibles :"
	@echo "  make run      : Lancer le jeu Othello (Interface Console)"
	@echo "  make tournoi  : Lancer le tournoi automatique entre IA"
	@echo "  make clean    : Nettoyer les fichiers temporaires"

run:
	$(PYTHON) $(MAIN)

tournoi:
	$(PYTHON) $(TOURNOI)

clean:
	rm -rf __pycache__ src/__pycache__ src/*/__pycache__ results.csv
