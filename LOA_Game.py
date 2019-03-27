import tkinter

SIDE = 1  # white:0, black:1
SELECTED = 0 # white:1 black:2
SELECTED_WHITE_PIECE = 0
SELECTED_BLACK_PIECE = 0
# tag of pieces
white = []
black = []
#  pos in board
black_piece = [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1],
               [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8]]
white_piece = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
               [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]]


def legal_move(x, y, piece):
    if x == piece[0] or y == piece[1]:
        return True
    if abs(x - piece[0]) == abs(y - piece[1]):
        return True
    return False


def mouse_call(event):
    posx = event.x // 30  # 1-8
    posy = 9 - event.y // 30  # 8-1
    global SELECTED
    global SELECTED_BLACK_PIECE
    global SELECTED_WHITE_PIECE
    global black_piece
    global white_piece
    print("click at", posx, posy)
    if not SELECTED:
        if SIDE and [posx, posy] in black_piece:    # black and clicked a black piece
            SELECTED = 1
            SELECTED_BLACK_PIECE = black_piece.index([posx, posy])
            print(SELECTED_BLACK_PIECE)
        if not SIDE and [posx, posy] in white_piece:    # white and clicked a white piece
            SELECTED = 1
            SELECTED_WHITE_PIECE = white_piece.index([posx, posy])
            print(SELECTED_WHITE_PIECE)
    else:
        if SIDE:  # black
            if [posx, posy] == black_piece[SELECTED_BLACK_PIECE]:   # click the selected piece
                SELECTED = 0
                print("release piece")
            elif [posx, posy] not in black_piece and legal_move(posx, posy, black_piece[SELECTED_BLACK_PIECE]):
                SELECTED = 0
                black_piece[SELECTED_BLACK_PIECE] = [posx, posy]
                board.coords(black[SELECTED_BLACK_PIECE],
                             posx * 30 + 4, (9 - posy) * 30 + 4,
                             posx * 30 + 26, (9 - posy) * 30 + 26
                             )
                # if [posx, posy] in white_piece:
                #     white_piece[white_piece.index([posx, posy])] = [-1, -1]  # out


top = tkinter.Tk()
top.title("Line of Action")
top.geometry('500x500')
top.resizable(width=False, height=False)

# draw board
board = tkinter.Canvas(top, width=300, height=300, bg='Beige')
board.bind("<Button-1>", mouse_call)
board.pack()
for i in range(1, 9):
    for j in range(1, 9):
        board.create_rectangle(i * 30, j * 30, i * 30 + 30, j * 30 + 30)
board.create_rectangle(29, 29, 271, 271)
board.create_text(150, 15, text='A  B  C  D  E  F  G  H', font="Courier 13 bold")
board.create_text(150, 285, text='A  B  C  D  E  F  G  H', font="Courier 13 bold")
for i in range(8):
    board.create_text(15, 45 + 30 * i, text=8-i, font="Courier 13 bold")
    board.create_text(285, 45 + 30 * i, text=8-i, font="Courier 13 bold")

for i in range(12):
    white.append(board.create_oval(white_piece[i][0] * 30 + 4, white_piece[i][1] * 30 + 4,
                                   white_piece[i][0] * 30 + 26, white_piece[i][1] * 30 + 26,
                                   fill="white")
                 )
for i in range(12):
    black.append(board.create_oval(black_piece[i][0] * 30 + 4, 300 - (black_piece[i][1] * 30 + 4),
                                   black_piece[i][0] * 30 + 26, 300 - (black_piece[i][1] * 30 + 26),
                                   fill="black")
                 )
top.mainloop()

