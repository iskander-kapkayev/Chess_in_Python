# we need to create a chess game
# we will need to do the following minimum things:
#       1) create a game board to keep track of pieces and movement
#       2) assign restriction to pieces (pawns, rooks, etc.)
#       3) allow each player to make one "legal" move
#       4) keep track of lost pieces as a player score
#       5) create a "check" and "checkmate" situation so that a player can win the game
#       6) once game ends, option to play again

class ChessPlayer:
    # set player color
    def __init__(self, player):
        self.player = player

class ChessPiece(ChessPlayer):
    def __init__(self, player, piece, position):
        self.piece = piece
        self.position = position
        super().__init__(player)

    # get the position of the piece
    def get_position(self):
        x, y = self.position
        return x, y

    # update the position of the piece if checks are complete
    def update_position(self, new_position):
        self.position = new_position

    # evaluate position of a chess piece based on given x, y
    def evaluate_position_of_piece(self, position_x, position_y):
        x, y = self.position
        if position_x == x and position_y == y:
            return True
        return False

    # function to check if piece belongs to player
    def player_check(self, player):
        if player % 2 == 0 and self.player == 'white':
            return True
        elif player % 2 == 1 and self.player == 'black':
            return True
        return False

    # so that only the piece name prints in the lists
    def __repr__(self):
        return self.piece


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

def initialize_chess_board(board_size):
    # create a 2D array to represent the board
    chess_board = [[' ' for i in range(board_size)] for k in range(board_size)]

    # initialize pieces on chess board
    all_game_pieces = initialize_pieces()
    for game_piece in all_game_pieces:
        x_coord, y_coord = game_piece.get_position()
        chess_board[x_coord][y_coord] = game_piece

    return chess_board

def legal_movement(chess_board, selected_piece_x, selected_piece_y, new_x, new_y):
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    enemy_piece = chess_board[new_x][new_y]

    # make sure that the new spot is not the old spot (clicking the same piece error)
    if current_piece == enemy_piece:
        return False

    # first check if the path is legal (aka move makes sense for selected piece)
    if legal_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y):

        # if movement is legal for a piece, now check for a piece in pathway of a piece

        # --------------- Pawn movements! ---------------
        if current_piece.piece == 'wP' or current_piece.piece == 'bP':
            # if the pawn moves 2 spaces
            if abs(selected_piece_x - new_x) == 2:
                # make sure nothing exists between new_x
                if current_piece.piece == 'wP':
                    # if white pawn, check space above it
                    if chess_board[selected_piece_x + 1][selected_piece_y] == ' ':
                        return True
                elif current_piece.piece == 'bP':
                    #  if black pawn, check space below it
                    if chess_board[selected_piece_x - 1][selected_piece_y] == ' ':
                        return True
            # else if the pawn moves one space (not a capture, capture is already legalized in legal_path function)
            elif abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 1:
                # make sure that space is available
                if enemy_piece == ' ':
                    return True

        # --------------- Rook movements! ---------------
        # check all spaces between rooks current spot and next spot
        elif current_piece.piece == 'wR' or current_piece.piece == 'bR':
            change_in_x = selected_piece_x - new_x
            change_in_y = selected_piece_y - new_y
            # check if rook is moving up/down or left/right
            if abs(change_in_x) == 0:
                # rook is moving left and right
                if change_in_y < 0:
                    # in case rook is moving 1 square
                    if change_in_y == -1:
                        change_in_y -= 1
                    for iterator in range(1, abs(change_in_y), 1):
                        if chess_board[selected_piece_x][selected_piece_y - iterator] != ' ':
                            # break loop and return false if a piece is found in the way!
                            return False
                        # else return true if no pieces found in the way
                        return True
                elif change_in_y > 0:
                    # in case rook is moving 1 square
                    if change_in_y == 1:
                        change_in_y += 1
                    for iterator in range(1, change_in_y, 1):
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
                        change_in_x -= 1
                    for iterator in range(1, abs(change_in_x), 1):
                        if chess_board[selected_piece_x - iterator][selected_piece_y] != ' ':
                            # break loop and return false if a piece is found in the way!
                            return False
                        # else return true if no pieces found in the way
                        return True
                elif change_in_x > 0:
                    # in case rook is moving 1 square
                    if change_in_x == 1:
                        change_in_x += 1
                    for iterator in range(1, change_in_x, 1):
                        if chess_board[selected_piece_x + iterator][selected_piece_y] != ' ':
                            # break loop and return false if a piece is found in the way!
                            return False
                        # else return true if no pieces found in the way
                        return True


        # --------------- Knight movements! ---------------
        # knights do not have blocked issues
        # this should return true always, unless your own piece is in the way
        elif current_piece.piece == 'wN' or current_piece.piece == 'bN':
            # if the space is empty
            if enemy_piece == ' ':
                return True
            # if the space is not empty, then it must have a different color piece
            elif enemy_piece.player != current_piece.player:
                return True


        # --------------- Bishop movements! ---------------
        # Bishops move along diagonals, with a +- 1 slope
        # Bishop's only restriction is a piece in the way
        elif current_piece.piece == 'wB' or current_piece.piece == 'bB':
            # since we know the path of the bishop is valid, then we can use the delta to check in between
            change_in_x = selected_piece_x - new_x
            change_in_y = selected_piece_y - new_y

            # both x and y decrease
            if change_in_x < 0 and change_in_y < 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y - iterator] != ' ':
                        return False
                    return True

            # only x decreases
            elif change_in_x < 0 < change_in_y:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y + iterator] != ' ':
                        return False
                    return True

            # only y decreases
            elif change_in_y < 0 < change_in_x:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y - iterator] != ' ':
                        return False
                    return True

            # both x and y increase
            elif change_in_x > 0 and change_in_y > 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y + iterator] != ' ':
                        return False
                    return True

        # --------------- Queen movements! ---------------
        # Queens need mad space between their movements
        elif current_piece.piece == 'wQ' or current_piece.piece == 'bQ':
            # if queen makes a rook movement type
            change_in_x = selected_piece_x - new_x
            change_in_y = selected_piece_y - new_y
            # check if queen is moving up/down or left/right
            if abs(change_in_x) == 0:
                # queen is moving left and right
                if change_in_y < 0:
                    # in case queen is moving 1 square
                    if change_in_y == -1:
                        change_in_y -= 1
                    for iterator in range(1, abs(change_in_y), 1):
                        if chess_board[selected_piece_x][selected_piece_y - iterator] != ' ':
                            # break loop and return false if a piece is found in the way!
                            return False
                        # else return true if no pieces found in the way
                        return True
                elif change_in_y > 0:
                    # in case queen is moving 1 square
                    if change_in_y == 1:
                        change_in_y += 1
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
                        change_in_x -= 1
                    for iterator in range(1, abs(change_in_x), 1):
                        if chess_board[selected_piece_x - iterator][selected_piece_y] != ' ':
                            # break loop and return false if a piece is found in the way!
                            return False
                        # else return true if no pieces found in the way
                        return True
                elif change_in_x > 0:
                    # in case queen is moving 1 square
                    if change_in_x == 1:
                        change_in_x += 1
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
                    return True

            # only x decreases
            elif change_in_x < 0 < change_in_y:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x - iterator][selected_piece_y + iterator] != ' ':
                        return False
                    return True

            # only y decreases
            elif change_in_y < 0 < change_in_x:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y - iterator] != ' ':
                        return False
                    return True

            # both x and y increase
            elif change_in_x > 0 and change_in_y > 0:
                for iterator in range(1, abs(change_in_x), 1):
                    if chess_board[selected_piece_x + iterator][selected_piece_y + iterator] != ' ':
                        return False
                    return True


        # --------------- King movements! ---------------
        # Kings can move any direction by 1 square
        # there must be no piece in his way, or he must capture an enemy piece
        elif current_piece.piece == 'wK' or current_piece.piece == 'bK':
            # if the space is empty
            if enemy_piece == ' ':
                return True
            # else if the space is taken, must be the other color piece
            elif enemy_piece.player != current_piece.player:
                return True

    # return false if nothing is triggered above
    return False

def legal_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y):
    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    enemy_piece = chess_board[new_x][new_y]


    # --------------- Pawn movements! ---------------
    # dependent on white or black because of movement restrictions
    if current_piece.piece == 'wP' or current_piece.piece == 'bP':
        if current_piece.piece == 'wP':
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
                # if the other player is different
                if enemy_piece != ' ':
                    if enemy_piece.player != current_piece.player:
                        # if the new position of the pawn is 1 row away
                        if selected_piece_x - new_x == 1:
                            # if the position of the pawn will be +-1 col
                            if abs(selected_piece_y - new_y) == 1:
                                return True

        elif current_piece.piece == 'bP':
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
                # if the other player is different
                if enemy_piece != ' ':
                    if enemy_piece.player != current_piece.player:
                        # if the new position of the pawn is 1 row away
                        if new_x - selected_piece_x == 1:
                            # if the position of the pawn will be +-1 col
                            if abs(new_y - selected_piece_y) == 1:
                                return True


    # --------------- Rook movements! ---------------
    # rooks can only move up/down left/right
    # this only says rooks legal move, does not check for a piece in the way
    elif current_piece.piece == 'wR' or current_piece.piece == 'bR':
        # check if blank or an enemy in the spot
        if enemy_piece == ' ' or (enemy_piece.player != current_piece.player):
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


    # --------------- Knight movements! ---------------
    # knights move in a L-shape, with a +- 2 or +- 0.5 slope, where abs(dx)+abs(dy) = 3
    # knight has no movement restrictions
    elif current_piece.piece == 'wN' or current_piece.piece == 'bN':
        # check if your own color piece is in the way, if it is, then not allowed
        if enemy_piece == ' ' or (enemy_piece.player != current_piece.player):
            # check for maximum change of 3 squares
            if abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 3:
                # if 3 square movement, then check slope for +-2 or = -0.5
                if abs(selected_piece_y - new_y) == 2 * abs(selected_piece_x - new_x) or abs(selected_piece_y - new_y) == 0.5 * abs(selected_piece_x - new_x):
                    return True


    # --------------- Bishop movements! ---------------
    # Bishops move along diagonals, with a +- 1 slope
    # Bishop's only restriction is a piece in the way
    elif current_piece.piece == 'wB' or current_piece.piece == 'bB':
        # check if your own color piece is in the new square, if it is, then not allowed
        if enemy_piece == ' ' or (enemy_piece.player != current_piece.player):
            # check for slope of +- 1
            if abs(selected_piece_y - new_y) == abs(selected_piece_x - new_x):
                return True


    # --------------- Queen movements! ---------------
    # Queens can move both like a Rook and like a bishop
    # Must apply same rules as above
    elif current_piece.piece == 'wQ' or current_piece.piece == 'bQ':
        if enemy_piece == ' ' or (enemy_piece.player != current_piece.player):
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


    # --------------- King movements! ---------------
    # Kings can move any direction by 1 square
    # there must be no piece in his way, or he must capture an enemy piece
    elif current_piece.piece == 'wK' or current_piece.piece == 'bK':
        if enemy_piece == ' ' or (enemy_piece.player != current_piece.player):
            # king is only allowed to move around radius
            if selected_piece_y == new_y:
                if abs(selected_piece_x - new_x) == 1:
                    return True
            elif selected_piece_x == new_x:
                if abs(selected_piece_y - new_y) == 1:
                    return True
            elif abs(selected_piece_x - new_x) + abs(selected_piece_y - new_y) == 2:
                return True

    # return false if none of the above legal moves are correct
    return False

def board_for_testing():
    # initialize game pieces and chess board
    board_size = 8
    chess_board = initialize_chess_board(board_size)
    return chess_board

def board_for_testing_scattered():
    # initialize game pieces and chess board with scattered pieces
    board_size = 8
    chess_board = initialize_chess_board_testing_scattered(board_size)
    return chess_board

def initialize_chess_board_testing_scattered(board_size):
    # create a 2D array to represent the board
    chess_board = [[' ' for i in range(board_size)] for k in range(board_size)]

    # initialize pieces on chess board
    all_game_pieces = initialize_pieces_testing_scattered()
    for game_piece in all_game_pieces:
        x, y = game_piece.get_position()
        chess_board[x][y] = game_piece

    return chess_board

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