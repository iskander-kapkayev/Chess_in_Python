import pygame
from chess_scripts_2 import *

# ---------- this will draw the board ---------- #

def draw_board():
    for chess_row in range(board_size):
        for chess_col in range(board_size):
            color = white if (chess_row + chess_col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (chess_col * square_size, chess_row * square_size, square_size, square_size))

            # add pieces from chess board
            chess_piece = chess_board[chess_row][chess_col]

            if chess_piece != ' ':
                font = pygame.font.Font(None, 50)
                text = font.render(chess_piece.get_piece(), True, black if color == white else white)
                text_rect = text.get_rect(center=((chess_col + 0.5) * square_size, (chess_row + 0.5) * square_size))
                screen.blit(text, text_rect)

# ---------- this will initialize the pygame ---------- #
pygame.init()
pygame.display.set_caption('Iskander\'s Chess-u~!')

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# colors for game board and font
black = (0, 0, 0)
white = (255, 255, 255)

# size of board and chess squares
board_size = 8 # num of squares
square_size = 100 # pixel size

# initialize game pieces and chess board
chess_board = initialize_chess_board(board_size)
chess_board = obtain_possible_moves(chess_board, board_size, None, True)

# ---------- game loop that will keep working until game ends ---------- #

previous_move = None # previous move will be a tuple of player color, player piece and player placement
running = True
selected_piece = None
player = 0
active_check = False
alternate_chess_board = None
print(f'{chess_board}')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // square_size
            col = x // square_size

            # while not in check, play the game normally
            print(f'active check is currently: {active_check}')
            #if active_check is False:
                # if selecting a piece and no active check
            print(player)
            if selected_piece:
                # make sure players go in order: W, B, W, B, etc.
                if((chess_board[selected_piece[0]][selected_piece[1]].get_player() == 'white' and player % 2 == 0)
                        or (chess_board[selected_piece[0]][selected_piece[1]].get_player() == 'black' and player % 2 == 1)):
                    print(f'piece selected: {selected_piece}')
                    # make sure a legal move is selected
                    print(f'correct player and piece combo')
                    if legal_movement(chess_board, selected_piece[0], selected_piece[1], row, col, previous_move, False):
                        print(f'legal movement confirmed')
                        # in case of a king's castle
                        if (((chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'wK')
                             or (chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'bK'))
                                and (abs(selected_piece[1] - col) == 2)):
                            # perform king's castle
                            chess_board = king_castle(chess_board, selected_piece[0], selected_piece[1], row, col)
                            # perform end of move actions
                            chess_board, previous_move, black_king_check, white_king_check = end_of_move(chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 3)
                            player += 1

                        # in case of an en passant by pawns
                        elif (((chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'bP')
                               or (chess_board[selected_piece[0]][selected_piece[1]].get_piece() == 'wP'))
                              and (abs(selected_piece[0] - row) == 1 and abs(selected_piece[1] - col) == 1)
                              and (chess_board[row][col] == ' ')):
                            # perform end of move actions for en passant
                            chess_board, previous_move, black_king_check, white_king_check = end_of_move(chess_board, selected_piece[0] , selected_piece[1], row, col, board_size, 1)
                            player += 1

                        # any other legal move
                        else:
                            # perform end of move actions
                            chess_board, previous_move, black_king_check, white_king_check = end_of_move(chess_board, selected_piece[0], selected_piece[1], row, col, board_size, 2)

                        # iterate to next player, evaluate a check, and reset piece to none
                        player += 1
                        print(f'player #: {player}')
                        active_check = active_check_lookup(player, black_king_check, white_king_check)
                        selected_piece = None
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

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
