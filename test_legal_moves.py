import unittest as ut
from chess_scripts_2 import *

class TestLegalMoves(ut.TestCase):

    def setUp(self):
        self.chess_board_starting = board_for_testing()
        self.chess_board_scattered = board_for_testing_scattered()

    # ---------- testing of legal path function (only considers possible movements for a piece) ----------
    def test_legal_path_pawn(self):
        # starting board checks
        # move a pawn from 6,2 to 4,2 from starting position
        legal_check = legal_path(self.chess_board_starting, 6, 2, 4, 2, None)
        # move a pawn from 6,2 to 3,2 from starting position (not legal)
        legal_check_2 = legal_path(self.chess_board_starting, 6, 2, 3, 2, None)
        self.assertTrue(legal_check, "The white pawn was unable to move 2 squares up from the starting position!")
        self.assertFalse(legal_check_2, "The pawn can't move 3 spaces!")

        # scattered board checks
        # move a pawn from 4,3 to 3,3 when there's a pawn in the way (not legal)
        legal_check_3 = legal_path(self.chess_board_scattered, 4, 3, 3, 3, None)
        self.assertFalse(legal_check_3, "The pawn can't move 3 spaces!")

    def test_legal_path_knight(self):
        # starting board checks
        # move a white knight from 7,1 to 5,2
        legal_check_1 = legal_path(self.chess_board_starting, 7, 1, 5, 2, None)
        # move a black knight from 0,6 to 2,5
        legal_check_2 = legal_path(self.chess_board_starting, 0, 6, 2, 5, None)
        # move a black knight from 0,6 to 2,4 (not a legal L-shape movement)
        legal_check_3 = legal_path(self.chess_board_starting, 0, 6, 2, 4, None)
        # move a white knight from 7,6 to 6,4 (not legal because current player's piece is in the way)
        legal_check_4 = legal_path(self.chess_board_starting, 7, 6, 6, 4, None)
        self.assertTrue(legal_check_1, "The knight is unable to move to L-shape space!")
        self.assertTrue(legal_check_2, "The knight is unable to move to L-shape space!")
        self.assertFalse(legal_check_3, "The knight is unable to move to L-shape space!")
        self.assertFalse(legal_check_4, "The knight is unable to move to L-shape space!")

    def test_legal_path_bishop(self):
        # scattered board checks
        # move a white bishop from 5,2 to 7,4
        legal_check_1 = legal_path(self.chess_board_scattered, 5, 2, 7, 4, None)
        # move a black bishop from 2,5 to 3,6
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 5, 3, 6, None)

        self.assertTrue(legal_check_1, "The Bishop is unable to make this move!")
        self.assertFalse(legal_check_2, "The Bishop should not be able to make this move!")

    def test_legal_path_queen(self):
        # scattered board checks
        # move a white queen from 5,3 to 7,5 (diagonal move)
        legal_check_1 = legal_path(self.chess_board_scattered, 5, 3, 7, 5, None)
        # move a black queen from 2,3 to 0,3 (rook movement)
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 3, 0, 3, None)
        # move a black queen from 2,3 to 2,4 (illegal rook movement since space is taken)
        legal_check_3 = legal_path(self.chess_board_scattered, 2, 3, 2, 4, None)

        self.assertTrue(legal_check_1, "Queen unable to make bishop movement!")
        self.assertTrue(legal_check_2, "Queen unable to make rook movement!")
        self.assertFalse(legal_check_3, "Queen should be unable to move to friendly spot!")

    def test_legal_path_king(self):
        # starting board checks
        # move a white king from 7,4 to 6,3 (illegal move since current player pawn is in the way)
        legal_check_1 = legal_path(self.chess_board_starting, 7, 4, 6, 3, None)

        # scattered board checks
        # move a black king from 2,4 to 1,3 (diagonal movement)
        legal_check_2 = legal_path(self.chess_board_scattered, 2, 4, 1, 3, None)
        # move a white king from 5,4 to 5,3 (illegal rook movement)
        legal_check_3 = legal_path(self.chess_board_scattered, 5, 4, 5, 3, None)

        self.assertFalse(legal_check_1, "King cant move with another piece in the way!")
        self.assertTrue(legal_check_2, "King unable to make diagonal movement!")
        self.assertFalse(legal_check_3, "King should be unable to move to this spot.")

    # ---------- testing for legal pathways, this means no pieces are in the way of the legal movements ----------

    def test_legal_movement_pawn(self):
        # scattered board checks
        # move a white pawn from 4,3 to 3,3 when there's a pawn in the way (not legal)
        legal_check_1 = legal_movement(self.chess_board_scattered, 4, 3, 3, 3, None)
        self.assertFalse(legal_check_1, "The pawn can't move when blocked!")

        # starting board checks
        # move starting pawn two spaces from 6,1 to 4,1
        legal_check_2 = legal_movement(self.chess_board_starting, 6, 1, 4, 1, None)
        self.assertTrue(legal_check_2, "The pawn should be able to move 2 spaces in the beginning!")

    def test_legal_movement_king(self):
        # starting board checks
        # move a white king from 7,4 to 6,3 (illegal move since current player pawn is in the way)
        legal_check_1 = legal_movement(self.chess_board_starting, 7, 4, 6, 3, None)
        self.assertFalse(legal_check_1, "The king can't move when blocked!")

    def test_legal_movement_knight(self):
        # starting board checks
        # move a white knight from 7,6 to 6,4 (not legal because current player's piece is in the way)
        legal_check_1 = legal_movement(self.chess_board_starting, 7, 6, 6, 4, None)
        self.assertFalse(legal_check_1, "The knight can't move when blocked at the new space!")

    def test_legal_movement_rook(self):
        # scattered board checks
        # move bR from scattered spot to 1,7
        self.chess_board_scattered[1][7] = self.chess_board_scattered[2][7]
        # replace old spot with an empty piece
        self.chess_board_scattered[2][7] = ' '
        # now move the bR from 1,7 to 1,1 (legal movement)
        legal_check_1 = legal_movement(self.chess_board_scattered, 1, 7, 1, 1, None)
        self.assertTrue(legal_check_1, "The rook has a blockade in the way!")
        # actually move the bR
        self.chess_board_scattered[1][1] = self.chess_board_scattered[1][7]
        self.chess_board_scattered[1][7] = ' '
        # move bQ up 1 space
        self.chess_board_scattered[1][3] = self.chess_board_scattered[2][3]
        self.chess_board_scattered[2][3] = ' '
        # now there's a blockade for the rook, it should NOT be able to move back to it's og spot
        legal_check_2 = legal_movement(self.chess_board_scattered, 1, 1, 1, 7, None)
        self.assertFalse(legal_check_2, "The rook should be blocked and can't move here!")

    def test_legal_movement_bishop(self):
        # scattered board checks
        # move bR from scattered spot to 1,7
        self.chess_board_scattered[1][7] = self.chess_board_scattered[2][7]
        self.chess_board_scattered[2][7] = ' '
        # now move the bR from 1,7 to 1,1
        self.chess_board_scattered[1][1] = self.chess_board_scattered[1][7]
        self.chess_board_scattered[1][7] = ' '
        # move bQ up 1 space
        self.chess_board_scattered[1][3] = self.chess_board_scattered[2][3]
        self.chess_board_scattered[2][3] = ' '
        # now there's a blockade for the bishop in both directions upward
        legal_check_1 = legal_movement(self.chess_board_scattered, 2, 2, 0, 0, None)
        legal_check_2 = legal_movement(self.chess_board_scattered, 2, 2, 0, 4, None)
        self.assertFalse(legal_check_1, "The bishop should be blocked and can't move here!")
        self.assertFalse(legal_check_2, "The bishop should be blocked and can't move here!")

    def test_legal_movement_queen(self):
        # scattered board checks
        # move bR from scattered spot to 1,7
        self.chess_board_scattered[1][7] = self.chess_board_scattered[2][7]
        self.chess_board_scattered[2][7] = ' '
        # now move the bR from 1,7 to 1,1
        self.chess_board_scattered[1][1] = self.chess_board_scattered[1][7]
        self.chess_board_scattered[1][7] = ' '
        # now move the bB from 2,2 to 0,4
        self.chess_board_scattered[0][4] = self.chess_board_scattered[2][2]
        self.chess_board_scattered[2][2] = ' '
        # move bQ up 1 space
        self.chess_board_scattered[1][3] = self.chess_board_scattered[2][3]
        self.chess_board_scattered[2][3] = ' '
        # now there's a blockade for the queen to go from 1,3 to 1,0 or 1,3 to 0,4
        legal_check_1 = legal_movement(self.chess_board_scattered, 1, 3, 1, 0, None)
        legal_check_2 = legal_movement(self.chess_board_scattered, 1, 3, 0, 4, None)
        self.assertFalse(legal_check_1, "The queen should be blocked and can't move here!")
        self.assertFalse(legal_check_2, "The queen should be blocked and can't move here!")

    def test_legal_movement_en_passant_wp(self):
        # starting board checks
        # move wP from 6,4 to 4,4 then to 3,4
        self.chess_board_starting[4][4] = self.chess_board_starting[6][4]
        self.chess_board_starting[6][4] = ' '

        self.chess_board_starting[3][4] = self.chess_board_starting[4][4]
        self.chess_board_starting[4][4] = ' '

        # move bP from 1,3 to 3,3
        self.chess_board_starting[3][3] = self.chess_board_starting[1][3]
        self.chess_board_starting[1][3] = ' '

        # now the wP should be able to capture the bP via en passant
        previous = ('black', 'bP', (1, 3), (3, 3))
        legal_check_1 = legal_movement(self.chess_board_starting, 3, 4, 2, 3, previous)
        self.assertTrue(legal_check_1, "White pawn should be able to perform en passant!")

    def test_legal_movement_en_passant_bp(self):
        # starting board checks
        # move bP from 1,4 to 3,4 then to 4,4
        self.chess_board_starting[3][4] = self.chess_board_starting[1][4]
        self.chess_board_starting[1][4] = ' '

        self.chess_board_starting[4][4] = self.chess_board_starting[3][4]
        self.chess_board_starting[3][4] = ' '

        # move wP from 6,5 to 4,5
        self.chess_board_starting[4][5] = self.chess_board_starting[6][5]
        self.chess_board_starting[6][5] = ' '

        # now the bP should be able to capture the bP via en passant
        previous = ('white', 'wP', (6, 5), (4, 5))
        legal_check_1 = legal_movement(self.chess_board_starting, 4, 4, 5, 5, previous)
        self.assertTrue(legal_check_1, "Black pawn should be able to perform en passant!")

        # move a totally different piece, previously, but the pawn is in the right space for en passant
        previous_2 = ('white', 'wB', (1, 1), (2, 2))
        legal_check_2 = legal_movement(self.chess_board_starting, 4, 4, 5, 5, previous_2)
        self.assertFalse(legal_check_2, "En passant only allowed on first attempt!")

    def test_legal_movement_self_check(self):
        # scattered board checks
        # move bP from 3,6 to 4,5
        self.chess_board_scattered[4][5] = self.chess_board_scattered[3][6]
        self.chess_board_scattered[3][6] = ' '

        # now the wK can eat the 4,5 bP
        legal_check_1 = legal_movement(self.chess_board_starting, 5, 4, 4, 5, None)
        self.assertFalse(legal_check_1, "Not possible; King would be placed into a check position!")

    def tearDown(self):
        del self.chess_board_starting
        del self.chess_board_scattered

ut.main()