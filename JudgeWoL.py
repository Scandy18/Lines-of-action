#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:03:00 2019

@author: zhe
"""

"""
1.每次吃掉某个子需要从数组中删掉
2.为了避免超出范围board_situation下面可以加一层（目前check_map复制之后先手动加了右面与下面一层）
3.未测试
judge winer:
    1 : black win
    0  : not end
    -1  : white win
"""
count = 0
check_map = []

def black_DFS(x,y):
    global count
    global check_map
    check_map[x][y] == 10
    count += 1
    if check_map[x-1][y-1] == 1:
        black_DFS(x-1,y-1)    
    if check_map[x - 1][y] == 1:
        black_DFS(x-1,y)
    if check_map[x-1][y+1] == 1:
        black_DFS(x-1,y+1)
    if check_map[x][y - 1] == 1:
        black_DFS(x,y-1)
    if check_map[x][y + 1] == 1:
        black_DFS(x,y+1)
    if check_map[x+1][y-1] == 1:
        black_DFS(x+1,y-1)
    if check_map[x + 1][y] == 1:
        black_DFS(x+1,y)
    if check_map[x+1][y+1] == 1:
        black_DFS(x+1,y+1)   
        
def white_DFS(x,y):
    global count
    global check_map
    check_map[x][y] == 20
    count += 1
    if check_map[x-1][y-1] == 2:
        white_DFS(x-1,y-1)    
    if check_map[x - 1][y] == 2:
        white_DFS(x-1,y)
    if check_map[x-1][y+1] == 2:
        white_DFS(x-1,y+1)
    if check_map[x][y - 1] == 2:
        white_DFS(x,y-1)
    if check_map[x][y + 1] == 2:
        white_DFS(x,y+1)
    if check_map[x+1][y-1] == 2:
        white_DFS(x+1,y-1)
    if check_map[x + 1][y] == 2:
        white_DFS(x+1,y)
    if check_map[x+1][y+1] == 2:
        white_DFS(x+1,y+1) 
        
def judgeWin():
    global black_piece
    global white_piece
    global count
    global check_map
    global board_situation
    black_count = len(black_piece)
    white_count = len(white_piece)
    check_map = board_situation
    #expand the size to avoid out of index
    for i in range(0,9):
        check_map[i].append(-1)
    check_map.append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
    if black_count == 1:
        return -1
    if white_count == 1:
        return 1
    
    #check black
    count = 0
    check_x = black_piece[0][0]
    check_y = black_piece[0][1]
    #for i in range(0,len(black_piece)):
    #    check_list.append(0)   #0 represent not check
    black_DFS(check_x,check_y)
    if count == black_count:
        return 1

    #check white
    count = 0
    check_x = white_piece[0][0]
    check_y = white_piece[0][1]
    white_DFS(check_x,check_y)
    if count == white_count:
        return -1
    
    return 0