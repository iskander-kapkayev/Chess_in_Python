import unittest as ut
from chess_scripts_2 import *

class TestLegalMoves(ut.TestCase):

    def setUp(self):
        self.chess_board_starting = board_for_testing()
        self.chess_board_scattered = board_for_testing_scattered()

    def test_legal_path_pawn(self):
        # starting board checks
        # move a pawn from 6,2 to 4,2 from starting position
        legal_check = legal_path(self.chess_board_starting, 6, 2, 4, 2)
        # move a pawn from 6,2 to 3,2 from starting position (not legal)
        legal_check_2 = legal_path(self.chess_board_starting, 6, 2, 3, 2)
        self.assertTrue(legal_check, "The white pawn was unable to move 2 squares up from the starting position!")
        self.assertFalse(legal_check_2, "The pawn can't move 3 spaces!")

        # scattered board checks
        # move a pawn from 4,3 to 3,3 when there's a pawn in the way (not legal)
        legal_check_3 = legal_path(self.chess_board_scattered, 4, 3, 3, 3)
        self.assertFalse(legal_check_3, "The pawn can't move 3 spaces!")

    def test_legal_path_knight(self):
        # starting board checks
        # move a white knight from 7,1 to 5,2
        legal_check_1 = legal_path(self.chess_board_starting, 7, 1, 5, 2)
        # move a black knight from 0,6 to 2,5
        legal_check_2 = legal_path(self.chess_board_starting, 0, 6, 2, 5)
        # move a black knight from 0,6 to 2,4 (not a legal L-shape movement)
        legal_check_3 = legal_path(self.chess_board_starting, 0, 6, 2, 4)
        # move a white knight from 7,6 to 6,4 (not legal because current player's piece is in the way)
        legal_check_4 = legal_path(self.chess_board_starting, 7, 6, 6, 4)
        self.assertTrue(legal_check_1, "The knight is unable to move to L-shape space!")
        self.assertTrue(legal_check_2, "The knight is unable to move to L-shape space!")
        self.assertFalse(legal_check_3, "The knight is unable to move to L-shape space!")
        self.assertFalse(legal_check_4, "The knight is unable to move to L-shape space!")

    def test_legal_path_bishop(self):
        # scattered board checks
        # move a white bishop from 5,2 to 7,4
        legal_check_1 = legal_path(self.chess_board_scattered, 5, 2, 7, 4)
        # move a black bishop from 2,5 to 3,6
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 5, 3, 6)

        self.assertTrue(legal_check_1, "The Bishop is unable to make this move!")
        self.assertFalse(legal_check_2, "The Bishop should not be able to make this move!")

    def test_legal_path_queen(self):
        # scattered board checks
        # move a white queen from 5,3 to 7,5 (diagonal move)
        legal_check_1 = legal_path(self.chess_board_scattered, 5, 3, 7, 5)
        # move a black queen from 2,3 to 0,3 (rook movement)
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 3, 0, 3)
        # move a black queen from 2,3 to 2,4 (illegal rook movement since space is taken)
        legal_check_3 = legal_path(self.chess_board_scattered, 2, 3, 2, 4)

        self.assertTrue(legal_check_1, "Queen unable to make bishop movement!")
        self.assertTrue(legal_check_2, "Queen unable to make rook movement!")
        self.assertFalse(legal_check_3, "Queen should be unable to move to friendly spot!")

    def test_legal_path_king(self):
        # starting board checks
        # move a white king from 7,4 to 6,3 (illegal move since current player pawn is in the way)
        legal_check_1 = legal_path(self.chess_board_starting, 7, 4, 6, 3)

        # scattered board checks
        # move a black king from 2,4 to 1,3 (diagonal movement)
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 4, 1, 3)
        # move a white king from 5,4 to 5,3 (illegal rook movement)
        legal_check_3 = legal_path(self.chess_board_scattered, 5, 4, 5, 3)

        self.assertFalse(legal_check_1, "King cant move with another piece in the way!")
        self.assertTrue(legal_check_2, "King unable to make diagonal movement!")
        self.assertFalse(legal_check_3, "King should be unable to move to this spot.")

    def tearDown(self):
        del self.chess_board_starting
        del self.chess_board_scattered

ut.main()