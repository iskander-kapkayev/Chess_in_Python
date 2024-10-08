import unittest as ut
from chess_scripts_2 import *

class TestLegalMoves(ut.TestCase):

    def setUp(self):
        self.chess_board = board_for_testing()

    def test_legal_path(self):
        # move a pawn from 6,2 to 4,2 from starting position
        legal_check = legal_path(self.chess_board, 6, 2, 4, 2)
        self.assertTrue(legal_check, "The white pawn was able to move 2 squares up from the starting position!")

    def tearDown(self):
        del self.chess_board

ut.main()