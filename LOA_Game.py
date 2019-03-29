import tkinter

SIDE = 1  # white:0, black:1
SELECTED = 0 # white:1 black:2
SELECTED_WHITE_PIECE = 0
SELECTED_BLACK_PIECE = 0
# tag of pieces
white_in_canvas = []
black_in_canvas = []
#  pos in board
black_piece = [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1],
               [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8]]
white_piece = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
               [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]]
#  each line has how many piece
line_count = [2] * 42
line_count[0] = line_count[7] = line_count[8] = line_count[15] = 6
line_count[22] = line_count[35] = 0

#  state of board, valid part from [1,1] to [8,8]
#  up-down reverse to board, adjust according to COORD
#  white:1 black:2
board_situation = [[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                   [-1, 0, 1, 1, 1, 1, 1, 1, 0],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                   [-1, 0, 1, 1, 1, 1, 1, 1, 0]]


def legal_move(piece):
    x: int = piece[0]
    y: int = piece[1]
    move_list = []
    # up-down
    pace = line_count[x + 7]
    if y + pace <= 8:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x][y + i] != SIDE + 1 and board_situation[x][y + i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x, y + pace])
    if y - pace >= 1:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x][y - i] != SIDE + 1 and board_situation[x][y + i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x, y - pace])
    # left-right
    pace = line_count[y - 1]
    if x + pace <= 8:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x + i][y] != SIDE + 1 and board_situation[x + i][y] != 0:
                flag = False
                break
        if flag:
            move_list.append([x + pace, y])
    if x - pace >= 0:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x - i][y] != SIDE + 1 and board_situation[x - i][y] != 0:
                flag = False
                break
        if flag:
            move_list.append([x - pace, y])
    # 2-4
    pace = line_count[x + y + 13]
    if x + pace <= 8:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x + i][y - i] != SIDE + 1 and board_situation[x + i][y - i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x + pace, y - pace])
    if x - pace >= 0:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x - i][y + i] != SIDE + 1 and board_situation[x - i][y + i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x - pace, y + pace])
    # 1-3
    pace = line_count[x - y + 35]
    if x + pace <= 8:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x + i][y + i] != SIDE + 1 and board_situation[x + i][y + i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x + pace, y + pace])
    if x - pace >= 0:
        flag = True
        for i in range(1, pace - 1):
            if board_situation[x - i][y - i] != SIDE + 1 and board_situation[x - i][y - i] != 0:
                flag = False
                break
        if flag:
            move_list.append([x - pace, y - pace])
    return move_list


def mouse_call(event):
    posx = event.x // 30  # 1-8
    posy = 9 - event.y // 30  # 8-1
    global SIDE
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
            print("Select Black", SELECTED_BLACK_PIECE)
            print(legal_move(black_piece[SELECTED_BLACK_PIECE]))
        if not SIDE and [posx, posy] in white_piece:    # white and clicked a white piece
            SELECTED = 1
            SELECTED_WHITE_PIECE = white_piece.index([posx, posy])
            print("Select Black", SELECTED_WHITE_PIECE)
            print(legal_move(white_piece[SELECTED_BLACK_PIECE]))
    else:
        if SIDE:  # black
            if [posx, posy] == black_piece[SELECTED_BLACK_PIECE]:   # click the selected piece
                SELECTED = 0
                print("Release piece")
            elif [posx, posy] not in black_piece and [posx, posy] in legal_move(black_piece[SELECTED_BLACK_PIECE]):
                SELECTED = 0
                oldx = black_piece[SELECTED_BLACK_PIECE][0]
                oldy = black_piece[SELECTED_BLACK_PIECE][1]
                # update board situation
                board_situation[oldx][oldy] = 0  # empty
                board_situation[posx][posy] = 2  # black
                # update line of board
                line_count[oldx + 7] = line_count[oldx + 7] - 1
                line_count[oldy - 1] = line_count[oldy - 1] - 1
                line_count[oldx + oldy + 13] = line_count[oldx + oldy + 13] - 1
                line_count[oldx - oldy + 35] = line_count[oldx - oldy + 35] - 1
                # update piece info
                black_piece[SELECTED_BLACK_PIECE] = [posx, posy]
                # update canvas
                board.coords(black_in_canvas[SELECTED_BLACK_PIECE],
                             posx * 30 + 4, (9 - posy) * 30 + 4,
                             posx * 30 + 26, (9 - posy) * 30 + 26
                             )
                # eat piece
                if [posx, posy] in white_piece:  # one white out
                    board.delete(white_in_canvas[white_piece.index([posx, posy])])
                    white_piece[white_piece.index([posx, posy])] = [-1, -1]
                else:
                    line_count[posx + 7] = line_count[posx + 7] + 1
                    line_count[posy - 1] = line_count[posy - 1] + 1
                    line_count[posx + posy + 13] = line_count[posx + posy + 13] + 1
                    line_count[posx - posy + 35] = line_count[posx - posy + 35] + 1
                # change side to white
                SIDE = 0
        else:  # white
            if [posx, posy] == white_piece[SELECTED_WHITE_PIECE]:   # click the selected piece
                SELECTED = 0
                print("Release piece")
            elif [posx, posy] not in white_piece and [posx, posy] in legal_move(white_piece[SELECTED_WHITE_PIECE]):
                SELECTED = 0
                oldx = white_piece[SELECTED_WHITE_PIECE][0]
                oldy = white_piece[SELECTED_WHITE_PIECE][1]
                # update board situation
                board_situation[oldx][oldy] = 0  # empty
                board_situation[posx][posy] = 1  # white
                # update line of board
                line_count[oldx + 7] = line_count[oldx + 7] - 1
                line_count[oldy - 1] = line_count[oldy - 1] - 1
                line_count[oldx + oldy + 13] = line_count[oldx + oldy + 13] - 1
                line_count[oldx - oldy + 35] = line_count[oldx - oldy + 35] - 1
                # update piece info
                white_piece[SELECTED_WHITE_PIECE] = [posx, posy]
                # update canvas
                board.coords(white_in_canvas[SELECTED_WHITE_PIECE],
                             posx * 30 + 4, (9 - posy) * 30 + 4,
                             posx * 30 + 26, (9 - posy) * 30 + 26
                             )
                # eat piece
                if [posx, posy] in black_piece:  # one white out
                    board.delete(black_in_canvas[black_piece.index([posx, posy])])
                    black_piece[black_piece.index([posx, posy])] = [-1, -1]
                else:
                    line_count[posx + 7] = line_count[posx + 7] + 1
                    line_count[posy - 1] = line_count[posy - 1] + 1
                    line_count[posx + posy + 13] = line_count[posx + posy + 13] + 1
                    line_count[posx - posy + 35] = line_count[posx - posy + 35] + 1
                # change side to black
                SIDE = 1


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
    white_in_canvas.append(board.create_oval(white_piece[i][0] * 30 + 4, 300 - (white_piece[i][1] * 30 + 4),
                                             white_piece[i][0] * 30 + 26, 300 - (white_piece[i][1] * 30 + 26),
                                             fill="white")
                           )
for i in range(12):
    black_in_canvas.append(board.create_oval(black_piece[i][0] * 30 + 4, 300 - (black_piece[i][1] * 30 + 4),
                                             black_piece[i][0] * 30 + 26, 300 - (black_piece[i][1] * 30 + 26),
                                             fill="black")
                           )
top.mainloop()

