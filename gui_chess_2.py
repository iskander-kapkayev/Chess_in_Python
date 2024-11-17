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
green_alt = '#AAC4AC'
mimi_pink = '#EDCDE3'
pink_lavender = '#D0A6B4'

# size of board and chess squares
board_size = 8 # num of squares
square_size = 100 # pixel size

# initialize game pieces and chess board
chess_board = initialize_chess_board(board_size)
obtain_possible_moves_v2(chess_board, None)

# ---------- game loop that will keep working until game ends ---------- #

previous_move = None # previous move will be a tuple of player color, player piece and player placement
running = True # this tells the game to keep running
selected_piece = None # this will represent the X, Y coordinate of the selected piece
player = 0 # mod 2 will return 0 or 1, player white or black
active_check = False # tells the game to focus on a player

'''
# create a highlight
highlight = pygame.image.load('pokemon_icons/wQ.png')
'''

while running:

    for event in pygame.event.get():


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

                    '''
                    # highlight the square
                    #highlight_rect = highlight.get_rect(center=((x + 0.5) * square_size, (y + 0.5) * square_size))
                    #screen.blit(highlight, highlight_rect)
                    #pygame.display.flip()
                    '''

                    # set current piece and player for ease
                    current_piece = chess_board[selected_piece[0]][selected_piece[1]]
                    current_player = current_piece.get_player()

                    # make sure players go in order: W, B, W, B, etc.
                    if((current_player == 'white' and player % 2 == 0)
                            or (current_player == 'black' and player % 2 == 1)):

                        # make sure a legal move is selected from possible moves list
                        if (row, col) in current_piece.get_possible_moves():

                            # evaluate move and apply end of move actions
                            if evaluate_action(chess_board, selected_piece[0], selected_piece[1], row, col, previous_move):
                                (prev_color, prev_piece, prev_moved_from,
                                 prev_moved_to, player, black_king_check,
                                 white_king_check, active_check, selected_piece) = perform_action_ending(
                                    chess_board, selected_piece[0], selected_piece[1], row, col, player)

                            else:
                                # if move is not in legal move set
                                messagebox.showinfo('Illegal Move', f'This piece cannot move here!')
                                selected_piece = None

                        else:
                            # if move is not in legal move set
                            messagebox.showinfo('Illegal Move', f'This piece cannot move here!')
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

                if count_moves(chess_board, player) > 0:

                    # when piece is selected
                    if selected_piece:

                        # set current piece and player for ease
                        current_piece = chess_board[selected_piece[0]][selected_piece[1]]
                        current_player = current_piece.get_player()

                        # make sure players go in order: W, B, W, B, etc.
                        if ((current_player == 'white' and player % 2 == 0)
                                or (current_player == 'black' and player % 2 == 1)):

                            # make sure a legal move is selected from possible moves list
                            if (row, col) in current_piece.get_possible_moves():

                                # evaluate move and apply end of move actions
                                if evaluate_action(chess_board, selected_piece[0], selected_piece[1], row, col, previous_move):
                                    (prev_color, prev_piece, prev_moved_from,
                                     prev_moved_to, player, black_king_check,
                                     white_king_check, active_check, selected_piece) = perform_action_ending(
                                        chess_board, selected_piece[0], selected_piece[1], row, col, player)

                                else:
                                    # if move is not in legal move set
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
                else:
                    # there are no more possible moves! end the game
                    messagebox.showinfo('CHECKMATE', f'There are no more possible moves. Player {player % 2} WINS!!')
                    running = False

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
