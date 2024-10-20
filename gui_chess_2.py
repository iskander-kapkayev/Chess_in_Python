import pygame
from chess_scripts_2 import *

# ---------- this will draw the board ---------- #

def draw_board():
    for chess_row in range(board_size):
        for chess_col in range(board_size):
            color = white if (chess_row + chess_col) % 2 == 0 else mimi_pink
            pygame.draw.rect(screen, color, (chess_col * square_size, chess_row * square_size, square_size, square_size))

            # add pieces from chess board
            chess_piece = chess_board[chess_row][chess_col]

            if chess_piece != ' ':
                # instead of displaying the text name of the piece below (uncomment for text)
                '''
                font = pygame.font.Font(None, 50)
                text = font.render(chess_piece.get_piece(), True, black if color == white else white)
                text_rect = text.get_rect(center=((chess_col + 0.5) * square_size, (chess_row + 0.5) * square_size))
                screen.blit(text, text_rect)
                '''
                # display the image of a piece!
                piece_image = pygame.image.load(chess_piece.get_image())
                image_rect = piece_image.get_rect(center=((chess_col + 0.5) * square_size, (chess_row + 0.5) * square_size))
                screen.blit(piece_image, image_rect)

# ---------- this will initialize the pygame ---------- #
pygame.init()
pygame.display.set_caption('Iskander\'s Chess-u~!')

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# colors for game board and font
black = (0, 0, 0)
white = (255, 255, 255)
green = (170, 196, 172)
green_alt = "#AAC4AC"
mimi_pink = '#EDCDE3'
pink_lavender = '#D0A6B4'

# size of board and chess squares
board_size = 8 # num of squares
square_size = 100 # pixel size

# initialize game pieces and chess board
chess_board = initialize_chess_board(board_size)
obtain_possible_moves(chess_board, None)

# ---------- game loop that will keep working until game ends ---------- #

previous_move = None # previous move will be a tuple of player color, player piece and player placement
running = True # this tells the game to keep running
selected_piece = None # this will represent the X, Y coordinate of the selected piece
player = 0 # mod 2 will return 0 or 1, player white or black
active_check = False # tells the game to focus on a player

while running:
    for event in pygame.event.get():

        # alternative chess board used for evaluating an in check position
        a_chess_board = None

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // square_size
            col = x // square_size

            # when not in check, play the game normally
            if not active_check:

                # when piece is selected
                if selected_piece:

                    # set check everything chessboard
                    a_chess_board = copy.deepcopy(chess_board)

                    # set current piece for ease
                    current_piece = chess_board[selected_piece[0]][selected_piece[1]]

                    # set current player for ease
                    current_player = current_piece.get_player()

                    # make sure players go in order: W, B, W, B, etc.
                    if((current_player == 'white' and player % 2 == 0)
                            or (current_player == 'black' and player % 2 == 1)):

                        # make sure a legal move is selected from possible moves list
                        if (row, col) in current_piece.get_possible_moves():

                            # in case of a king's castle
                            if (((current_piece.get_piece() == 'wK')
                                 or (current_piece.get_piece() == 'bK'))
                                    and (abs(selected_piece[1] - col) == 2)):

                                # double check king movement logic to not pass through a check
                                if castle_movement_v2(a_chess_board, selected_piece[0], selected_piece[1], row, col):

                                    # perform king's castle, obtain new possible moves, obtain check values
                                    king_castle(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                    previous_move = assume_prev_move(a_chess_board, row, col)
                                    obtain_possible_moves(a_chess_board, previous_move)
                                    black_king_check, white_king_check = player_check_logic(a_chess_board)

                                    if accidental_self_check(black_king_check, white_king_check, current_player) is False:

                                        # perform on actual board!
                                        king_castle(chess_board, selected_piece[0], selected_piece[1], row, col)

                                        # track previous move made
                                        previous_move = retain_prev_move(chess_board, row, col)

                                        # update possible moves list because change has occurred
                                        obtain_possible_moves(chess_board, previous_move)

                                        # iterate to next player
                                        player += 1

                                        # update active_check, should return true if the new iterated player is in check
                                        active_check = active_check_lookup(player, black_king_check, white_king_check)

                                        # print to console
                                        print(f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                        # reset piece
                                        selected_piece = None

                                else:
                                    # not legal castle
                                    selected_piece = None

                            # in case of an en passant by pawns
                            elif (((current_piece.get_piece() == 'bP')
                                   or (current_piece.get_piece() == 'wP'))
                                  and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                  and (chess_board[row][col] == ' ')):

                                # perform en passant, obtain new possible moves, obtain check values
                                # perform en passant on fake board
                                en_passant(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move = assume_prev_move(a_chess_board, row, col)
                                obtain_possible_moves(a_chess_board, previous_move)
                                black_king_check, white_king_check = player_check_logic(a_chess_board)

                                if accidental_self_check(black_king_check, white_king_check, current_player) is False:

                                    # this means en passant on actual board!
                                    en_passant(chess_board, selected_piece[0], selected_piece[1], row, col)

                                    # track previous move made
                                    previous_move = retain_prev_move(chess_board, row, col)

                                    # update possible moves list because change has occurred
                                    obtain_possible_moves(chess_board, previous_move)

                                    # iterate to next player
                                    player += 1

                                    # update active_check, should return true if the new iterated player is in check
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)

                                    # print to console
                                    print(f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                    # reset piece
                                    selected_piece = None

                            else:

                                # perform any legal move, obtain new possible moves, obtain check values
                                any_legal_move(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move = assume_prev_move(a_chess_board, row, col)
                                obtain_possible_moves(a_chess_board, previous_move)
                                black_king_check, white_king_check = player_check_logic(a_chess_board)

                                if accidental_self_check(black_king_check, white_king_check, current_player) is False:

                                    # this means perform the legal move on the actual board!
                                    any_legal_move(chess_board, selected_piece[0], selected_piece[1], row, col)

                                    # track previous move made
                                    previous_move = retain_prev_move(a_chess_board, row, col)

                                    # update possible moves list because change has occurred
                                    obtain_possible_moves(chess_board, previous_move)

                                    # iterate to next player
                                    player += 1

                                    # update active_check, should return true if the new iterated player is in check
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)

                                    # print to console
                                    print(f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                    # reset piece
                                    selected_piece = None

                        else:
                            # if move is not in legal move set
                            selected_piece = None

                    else:
                        # if wrong color
                        selected_piece = None

                elif not selected_piece:
                    # this is where the reset piece points to, do not allow blank spaces to be selected
                    if chess_board[row][col] != ' ':
                        selected_piece = (row, col)


            # now the game enters check phase
            # player being checked must make a move to remove check
            if active_check:

                print('check has been reached, game will now end')

                running = False

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
