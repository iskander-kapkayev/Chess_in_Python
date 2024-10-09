import pygame
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

# this will draw the board
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

# game loop that will keep working until game ends
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

                    if legal_movement(chess_board, selected_piece[0], selected_piece[1], row, col):

                        #move selected piece to the new spot
                        chess_board[row][col] = chess_board[selected_piece[0]][selected_piece[1]]

                        # remove the selected piece from the old spot
                        chess_board[selected_piece[0]][selected_piece[1]] = ' '
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
    # create a function that checks if the KING is in check or checkmate
    draw_board()
    pygame.display.flip()

pygame.quit()