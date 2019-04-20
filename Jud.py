#######################################################
# use of judge win
# 1.每次吃掉某个子需要从数组中删掉
# 2.为了避免超出范围board_situation下面可以加一层（目前check_map复制之后先手动加了右面与下面一层）
# 3.未测试
# judge winner:
#    1 : black win
#    0  : not end
#    -1  : white win
import copy

con_count = 0  # the count of continuously piece 
check_map = []


def black_DFS(x, y):
    global con_count
    global check_map
    check_map[x][y] = 20
    con_count += 1
    if check_map[x - 1][y - 1] == 2:
        black_DFS(x - 1, y - 1)
    if check_map[x - 1][y] == 2:
        black_DFS(x - 1, y)
    if check_map[x - 1][y + 1] == 2:
        black_DFS(x - 1, y + 1)
    if check_map[x][y - 1] == 2:
        black_DFS(x, y - 1)
    if check_map[x][y + 1] == 2:
        black_DFS(x, y + 1)
    if check_map[x + 1][y - 1] == 2:
        black_DFS(x + 1, y - 1)
    if check_map[x + 1][y] == 2:
        black_DFS(x + 1, y)
    if check_map[x + 1][y + 1] == 2:
        black_DFS(x + 1, y + 1)


def white_DFS(x, y):
    global con_count
    global check_map
    check_map[x][y] = 10
    con_count += 1
    if check_map[x - 1][y - 1] == 1:
        white_DFS(x - 1, y - 1)
    if check_map[x - 1][y] == 1:
        white_DFS(x - 1, y)
    if check_map[x - 1][y + 1] == 1:
        white_DFS(x - 1, y + 1)
    if check_map[x][y - 1] == 1:
        white_DFS(x, y - 1)
    if check_map[x][y + 1] == 1:
        white_DFS(x, y + 1)
    if check_map[x + 1][y - 1] == 1:
        white_DFS(x + 1, y - 1)
    if check_map[x + 1][y] == 1:
        white_DFS(x + 1, y)
    if check_map[x + 1][y + 1] == 1:
        white_DFS(x + 1, y + 1)


def judgeWin(black_piece,white_piece,black_piece_count,white_piece_count,board_situation): 
    global con_count
    global check_map
    check_map = copy.deepcopy(board_situation)
    #   expand the size to avoid out of index
    for i in range(0, 9):
        check_map[i].append(-1)
    check_map.append([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
    if white_piece_count == 1:
        return 1
    if black_piece_count == 1:
        return -1

    #   check black
    con_count = 0
    for i in range(0, 12):
        if black_piece[i][0] != 114:
            break
    check_x = black_piece[i][0]
    check_y = black_piece[i][1]
    #   for i in range(0,len(black_piece)):
    #    check_list.append(0)   #0 represent not check
    black_DFS(check_x, check_y)
    if con_count == black_piece_count:
        return 1

    #   check white
    con_count = 0
    for i in range(0, 12):
        if white_piece[i][0] != 114:
            break
    check_x = white_piece[i][0]
    check_y = white_piece[i][1]
    white_DFS(check_x, check_y)
    if con_count == white_piece_count:
        return -1

    return 0
