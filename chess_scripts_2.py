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

def legal_moves(piece, new_x, new_y, all_game_pieces):
    # this function will return True if move is allowed, False if not

    # start with pawn movement and pawn capture
    # check if this is a pawn
    old_x, old_y = piece.position
    if piece.piece == 'p':
        # check if pawn is in original spot
        if old_x == 1 and piece.player == 'white':
            if (new_x == 2 or new_x == 3) and new_y == old_y:
                return True
        elif old_x == 6 and piece.player == 'black':
            if (new_x == 5 or new_x == 4) and new_y == old_y:
                return True
        # if not in original spot, one directionality of pawns
        elif (new_x == old_x + 1 and piece.player == 'white' and new_y == old_y) or (new_x == old_x - 1 and piece.player == 'black' and new_y == old_y):
            # make sure nothing is in the way
            if check_for_piece(new_x, new_y, all_game_pieces) is None:
                return True
        # if you want to capture with a pawn
        # check if a piece is in capture position
        elif ((new_x == old_x + 1 and piece.player == 'white' and new_y == old_y + 1 and check_for_piece(new_x, new_y, all_game_pieces) is not None)
            or (new_x == old_x + 1 and piece.player == 'white' and new_y == old_y - 1 and check_for_piece(new_x, new_y, all_game_pieces) is not None)):
            return True
        elif ((new_x == old_x - 1 and piece.player == 'black' and new_y == old_y + 1 and check_for_piece(new_x, new_y, all_game_pieces) is not None)
            or (new_x == old_x - 1 and piece.player == 'black' and new_y == old_y + 1 and check_for_piece(new_x, new_y, all_game_pieces) is not None)):
            return True
        #eventually add en passant here
        return False
