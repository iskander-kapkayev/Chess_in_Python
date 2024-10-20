import unittest as ut
from chess_scripts_2 import *

class TestLegalMove(ut.TestCase):

    def setUp(self):
        self.chess_board_starting = board_for_testing()
        self.chess_board_scattered = board_for_testing_scattered()
        obtain_possible_moves(self.chess_board_starting, None)
        obtain_possible_moves(self.chess_board_scattered, None)

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

    def test_legal_conclusion_self_check(self):
        # scattered board checks
        # move bP from 3,6 to 4,5
        self.chess_board_scattered[4][5] = self.chess_board_scattered[3][6]
        self.chess_board_scattered[3][6] = ' '
        previous = ('black', 'bP', (3, 6), (4, 5))
        obtain_possible_moves(self.chess_board_scattered, previous)

        # now the wK can eat the 4,5 bP
        legal_check_1 = legal_conclusion(self.chess_board_scattered, 5, 4, 4, 5, previous)
        self.assertFalse(legal_check_1, "Not possible; King would be placed into a check position!")

    def test_move_counter(self):
        # count the number of moves at the start of the game (should be 20 per color, 8 pawns * 2 moves + 2 knights * 2 moves)
        check_white_moves = count_moves(self.chess_board_starting, 0)
        self.assertEqual(check_white_moves, 20,"There should be 20 moves for each color.")
        check_black_moves = count_moves(self.chess_board_starting, 1)
        self.assertEqual(check_black_moves, 20, "There should be 20 moves for each color.")
    
    def test_gui_movements(self):
        # play a short game and assert movements that are allowed and not allowed
        active_check = False
        # selected piece is a white pawn
        selected_piece = (6,4)
        selected_x, selected_y = selected_piece
        # movement spot is 2 spaces up (initial pawn move)
        row = 4
        col = 4
        # set player to white
        player = 0
        if not active_check:

            if selected_piece:
                current_piece = self.chess_board_starting[selected_x][selected_y]

                # make sure players go in order: W, B, W, B, etc.
                if ((current_piece.get_player() == 'white' and player % 2 == 0)
                        or (current_piece.get_player() == 'black' and player % 2 == 1)):

                    # make sure a legal move is selected
                    # since all possible moves are labeled
                    if (row, col) in current_piece.get_possible_moves():

                        # in case of a king's castle
                        if (((current_piece.get_piece() == 'wK')
                             or (current_piece.get_piece() == 'bK'))
                                and (abs(selected_x - col) == 2)):
                            # perform king's castle
                            chess_board = king_castle(self.chess_board_starting, selected_x, selected_y, row, col)
                            # perform end of move actions

                            # chess_board, previous_move = end_of_move(chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 3)
                            # track previous move made
                            previous_move = (self.chess_board_starting[row][col].get_player(),
                                             self.chess_board_starting[row][col].get_piece(),
                                             self.chess_board_starting[row][col].get_moved_from(),
                                             self.chess_board_starting[row][col].get_moved_to()
                                             )
                            # update possible moves list
                            obtain_possible_moves(self.chess_board_starting, previous_move)
                            black_king_check, white_king_check = player_check_logic(self.chess_board_starting)

                        # in case of an en passant by pawns
                        elif (((current_piece.get_piece() == 'bP')
                               or (current_piece.get_piece() == 'wP'))
                              and (abs(selected_x - row) == 1 and abs(selected_y - col) == 1)
                              and (self.chess_board_starting[row][col] == ' ')):
                            # perform end of move actions for en passant
                            # chess_board, previous_move = end_of_move(chess_board, selected_piece[0] , selected_piece[1], row, col, board_size, 1)
                            # this means en passant was done!
                            self.chess_board_starting[row][col] = self.chess_board_starting[selected_x][selected_y]
                            # remove the selected piece from the old spot
                            self.chess_board_starting[selected_x][selected_y] = ' '

                            # capture the pawn by en passant
                            if self.chess_board_starting[row][col].get_piece() == 'bP':
                                # if black, pawn to capture is above it
                                self.chess_board_starting[row - 1][col] = ' '
                            elif self.chess_board_starting[row][col].get_piece() == 'wP':
                                # if white, pawn to capture is below it
                                self.chess_board_starting[row + 1][col] = ' '

                            # update the moved_to and moved_from positions in the chess piece class
                            self.chess_board_starting[row][col].update_moved_to((row, col))
                            self.chess_board_starting[row][col].update_moved_from((selected_x, selected_y))

                            # track previous move made
                            previous_move = (self.chess_board_starting[row][col].get_player(),
                                             self.chess_board_starting[row][col].get_piece(),
                                             self.chess_board_starting[row][col].get_moved_from(),
                                             self.chess_board_starting[row][col].get_moved_to()
                                             )

                            # update possible moves list
                            obtain_possible_moves(self.chess_board_starting, previous_move)
                            black_king_check, white_king_check = player_check_logic(self.chess_board_starting)

                        # any other legal move
                        else:
                            # perform end of move actions
                            # this means a regular legal move was done
                            self.chess_board_starting[row][col] = self.chess_board_starting[selected_x][selected_y]
                            # remove the selected piece from the old spot
                            self.chess_board_starting[selected_x][selected_y] = ' '
                            # update the moved_to and moved_from positions in the chess piece class
                            self.chess_board_starting[row][col].update_moved_to((row, col))
                            self.chess_board_starting[row][col].update_moved_from((selected_x, selected_y))

                            # track previous move made
                            previous_move = (self.chess_board_starting[row][col].get_player(),
                                             self.chess_board_starting[row][col].get_piece(),
                                             self.chess_board_starting[row][col].get_moved_from(),
                                             self.chess_board_starting[row][col].get_moved_to()
                                             )

                            # update possible moves list
                            obtain_possible_moves(self.chess_board_starting, previous_move)
                            black_king_check, white_king_check = player_check_logic(self.chess_board_starting)

                        # iterate to next player, evaluate a check, and reset piece to none
                        player += 1
                        active_check = active_check_lookup(player, black_king_check, white_king_check)
                        selected_piece = None

                    else:
                        # if move is not in legal move set
                        selected_piece = None

                else:
                    # if wrong color
                    selected_piece = None

            elif not selected_piece:
                # this will select a piece if none have been selected
                if self.chess_board_starting[row][col] != ' ':
                    selected_piece = (row, col)

        self.assertEqual(self.chess_board_starting[6][4], ' ', "the pawn should have moved")
        self.assertEqual(self.chess_board_starting[4][4], 'wP', "the pawn is now here")
        self.assertEqual(self.chess_board_starting[4][4].get_possible_moves(), [(3,4)], "the only possible pawn move is now 3, 5")
        # since the king was revealed, the wK now has a new move
        self.assertEqual(self.chess_board_starting[7][4].get_possible_moves(), [(6, 4)],"the king now can move to 6, 4")
        self.assertEqual(selected_piece, None, "when run correctly, the selected piece refreshes")
        
'''
    def tearDown(self):
        del self.chess_board_starting
        del self.chess_board_scattered
'''

if __name__ == "__main__":
    ut.main()