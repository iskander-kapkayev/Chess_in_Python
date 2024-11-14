from chess_scripts_2 import *

def attempt_one():
    # initialize game pieces and chess board
    chess_board = initialize_chess_board(8)
    obtain_possible_moves_v2(chess_board, None)

    print(chess_board)
    # print the possible moves (should only be one)

    # move wP from 6,1 to 2,3
    chess_board[2][3] = chess_board[6][1]
    chess_board[6][1] = ' '
    chess_board[2][3].update_moved_from((6, 1))
    chess_board[2][3].update_moved_to((2, 3))

    # set previous move
    previous_move = ('white', 'wP', (3, 3), (2, 3))
    obtain_possible_moves_v2(chess_board, previous_move)

    # run through every combo of (0,0) to (7,7) to calculate available moves

    list_of_moves = []

    print(f'this is the piece in 2,3: {chess_board[2][3]}')
    for row in range(8):
        for col in range(8):
            print(f'checking row: {row} and col: {col}')

            if legal_path(chess_board, 1, 4, row, col, previous_move):
                list_of_moves.append((row,col))
                print(f'---approved! row: {row} and col: {col}')

    return list_of_moves

def attempt_two():
    # initialize game pieces and chess board
    chess_board = initialize_chess_board(8)
    obtain_possible_moves_v2(chess_board, None)

    print(chess_board)
    # print the possible moves (should only be one)

    # move bP from 1,4 to 5,4
    chess_board[5][4] = chess_board[1][4]
    chess_board[1][4] = ' '
    chess_board[5][4].update_moved_from((1, 4))
    chess_board[5][4].update_moved_to((5, 4))

    # set previous move
    previous_move = ('black', 'bP', (1, 4), (5, 4))
    obtain_possible_moves_v2(chess_board, previous_move)

    # run through every combo of (0,0) to (7,7) to calculate available moves

    list_of_moves = []

    print(f'this is the piece in 5,4: {chess_board[5][4]}')
    for row in range(8):
        for col in range(8):
            print(f'checking row: {row} and col: {col}')

            if legal_path(chess_board, 6, 3, row, col, previous_move):
                list_of_moves.append((row,col))
                print(f'---approved! row: {row} and col: {col}')

    return list_of_moves

print(f'{attempt_one()} \n {attempt_two()}')
