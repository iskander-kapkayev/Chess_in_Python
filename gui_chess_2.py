import pygame
import pyautogui
from chess_scripts_2 import *

# Initialize Pygame
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

# ---------- this will draw the board ----------

def draw_board():
    for chess_row in range(board_size):
        for chess_col in range(board_size):
            color = white if (chess_row + chess_col) % 2 == 0 else black
            pygame.draw.rect(screen, color, (chess_col * square_size, chess_row * square_size, square_size, square_size))

            # add pieces from chess board
            chess_piece = chess_board[chess_row][chess_col]

            if chess_piece != ' ':
                font = pygame.font.Font(None, 50)
                text = font.render(chess_piece.piece, True, black if color == white else white)
                text_rect = text.get_rect(center=((chess_col + 0.5) * square_size, (chess_row + 0.5) * square_size))
                screen.blit(text, text_rect)

# ---------- this will apply a castle ----------

def king_castle(selected_piece_x, selected_piece_y, new_row, new_col):
    current_piece = chess_board[selected_piece_x][selected_piece_y]
    change_in_y = new_col - selected_piece_y
    # if change in y is negative
    if change_in_y < 0:
        # move king to castle position and remove old king piece
        chess_board[new_row][new_col] = chess_board[selected_piece_x][selected_piece_y]
        chess_board[selected_piece_x][selected_piece_y] = ' '
        # update chess piece class
        chess_board[new_row][new_col].update_moved_to((new_row, new_col))
        chess_board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            chess_board[new_row][new_col + 1] = chess_board[7][0]
            chess_board[7][0] = ' '
            # update chess piece class
            chess_board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            chess_board[new_row][new_col + 1].update_moved_from((7, 0))
        elif current_piece.piece == 'bK':
            chess_board[new_row][new_col + 1] = chess_board[0][0]
            chess_board[0][0] = ' '
            # update chess piece class
            chess_board[new_row][new_col + 1].update_moved_to((new_row, new_col + 1))
            chess_board[new_row][new_col + 1].update_moved_from((0, 0))
    elif change_in_y > 0:
        # move king to castle position and remove old king piece
        chess_board[new_row][new_col] = chess_board[selected_piece_x][selected_piece_y]
        chess_board[selected_piece[0]][selected_piece[1]] = ' '
        # update chess piece class
        chess_board[new_row][new_col].update_moved_to((new_row, new_col))
        chess_board[new_row][new_col].update_moved_from((selected_piece_x, selected_piece_y))
        # move rook to castle position, and remove old rook piece
        if current_piece.piece == 'wK':
            chess_board[new_row][new_col - 1] = chess_board[7][7]
            chess_board[7][7] = ' '
            # update chess piece class
            chess_board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            chess_board[new_row][new_col - 1].update_moved_from((7, 7))
        elif current_piece.piece == 'bK':
            chess_board[new_row][new_col - 1] = chess_board[0][7]
            chess_board[0][7] = ' '
            # update chess piece class
            chess_board[new_row][new_col - 1].update_moved_to((new_row, new_col - 1))
            chess_board[new_row][new_col - 1].update_moved_from((0, 7))

# ---------- game loop that will keep working until game ends ----------
previous_move = None # previous move will be a tuple of player color, player piece and player placement
running = True
selected_piece = None
player = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = y // square_size
            col = x // square_size

            if selected_piece:
                if (chess_board[selected_piece[0]][selected_piece[1]].player == 'white' and player % 2 == 0) or (chess_board[selected_piece[0]][selected_piece[1]].player == 'black' and player % 2 == 1):

                    if legal_movement(chess_board, selected_piece[0], selected_piece[1], row, col, previous_move):

                        if (chess_board[selected_piece[0]][selected_piece[1]].piece == 'wK' or chess_board[selected_piece[0]][selected_piece[1]].piece == 'bK') and abs(selected_piece[1] - col) == 2:
                            # perform king's castle
                            king_castle(selected_piece[0], selected_piece[1], row, col)
                            previous_move = (chess_board[row][col].get_player(), chess_board[row][col].get_piece(), chess_board[row][col].get_moved_from(), chess_board[row][col].get_moved_to())
                        else:
                            #move selected piece to the new spot
                            chess_board[row][col] = chess_board[selected_piece[0]][selected_piece[1]]

                            # remove the selected piece from the old spot
                            chess_board[selected_piece[0]][selected_piece[1]] = ' '

                            # update the moved_to and moved_from positions in the chess piece class
                            chess_board[row][col].update_moved_to((row,col))
                            chess_board[row][col].update_moved_from((selected_piece[0], selected_piece[1]))

                            previous_move = (chess_board[row][col].get_player(), chess_board[row][col].get_piece(), chess_board[row][col].get_moved_from(), chess_board[row][col].get_moved_to())
                            print(previous_move)

                        player += 1
                        selected_piece = None
                    else:
                        selected_piece = None
                else:
                    selected_piece = None

            else:
                # select a piece
                if chess_board[row][col] != ' ':
                    selected_piece = (row, col)

    # this will draw the board each time
    draw_board()
    pygame.display.flip()

pygame.quit()
