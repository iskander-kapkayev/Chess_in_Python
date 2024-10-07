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