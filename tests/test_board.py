import unittest
from src.engine.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_state(self):
        """Vérifie le placement des 4 pions initiaux."""
        self.assertEqual(self.board.board[3][3], Board.BLANC)
        self.assertEqual(self.board.board[4][4], Board.BLANC)
        self.assertEqual(self.board.board[3][4], Board.NOIR)
        self.assertEqual(self.board.board[4][3], Board.NOIR)
        
        black, white = self.board.get_score()
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)

    def test_valid_moves_initial(self):
        """Vérifie les coups possibles au premier tour pour le joueur Noir."""
        valid_moves = self.board.get_valid_moves(Board.NOIR)
        expected_moves = [(3, 2), (2, 3), (5, 4), (4, 5)]
        self.assertEqual(set(valid_moves), set(expected_moves))

    def test_apply_move(self):
        """Vérifie qu'un coup retourne bien les pions adverses."""
        # Le noir joue en (3, 2)
        self.assertTrue(self.board.is_valid_move(3, 2, Board.NOIR))
        self.board.apply_move(3, 2, Board.NOIR)
        
        # Le pion en (3, 3) (initialement blanc) doit devenir noir
        self.assertEqual(self.board.board[3][3], Board.NOIR)
        self.assertEqual(self.board.board[2][3], Board.NOIR)
        
        black, white = self.board.get_score()
        self.assertEqual(black, 4)
        self.assertEqual(white, 1)

if __name__ == '__main__':
    unittest.main()
