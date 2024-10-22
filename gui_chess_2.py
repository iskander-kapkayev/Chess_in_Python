import copy

import pygame
from chess_scripts_2 import *

from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw() #to hide the main window


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
red = (255, 0, 0)
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

# create a highlight
highlight = pygame.image.load('pokemon_icons/wQ.png')

while running:

    for event in pygame.event.get():

        # alternative chess board used for evaluating an in check position
        a_chess_board = None
        b_chess_board = None

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

                    # highlight the square
                    #highlight_rect = highlight.get_rect(center=((x + 0.5) * square_size, (y + 0.5) * square_size))
                    #screen.blit(highlight, highlight_rect)
                    #pygame.display.flip()

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
                                if castle_movement_v2(chess_board, selected_piece[0], selected_piece[1], row, col):

                                    # perform king's castle, obtain new possible moves, obtain check values
                                    king_castle(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                    previous_move = retain_prev_move(a_chess_board, row, col)
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
                                        # if accidental self check
                                        messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                        selected_piece = None

                                else:
                                    # not legal castle
                                    messagebox.showinfo('Illegal Castle', f'Your king passes through check!')
                                    selected_piece = None

                            # in case of an en passant by pawns
                            elif (((current_piece.get_piece() == 'bP')
                                   or (current_piece.get_piece() == 'wP'))
                                  and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                  and (chess_board[row][col] == ' ')):

                                # perform en passant, obtain new possible moves, obtain check values
                                # perform en passant on fake board
                                en_passant(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move = retain_prev_move(a_chess_board, row, col)
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
                                    # if accidental self check
                                    messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                    selected_piece = None

                            else:

                                # perform any legal move, obtain new possible moves, obtain check values
                                any_legal_move(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move = retain_prev_move(a_chess_board, row, col)
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

                                    # print checker
                                    for rows in chess_board:
                                        for square in rows:
                                            if square != ' ':
                                                if square.get_player() != current_player:
                                                    print(f'Moves for {square.get_piece()} are: {square.get_possible_moves()}')

                                    print('\n---------\n')

                                    # reset piece
                                    selected_piece = None

                                else:
                                    # if accidental self check
                                    messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                    selected_piece = None

                        else:
                            # if move is not in legal move set
                            messagebox.showinfo('Illegal Move', f'This piece cannot move there!')
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

                print(f'\n----------\n')

                # double check every possible move and see if it changes game
                if player % 2 == 0:
                    if checkmate_trigger(chess_board, previous_move, 'white'):
                        messagebox.showinfo('CHECKMATE', f'Checkmate on white! Black wins!! Please play again!')
                        running = False
                if player % 2 == 1:
                    if checkmate_trigger(chess_board, previous_move, 'black'):
                        messagebox.showinfo('CHECKMATE', f'Checkmate on black! White wins!! Please play again!')
                        running = False

                # when piece is selected
                if selected_piece:

                    print(f' the piece selected is: {selected_piece}')

                    # set check everything chessboard
                    a_chess_board = copy.deepcopy(chess_board)

                    # set current piece for ease
                    current_piece = chess_board[selected_piece[0]][selected_piece[1]]

                    # set current player for ease
                    current_player = current_piece.get_player()

                    # make sure players go in order: W, B, W, B, etc.
                    if ((current_player == 'white' and player % 2 == 0)
                            or (current_player == 'black' and player % 2 == 1)):

                        # make sure a legal move is selected from possible moves list
                        print(f' this piece can move: {current_piece.get_possible_moves()}')
                        if (row, col) in current_piece.get_possible_moves():

                            # in case of a king's castle
                            if (((current_piece.get_piece() == 'wK')
                                 or (current_piece.get_piece() == 'bK'))
                                    and (abs(selected_piece[1] - col) == 2)):

                                # double check king movement logic to not pass through a check
                                if castle_movement_v2(a_chess_board, selected_piece[0], selected_piece[1], row, col):

                                    # perform king's castle, obtain new possible moves, obtain check values
                                    king_castle(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                    previous_move_in_check = retain_prev_move(a_chess_board, row, col)
                                    obtain_possible_moves(a_chess_board, previous_move_in_check)
                                    black_king_check, white_king_check = player_check_logic(a_chess_board)

                                    if accidental_self_check(black_king_check, white_king_check, current_player) is False:
                                        # perform on actual board!
                                        king_castle(chess_board, selected_piece[0], selected_piece[1], row, col)

                                        # track previous move made
                                        previous_move_in_check = retain_prev_move(chess_board, row, col)

                                        # update possible moves list because change has occurred
                                        obtain_possible_moves(chess_board, previous_move_in_check)

                                        # iterate to next player
                                        player += 1

                                        # update active_check, should return true if the new iterated player is in check
                                        active_check = active_check_lookup(player, black_king_check, white_king_check)

                                        # print to console
                                        print(f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                        # reset piece
                                        selected_piece = None

                                    else:
                                        # if accidental self check
                                        messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                        selected_piece = None

                                else:
                                    # not legal castle
                                    messagebox.showinfo('Illegal Castle', f'Your king passes through check!')
                                    selected_piece = None

                            # in case of an en passant by pawns
                            elif (((current_piece.get_piece() == 'bP')
                                   or (current_piece.get_piece() == 'wP'))
                                  and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                                  and (chess_board[row][col] == ' ')):

                                # perform en passant, obtain new possible moves, obtain check values
                                # perform en passant on fake board
                                en_passant(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move_in_check = retain_prev_move(a_chess_board, row, col)
                                obtain_possible_moves(a_chess_board, previous_move_in_check)
                                black_king_check, white_king_check = player_check_logic(a_chess_board)

                                if accidental_self_check(black_king_check, white_king_check, current_player) is False:
                                    # this means en passant on actual board!
                                    en_passant(chess_board, selected_piece[0], selected_piece[1], row, col)

                                    # track previous move made
                                    previous_move_in_check = retain_prev_move(chess_board, row, col)

                                    # update possible moves list because change has occurred
                                    obtain_possible_moves(chess_board, previous_move_in_check)

                                    # iterate to next player
                                    player += 1

                                    # update active_check, should return true if the new iterated player is in check
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)

                                    # print to console
                                    print(
                                        f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                    # reset piece
                                    selected_piece = None

                                else:
                                    # if accidental self check
                                    messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                    selected_piece = None

                            else:

                                # perform any legal move, obtain new possible moves, obtain check values
                                any_legal_move(a_chess_board, selected_piece[0], selected_piece[1], row, col)
                                previous_move_in_check = retain_prev_move(a_chess_board, row, col)
                                obtain_possible_moves(a_chess_board, previous_move_in_check)
                                black_king_check, white_king_check = player_check_logic(a_chess_board)

                                if accidental_self_check(black_king_check, white_king_check, current_player) is False:
                                    # this means perform the legal move on the actual board!
                                    any_legal_move(chess_board, selected_piece[0], selected_piece[1], row, col)

                                    # track previous move made
                                    previous_move_in_check = retain_prev_move(a_chess_board, row, col)

                                    # update possible moves list because change has occurred
                                    obtain_possible_moves(chess_board, previous_move_in_check)

                                    # iterate to next player
                                    player += 1

                                    # update active_check, should return true if the new iterated player is in check
                                    active_check = active_check_lookup(player, black_king_check, white_king_check)

                                    # print to console
                                    print(
                                        f'{current_player} just played his {current_piece.get_piece()} from {(selected_piece[0], selected_piece[1])} to {(row, col)}')

                                    # reset piece
                                    selected_piece = None

                                else:
                                    # if accidental self check
                                    messagebox.showinfo('Illegal Move', f'This puts you in check!')
                                    selected_piece = None

                        else:
                            # if move is not in legal move set
                            messagebox.showinfo('Illegal Move', f'This piece cannot move there!')
                            selected_piece = None

                    else:
                        # if wrong color
                        selected_piece = None

                elif not selected_piece:
                    # this is where the reset piece points to, do not allow blank spaces to be selected
                    if chess_board[row][col] != ' ':
                        selected_piece = (row, col)

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()




'''
                if player % 2 == 0:
                    opposite = 'black'
                elif player % 2 == 1:
                    opposite = 'white'

                for rows in chess_board:
                    for square in rows:
                        if square != ' ':
                            # look for current possible moves
                            if square.get_player() != opposite:
                                # only look at pieces with moves
                                if len(square.get_possible_moves()) > 0:

                                    # if a move still leads to check, then remove that from the list
                                    get_moves = square.get_possible_moves()
                                    get_piece_x, get_piece_y = square.get_position()
                                    a_chess_board = copy.deepcopy(chess_board)

                                    for move in get_moves:
                                        # unpack move
                                        new_x, new_y = move

                                        # perform any legal move, obtain new possible moves, obtain check values
                                        any_legal_move(a_chess_board, get_piece_x, get_piece_y, new_x, new_y)
                                        previous_move = retain_prev_move(a_chess_board, new_x, new_y)
                                        obtain_possible_moves(a_chess_board, previous_move)
                                        black_king_check, white_king_check = player_check_logic(a_chess_board)

                                        if accidental_self_check(black_king_check, white_king_check, square.get_player()) is True:
                                            # clean up the moves list for this piece
                                            get_moves.remove(move)

                                        # reverse the move
                                        any_legal_move(a_chess_board, new_x, new_y, get_piece_x, get_piece_y)
                                        previous_move = retain_prev_move(a_chess_board, get_piece_x, get_piece_y)
                                        obtain_possible_moves(a_chess_board, previous_move)
                                        black_king_check, white_king_check = player_check_logic(a_chess_board)

                                    # after all moves for a piece are done, set the moves back to the piece
                                    chess_board[get_piece_x][get_piece_y].update_possible_moves(get_moves)
                                    print(f'Moves for {square.get_piece()} are: {square.get_possible_moves()}')

                if count_moves(chess_board, player) > 0:

                    print(f'\n----------\n')
                    print(f'there are moves available to remove yourself from check!')

                    for rows in chess_board:
                        for square in rows:
                            if square != ' ':
                                if square.get_player() != opposite:
                                    print(f'Moves for {square.get_piece()} are: {square.get_possible_moves()}')

                running = False

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
'''