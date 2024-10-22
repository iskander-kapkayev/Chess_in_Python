# first chess board attempt
def make_chess_board():
    # create blank chess board
    chess_board = []
    # set up pieces structure
    pawn_row_black = [ChessPiece('black', 'p', (6, i)) for i in range(8)]
    pawn_row_white = [ChessPiece('white', 'p', (1, i)) for i in range(8)]
    blank_row = [None for i in range(8)]
    back_row_white = [ChessPiece('white', 'r', (0, 0)),
                      ChessPiece('white', 'n', (0, 1)),
                      ChessPiece('white', 'b', (0, 2)),
                      ChessPiece('white', 'k', (0, 3)),
                      ChessPiece('white', 'q', (0, 4)),
                      ChessPiece('white', 'b', (0, 5)),
                      ChessPiece('white', 'n', (0, 6)),
                      ChessPiece('white', 'r', (0, 7))
    ]
    back_row_black = [ChessPiece('black', 'r', (7, 0)),
                      ChessPiece('black', 'n', (7, 1)),
                      ChessPiece('black', 'b', (7, 2)),
                      ChessPiece('black', 'k', (7, 3)),
                      ChessPiece('black', 'q', (7, 4)),
                      ChessPiece('black', 'b', (7, 5)),
                      ChessPiece('black', 'n', (7, 6)),
                      ChessPiece('black', 'r', (7, 7))
    ]
    # create a game board for the start of chess
    chess_board.append(back_row_white)
    chess_board.append(pawn_row_white)
    for num_rows in range(4):
        chess_board.append(blank_row)
    chess_board.append(pawn_row_black)
    chess_board.append(back_row_black)
    # return chess board
    return chess_board

import tkinter as tk
#from PIL import Image, ImageTk
# --- image fixes ---

def create_image_rectangle(canvas, x, y, width, height, image_path, color):
    # Open and resize the image
    #image = Image.open(image_path)
    #image = image.resize((width, height), Image.LANCZOS)
    #photo = ImageTk.PhotoImage(image)

    # Create the rectangle
    rect = canvas.create_rectangle(x, y, x + width, y + height, fill=color)

    # Add the image to the rectangle
    #canvas.create_image(x, y, anchor=tk.NW, image=photo)
    #canvas.photo = photo  # Keep reference to avoid garbage collection
    text_color = 'black'
    if color == 'black':
        text_color = 'white'
    canvas.create_text(x + width/2, y + width/2, text="P", fill=text_color, font=('Helvetica 30 bold'))


def make_chess_board_v3():
    # create a list of chess pieces

    pawn_row_black = [ChessPiece('black', 'p', (6, i)) for i in range(8)]
    pawn_row_white = [ChessPiece('white', 'p', (1, i)) for i in range(8)]
    back_row_white = [ChessPiece('white', 'r', (0, 0)),
                      ChessPiece('white', 'n', (0, 1)),
                      ChessPiece('white', 'b', (0, 2)),
                      ChessPiece('white', 'k', (0, 3)),
                      ChessPiece('white', 'q', (0, 4)),
                      ChessPiece('white', 'b', (0, 5)),
                      ChessPiece('white', 'n', (0, 6)),
                      ChessPiece('white', 'r', (0, 7))
    ]
    back_row_black = [ChessPiece('black', 'r', (7, 0)),
                      ChessPiece('black', 'n', (7, 1)),
                      ChessPiece('black', 'b', (7, 2)),
                      ChessPiece('black', 'k', (7, 3)),
                      ChessPiece('black', 'q', (7, 4)),
                      ChessPiece('black', 'b', (7, 5)),
                      ChessPiece('black', 'n', (7, 6)),
                      ChessPiece('black', 'r', (7, 7))
    ]

    all_game_pieces = pawn_row_black + pawn_row_white + back_row_black + back_row_white

    # --- constants --- (UPPER_CASE_NAMES)

    SIZE = 100

    # --- main --- (lower_case_names)

    root = tk.Tk()
    root.geometry('800x800')

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.pack()

    color = 'white'

    for y in range(8):

        for x in range(8):
            x1 = x * SIZE
            y1 = y * SIZE

            create_image_rectangle(canvas, x1, y1, SIZE, SIZE, './whitePawn.png', color)

            if color == 'white':
                color = 'black'
            else:
                color = 'white'

        if color == 'white':
            color = 'black'
        else:
            color = 'white'

    root.mainloop()

    # add units from chess pieces list to the chess board
    for piece in all_game_pieces:
        piece_x, piece_y = piece.position
        chess_board[piece_x][piece_y] = piece

    return all_game_pieces, chess_board

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

    # ---------- this will perform active check logic ---------- #

    def active_check_logic(chess_board, previous_move):
        # we need to figure out if a check is happening, or will happen for a king movement
        #   1) currently, after every move, we recreate the possible moves list for every piece
        #   2) we can scan through to determine if the possible move is indeed the king's square
        #   3) if king's square, then next player must move king
        #   4) this does not encapsulate revealing a check on yourself! (will do something else for that)

        # initiate some vars for processing check
        prev_player, prev_piece, prev_moved_from, prev_moved_to = previous_move
        active_check = False

        print(previous_move)
        print(prev_player)
        # identify the black and white king
        if prev_player == 'white':
            find = 'bK'
        elif prev_player == 'black':
            find = 'wK'

        print(find)
        print(chess_board)
        # find the current_king
        for rows in chess_board:
            print(rows)
            for chess_piece in rows:
                print(chess_piece)
                # non-empty chess piece
                if chess_piece != ' ':
                    # if prev player is white, find the black king to scan for attacks
                    if chess_piece.get_piece() == find:
                        current_king = chess_piece
                        print(chess_piece)
                        print(current_king)
                        break

        print(current_king)
        # scan through enemy pieces only, this means the previous player that moved is the enemy
        # prev_player is the enemy

        king_x, king_y = current_king.get_position()
        king_set = {(king_x, king_y)}

        for rows in chess_board:
            for chess_piece in rows:
                # scan for a non-empty chess piece and one that matches the prev player
                if chess_piece != ' ' and chess_piece.get_player() == prev_player:
                    # found an enemy piece, now scan it's possible moves
                    print(f'king set is: {king_set}')
                    piece_set = set(chess_piece.get_possible_moves())
                    print(f'piece set is: {piece_set}')
                    intersection = king_set.intersection(piece_set)
                    print(f'intersection set is: {intersection}')
                    if len(intersection) > 0:
                        active_check = True
                        break

        print(active_check)

        # return False if current player is not actively being checked
        # return True if current player has just been put into check

        return active_check, current_king.get_player()

    '''
                # if check, then must leave check no matter what
                elif active_check is True:
                    print('check has been reached')
                    alternate_chess_board = chess_board
                    # if selecting a piece
                    if selected_piece:
                        # make sure players go in order: W, B, W, B, etc.
                        if ((alternate_chess_board[selected_piece[0]][selected_piece[1]].get_player() == 'white' and player % 2 == 0)
                                or (alternate_chess_board[selected_piece[0]][
                                        selected_piece[1]].get_player() == 'black' and player % 2 == 1)):
                            # make sure a legal move is selected
                            if legal_movement(alternate_chess_board, selected_piece[0], selected_piece[1], row, col, previous_move, False):
                                # in case of a king's castle
                                if (((alternate_chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'wK')
                                     or (alternate_chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'bK'))
                                        and (abs(selected_piece[1] - col) == 2)):
                                    # perform king's castle
                                    alternate_chess_board = king_castle(alternate_chess_board, selected_piece[0], selected_piece[1], row, col)
                                    # perform end of move actions
                                    alternate_chess_board, previous_mov, black_king_check, white_king_check = end_of_move(alternate_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 3)
                                    # break the cycle if active check is now gone
                                    chess_board, player, selected_piece = cycle_breaker_check(alternate_chess_board, active_check, player)

                                # in case of an en passant by pawns
                                elif (((alternate_chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'bP')
                                       or (alternate_chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'wP'))
                                      and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                      and (alternate_chess_board[row][col] == ' ')):
                                    # perform end of move actions for en passant
                                    alternate_chess_board, previous_move, black_king_check, white_king_check = end_of_move(alternate_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 1)

                                    # break the cycle if active check is now gone
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)
                                    chess_board, player, selected_piece = cycle_breaker_check(alternate_chess_board, active_check, player)

                                # any other legal move
                                else:
                                    # perform end of move actions
                                    alternate_chess_board, previous_move, black_king_check, white_king_check = end_of_move(alternate_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 2)
                                    # break the cycle if active check is now gone
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)
                                    chess_board, player, selected_piece = cycle_breaker_check(alternate_chess_board, active_check, player)

                            else:
                                # if not a legal move, reset piece to none
                                selected_piece = None
                        else:
                            # if the player chooses the wrong color, reset piece to none
                            selected_piece = None

                    elif not selected_piece:
                        # this will select a piece if none have been selected
                        if chess_board[row][col] != ' ':
                            selected_piece = (row, col)
    '''

    # ---------- activate legal_chess_board checks in movement function ---------- #


def run_legal_chess_board(legal_chess_board, selected_piece_x, selected_piece_y, new_x, new_y, current_player):
    deep_fake = copy.deepcopy(legal_chess_board)

    deep_fake[new_x][new_y] = deep_fake[selected_piece_x][selected_piece_y]
    deep_fake[selected_piece_x][selected_piece_y] = ' '
    black_check, white_check = player_check_logic(deep_fake)

    if accidental_self_check(black_check, white_check, current_player) is False:
        return True

    return False


# ---------- this will perform the ending of moves when running the game ---------- #
'''
def end_of_move(chess_board, selected_piece_x, selected_piece_y, row, col, board_size, to_do):

    if to_do == 1:


    elif to_do == 2:


    elif to_do == 3:


    return chess_board, previous_move
'''

# ---------- This function evaluates check logic on a move  ---------- #
# if legal movement is allowed, then obtain check logic
# legal movement confirms that no pieces or blocks occur

def legal_conclusion(chess_board, selected_piece_x, selected_piece_y, new_x, new_y, previous):

    # deep copy of chess board
    a_chess_board = copy.deepcopy(chess_board)
    print(chess_board)

    # run legal movement, must return true to continue
    if legal_movement(chess_board, selected_piece_x, selected_piece_y, new_x, new_y, previous):

        print('\n-----1-----\n')
        print(chess_board)

        # now we can undergo check logic
        current_piece = chess_board[selected_piece_x][selected_piece_y]

        if current_piece.get_piece() == 'wK' or current_piece.get_piece() == 'bK':
            # include extra logic for king movement ability
            king_allowed_moves = current_piece.get_possible_moves()
            if (new_x, new_y) not in king_allowed_moves:
                return False

        current_player = current_piece.get_player()
        #legal_move = run_legal_chess_board(a_chess_board, selected_piece_x, selected_piece_y, new_x, new_y, current_player)
        # check that the legal move didn't activate check on the current player king

        # adjust the piece
        a_chess_board[new_x][new_y] = current_piece
        a_chess_board[selected_piece_x][selected_piece_y] = ' '

        print('\n-----2-----\n')
        print(a_chess_board)

        # find black/white king checks
        black_check, white_check = player_check_logic(a_chess_board)

        print('\n-----3-----\n')
        print(a_chess_board)

        if accidental_self_check(black_check, white_check, current_player) is False:
            return True

    # if not legal movement, then return false
    return False


# ---------- gui functions - assume previous move ---------- #

def assume_prev_move(board, selected_x, selected_y):
    # track previous move made
    previous_move = (board[selected_x][selected_y].get_player(),
                     board[selected_x][selected_y].get_piece(),
                     board[selected_x][selected_y].get_moved_from(),
                     board[selected_x][selected_y].get_moved_to()
                     )

    return previous_move


escape_mate = False
for rows in chess_board:
    for square in rows:
        if square != ' ':
            if square.get_player() != current_player:
                for move in square.get_possible_moves():
                    b_chess_board = copy.deepcopy(chess_board)
                    any_legal_move(b_chess_board, square.get_position()[0], square.get_position()[1], move[0], move[1])
                    previous_move = retain_prev_move(b_chess_board, move[0], move[1])
                    obtain_possible_moves(b_chess_board, previous_move)
                    black_king_check, white_king_check = player_check_logic(b_chess_board)
                    if accidental_self_check(black_king_check, white_king_check, square.get_player()) is False:
                        # this means that a move exists to get us out of check
                        escape_mate = True
if escape_mate is False:
    running = False