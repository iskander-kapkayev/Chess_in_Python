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

                    # set current piece for ease
                    current_piece = chess_board[selected_piece[0]][selected_piece[1]]

                    # make sure players go in order: W, B, W, B, etc.
                    if((current_piece.get_player() == 'white' and player % 2 == 0)
                            or (current_piece.get_player() == 'black' and player % 2 == 1)):

                        # make sure a legal move is selected from possible moves list
                        if (row, col) in current_piece.get_possible_moves():

                            # in case of a king's castle
                            if (((current_piece.get_piece() == 'wK')
                                 or (current_piece.get_piece() == 'bK'))
                                    and (abs(selected_piece[1] - col) == 2)):
                                # perform king's castle
                                chess_board = king_castle(chess_board, selected_piece[0], selected_piece[1], row, col)

                                # perform end of move actions

                                # track previous move made
                                previous_move = (chess_board[row][col].get_player(),
                                                 chess_board[row][col].get_piece(),
                                                 chess_board[row][col].get_moved_from(),
                                                 chess_board[row][col].get_moved_to()
                                                 )


                                # update possible moves list because change has occurred
                                obtain_possible_moves(chess_board, previous_move)

                                # check to see if either player is in check (self check would not happen at this point)
                                black_king_check, white_king_check = player_check_logic(chess_board)

                            # in case of an en passant by pawns
                            elif (((current_piece.get_piece() == 'bP')
                                   or (current_piece.get_piece() == 'wP'))
                                  and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                  and (a_chess_board[row][col] == ' ')):

                                # perform end of move actions for en passant
                                #chess_board, previous_move = end_of_move(chess_board, selected_piece[0] , selected_piece[1], row, col, board_size, 1)

                                # this means en passant was done!
                                chess_board[row][col] = chess_board[selected_piece[0]][selected_piece[1]]
                                # remove the selected piece from the old spot
                                chess_board[selected_piece[0]][selected_piece[1]] = ' '

                                # capture the pawn by en passant
                                if chess_board[row][col].get_piece() == 'bP':
                                    # if black, pawn to capture is above it
                                    chess_board[row - 1][col] = ' '
                                elif chess_board[row][col].get_piece() == 'wP':
                                    # if white, pawn to capture is below it
                                    chess_board[row + 1][col] = ' '

                                # update the moved_to and moved_from positions in the chess piece class
                                chess_board[row][col].update_moved_to((row, col))
                                chess_board[row][col].update_moved_from((selected_piece[0], selected_piece[1]))

                                # track previous move made
                                previous_move = (chess_board[row][col].get_player(),
                                                 chess_board[row][col].get_piece(),
                                                 chess_board[row][col].get_moved_from(),
                                                 chess_board[row][col].get_moved_to()
                                                 )

                                # update possible moves list because change has occurred
                                obtain_possible_moves(chess_board, previous_move)

                                # check to see if either player is in check (self check would not happen at this point)
                                black_king_check, white_king_check = player_check_logic(chess_board)


                            else:
                                # any other legal move
                                # perform end of move actions

                                # this means a regular legal move was done
                                chess_board[row][col] = chess_board[selected_piece[0]][selected_piece[1]]
                                # remove the selected piece from the old spot
                                chess_board[selected_piece[0]][selected_piece[1]] = ' '
                                # update the moved_to and moved_from positions in the chess piece class
                                chess_board[row][col].update_moved_to((row, col))
                                chess_board[row][col].update_moved_from((selected_piece[0], selected_piece[1]))

                                # track previous move made
                                previous_move = (chess_board[row][col].get_player(),
                                                 chess_board[row][col].get_piece(),
                                                 chess_board[row][col].get_moved_from(),
                                                 chess_board[row][col].get_moved_to()
                                                 )

                                # update possible moves list because change has occurred
                                obtain_possible_moves(chess_board, previous_move)

                                # check to see if either player is in check (self check would not happen at this point)
                                black_king_check, white_king_check = player_check_logic(chess_board)

                            # iterate to next player
                            player += 1

                            # update active_check, should return true if the new iterated player is in check
                            active_check = active_check_lookup(player, black_king_check, white_king_check)

                            # print to console
                            print(f'{current_piece.get_player()} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

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
            elif active_check:

                print('check has been reached')

                if count_moves(chess_board, player) > 0:

                    # as long as moves exist...
                    if selected_piece:

                        print(f'this piece was selected: {selected_piece}')
                        a_chess_board = copy.deepcopy(chess_board)
                        test_chess_board = copy.deepcopy(chess_board)
                        a_current_piece = test_chess_board[selected_piece[0]][selected_piece[1]]

                        # make sure players go in order: W, B, W, B, etc.
                        if ((a_current_piece.get_player() == 'white' and player % 2 == 0)
                                or (a_current_piece.get_player() == 'black' and player % 2 == 1)):

                            print(f'this si the player escaping check: {a_current_piece.get_player()}')

                            # make sure a legal move is selected
                            if legal_conclusion(test_chess_board, selected_piece[0], selected_piece[1], row, col, previous_move):

                                print(f'this move is legal')

                                # in case of a king's castle
                                if (((a_current_piece.get_piece() == 'wK')
                                     or (a_current_piece.get_piece() == 'bK'))
                                        and (abs(selected_piece[1] - col) == 2)):
                                    # perform king's castle
                                    a_chess_board = king_castle(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                    # perform end of move actions
                                    a_chess_board, previous_move, black_king_check, white_king_check = end_of_move(a_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 3)

                                # in case of an en passant by pawns
                                elif (((a_current_piece.get_piece() == 'bP')
                                       or (a_current_piece.get_piece() == 'wP'))
                                      and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                      and (a_chess_board[row][col] == ' ')):
                                    # perform end of move actions for en passant
                                    a_chess_board, previous_move, black_king_check, white_king_check = end_of_move(a_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 1)

                                # any other legal move
                                else:
                                    print(f'reached else statement')
                                    # perform end of move actions
                                    a_chess_board, previous_move, black_king_check, white_king_check = end_of_move(a_chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 2)

                                print(f'this is the value of black king check: {black_king_check}')
                                print(f'this is the value of white king check: {white_king_check}')

                                # iterate to next player, evaluate a check, and reset piece to none
                                active_check = active_check_lookup(player, black_king_check, white_king_check)

                                print(f'this is the active check value: {active_check}')

                                if active_check is False:
                                    # assign new chess board if we removed check
                                    chess_board, player, selected_piece = cycle_breaker_check(a_chess_board, active_check, player)

                            else:
                                # if not a legal move, reset piece to none
                                selected_piece = None
                        else:
                            # if wrong color
                            selected_piece = None

                    elif not selected_piece:
                        # this will select a piece if none have been selected
                        if chess_board[row][col] != ' ':
                            selected_piece = (row, col)

                elif count_moves(a_chess_board, player) == 0:
                    # there are no possible moves!
                    # the player has been checkmated
                    running = False
                    print(f'Thanks for playing! {player % 2} has been checkmated!')


    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
