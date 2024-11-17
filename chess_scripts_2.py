# we need to create a chess game
# we will need to do the following things:
#       1) create a game board to keep track of pieces and movement
#       2) assign restriction to pieces (pawns, rooks, etc.)
#       3) allow each player to make one "legal" move
#       4) keep track of lost pieces as a player score
#       5) create a "check" and "checkmate" situation so that a player can win the game
#       6) once game ends, option to play again

import copy

# ---------- Chess Player class determines the color of the player ---------- #
class ChessPlayer:
    # set player color
    def __init__(self, player):
        self.player = player

# ---------- Chess Piece falls under the chess player parent class and defines piece attributes ---------- #
# piece = name of a piece
# position = current position
# moved_to = newest position
# moved_from = previous position
# possible_moves = possible legal positions
class ChessPiece(ChessPlayer):
    def __init__(self, player, piece, position, image_path):
        self.piece = piece
        self.position = position
        self.moved_to = None
        self.moved_from = position
        self.possible_moves = None
        self.image_path = image_path
        super().__init__(player)

    # get the position of the piece
    def get_position(self):
        x, y = self.position
        return x, y

    # get the image of the piece
    def get_image(self):
        return self.image_path

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
    pawn_row_black = [ChessPiece('black', 'bP', (1, i), 'pokemon_icons/bP.png') for i in range(8)]
    pawn_row_white = [ChessPiece('white', 'wP', (6, i), 'pokemon_icons/wP.png') for i in range(8)]
    back_row_white = [ChessPiece('white', 'wR', (7, 0), 'pokemon_icons/wR.png'),
                      ChessPiece('white', 'wN', (7, 1), 'pokemon_icons/wN.png'),
                      ChessPiece('white', 'wB', (7, 2), 'pokemon_icons/wB.png'),
                      ChessPiece('white', 'wQ', (7, 3), 'pokemon_icons/wQ.png'),
                      ChessPiece('white', 'wK', (7, 4), 'pokemon_icons/wK.png'),
                      ChessPiece('white', 'wB', (7, 5), 'pokemon_icons/wB.png'),
                      ChessPiece('white', 'wN', (7, 6), 'pokemon_icons/wN.png'),
                      ChessPiece('white', 'wR', (7, 7), 'pokemon_icons/wR.png')
    ]
    back_row_black = [ChessPiece('black', 'bR', (0, 0),'pokemon_icons/bR.png'),
                      ChessPiece('black', 'bN', (0, 1), 'pokemon_icons/bN.png'),
                      ChessPiece('black', 'bB', (0, 2), 'pokemon_icons/bB.png'),
                      ChessPiece('black', 'bQ', (0, 3),'pokemon_icons/bQ.png'),
                      ChessPiece('black', 'bK', (0, 4), 'pokemon_icons/bK.png'),
                      ChessPiece('black', 'bB', (0, 5), 'pokemon_icons/bB.png'),
                      ChessPiece('black', 'bN', (0, 6), 'pokemon_icons/bN.png'),
                      ChessPiece('black', 'bR', (0, 7), 'pokemon_icons/bR.png')
    ]

    all_game_pieces = pawn_row_black + pawn_row_white + back_row_black + back_row_white
    return all_game_pieces

# ---------- initialize starting chess board ---------- #

def initialize_chess_board(board_size):
    # create a 2D array to represent the board
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

    # initialize pieces on chess board
    all_game_pieces = initialize_pieces()
    for game_piece in all_game_pieces:
        x_coord, y_coord = game_piece.get_position()
        board[x_coord][y_coord] = game_piece

    return board

# ---------- This evaluates the legal movement of a piece - is there anything in the way? ---------- #
# this function calls on the legal path function before moving on
# legal movement confirms that no pieces or blocks occur

def legal_movement(board, selected_piece_x, selected_piece_y, new_x, new_y, previous):
    
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]

    # make sure that the new spot is not the old spot (clicking the same piece error), and not empty
    if current_piece == enemy_piece or current_piece == ' ':
        return False

    # first check if the path is legal (aka move makes sense for selected piece)
    if legal_path(board, selected_piece_x, selected_piece_y, new_x, new_y, previous):

        # if movement is legal for a piece, now check for a piece in the pathway of a piece

        # --------------- Pawn movements! --------------- #
        if 'P' in current_piece.get_piece():
            # all pawn movements legalized in legal path
            return True

        # --------------- Rook movements! --------------- #
        # check all spaces between rooks current spot and next spot
        elif 'R' in current_piece.get_piece():
            # check if rooks path is obstructed
            if rook_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):
                return True

        # --------------- Knight movements! --------------- #
        # knights do not have blocked issues
        # this should return true always, unless your own piece is in the way
        elif 'N' in current_piece.get_piece():
            # all knight movements legalized in legal path
            return True

        # --------------- Bishop movements! --------------- #
        # Bishops move along diagonals, with a +- 1 slope
        # Bishop's only restriction is a piece in the way
        elif 'B' in current_piece.get_piece():
            # check if bishops path is obstructed
            if bishop_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):
                return True

        # --------------- Queen movements! --------------- #
        # Queens need mad space between their movements
        elif 'Q' in current_piece.get_piece():
            # check if queens path is obstructed
            if queen_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):
                return True

        # --------------- King movements! --------------- #
        # Kings can move any direction by 1 square
        # there must be no piece in his way, or he must capture an enemy piece
        # check possible placements before allowing move
        elif 'K' in current_piece.get_piece():
            # all king moves have already been approved in legal path
            return True

    # return false if nothing is triggered above
    return False

# ---------- This defines the path for a pawn ---------- #

def pawn_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y, previous):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # --------------- Pawn movements! --------------- #
    # dependent on white or black because of movement restrictions

    # either pawn moves one square
    if abs(change_in_y) == 0 and abs(change_in_x) == 1 and enemy_piece == ' ':
        # prevent backward movement
        if current_piece.get_player() == 'white' and change_in_x == -1:
            return True
        if current_piece.get_player() == 'black' and change_in_x == 1:
            return True

    # either pawn moves 2 squares, check that piece is in original spot, and no piece blocking it
    elif abs(change_in_y) == 0 and abs(change_in_x) == 2 and enemy_piece == ' ':
        if current_piece.get_player() == 'white' and current_piece.moved() is False:
            if board[selected_piece_x - 1][selected_piece_y] == ' ' and change_in_x == -2:
                return True
        if current_piece.get_player() == 'black' and current_piece.moved() is False:
            if board[selected_piece_x + 1][selected_piece_y] == ' ' and change_in_x == 2:
                return True

    # either pawn captures a piece
    elif abs(change_in_y) == 1 and abs(change_in_x) == 1 and enemy_piece != ' ':
        # prevent backward movement
        if current_piece.get_player() == 'white' and enemy_piece.get_player() == 'black':
            if change_in_x == -1:
                return True
        if current_piece.get_player() == 'black' and enemy_piece.get_player() == 'white':
            if change_in_x == 1:
                return True

    # either pawn attempting an en passant
    elif abs(change_in_y) == 1 and abs(change_in_x) == 1 and enemy_piece == ' ' and previous is not None:

        # each condition must be met in order to allow for an en passant
        prev_color, prev_piece, prev_moved_from, prev_moved_to = previous
        prev_moved_from_x, prev_moved_from_y = prev_moved_from
        prev_moved_to_x, prev_moved_to_y = prev_moved_to

        if current_piece.get_piece() == 'wP':
            # player color must be different from previous player, previous moved piece is bP
            if prev_color != current_piece.get_player() and prev_piece == 'bP':
                # previous move was a black pawn that moved from original x to x+2
                if prev_moved_from_x == 1 and prev_moved_to_x == 3:
                    # if the pawn moved perfectly to the side of your pawn then you can capture as if no double movement
                    if new_x == prev_moved_to_x - 1 and new_y == prev_moved_to_y:
                        # en passant conditions are met
                        return True

        if current_piece.get_piece() == 'bP':
            # player color must be different from previous player, previous moved piece is bP
            if prev_color != current_piece.get_player() and prev_piece == 'wP':
                # previous move was a white pawn that moved from original x to x-2
                if prev_moved_from_x == 6 and prev_moved_to_x == 4:
                    # if the pawn moved perfectly to the side of your pawn then you can capture as if no double movement
                    if new_x == prev_moved_to_x + 1 and new_y == prev_moved_to_y:
                        # en passant conditions are met
                        return True

    # if no legal path is satisfied, return false
    return False

# ---------- This defines the path for a rook ---------- #

def rook_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]

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

    # if no legal path is satisfied, return false
    return False

# ---------- This defines the path for a knight ---------- #

def knight_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # check if your own color piece is in the way, if it is, then not allowed
    if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
        # check for maximum change of 3 squares
        if abs(change_in_x) + abs(change_in_y) == 3:
            # if 3 square movement, then check slope for +-2 or = -0.5
            if abs(change_in_y) == 2 * abs(change_in_x) or abs(change_in_y) == 0.5 * abs(change_in_x):
                # if the space is empty
                if enemy_piece == ' ':
                    return True
                # if the space is not empty, then it must have a different color piece
                elif enemy_piece.get_player() != current_piece.get_player():
                    return True

    # if no legal path is satisfied, return false
    return False

# ---------- This defines the path for a bishop ---------- #

def bishop_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # check if your own color piece is in the new square, if it is, then not allowed
    if enemy_piece == ' ' or (enemy_piece.get_player() != current_piece.get_player()):
        # check for slope of +- 1
        if abs(change_in_y) == abs(change_in_x):
            return True

    # if no legal path is satisfied, return false
    return False

# ---------- This defines the path for a queen ---------- #

def queen_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

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
        elif abs(change_in_y / change_in_x) == 1:
            return True

    # if no legal path is satisfied, return false
    return False

# ---------- This defines the path for a king ---------- #

def king_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):

    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    if (abs(change_in_x) == 0
        and abs(change_in_y) == 2
        and current_piece.moved() is False):

        # initiate alternative chess board to validate the movement for check logic
        king_chess_board = copy.deepcopy(board)
        current_player = current_piece.get_player()

        # is king moving left or right?
        if change_in_y > 0:
            # king is moving right
            if current_player == 'white' and board[7][7] != ' ' and board[7][7].get_piece() == 'wR':
                if board[7][7].moved() is False:
                    # white king and white rook, check all spaces between it and the rook
                    # check 7,5 and 7,6 for any pieces and for possible checks
                    if board[7][5] == ' ' and board[7][6] == ' ':
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
            if current_player == 'black' and board[0][7] != ' ' and board[0][7].get_piece() == 'bR':
                if board[0][7].moved() is False:
                    # white king and white rook, check all spaces between it and the rook
                    # check 0,5 and 0,6 for any pieces and possible checks
                    if board[0][5] == ' ' and board[0][6] == ' ':
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
            if current_player == 'white' and board[7][0] != ' ' and board[7][0].get_piece() == 'wR':
                if board[7][0].moved() is False:
                    # white king and white rook, check all spaces between it and the rook
                    # check 7,1 and 7,2 and 7,3 for any pieces
                    if board[7][1] == ' ' and board[7][2] == ' ' and board[7][3] == ' ':
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
            if current_player == 'black' and board[0][0] != ' ' and board[0][0].get_piece() == 'bR':
                if board[0][0].moved() is False:
                    # white king and white rook, check all spaces between it and the rook
                    # check 0,1 and 0,2 and 0,3 for any pieces
                    if board[0][1] == ' ' and board[0][2] == ' ' and board[0][3] == ' ':
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

    # if no legal path is satisfied, return false
    return False

# ---------- This checks path for a block on rook ---------- #

def rook_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):

    current_piece = board[selected_piece_x][selected_piece_y]
    enemy_piece = board[new_x][new_y]
    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # --------------- Rook movements! --------------- #
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
                    if board[selected_piece_x][selected_piece_y - iterator] != ' ':
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
                    if board[selected_piece_x][selected_piece_y + iterator] != ' ':
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
                    if board[selected_piece_x - iterator][selected_piece_y] != ' ':
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
                    if board[selected_piece_x + iterator][selected_piece_y] != ' ':
                        # break loop and return false if a piece is found in the way!
                        return False
                # else return true if no pieces found in the way
                return True

    # if no legal path is satisfied, return false
    return False

# ---------- This checks path for a block on bishop ---------- #

def bishop_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):

    change_in_x = new_x - selected_piece_x
    change_in_y = new_y - selected_piece_y

    # both x and y decrease
    if change_in_x < 0 and change_in_y < 0:
        for iterator in range(1, abs(change_in_x), 1):
            if board[selected_piece_x - iterator][selected_piece_y - iterator] != ' ':
                return False
        # else return true if no pieces found in the way
        return True
    # only x decreases
    elif change_in_x < 0 < change_in_y:
        for iterator in range(1, abs(change_in_x), 1):
            if board[selected_piece_x - iterator][selected_piece_y + iterator] != ' ':
                return False
        # else return true if no pieces found in the way
        return True

    # only y decreases
    elif change_in_y < 0 < change_in_x:
        for iterator in range(1, abs(change_in_x), 1):
            if board[selected_piece_x + iterator][selected_piece_y - iterator] != ' ':
                return False
        # else return true if no pieces found in the way
        return True

    # both x and y increase
    elif change_in_x > 0 and change_in_y > 0:
        for iterator in range(1, abs(change_in_x), 1):
            if board[selected_piece_x + iterator][selected_piece_y + iterator] != ' ':
                return False
        # else return true if no pieces found in the way
        return True

    # if no legal path is satisfied, return false
    return False

# ---------- This checks path for a block on queen ---------- #

def queen_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y):

    #check movements from bishop and rook
    if (bishop_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y)
        or rook_path_blocker(board, selected_piece_x, selected_piece_y, new_x, new_y)):
        return True

    # if no legal path is satisfied, return false
    return False

# ---------- This evaluates the legal path of a piece - where can a piece move? ---------- #
# this function should return true if a piece can make a move

def legal_path(board, selected_piece_x, selected_piece_y, new_x, new_y, previous):
    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = board[selected_piece_x][selected_piece_y]

    # --------------- Pawn movements! --------------- #
    if 'P' in current_piece.get_piece():
        if pawn_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y, previous):
            return True

    # --------------- Rook movements! --------------- #
    # rooks can only move up/down left/right
    # this only says rooks legal move, does not check for a piece in the way
    elif 'R' in current_piece.get_piece():
        if rook_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):
            return True

    # --------------- Knight movements! --------------- #
    # knights move in an L-shape, with a +- 2 or +- 0.5 slope, where abs(dx)+abs(dy) = 3
    # knight has no movement restrictions
    elif 'N' in current_piece.get_piece():
        if knight_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):
            return True

    # --------------- Bishop movements! --------------- #
    # Bishops move along diagonals, with a +- 1 slope
    # Bishop's only restriction is a piece in the way
    elif 'B' in current_piece.get_piece():
        if bishop_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):
            return True

    # --------------- Queen movements! --------------- #
    # Queens can move both like a Rook and like a bishop
    # Must apply same rules as above
    elif 'Q' in current_piece.get_piece():
        if queen_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):
            return True

    # --------------- King movements! --------------- #
    # Kings can move any direction by 1 square
    # there must be no piece in his way, or he must capture an enemy piece
    # we can cycle list of possible moves to make sure that he is not in the range of an enemy piece
    elif 'K' in current_piece.get_piece():
        if king_path_creator(board, selected_piece_x, selected_piece_y, new_x, new_y):
            return True

    # return false if none of the above legal moves are correct
    return False

# ---------- this will apply a castle ---------- #

def king_castle(board, selected_piece_x, selected_piece_y, new_row, new_col):

    # initiate current piece and change in y vars
    current_piece = board[selected_piece_x][selected_piece_y]
    change_in_y = new_col - selected_piece_y

    # if change in y is negative
    if change_in_y < 0:
        # move king to castle position and remove old king piece
        board[new_row][new_col] = current_piece
        board[selected_piece_x][selected_piece_y] = ' '
        # update chess piece class
        board[new_row][new_col].update_moved_to((new_row, new_col))
        board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            board[new_row][new_col + 1] = board[7][0]
            board[7][0] = ' '
            # update chess piece class
            board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            board[new_row][new_col + 1].update_moved_from((7, 0))
        elif current_piece.piece == 'bK':
            board[new_row][new_col + 1] = board[0][0]
            board[0][0] = ' '
            # update chess piece class
            board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            board[new_row][new_col + 1].update_moved_from((0, 0))
    elif change_in_y > 0:
        # move king to castle position and remove old king piece
        board[new_row][new_col] = current_piece
        board[selected_piece_x][selected_piece_y] = ' '
        # update chess piece class
        board[new_row][new_col].update_moved_to((new_row, new_col))
        board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            board[new_row][new_col - 1] = board[7][7]
            board[7][7] = ' '
            # update chess piece class
            board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            board[new_row][new_col - 1].update_moved_from((7, 7))
        elif current_piece.piece == 'bK':
            board[new_row][new_col - 1] = board[0][7]
            board[0][7] = ' '
            # update chess piece class
            board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            board[new_row][new_col - 1].update_moved_from((0, 7))


# ---------- this will perform player check logic ---------- #

def player_check_logic(board):
    # I will look to see if the black king or white king is being checked
    # will return both statuses of the black/white king

    # initiate some vars for processing check
    black_king_check = False
    white_king_check = False
    black_king = None
    white_king = None

    # identify the black and white king
    find_bk = 'bK'
    find_wk = 'wK'

    # find the kings
    for rows in board:
        for chess_piece in rows:
            # non-empty chess piece
            if chess_piece != ' ':
                # mark the black and white kings
                if chess_piece.get_piece() == find_bk:
                    black_king = chess_piece
                if chess_piece.get_piece() == find_wk:
                    white_king = chess_piece

    # scan through enemy pieces only, this means opposite color of the king

    black_king_position = black_king.get_position()
    white_king_position = white_king.get_position()

    # run for black king first
    for rows in board:
        for chess_piece in rows:

            # scan for a non-empty chess piece and one that matches other player
            if chess_piece != ' ' and chess_piece.get_player() == 'white':

                # found an enemy piece, now scan it's possible moves
                get_moves = chess_piece.get_possible_moves()
                if black_king_position in get_moves:
                    black_king_check = True

            # scan for a non-empty chess piece and one that matches other player
            elif chess_piece != ' ' and chess_piece.get_player() == 'black':

                # found an enemy piece, now scan it's possible moves
                get_moves = chess_piece.get_possible_moves()
                if white_king_position in get_moves:
                    white_king_check = True

    # return True if checks on king, or return false if not
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
    else:
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

# ---------- gui functions - function to count possible moves ---------- #

def count_moves(board, player):
    # set current_player to remove reference before assignment problem
    current_player = None

    # identify current player
    if player % 2 == 0:
        current_player = 'white'
    elif player % 2 == 1:
        current_player = 'black'

    # counter
    move_counter = 0

    # scan all moves for the current player
    for rows in board:
        for chess_piece in rows:
            # scan for a non-empty chess piece and one that matches the current player
            if chess_piece != ' ':
                if chess_piece.get_player() == current_player:
                    # found an enemy piece, now scan it's possible moves
                    get_moves = chess_piece.get_possible_moves()
                    move_counter += len(get_moves)

    return move_counter


# ---------- gui functions - perform an en passant ---------- #

def en_passant(board, selected_x, selected_y, new_x, new_y):
    # perform en passant
    board[new_x][new_y] = board[selected_x][selected_y]
    board[selected_x][selected_y] = ' '

    # capture the pawn by en passant
    if board[new_x][new_y].get_piece() == 'bP':
        # if black, pawn to capture is above it
        board[new_x - 1][new_y] = ' '
    elif board[new_x][new_y].get_piece() == 'wP':
        # if white, pawn to capture is below it
        board[new_x + 1][new_y] = ' '

    # update the moved_to and moved_from positions in the chess piece class
    board[new_x][new_y].update_moved_to((new_x, new_y))
    board[new_x][new_y].update_moved_from((selected_x, selected_y))


# ---------- gui functions - perform an en passant ---------- #

def pawn_promotion(current_piece, current_player, new_x, new_y):
    if current_piece == 'wP' and current_player == 'white':
        for i in range(8):
            if (new_x, new_y) == (0, i):
                # pawn has reached promotion!
                return True

    elif current_piece == 'bP' and current_player == 'black':
        for i in range(8):
            if (new_x, new_y) == (7, i):
                # pawn has reached promotion!
                return True

    return False


# ---------- gui functions - perform any legal movement ---------- #

def any_legal_move(board, selected_x, selected_y, new_x, new_y):
    # this means a regular legal move was done
    board[new_x][new_y] = board[selected_x][selected_y]

    # remove the selected piece from the old spot
    board[selected_x][selected_y] = ' '

    # update the moved_to and moved_from positions in the chess piece class
    board[new_x][new_y].update_moved_to((new_x, new_y))
    board[new_x][new_y].update_moved_from((selected_x, selected_y))

    current_piece = board[new_x][new_y].get_piece()
    current_player = board[new_x][new_y].get_player()
    # if legal move is made and pawn promotion is allowed
    if pawn_promotion(current_piece, current_player, new_x, new_y):

        # if true, then promote pawn to queen
        if current_player == 'black':
            board[new_x][new_y] = ChessPiece('black', 'bQ', (new_x, new_y), 'pokemon_icons/bQ.png')

        elif current_player == 'white':
            board[new_x][new_y] = ChessPiece('white', 'wQ', (new_x, new_y), 'pokemon_icons/wQ.png')

        # perform same end of move changes
        board[new_x][new_y].update_moved_to((new_x, new_y))
        board[new_x][new_y].update_moved_from((selected_x, selected_y))


# ---------- gui functions - retain previous move ---------- #

def retain_prev_move(board, new_x, new_y):
    # track previous move made
    previous_move = (board[new_x][new_y].get_player(),
                     board[new_x][new_y].get_piece(),
                     board[new_x][new_y].get_moved_from(),
                     board[new_x][new_y].get_moved_to()
                     )

    return previous_move


# ---------- gui functions - check castle check positions ---------- #

def castle_movement_v2(board, selected_piece_x, selected_piece_y, new_x, new_y):
    first_board = copy.deepcopy(board)
    second_board = copy.deepcopy(board)
    current_player = board[selected_piece_x][selected_piece_y].get_player()

    # only need to check the spaces between the selected and new
    change_in_y = new_y - selected_piece_y

    if change_in_y > 0:
        first_board[selected_piece_x][selected_piece_y + 1] = first_board[selected_piece_x][selected_piece_y]
        first_board[selected_piece_x][selected_piece_y] = ' '

        print(f'this is the 1st chess board castle check: {first_board}')

        black_king_check, white_king_check = player_check_logic(first_board)

        if current_player == 'white' and white_king_check:
            return False
        elif current_player == 'black' and black_king_check:
            return False

        second_board[selected_piece_x][selected_piece_y + 2] = second_board[selected_piece_x][selected_piece_y]
        second_board[selected_piece_x][selected_piece_y] = ' '

        print(f'this is the 2nd chess board castle check: {second_board}')

        black_king_check, white_king_check = player_check_logic(second_board)

        if current_player == 'white' and white_king_check:
            return False
        elif current_player == 'black' and black_king_check:
            return False

        return True

    elif change_in_y < 0:
        first_board[selected_piece_x][selected_piece_y - 1] = first_board[selected_piece_x][selected_piece_y]
        first_board[selected_piece_x][selected_piece_y] = ' '

        print(f'this is the 1st chess board castle check: {first_board}')

        black_king_check, white_king_check = player_check_logic(first_board)

        if current_player == 'white' and white_king_check:
            return False
        elif current_player == 'black' and black_king_check:
            return False

        second_board[selected_piece_x][selected_piece_y - 2] = second_board[selected_piece_x][selected_piece_y]
        second_board[selected_piece_x][selected_piece_y] = ' '

        print(f'this is the 1st chess board castle check: {second_board}')

        black_king_check, white_king_check = player_check_logic(second_board)

        if current_player == 'white' and white_king_check:
            return False
        elif current_player == 'black' and black_king_check:
            return False

        return True


# ---------- this will obtain the possible moves values for each piece after a move is completed  ---------- #

def obtain_possible_moves_v2(board, previous):
    # this function will cycle through every piece on the chess board
    # a blank list of possible moves will be created and then passed into ChessPiece class with update_possible_moves(list)

    # this is a chess board size
    board_size = 8

    # assign some vars before processing
    black_king = None
    white_king = None

    # find the kings and start assigning moves
    for rows in board:
        for square in rows:

            # if a piece is in the square
            if square != ' ':

                # assign white and black king
                if square.get_piece() == 'wK':
                    white_king = square
                if square.get_piece() == 'bK':
                    black_king = square

                # empty list for moves
                list_of_moves = []

                # set current piece
                current_piece_x, current_piece_y = square.get_position()

                # run through every combo of (0,0) to (7,7) to calculate available moves
                for row in range(board_size):
                    for col in range(board_size):

                        if legal_movement(board, current_piece_x, current_piece_y, row, col, previous):
                            list_of_moves.append((row, col))

                # after looping through the board, set list to chess_piece value
                square.update_possible_moves(list_of_moves)

    # last check, with above check moves removed
    # check to make sure king's possible moves do not intersect with enemy
    # get white/black king moves
    black_king_moves = black_king.get_possible_moves()
    white_king_moves = white_king.get_possible_moves()

    # assess moves for black king
    for rows in board:
        for square in rows:
            if square != ' ':
                if square.get_player() == 'white':
                    for move in black_king_moves:
                        if move in square.get_possible_moves():
                            black_king_moves.remove(move)

    # assess moves for white king
    for rows in board:
        for square in rows:
            if square != ' ':
                if square.get_player() == 'black':
                    for move in white_king_moves:
                        if move in square.get_possible_moves():
                            white_king_moves.remove(move)

    # update king moves!
    black_x, black_y = black_king.get_position()
    white_x, white_y = white_king.get_position()
    board[black_x][black_y].update_possible_moves(black_king_moves)
    board[white_x][white_y].update_possible_moves(white_king_moves)

    # now that every piece has assigned moves
    # check the player check logic on a move
    # function player_check_logic only checks to see if our king is in check

    # now we check if either player is in check
    black_king_check, white_king_check = player_check_logic(board)

    # black king in check!
    if black_king_check is True:
        black_x, black_y = black_king.get_position()

        # only way to escape check is 1) block it, 2) capture the checker, 3) move king
        block_path = one_block_check_moves(board, 'black')
        check_pieces = two_evaluate_checker(board, 'black')
        escape_plan = three_king_escape(board, 'black', check_pieces)

        # returns true if only one enemy in check_pieces is checking
        capture_enemy = four_capture_enemies(check_pieces)

        # scan through possible moves that check for:
        # 1) can block the path if block_path exists
        # 2) can capture enemy piece unless there are more than 1 piece

        enemy_check_piece = check_pieces[0]
        enemy_position = enemy_check_piece.get_position()

        for rows in board:
            for square in rows:
                if square != ' ' and square.get_player() == 'black':
                    mover = []
                    for move in square.get_possible_moves():
                        # check if piece can block, or can be captured
                        if move in block_path or (capture_enemy and move == enemy_position):
                            mover.append(move)

                    # update list of moves
                    square_x, square_y = square.get_position()
                    board[square_x][square_y].update_possible_moves(mover)

        # for escape plan, king should be adjusted (if king is allowed any moves or not)
        # three_king_escape returns the kings set of possible moves
        board[black_x][black_y].update_possible_moves(escape_plan)

        # white king in check!
    elif white_king_check is True:
        white_x, white_y = white_king.get_position()

        # only way to escape check is 1) block it, 2) capture the checker, 3) move king
        block_path = one_block_check_moves(board, 'white')
        check_pieces = two_evaluate_checker(board, 'white')
        escape_plan = three_king_escape(board, 'white', check_pieces)

        # returns true if only one enemy in check_pieces is checking
        capture_enemy = four_capture_enemies(check_pieces)

        # scan through possible moves that check for:
        # 1) can block the path if block_path exists
        # 2) can capture enemy piece unless there are more than 1 piece

        enemy_check_piece = check_pieces[0]

        for rows in board:
            for square in rows:
                if square != ' ' and square.get_player() == 'white':
                    mover = []
                    for move in square.get_possible_moves():
                        if move in block_path or (capture_enemy and move in enemy_check_piece.get_position()):
                            mover.append(move)

                    # update list of moves
                    square_x, square_y = square.get_position()
                    board[square_x][square_y].update_possible_moves(mover)

        # for escape plan, king should be adjusted (if king is allowed any moves or not)
        # three_king_escape returns the kings set of possible moves
        board[white_x][white_y].update_possible_moves(escape_plan)


# ---------- function to get legal moves to block a check ---------- #

def one_block_check_moves(board, checked_player):
    king = None

    # can the king escape this check?
    for rows in board:
        for square in rows:
            if square != ' ':
                if checked_player == 'white' and square.get_piece() == 'wK':
                    king = square
                elif checked_player == 'black' and square.get_piece() == 'bK':
                    king = square

    # find the piece causing a check on the K
    for rows in board:
        for square in rows:
            if square != ' ':
                if king.get_position() in square.get_possible_moves():
                    # this piece is checking the king
                    enemy_to = square.get_moved_to()
                    enemy = square

    # previous move not necessarily causing check
    # cycle and check for an enemy piece that intersects king's position

    # discover the path between the K and the previous piece
    king_x, king_y = king.get_position()
    enemy_x, enemy_y = enemy_to
    change_in_x = enemy_x - king_x
    change_in_y = enemy_y - king_y
    path = []

    if 'N' in enemy.get_piece():
        # then you cannot block a path
        return path

    if change_in_y == 0:
        # up
        if change_in_x < 0:
            for i in range(-1, change_in_x, -1):
                path.append((king_x + i, king_y))
        # down
        elif change_in_x > 0:
            for i in range(1, change_in_x, 1):
                path.append((king_x + i, king_y))

    elif change_in_x == 0:
        # left
        if change_in_y < 0:
            for i in range(-1, change_in_y, -1):
                path.append((king_x, king_y + i))
        # right
        elif change_in_y > 0:
            for i in range(1, change_in_y, 1):
                path.append((king_x, king_y + i))

    elif abs(change_in_y) == abs(change_in_x):
        # diagonal movements
        if change_in_x < 0 and change_in_y < 0:
            for i in range(1, abs(change_in_x), 1):
                path.append((king_x - i, king_y - i))

        # only x decreases
        elif change_in_x < 0 < change_in_y:
            for i in range(1, abs(change_in_x), 1):
                path.append((king_x - i, king_y + i))

        # only y decreases
        elif change_in_y < 0 < change_in_x:
            for i in range(1, abs(change_in_x), 1):
                path.append((king_x + i, king_y - i))

        # both x and y increase
        elif change_in_x > 0 and change_in_y > 0:
            for i in range(1, abs(change_in_x), 1):
                path.append((king_x + i, king_y + i))

    # we now have a path of moves to check for blocking check
    return path


# ---------- function to figure out which pieces are checking the king ---------- #

def two_evaluate_checker(board, checked_player):
    king = None
    check_pieces = []

    # using checked_player, find checked king
    for rows in board:
        for square in rows:
            if square != ' ' and square.get_player() == checked_player:
                if 'K' in square.get_piece():
                    king = square

    # now we have our checked king
    # look for pieces checking the king
    for rows in board:
        for square in rows:
            if square != ' ' and square.get_player() != checked_player:
                if king.get_position() in square.get_possible_moves():
                    # then add this piece to current checkers
                    check_pieces.append(square)

    return check_pieces


# ---------- function to figure out if the king can escape check ---------- #

def three_king_escape(board, checked_player, check_pieces):
    king = None

    # using checked_player, find checked king
    for rows in board:
        for square in rows:
            if square != ' ' and square.get_player() == checked_player:
                if 'K' in square.get_piece():
                    king = square

    # cycle through every piece and see if you can add the current check piece position to the opponents move
    checked_x, checked_y = check_pieces[0].get_position()
    hold_piece = board[checked_x][checked_y]
    board[checked_x][checked_y] = ' '
    for rows in board:
        for square in rows:
            if square != ' ' and square.get_player() != checked_player:
                square_x, square_y = square.get_position()
                if legal_movement(board, square_x, square_y, checked_x, checked_y, None):
                    # if the current checked position is being protected by another piece, add it to their list of moves
                    board[square_x][square_y].possible_moves.append((checked_x, checked_y))

    # return held piece back to its spot
    board[checked_x][checked_y] = hold_piece

    king_moves = king.get_possible_moves()
    bad_moves = []
    for move in king_moves:
        for rows in board:
            for square in rows:
                if square != ' ':
                    if checked_player != square.get_player():
                        if move in square.get_possible_moves():
                            bad_moves.append(move)

    # escape plan will hold all moves that are in the king moves that are not bad moves
    escape_plan = []
    for move in king_moves:
        if move not in bad_moves:
            escape_plan.append(move)

    # now undo the extra moves we added to the opponent
    for rows in board:
        for square in rows:
            if square != ' ' and square.get_player() != checked_player:
                square_x, square_y = square.get_position()
                if (checked_x, checked_y) in square.get_possible_moves():
                    board[square_x][square_y].possible_moves.remove((checked_x, checked_y))

    return escape_plan

# ---------- function to figure out if the checking piece can be captured ---------- #

def four_capture_enemies(check_pieces):

    # check if check_pieces is only one piece
    if len(check_pieces) > 1:
        return False
    elif len(check_pieces) == 1:
        return True

# ---------- gui function - end of moves - castle ---------- #

def end_castle(chess_board, select_x, select_y, row, col, current_player):
    # set check everything chessboard
    a_chess_board = copy.deepcopy(chess_board)

    if castle_movement_v2(chess_board, select_x, select_y, row, col):

        # perform king's castle, obtain new possible moves, obtain check values
        king_castle(a_chess_board, select_x, select_y, row, col)
        previous_move = retain_prev_move(a_chess_board, row, col)
        obtain_possible_moves_v2(a_chess_board, previous_move)
        black_king_check, white_king_check = player_check_logic(a_chess_board)

        if accidental_self_check(black_king_check, white_king_check, current_player) is False:
            # perform on actual board!
            king_castle(chess_board, select_x, select_y, row, col)

            # track previous move made
            previous_move = retain_prev_move(chess_board, row, col)

            # update possible moves list because change has occurred
            obtain_possible_moves_v2(chess_board, previous_move)

            return True

    return False


# ---------- gui function - end of moves - castle ---------- #

def end_en_passant(chess_board, select_x, select_y, row, col, current_player):
    # set check everything chessboard
    a_chess_board = copy.deepcopy(chess_board)

    # perform king's castle, obtain new possible moves, obtain check values
    en_passant(a_chess_board, select_x, select_y, row, col)
    previous_move = retain_prev_move(a_chess_board, row, col)
    obtain_possible_moves_v2(a_chess_board, previous_move)
    black_king_check, white_king_check = player_check_logic(a_chess_board)

    if accidental_self_check(black_king_check, white_king_check, current_player) is False:
        # perform on actual board!
        en_passant(chess_board, select_x, select_y, row, col)

        # track previous move made
        previous_move = retain_prev_move(chess_board, row, col)

        # update possible moves list because change has occurred
        obtain_possible_moves_v2(chess_board, previous_move)

        return True

    return False


# ---------- gui function - end of moves - castle ---------- #

def end_any_move(chess_board, select_x, select_y, row, col, current_player):
    # set check everything chessboard
    a_chess_board = copy.deepcopy(chess_board)

    # perform king's castle, obtain new possible moves, obtain check values
    any_legal_move(a_chess_board, select_x, select_y, row, col)
    previous_move = retain_prev_move(a_chess_board, row, col)
    obtain_possible_moves_v2(a_chess_board, previous_move)
    black_king_check, white_king_check = player_check_logic(a_chess_board)

    if accidental_self_check(black_king_check, white_king_check, current_player) is False:
        # perform on actual board!
        any_legal_move(chess_board, select_x, select_y, row, col)

        # track previous move made
        previous_move = retain_prev_move(chess_board, row, col)

        # update possible moves list because change has occurred
        obtain_possible_moves_v2(chess_board, previous_move)

        return True

    return False

# ---------- gui function - evaluate move to perform action! ---------- #

def evaluate_action(chess_board, selected_piece_x, selected_piece_y, row, col, previous_move):

    # set current piece and current player
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    current_player = current_piece.get_player()
    
    # in case of a king's castle
    if ('K' in current_piece.get_piece()
        and abs(selected_piece_y - col) == 2):

        # double check king movement logic to not pass through a check
        if end_castle(chess_board, selected_piece_x, selected_piece_y, row, col, current_player):
            return True

    # in case of an en passant by pawns
    elif (('P' in current_piece.get_piece() and previous_move is not None)
          and ('P' in prev_piece)
          and (chess_board[row][col] == ' ')):

        # perform en passant, obtain new possible moves, obtain check values
        if end_en_passant(chess_board, selected_piece_x, selected_piece_y, row, col, current_player):
            return True

    else:
        # perform any legal move, obtain new possible moves, obtain check values
        if end_any_move(chess_board, selected_piece_x, selected_piece_y, row, col, current_player):
            return True

    return False

# ---------- gui function - perform final actions! ---------- #

def perform_action_ending(chess_board, selected_piece_x, selected_piece_y, row, col, player):

    # set current piece and current player
    current_piece = chess_board[row][col]
    current_player = current_piece.get_player()

    # track previous move made
    previous_move = retain_prev_move(chess_board, row, col)
    prev_color, prev_piece, prev_moved_from, prev_moved_to = previous_move

    # iterate to next player
    player += 1

    # update checks for black/white
    black_king_check, white_king_check = player_check_logic(chess_board)

    # update active_check, should return true if the new iterated player is in check
    active_check = active_check_lookup(player, black_king_check, white_king_check)

    # print to console
    print(f'{current_player} just played his {current_piece.get_piece()} '
          f'from {(selected_piece_x, selected_piece_y)} to {(row, col)}')

    # reset piece
    selected_piece = None

    return prev_color, prev_piece, prev_moved_from, prev_moved_to, player, black_king_check, white_king_check, active_check, selected_piece