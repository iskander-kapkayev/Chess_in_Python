from chess_scripts_2 import *

# initialize game pieces and chess board
chess_board = initialize_chess_board(8)
obtain_possible_moves_v2(chess_board, None)

print(chess_board)
# print the possible moves (should only be one)
for rows in chess_board:
    for square in rows:
        if square != ' ' and square.get_player() == 'black':
            print(f' The current piece is {square.get_piece()}, the current position is ({square.get_position()}), and all the possible moves are: {square.get_possible_moves()}')

print('\n ------------ \n')

# first move the wP from 6,4 to 4,4
chess_board[4][4] = chess_board[6][4]
chess_board[6][4] = ' '
chess_board[4][4].update_moved_from((6,4))
chess_board[4][4].update_moved_to((4,4))
obtain_possible_moves_v2(chess_board, None)

# print the possible moves (should only be one)
for rows in chess_board:
    for square in rows:
        if square != ' ' and square.get_player() == 'black':
            print(f' The current piece is {square.get_piece()}, the current position is ({square.get_position()}), and all the possible moves are: {square.get_possible_moves()}')

print('\n ------------ \n')

# second move the bP from 1,5 to 2,5
chess_board[2][5] = chess_board[1][5]
chess_board[1][5] = ' '
chess_board[2][5].update_moved_from((1,5))
chess_board[2][5].update_moved_to((2,5))
obtain_possible_moves_v2(chess_board, None)

# print the possible moves (should only be one)
for rows in chess_board:
    for square in rows:
        if square != ' ' and square.get_player() == 'black':
            print(f' The current piece is {square.get_piece()}, the current position is ({square.get_position()}), and all the possible moves are: {square.get_possible_moves()}')

print('\n ------------ \n')

# next move the wQ into a check position from 7,3 to 3,7
chess_board[3][7] = chess_board[7][3]
chess_board[7][3] = ' '
chess_board[3][7].update_moved_from((7,3))
chess_board[3][7].update_moved_to((3,7))

# set previous move
previous_move = ('white', 'wQ', (7, 3), (3, 7))

obtain_possible_moves_v2(chess_board, previous_move)

print(chess_board)

# print the possible moves (should only be one)
for rows in chess_board:
    for square in rows:
        if square != ' ' and square.get_player() == 'black':
            print(f' The current piece is {square.get_piece()}, the current position is ({square.get_position()}), and all the possible moves are: {square.get_possible_moves()}')

print('\n ------------ \n')