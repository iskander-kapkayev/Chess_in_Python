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

def check_piece_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y):
    pass

def legal_path(chess_board, selected_piece_x, selected_piece_y, new_x, new_y):
    # select the current piece we are looking at, and the 'enemy' piece if exists
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    enemy_piece = chess_board[new_x][new_y]

    # pawn movements!
    if current_piece.piece == 'wP':
        # does the col change? if yes, then it means potential capture
        if selected_piece_y == new_y:
            # if pawn is in original spot
            if selected_piece_x == 6:
                # pawn can move one OR two squares
                if selected_piece_x - new_x == 1 or selected_piece_x - new_x == 2:
                    return True
            else:
                # pawn can move one square
                if selected_piece_x - new_x == 1:
                    return True
        elif selected_piece_y != new_y:
            # if the other player is black
            if enemy_piece.player != current_piece.player:
                # if the new position of the pawn is 1 row away
                if selected_piece_x - new_x == 1:
                    # if the position of the pawn will be +-1 col
                    if selected_piece_y - new_y == 1 or selected_piece_y - new_y == -1:
                        return True

    elif current_piece.piece == 'bP':
        # does the col change? if yes, then it means potential capture
        if selected_piece_y == new_y:
            # if pawn is in original spot
            if selected_piece_x == 1:
                # pawn can move one OR two squares
                if new_x - selected_piece_x == 1 or new_x - selected_piece_x == 2:
                    return True
            else:
                # pawn can move one square
                if new_x - selected_piece_x == 1:
                    return True
        elif selected_piece_y != new_y:
            # if the other player is black
            if enemy_piece.player != current_piece.player:
                # if the new position of the pawn is 1 row away
                if new_x - selected_piece_x == 1:
                    # if the position of the pawn will be +-1 col
                    if new_y - selected_piece_y == 1 or new_y - selected_piece_y == -1:
                        return True

    # Rook movements!
    # rooks can only move up/down left/right
    # this only says rooks legal move, does not check for a piece in the way
    if current_piece.piece == 'wR' or current_piece.piece == 'bR':
        # no enemy in new spot
        if enemy_piece == ' ':
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
        # potential enemy in new spot
        elif enemy_piece != ' ':
            # is the enemy piece opposite color?
            if enemy_piece.player != current_piece.player:
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
    
    return False

def board_for_testing():
    # initialize game pieces and chess board
    board_size = 8
    chess_board = initialize_chess_board(board_size)
    return chess_board