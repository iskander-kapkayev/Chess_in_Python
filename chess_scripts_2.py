# we need to create a chess game
# we will need to do the following things:
#       1) create a game board to keep track of pieces and movement
#       2) assign restriction to pieces (pawns, rooks, etc.)
#       3) allow each player to make one "legal" move
#       4) keep track of lost pieces as a player score
#       5) create a "check" and "checkmate" situation so that a player can win the game
#       6) once game ends, option to play again

# ---------- Chess Player class determines the color of the player ---------- #
class ChessPlayer:
    # set player color
    def __init__(self, player):
        self.player = player

# ---------- Chess Piece falls under the chess player and defines piece attributes ---------- #
# piece = name of a piece
# position = current position
# moved_to = newest position
# moved_from = previous position
# possible_moves = possible legal positions
class ChessPiece(ChessPlayer):
    def __init__(self, player, piece, position):
        self.piece = piece
        self.position = position
        self.moved_to = None
        self.moved_from = position
        self.possible_moves = None
        super().__init__(player)

    # get the position of the piece
    def get_position(self):
        x, y = self.position
        return x, y

    # get the player of the piece
    def get_player(self):
        return self.player

    # get the player of the piece
    def get_piece(self):
        return self.piece

    # get moved to
    def get_moved_to(self):
        return self.moved_to

    # get moved from
    def get_moved_from(self):
        return self.moved_from

    # get possible moves
    def get_possible_moves(self):
        return self.possible_moves

    # update the position of the piece if checks are complete
    def update_position(self, new_position):
        self.position = new_position

    # update to new position
    def update_moved_to(self, new_position):
        self.moved_to = new_position
        self.update_position(self.moved_to)

    # update to old position
    def update_moved_from(self, new_position):
        self.moved_from = new_position

    # update possible moves
    def update_possible_moves(self, list_of_moves):
        self.possible_moves = list_of_moves

    # evaluate position of a chess piece based on given x, y
    def moved(self):
        if self.moved_to is None:
            return False
        return True

    # so that only the piece name prints in the lists
    def __repr__(self):
        return self.piece

# ---------- initialize starting game pieces ---------- #

def initialize_pieces():
    pawn_row_black = [ChessPiece('black', 'bP', (1, i)) for i in range(8)]
    pawn_row_white = [ChessPiece('white', 'wP', (6, i)) for i in range(8)]
    back_row_white = [ChessPiece('white', 'wR', (7, 0)),
                      ChessPiece('white', 'wN', (7, 1)),
                      ChessPiece('white', 'wB', (7, 2)),
                      ChessPiece('white', 'wQ', (7, 3)),
                      ChessPiece('white', 'wK', (7, 4)),
                      ChessPiece('white', 'wB', (7, 5)),
                      ChessPiece('white', 'wN', (7, 6)),
                      ChessPiece('white', 'wR', (7, 7))
    ]
    back_row_black = [ChessPiece('black', 'bR', (0, 0)),
                      ChessPiece('black', 'bN', (0, 1)),
                      ChessPiece('black', 'bB', (0, 2)),
                      ChessPiece('black', 'bQ', (0, 3)),
                      ChessPiece('black', 'bK', (0, 4)),
                      ChessPiece('black', 'bB', (0, 5)),
                      ChessPiece('black', 'bN', (0, 6)),
                      ChessPiece('black', 'bR', (0, 7))
    ]

    all_game_pieces = pawn_row_black + pawn_row_white + back_row_black + back_row_white
    return all_game_pieces

# ---------- initialize starting chess board ---------- #

def initialize_chess_board(board_size):
    # create a 2D array to represent the board
    chess_board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

    # initialize pieces on chess board
    all_game_pieces = initialize_pieces()
    for game_piece in all_game_pieces:
        x_coord, y_coord = game_piece.get_position()
        chess_board[x_coord][y_coord] = game_piece
        
    return chess_board

# ---------- This evaluates the legal movement of a piece - is there anything in the way? ---------- #

def legal_movement(chess_board, selected_piece_x, selected_piece_y, new_x, new_y, previous, initial):
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    enemy_piece = chess_board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # make sure that the new spot is not the old spot (clicking the same piece error), and not empty
    if current_piece == enemy_piece or current_piece == ' ':
        return False

    # grab player color for evaluation
    current_player = current_piece.get_player()

    # first check if the path is legal (aka move makes sense for selected piece)
    if legal_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y, previous):

        # if movement is legal for a piece, now check for a piece in pathway of a piece

        # --------------- Pawn movements! --------------- #
        if current_piece.get_piece() == 'wP' or current_piece.get_piece() == 'bP':
            # if the pawn moves 2 spaces
            if abs(selected_piece_x - new_x) == 2:
                # make sure nothing exists between new_x
                if current_piece.get_piece() == 'wP':
                    # if white pawn, check space above it
                    if chess_board[selected_piece_x - 1][selected_piece_y] == ' ':
                        return True
                elif current_piece.get_piece() == 'bP':
                    #  if black pawn, check space below it
                    if chess_board[selected_piece_x + 1][selected_piece_y] == ' ':
                        return True
            # else if the pawn moves one space (not a capture, capture is already legalized in legal_path function)
            elif abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 1:
                # make sure that space is available
                if enemy_piece == ' ':
                    return True
            # else if capturing a piece, this was approved in legal path so we can move on
            elif abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 2:
                return True

        # --------------- Rook movements! --------------- #
        # check all spaces between rooks current spot and next spot
        elif current_piece.get_piece() == 'wR' or current_piece.get_piece() == 'bR':
            # check if rook is moving up/down or left/right
            if abs(change_in_x) == 0:
                # rook is moving left and right
                if change_in_y < 0:
                    # in case rook is moving 1 square
                    if change_in_y == -1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, abs(change_in_y), 1):
                            if chess_board[selected_piece_x][selected_piece_y - iterator] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True
                elif change_in_y > 0:
                    # in case rook is moving 1 square
                    if change_in_y == 1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, abs(change_in_y), 1):
                            if chess_board[selected_piece_x][selected_piece_y + iterator] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True
            # check if rook is moving up/down or left/right
            elif abs(change_in_y) == 0:
                # rook is moving up and down
                if change_in_x < 0:
                    # in case rook is moving 1 square
                    if change_in_x == -1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, abs(change_in_x), 1):
                            if chess_board[selected_piece_x - iterator][selected_piece_y] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True
                elif change_in_x > 0:
                    # in case rook is moving 1 square
                    if change_in_x == 1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, change_in_x, 1):
                            if chess_board[selected_piece_x + iterator][selected_piece_y] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True


        # --------------- Knight movements! --------------- #
        # knights do not have blocked issues
        # this should return true always, unless your own piece is in the way
        elif current_piece.get_piece() == 'wN' or current_piece.get_piece() == 'bN':
            # if the space is empty
            if enemy_piece == ' ':
                return True
            # if the space is not empty, then it must have a different color piece
            elif enemy_piece.get_player() != current_piece.get_player():
                return True


        # --------------- Bishop movements! --------------- #
        # Bishops move along diagonals, with a +- 1 slope
        # Bishop's only restriction is a piece in the way
        elif current_piece.get_piece() == 'wB' or current_piece.get_piece() == 'bB':
            # since we know the path of the bishop is valid, then we can use the delta to check in between

            # both x and y decrease
            if change_in_x < 0 and change_in_y < 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y - iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True
            # only x decreases
            elif change_in_x < 0 < change_in_y:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y + iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

            # only y decreases
            elif change_in_y < 0 < change_in_x:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y - iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

            # both x and y increase
            elif change_in_x > 0 and change_in_y > 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y + iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

        # --------------- Queen movements! --------------- #
        # Queens need mad space between their movements
        elif current_piece.get_piece() == 'wQ' or current_piece.get_piece() == 'bQ':
            # if queen makes a rook movement type

            # check if queen is moving up/down or left/right
            if abs(change_in_x) == 0:
                # queen is moving left and right
                if change_in_y < 0:
                    # in case queen is moving 1 square
                    if change_in_y == -1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, abs(change_in_y), 1):
                            if chess_board[selected_piece_x][selected_piece_y - iterator] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True
                elif change_in_y > 0:
                    # in case queen is moving 1 square
                    if change_in_y == 1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, change_in_y, 1):
                            if chess_board[selected_piece_x][selected_piece_y + iterator] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True

            # check if queen is moving up/down or left/right
            elif abs(change_in_y) == 0:
                # queen is moving up and down
                if change_in_x < 0:
                    # in case queen is moving 1 square
                    if change_in_x == -1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, abs(change_in_x), 1):
                            if chess_board[selected_piece_x - iterator][selected_piece_y] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True
                elif change_in_x > 0:
                    # in case queen is moving 1 square
                    if change_in_x == 1:
                        if enemy_piece == ' ' or enemy_piece.get_player() != current_piece.get_player():
                            # return true if enemy piece or blank space for capture
                            return True
                    else:
                        for iterator in range(1, change_in_x, 1):
                            if chess_board[selected_piece_x + iterator][selected_piece_y] != ' ':
                                # break loop and return false if a piece is found in the way!
                                return False
                    # else return true if no pieces found in the way
                    return True

            # or if the queen makes a bishop movement
            # both x and y decrease
            elif change_in_x < 0 and change_in_y < 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y - iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

            # only x decreases
            elif change_in_x < 0 < change_in_y:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y + iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

            # only y decreases
            elif change_in_y < 0 < change_in_x:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y - iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True

            # both x and y increase
            elif change_in_x > 0 and change_in_y > 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y + iterator] != ' ':
                        return False
                # else return true if no pieces found in the way
                return True


        # --------------- King movements! --------------- #
        # Kings can move any direction by 1 square
        # there must be no piece in his way, or he must capture an enemy piece
        # check possible placements before allowing move
        elif current_piece.get_piece() == 'wK' or current_piece.get_piece() == 'bK':
            # all king moves have already been approved in legal path
            # now must consider enemy pieces in range
            # we can use the possible move list to make a move
            for rows in chess_board:
                for square in rows:
                    if square != ' ':
                        if square.get_player() != current_piece.get_player():
                            for item in square.get_possible_moves():
                                check_1, check_2 = item
                                if new_x == check_1 and new_y == check_2:
                                    return False
            return True

    # return false if nothing is triggered above
    return False

# ---------- This evaluates the legal path of a piece - where can a piece move? ---------- #

def legal_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y, previous):
    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    enemy_piece = chess_board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y


    # --------------- Pawn movements! --------------- #
    # dependent on white or black because of movement restrictions
    # en passant?
    if current_piece.get_piece() == 'wP' or current_piece.get_piece() == 'bP':
        if current_piece.get_piece() == 'wP':
            # does the col change? if yes, then it means potential capture
            if selected_piece_y == new_y:
                # if pawn is in original spot
                if selected_piece_x == 6:
                    # pawn can move one OR two squares if no piece is on that square
                    if enemy_piece == ' ':
                        if selected_piece_x - new_x == 1 or selected_piece_x - new_x == 2:
                            return True
                else:
                    # pawn can move one square
                    if enemy_piece == ' ':
                        if selected_piece_x - new_x == 1:
                            return True
            elif selected_piece_y != new_y:
                # attempt en passant
                if enemy_piece == ' ':
                    # if the selected piece is on the 3rd row of the board
                    if selected_piece_x == 3:
                        # each condition must be met in order to allow for an en passant
                        prev_color, prev_piece, prev_moved_from, prev_moved_to = previous
                        prev_moved_from_x, prev_moved_from_y = prev_moved_from
                        prev_moved_to_x, prev_moved_to_y = prev_moved_to
                        # player color must be different from previous player, previous moved piece is bP
                        if prev_color != current_piece.get_player() and prev_piece == 'bP':
                            # previous move was a black pawn moved from row 1 to row 3
                            if prev_moved_from_x == 1 and prev_moved_to_x == 3:
                                # if the pawn moved perfectly to the side of your pawn then you can capture as if no double movement
                                if new_x == prev_moved_to_x - 1 and new_y == prev_moved_to_y:
                                    # the conditions were met, so en passant is possible!
                                    return True
                # if the other player is different
                elif enemy_piece != ' ':
                    if enemy_piece.get_player() != current_piece.get_player():
                        # if the new position of the pawn is 1 row away
                        if selected_piece_x - new_x == 1:
                            # if the position of the pawn will be +-1 col
                            if abs(selected_piece_y - new_y) == 1:
                                return True

        elif current_piece.get_piece() == 'bP':
            # does the col change? if yes, then it means potential capture
            if selected_piece_y == new_y:
                # if pawn is in original spot
                if selected_piece_x == 1:
                    # pawn can move one OR two squares
                    if enemy_piece == ' ':
                        if new_x - selected_piece_x == 1 or new_x - selected_piece_x == 2:
                            return True
                else:
                    # pawn can move one square
                    if enemy_piece == ' ':
                        if new_x - selected_piece_x == 1:
                            return True
            elif selected_piece_y != new_y:
                # attempt en passant
                if enemy_piece == ' ':
                    # if the selected pawn is on the 4th row of the board
                    if selected_piece_x == 4:
                        # each condition must be met in order to allow for an en passant
                        prev_color, prev_piece, prev_moved_from, prev_moved_to = previous
                        prev_moved_from_x, prev_moved_from_y = prev_moved_from
                        prev_moved_to_x, prev_moved_to_y = prev_moved_to
                        # player color must be different from previous player, previous moved piece is bP
                        if prev_color != current_piece.get_player() and prev_piece == 'wP':
                            # previous move was a black pawn moved from row 1 to row 3
                            if prev_moved_from_x == 6 and prev_moved_to_x == 4:
                                # if the pawn moved perfectly to the side of your pawn then you can capture as if no double movement
                                if new_x == prev_moved_to_x + 1 and new_y == prev_moved_to_y:
                                    # the conditions were met, so en passant is possible!
                                    chess_board[prev_moved_to_x][prev_moved_to_y] = ' '
                                    return True
                # if the other player is different
                elif enemy_piece != ' ':
                    if enemy_piece.get_player() != current_piece.get_player():
                        # if the new position of the pawn is 1 row away
                        if new_x - selected_piece_x == 1:
                            # if the position of the pawn will be +-1 col
                            if abs(new_y - selected_piece_y) == 1:
                                return True


    # --------------- Rook movements! --------------- #
    # rooks can only move up/down left/right
    # this only says rooks legal move, does not check for a piece in the way
    elif current_piece.get_piece() == 'wR' or current_piece.get_piece() == 'bR':
        # check if blank or an enemy in the spot
        if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
            # assume rook is moving up/down
            if selected_piece_y == new_y:
                # rook moved left/right
                if selected_piece_x != new_x:
                    return True
            # assuming rook moves left/right
            elif selected_piece_x == new_x:
                # rook moved up/down
                if selected_piece_y != new_y:
                    return True


    # --------------- Knight movements! --------------- #
    # knights move in an L-shape, with a +- 2 or +- 0.5 slope, where abs(dx)+abs(dy) = 3
    # knight has no movement restrictions
    elif current_piece.get_piece() == 'wN' or current_piece.get_piece() == 'bN':
        # check if your own color piece is in the way, if it is, then not allowed
        if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
            # check for maximum change of 3 squares
            if abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 3:
                # if 3 square movement, then check slope for +-2 or = -0.5
                if abs(selected_piece_y - new_y) == 2 * abs(selected_piece_x - new_x) or abs(selected_piece_y - new_y) == 0.5 * abs(selected_piece_x - new_x):
                    return True


    # --------------- Bishop movements! --------------- #
    # Bishops move along diagonals, with a +- 1 slope
    # Bishop's only restriction is a piece in the way
    elif current_piece.get_piece() == 'wB' or current_piece.get_piece() == 'bB':
        # check if your own color piece is in the new square, if it is, then not allowed
        if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
            # check for slope of +- 1
            if abs(selected_piece_y - new_y) == abs(selected_piece_x - new_x):
                return True


    # --------------- Queen movements! --------------- #
    # Queens can move both like a Rook and like a bishop
    # Must apply same rules as above
    elif current_piece.get_piece() == 'wQ' or current_piece.get_piece() == 'bQ':
        if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
            # queen makes either rook movements
            # assume queen is moving up/down
            if selected_piece_y == new_y:
                # queen moved left/right
                if selected_piece_x != new_x:
                    return True
            # assuming queen moves left/right
            elif selected_piece_x == new_x:
                # queen moved up/down
                if selected_piece_y != new_y:
                    return True
            # or queen makes bishop movements
            elif abs((selected_piece_y - new_y)/(selected_piece_x - new_x)) == 1:
                return True


    # --------------- King movements! --------------- #
    # Kings can move any direction by 1 square
    # there must be no piece in his way, or he must capture an enemy piece
    # we can cycle list of possible moves to make sure that he is not in the range of an enemy piece
    elif current_piece.get_piece() == 'wK' or current_piece.get_piece() == 'bK':
        # check if king is trying to do a castle
        if (abs(change_in_x) == 0
            and abs(change_in_y) == 2
            and current_piece.moved() is False):
            # initiate alternative chess board to validate the movement for check logic
            king_chess_board = chess_board
            current_player = current_piece.get_player()

            # is king moving left or right?
            if change_in_y > 0:
                # king is moving right
                if current_piece.get_player() == 'white' and chess_board[7][7] != ' ' and chess_board[7][7].get_piece() == 'wR':
                    if chess_board[7][7].moved() is False:
                        # white king and white rook, check all spaces between it and the rook
                        # check 7,5 and 7,6 for any pieces and for possible checks
                        if chess_board[7][5] == ' ' and chess_board[7][6] == ' ':
                            # check in between first spot for a check
                            king_chess_board[7][5] = king_chess_board[selected_piece_x][selected_piece_y]
                            king_chess_board[selected_piece_x][selected_piece_y] = ' '
                            black_check, white_check = player_check_logic(king_chess_board)
                            if accidental_self_check(black_check, white_check, current_player) is False:
                                # check in between second spot for a check
                                king_chess_board[7][6] = king_chess_board[7][5]
                                king_chess_board[7][5] = ' '
                                black_check, white_check = player_check_logic(king_chess_board)
                                if accidental_self_check(black_check, white_check, current_player) is False:
                                    return True
                if current_piece.get_player() == 'black' and chess_board[0][7] != ' ' and chess_board[0][7].get_piece() == 'bR':
                    if chess_board[0][7].moved() is False:
                        # white king and white rook, check all spaces between it and the rook
                        # check 0,5 and 0,6 for any pieces and possible checks
                        if chess_board[0][5] == ' ' and chess_board[0][6] == ' ':
                            # check in between first spot for a check
                            king_chess_board[0][5] = king_chess_board[selected_piece_x][selected_piece_y]
                            king_chess_board[selected_piece_x][selected_piece_y] = ' '
                            black_check, white_check = player_check_logic(king_chess_board)
                            if accidental_self_check(black_check, white_check, current_player) is False:
                                # check in between second spot for a check
                                king_chess_board[0][6] = king_chess_board[0][5]
                                king_chess_board[0][5] = ' '
                                black_check, white_check = player_check_logic(king_chess_board)
                                if accidental_self_check(black_check, white_check, current_player) is False:
                                    return True
            if change_in_y < 0:
                # king is moving left
                if current_piece.get_player() == 'white' and chess_board[7][0] != ' ' and chess_board[7][0].get_piece() == 'wR':
                    if chess_board[7][0].moved() is False:
                        # white king and white rook, check all spaces between it and the rook
                        # check 7,1 and 7,2 and 7,3 for any pieces
                        if chess_board[7][1] == ' ' and chess_board[7][2] == ' ' and chess_board[7][3] == ' ':
                            # check in between first spot for a check
                            king_chess_board[7][3] = king_chess_board[selected_piece_x][selected_piece_y]
                            king_chess_board[selected_piece_x][selected_piece_y] = ' '
                            black_check, white_check = player_check_logic(king_chess_board)
                            if accidental_self_check(black_check, white_check, current_player) is False:
                                # check in between second spot for a check
                                king_chess_board[7][2] = king_chess_board[7][3]
                                king_chess_board[7][3] = ' '
                                black_check, white_check = player_check_logic(king_chess_board)
                                if accidental_self_check(black_check, white_check, current_player) is False:
                                    return True
                if current_piece.get_player() == 'black' and chess_board[0][0] != ' ' and chess_board[0][0].get_piece() == 'bR':
                    if chess_board[0][0].moved() is False:
                        # white king and white rook, check all spaces between it and the rook
                        # check 0,1 and 0,2 and 0,3 for any pieces
                        if chess_board[0][1] == ' ' and chess_board[0][2] == ' ' and chess_board[0][3] == ' ':
                            # check in between first spot for a check
                            king_chess_board[0][3] = king_chess_board[selected_piece_x][selected_piece_y]
                            king_chess_board[selected_piece_x][selected_piece_y] = ' '
                            black_check, white_check = player_check_logic(king_chess_board)
                            if accidental_self_check(black_check, white_check, current_player) is False:
                                # check in between second spot for a check
                                king_chess_board[0][2] = king_chess_board[0][3]
                                king_chess_board[0][3] = ' '
                                black_check, white_check = player_check_logic(king_chess_board)
                                if accidental_self_check(black_check, white_check, current_player) is False:
                                    return True

        elif enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
            # king is only allowed to move around radius
            # king can move left/right/up/down

            # king stays on same row
            if abs(change_in_x) == 0:
                # make sure it's moving 1 square left/right
                if abs(change_in_y) == 1:
                    return True

            # king stays on same col
            elif abs(change_in_y) == 0:
                # make sure it's moving 1 square up/down
                if abs(change_in_x) == 1:
                    return True

            # check diagonal movement (should be +- 1 slope)
            elif abs(change_in_y) == abs(change_in_x):
                # make sure king is only moving 1 square in any direction
                if abs(change_in_x) == 1:
                    return True

    # return false if none of the above legal moves are correct
    return False

# ---------- testing! initialize the starting chess board ---------- #

def board_for_testing():
    # initialize game pieces and chess board
    board_size = 8
    chess_board = initialize_chess_board(board_size)
    return chess_board

# ---------- testing! initialize the scattered chess board ---------- #

def board_for_testing_scattered():
    # initialize game pieces and chess board with scattered pieces
    board_size = 8
    chess_board = initialize_chess_board_testing_scattered(board_size)
    return chess_board

# ---------- testing! this is a scattered chess board for evaluation ---------- #

def initialize_chess_board_testing_scattered(board_size):
    # create a 2D array to represent the board
    chess_board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

    # initialize pieces on chess board
    all_game_pieces = initialize_pieces_testing_scattered()
    for game_piece in all_game_pieces:
        x, y = game_piece.get_position()
        chess_board[x][y] = game_piece

    return chess_board

# ---------- testing! this initializes scattered chess board pieces ---------- #

def initialize_pieces_testing_scattered():
    pawn_row_black = [ChessPiece('black', 'bP', (3, i)) for i in range(8)]
    pawn_row_white = [ChessPiece('white', 'wP', (4, i)) for i in range(8)]
    back_row_white = [ChessPiece('white', 'wR', (5, 0)),
                      ChessPiece('white', 'wN', (5, 1)),
                      ChessPiece('white', 'wB', (5, 2)),
                      ChessPiece('white', 'wQ', (5, 3)),
                      ChessPiece('white', 'wK', (5, 4)),
                      ChessPiece('white', 'wB', (5, 5)),
                      ChessPiece('white', 'wN', (5, 6)),
                      ChessPiece('white', 'wR', (5, 7))
    ]
    back_row_black = [ChessPiece('black', 'bR', (2, 0)),
                      ChessPiece('black', 'bN', (2, 1)),
                      ChessPiece('black', 'bB', (2, 2)),
                      ChessPiece('black', 'bQ', (2, 3)),
                      ChessPiece('black', 'bK', (2, 4)),
                      ChessPiece('black', 'bB', (2, 5)),
                      ChessPiece('black', 'bN', (2, 6)),
                      ChessPiece('black', 'bR', (2, 7))
    ]

    all_game_pieces = pawn_row_black + pawn_row_white + back_row_black + back_row_white
    return all_game_pieces

# ---------- this will apply a castle ---------- #

def king_castle(chess_board, selected_piece_x, selected_piece_y, new_row, new_col):
    # initiate current piece and change in y vars
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    change_in_y = new_col - selected_piece_y

    # if change in y is negative
    if change_in_y < 0:
        # move king to castle position and remove old king piece
        chess_board[new_row][new_col] = chess_board[selected_piece_x][selected_piece_y]
        chess_board[selected_piece_x][selected_piece_y] = ' '
        # update chess piece class
        chess_board[new_row][new_col].update_moved_to((new_row, new_col))
        chess_board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            chess_board[new_row][new_col + 1] = chess_board[7][0]
            chess_board[7][0] = ' '
            # update chess piece class
            chess_board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            chess_board[new_row][new_col + 1].update_moved_from((7, 0))
        elif current_piece.piece == 'bK':
            chess_board[new_row][new_col + 1] = chess_board[0][0]
            chess_board[0][0] = ' '
            # update chess piece class
            chess_board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            chess_board[new_row][new_col + 1].update_moved_from((0, 0))
    elif change_in_y > 0:
        # move king to castle position and remove old king piece
        chess_board[new_row][new_col] = chess_board[selected_piece_x][selected_piece_y]
        chess_board[selected_piece_x][selected_piece_y] = ' '
        # update chess piece class
        chess_board[new_row][new_col].update_moved_to((new_row, new_col))
        chess_board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            chess_board[new_row][new_col - 1] = chess_board[7][7]
            chess_board[7][7] = ' '
            # update chess piece class
            chess_board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            chess_board[new_row][new_col - 1].update_moved_from((7, 7))
        elif current_piece.piece == 'bK':
            chess_board[new_row][new_col - 1] = chess_board[0][7]
            chess_board[0][7] = ' '
            # update chess piece class
            chess_board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            chess_board[new_row][new_col - 1].update_moved_from((0, 7))

    return chess_board

# ---------- this will obtain the possible moves values for each piece after a move is completed  ---------- #

def obtain_possible_moves(chess_board, board_size, previous, initial):
    # this function will cycle through every piece on the chess board
    # a blank list of possible moves will be created and then passed into ChessPiece class with update_possible_moves(list)

    for rows in chess_board:
        for square in rows:
            # if a piece is in the square
            if square != ' ':
                # new list for each piece
                list_of_moves = []
                # set current piece
                current_piece_x, current_piece_y = square.get_position()
                #print(f'the current piece x is: {current_piece_x} and the y is: {current_piece_y}')
                # run through every combo of (0,0) to (7,7) to calculate available moves
                for row in range(board_size):
                    for col in range(board_size):
                        #print(f'this is the row: {row} and the col: {col}')
                        if legal_movement(chess_board, current_piece_x, current_piece_y, row, col, previous, initial):
                            list_of_moves.append((row, col))
                # after looping through the board, set list to chess_piece value
                square.update_possible_moves(list_of_moves)
                #square_list = square.get_possible_moves()
                #print(f'the piece is: {square} and the possible moves are: {square_list}')

    #print('\n ------------- \n')
    return chess_board

# ---------- this will perform the ending of moves when running the game ---------- #

def end_of_move(chess_board, selected_piece_x, selected_piece_y, row, col, board_size, to_do):

    if to_do == 1:
        # this means en passant was done!
        chess_board[row][col] = chess_board[selected_piece_x][selected_piece_y]
        # remove the selected piece from the old spot
        chess_board[selected_piece_x][selected_piece_y] = ' '

        # capture the pawn by en passant
        if chess_board[row][col].get_piece() == 'bP':
            # if black, pawn to capture is above it
            chess_board[row - 1][col] = ' '
        elif chess_board[row][col].get_piece() == 'wP':
            # if white, pawn to capture is below it
            chess_board[row + 1][col] = ' '

        # update the moved_to and moved_from positions in the chess piece class
        chess_board[row][col].update_moved_to((row, col))
        chess_board[row][col].update_moved_from((selected_piece_x, selected_piece_y))

        # track previous move made
        previous_move = (chess_board[row][col].get_player(),
                         chess_board[row][col].get_piece(),
                         chess_board[row][col].get_moved_from(),
                         chess_board[row][col].get_moved_to()
                        )

        # update possible moves list
        chess_board = obtain_possible_moves(chess_board, board_size, previous_move, False)
        black_king_check, white_king_check = player_check_logic(chess_board)

    elif to_do == 2:
        # this means en passant was done!
        chess_board[row][col] = chess_board[selected_piece_x][selected_piece_y]
        # remove the selected piece from the old spot
        chess_board[selected_piece_x][selected_piece_y] = ' '
        # update the moved_to and moved_from positions in the chess piece class
        chess_board[row][col].update_moved_to((row, col))
        chess_board[row][col].update_moved_from((selected_piece_x, selected_piece_y))

        # track previous move made
        previous_move = (chess_board[row][col].get_player(),
                         chess_board[row][col].get_piece(),
                         chess_board[row][col].get_moved_from(),
                         chess_board[row][col].get_moved_to()
                         )

        # update possible moves list
        chess_board = obtain_possible_moves(chess_board, board_size, previous_move, False)
        black_king_check, white_king_check = player_check_logic(chess_board)

    elif to_do == 3:
        # track previous move made
        previous_move = (chess_board[row][col].get_player(),
                         chess_board[row][col].get_piece(),
                         chess_board[row][col].get_moved_from(),
                         chess_board[row][col].get_moved_to()
                         )
        # update possible moves list
        chess_board = obtain_possible_moves(chess_board, board_size, previous_move, False)
        black_king_check, white_king_check = player_check_logic(chess_board)

    return chess_board, previous_move, black_king_check, white_king_check

# ---------- this will break the game cycle for a check ---------- #

def cycle_breaker_check(chess_board, active_check, player):
    # break the cycle if active check is now gone
    if active_check is False:
        # iterate to next player
        player += 1
        # reset piece to none
        selected_piece = None
        # return new chess board, player count, and None for selection
        return chess_board, player, selected_piece

# ---------- this will perform player check logic ---------- #

def player_check_logic(chess_board):
    # I will look to see if the black king or white king is being checked
    # will return both statuses of the black/white king

    # initiate some vars for processing check
    black_king_check = False
    white_king_check = False

    # identify the black and white king
    find_bk = 'bK'
    find_wk = 'wK'

    # find the kings
    for rows in chess_board:
        for chess_piece in rows:
            # non-empty chess piece
            if chess_piece != ' ':
                # mark the black and white kings
                if chess_piece.get_piece() == find_bk:
                    black_king = chess_piece
                if chess_piece.get_piece() == find_wk:
                    white_king = chess_piece

    # scan through enemy pieces only, this means opposite color of the king

    black_king_x, black_king_y = black_king.get_position()
    black_king_moves = (black_king_x, black_king_y)
    white_king_x, white_king_y = white_king.get_position()
    white_king_moves = (white_king_x, white_king_y)

    # run for black king first
    for rows in chess_board:
        for chess_piece in rows:
            # scan for a non-empty chess piece and one that matches the prev player
            if chess_piece != ' ':
                if chess_piece.get_player() == 'white':
                    # found an enemy piece, now scan it's possible moves
                    get_moves = chess_piece.get_possible_moves()
                    if black_king_moves in get_moves:
                        black_king_check = True
                        break

    # run for white king second
    for rows in chess_board:
        for chess_piece in rows:
            # scan for a non-empty chess piece and one that matches the prev player
            if chess_piece != ' ':
                if chess_piece.get_player() == 'black':
                    # found an enemy piece, now scan it's possible moves
                    get_moves = chess_piece.get_possible_moves()
                    if white_king_moves in get_moves:
                        white_king_check = True
                        break

    # return True if check on king, or return false if not
    return black_king_check, white_king_check

# ---------- function to check if the player has accidentally checked themself ---------- #

def accidental_self_check(black_check, white_check, current_player):
    # this will return true if white makes a move to check himself
    if current_player == 'white' and white_check is True:
        return True
    # this will return true if black makes a move to check himself
    elif current_player == 'black' and black_check is True:
        return True
    # otherwise, this will return false
    return False

# ---------- function to check for active check on current player ---------- #

def active_check_lookup(player, black_check, white_check):
    # this function will use the end of move results to check if an opponent has created an active check

    current_player = player % 2

    if current_player == 0:
        if white_check is True:
            return True
    elif current_player == 1:
        if black_check is True:
            return True

    # return false if no active check
    return False

# ---------- activate legal_chess_board checks in movement function ---------- #

def run_legal_chess_board(legal_chess_board, selected_piece_x, selected_piece_y, new_x, new_y, current_player):

    legal_chess_board[new_x][new_y] = legal_chess_board[selected_piece_x][selected_piece_y]
    legal_chess_board[selected_piece_x][selected_piece_y] = ' '
    black_check, white_check = player_check_logic(legal_chess_board)

    if accidental_self_check(black_check, white_check, current_player) is False:
        return True

    return False