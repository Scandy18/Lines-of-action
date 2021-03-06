import tkinter
import copy
import Jud
import MCTS
import time

total_time_cost = 0
SIDE = 1  # white:0, black:1
SELECTED = 0  # white:1 black:2
SELECTED_WHITE_PIECE = 0
SELECTED_BLACK_PIECE = 0
# tag of pieces
white_in_canvas = []
black_in_canvas = []
legal_move_marks = []
#  pos in board
black_piece_count = 12
black_piece = [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1],
               [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8]]
white_piece_count = 12
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


def reset():
    global SIDE
    global SELECTED
    global SELECTED_BLACK_PIECE
    global SELECTED_WHITE_PIECE
    global black_piece
    global white_piece
    global black_piece_count
    global white_piece_count
    global board_situation
    global line_count
    global left_side_mark
    if not SIDE:
        right_side.delete(right_side_mark)
        left_side_mark = left_side.create_oval(39, 139, 61, 161, fill="black")
    del_legal_move_marks()
    SIDE = 1
    SELECTED = 0
    SELECTED_BLACK_PIECE = 0
    SELECTED_WHITE_PIECE = 0
    black_piece.clear()
    black_piece = [[2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1],
                   [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8]]
    black_piece_count = 12
    white_piece.clear()
    white_piece = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
                   [8, 2], [8, 3], [8, 4], [8, 5], [8, 6], [8, 7]]
    white_piece_count = 12
    board_situation = [[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, 0, 1, 1, 1, 1, 1, 1, 0],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 2, 0, 0, 0, 0, 0, 0, 2],
                       [-1, 0, 1, 1, 1, 1, 1, 1, 0]]
    line_count.clear()
    line_count = [2] * 42
    line_count[0] = line_count[7] = line_count[8] = line_count[15] = 6
    line_count[22] = line_count[35] = 0
    for i in range(12):
        board.coords(black_in_canvas[i],
                     black_piece[i][0] * 30 + 4, 300 - (black_piece[i][1] * 30 + 4),
                     black_piece[i][0] * 30 + 26, 300 - (black_piece[i][1] * 30 + 26))
    for i in range(12):
        board.coords(white_in_canvas[i],
                     white_piece[i][0] * 30 + 4, 300 - (white_piece[i][1] * 30 + 4),
                     white_piece[i][0] * 30 + 26, 300 - (white_piece[i][1] * 30 + 26))


def legal_move(piece):
    x: int = piece[0]
    y: int = piece[1]
    move_list = []
    # up-down
    pace = line_count[x + 7]
    if y + pace <= 8:
        flag = True
        for i in range(1, pace):
            if board_situation[x][y + i] != SIDE + 1 and board_situation[x][y + i] != 0:
                flag = False
                break
        if board_situation[x][y + pace] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x, y + pace])
    if y - pace >= 1:
        flag = True
        for i in range(1, pace):
            if board_situation[x][y - i] != SIDE + 1 and board_situation[x][y - i] != 0:
                flag = False
                break
        if board_situation[x][y - pace] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x, y - pace])
    # left-right
    pace = line_count[y - 1]
    if x + pace <= 8:
        flag = True
        for i in range(1, pace):
            if board_situation[x + i][y] != SIDE + 1 and board_situation[x + i][y] != 0:
                flag = False
                break
        if board_situation[x + pace][y] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x + pace, y])
    if x - pace >= 1:
        flag = True
        for i in range(1, pace):
            if board_situation[x - i][y] != SIDE + 1 and board_situation[x - i][y] != 0:
                flag = False
                break
        if board_situation[x - pace][y] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x - pace, y])
    # 2-4
    pace = line_count[x + y + 13]
    if x + pace <= 8 and y - pace >= 1:
        flag = True
        for i in range(1, pace):
            if board_situation[x + i][y - i] != SIDE + 1 and board_situation[x + i][y - i] != 0:
                flag = False
                break
        if board_situation[x + pace][y - pace] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x + pace, y - pace])
    if x - pace >= 1 and y + pace <= 8:
        flag = True
        for i in range(1, pace):
            if board_situation[x - i][y + i] != SIDE + 1 and board_situation[x - i][y + i] != 0:
                flag = False
                break
        if board_situation[x - pace][y + pace] == SIDE + 1:
            flag = False
        if flag:
            move_list.append([x - pace, y + pace])
    # 1-3
    if x != 8 or y != 1:
        pace = line_count[x - y + 35]
        if x + pace <= 8 and y + pace <= 8:
            flag = True
            for i in range(1, pace):
                if board_situation[x + i][y + i] != SIDE + 1 and board_situation[x + i][y + i] != 0:
                    flag = False
                    break
            if board_situation[x + pace][y + pace] == SIDE + 1:
                flag = False
            if flag:
                move_list.append([x + pace, y + pace])
        if x - pace >= 1 and y - pace >= 1:
            flag = True
            for i in range(1, pace):
                if board_situation[x - i][y - i] != SIDE + 1 and board_situation[x - i][y - i] != 0:
                    flag = False
                    break
            if board_situation[x - pace][y - pace] == SIDE + 1:
                flag = False
            if flag:
                move_list.append([x - pace, y - pace])
    return move_list


def print_legal_move_marks(marklist):
    global legal_move_marks
    for m in marklist:
        legal_move_marks.append(board.create_line(m[0] * 30 + 15, 300 - (m[1] * 30 + 10),
                                                  m[0] * 30 + 15, 300 - (m[1] * 30 + 20),
                                                  fill="red"))
        legal_move_marks.append(board.create_line(m[0] * 30 + 10, 300 - (m[1] * 30 + 15),
                                                  m[0] * 30 + 20, 300 - (m[1] * 30 + 15),
                                                  fill="red"))


def del_legal_move_marks():
    global legal_move_marks
    for m in legal_move_marks:
        board.delete(m)
    legal_move_marks.clear()


def AI_move():
    global total_time_cost
    global SIDE
    global left_side_mark
    global black_piece_count
    if not SIDE:  # white bot
        time_start = time.time()
        ret = MCTS.MCT_step(board_situation, black_piece, white_piece, line_count, black_piece_count, white_piece_count)
        time_end = time.time()
        time_cost = round(time_end - time_start, 4)
        total_time_cost += time_cost
        print(ret)
        print('totally cost = ', time_cost, 's')
        if time_cost > 60:
            print("black win")
        move_piece_index = white_piece.index(ret[0])
        oldx = ret[0][0]
        oldy = ret[0][1]
        posx = ret[1][0]
        posy = ret[1][1]
        # update board situation
        board_situation[oldx][oldy] = 0
        board_situation[posx][posy] = 1
        line_count[oldx + 7] = line_count[oldx + 7] - 1
        line_count[oldy - 1] = line_count[oldy - 1] - 1
        line_count[oldx + oldy + 13] = line_count[oldx + oldy + 13] - 1
        if oldx != 8 or oldy != 1:
            line_count[oldx - oldy + 35] = line_count[oldx - oldy + 35] - 1
        # update piece info
        white_piece[move_piece_index] = [posx, posy]
        # update canvas
        board.coords(white_in_canvas[move_piece_index],
                     posx * 30 + 4, (9 - posy) * 30 + 4,
                     posx * 30 + 26, (9 - posy) * 30 + 26
                     )
        # eat piece
        if [posx, posy] in black_piece:  # one black out
            board.coords(black_in_canvas[black_piece.index([posx, posy])], 301, 301, 301, 301)  # move out
            black_piece[black_piece.index([posx, posy])] = [114, 114]
            black_piece_count = black_piece_count - 1
        else:
            line_count[posx + 7] = line_count[posx + 7] + 1
            line_count[posy - 1] = line_count[posy - 1] + 1
            line_count[posx + posy + 13] = line_count[posx + posy + 13] + 1
            if posx != 8 or posy != 1:
                line_count[posx - posy + 35] = line_count[posx - posy + 35] + 1
        # change side to black
        SIDE = 1
        right_side.delete(right_side_mark)
        left_side_mark = left_side.create_oval(39, 139, 61, 161, fill="black")


def mouse_call(event):
    posx = event.x // 30  # 1-8
    posy = 9 - event.y // 30  # 8-1
    global SIDE
    global SELECTED
    global SELECTED_BLACK_PIECE
    global SELECTED_WHITE_PIECE
    global black_piece
    global white_piece
    global black_piece_count
    global white_piece_count
    global left_side_mark
    global right_side_mark
    if not SELECTED:
        if SIDE and [posx, posy] in black_piece:  # black and clicked a black piece
            SELECTED = 1
            SELECTED_BLACK_PIECE = black_piece.index([posx, posy])
            print("Select Black", SELECTED_BLACK_PIECE)
            print_legal_move_marks(legal_move(black_piece[SELECTED_BLACK_PIECE]))

        # if not SIDE and [posx, posy] in white_piece:  # white and clicked a white piece
        #     print("AI side:")
        #     print(MCTS.MCT_step(board_situation, black_piece, white_piece, line_count, black_piece_count, white_piece_count))
        #     SELECTED = 1
        #     SELECTED_WHITE_PIECE = white_piece.index([posx, posy])
        #     print("Select White", SELECTED_WHITE_PIECE)
        #     print_legal_move_marks(legal_move(white_piece[SELECTED_WHITE_PIECE]))
    else:
        if SIDE:  # black
            if [posx, posy] == black_piece[SELECTED_BLACK_PIECE]:  # click the selected piece
                SELECTED = 0
                del_legal_move_marks()
                print("Release piece")
            elif [posx, posy] in legal_move(black_piece[SELECTED_BLACK_PIECE]):
                SELECTED = 0
                del_legal_move_marks()
                oldx = black_piece[SELECTED_BLACK_PIECE][0]
                oldy = black_piece[SELECTED_BLACK_PIECE][1]
                # update board situation
                board_situation[oldx][oldy] = 0  # empty
                board_situation[posx][posy] = 2  # black
                # update line of board
                line_count[oldx + 7] = line_count[oldx + 7] - 1
                line_count[oldy - 1] = line_count[oldy - 1] - 1
                line_count[oldx + oldy + 13] = line_count[oldx + oldy + 13] - 1
                if oldx != 8 or oldy != 1:
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
                    board.coords(white_in_canvas[white_piece.index([posx, posy])], 301, 301, 301, 301)  # move out
                    white_piece[white_piece.index([posx, posy])] = [114, 114]
                    white_piece_count = white_piece_count - 1
                else:
                    line_count[posx + 7] = line_count[posx + 7] + 1
                    line_count[posy - 1] = line_count[posy - 1] + 1
                    line_count[posx + posy + 13] = line_count[posx + posy + 13] + 1
                    if posx != 8 and posy != 1:
                        line_count[posx - posy + 35] = line_count[posx - posy + 35] + 1
                # change side to white
                SIDE = 0
                left_side.delete(left_side_mark)
                right_side_mark = right_side.create_oval(39, 139, 61, 161, fill="white")
        # else:  # white
        #     if [posx, posy] == white_piece[SELECTED_WHITE_PIECE]:  # click the selected piece
        #         SELECTED = 0
        #         del_legal_move_marks()
        #         print("Release piece")
        #     elif [posx, posy] in legal_move(white_piece[SELECTED_WHITE_PIECE]):
        #         SELECTED = 0
        #         del_legal_move_marks()
        #         oldx = white_piece[SELECTED_WHITE_PIECE][0]
        #         oldy = white_piece[SELECTED_WHITE_PIECE][1]
        #         # update board situation
        #         board_situation[oldx][oldy] = 0  # empty
        #         board_situation[posx][posy] = 1  # white
        #         # update line of board
        #         line_count[oldx + 7] = line_count[oldx + 7] - 1
        #         line_count[oldy - 1] = line_count[oldy - 1] - 1
        #         line_count[oldx + oldy + 13] = line_count[oldx + oldy + 13] - 1
        #         if oldx != 8 or oldy != 1:
        #             line_count[oldx - oldy + 35] = line_count[oldx - oldy + 35] - 1
        #         # update piece info
        #         white_piece[SELECTED_WHITE_PIECE] = [posx, posy]
        #         # update canvas
        #         board.coords(white_in_canvas[SELECTED_WHITE_PIECE],
        #                      posx * 30 + 4, (9 - posy) * 30 + 4,
        #                      posx * 30 + 26, (9 - posy) * 30 + 26
        #                      )
        #         # eat piece
        #         if [posx, posy] in black_piece:  # one black out
        #             board.coords(black_in_canvas[black_piece.index([posx, posy])], 301, 301, 301, 301)  # move out
        #             black_piece[black_piece.index([posx, posy])] = [114, 114]
        #             black_piece_count = black_piece_count - 1
        #         else:
        #             line_count[posx + 7] = line_count[posx + 7] + 1
        #             line_count[posy - 1] = line_count[posy - 1] + 1
        #             line_count[posx + posy + 13] = line_count[posx + posy + 13] + 1
        #             if posx != 8 or posy != 1:
        #                 line_count[posx - posy + 35] = line_count[posx - posy + 35] + 1
        #         # change side to black
        #         SIDE = 1
        #         right_side.delete(right_side_mark)
        #         left_side_mark = left_side.create_oval(39, 139, 61, 161, fill="black")
        winres = Jud.judgeWin(black_piece,white_piece,black_piece_count,white_piece_count,board_situation)
        if winres == 1:
            print("black win")
            print(total_time_cost)
        elif winres == -1:
            print("white win")
            print(total_time_cost)


top = tkinter.Tk()
top.title("Line of Action")
top.geometry('500x500')
top.resizable(width=False, height=False)

'''
board region
'''
board = tkinter.Canvas(top, width=300, height=300, bg='Beige')
board.bind("<Button-1>", mouse_call)
#
board.pack()
for i in range(1, 9):
    for j in range(1, 9):
        board.create_rectangle(i * 30, j * 30, i * 30 + 30, j * 30 + 30)
board.create_rectangle(29, 29, 271, 271)
board.create_text(150, 15, text='A  B  C  D  E  F  G  H', font="Courier 13 bold")
board.create_text(150, 285, text='A  B  C  D  E  F  G  H', font="Courier 13 bold")
for i in range(8):
    board.create_text(15, 45 + 30 * i, text=8 - i, font="Courier 13 bold")
    board.create_text(285, 45 + 30 * i, text=8 - i, font="Courier 13 bold")
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

# reset button
tkinter.Button(top, text="RESET", command=reset).place(width=80, height=50, x=210, y=400)
tkinter.Button(top, text="AI Move", command=AI_move).place(width=80, height=50, x=210, y=325)
# player region
# left is black
left_side = tkinter.Canvas(top, width=100, height=300)
left_side.create_text(50, 100, text='BLACK', font="Courier 16 bold")
if SIDE:
    left_side_mark = left_side.create_oval(39, 139, 61, 161, fill="black")
left_side.place(x=0, y=0)
# right is white
right_side = tkinter.Canvas(top, width=100, height=300)
right_side.create_text(50, 100, text='WHITE', font="Courier 16 bold")
if not SIDE:
    right_side_mark = left_side.create_oval(39, 139, 61, 161, fill="white")
right_side.place(x=400, y=0)

top.mainloop()
