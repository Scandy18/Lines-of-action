import math
import sys
import random
import copy


MAX_ROUND = 200
################### init bot = 1 player = 0


class State(object):
    def __init__(self):
        self.current_value = 0.0
        self.board = None
        self.current_round_index = 0
        self.winner = 0
        self.player = 0
        self.pieces = []
        self.legal_move_list = []
        self.cumulative_choices = []

    def get_cumulative_choices(self):
        return self.cumulative_choices

    def set_cumulative_choices(self, choice):
        self.cumulative_choices = choice

    def get_current_round_index(self):
        return self.current_round_index

    def set_current_round_index(self, turn):
        self.current_round_index = turn

    def compute_reward(self):
        if self.winner == 1:
            return 1
        elif self.winner == 0:
            return -1
        else:
            print("error, compute_reward not called correctly")

    def set_value(self, value):
        self.current_value = value

    def set_player(self, player):
        self.player = player
        # 0 player
        # 1 bot player

    def set_pieces(self):

        if self.player == 1:
            self.pieces = black_piece
        else:
            self.pieces = white_piece
################not soluted :global virable

    def get_pieces(self):
        return self.pieces

    def get_legal_move_list(self):
        return self.legal_move_list

    def set_current_board(self, board):
        self.board = copy.deepcopy(board)

    def update_board(self, piece, move):  # tell board the move
        self.board = self.board  # need change

    def get_next_state(self):

        random_piece_choice = random.choice([choice for choice in self.get_pieces()])

        self.legal_move_list = legal_move(random_piece_choice,self.board)
        random_move_choice = random.choice([choice for choice in self.get_legal_move_list()])

        self.update_board(random_piece_choice, random_move_choice)  # update board

        next_state = State()
        next_state.set_current_board(LineOfA.board_situation)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_player(self.player)
        next_state.set_cumulative_choices(self.get_cumulative_choices() + [random_piece_choice, random_move_choice])
        next_state.check_winner()
        #
        return next_state
#############################################judge winner 
    #can't call

    def check_winner(self):
        self.winner = LineOfA.judgeWin()

    def is_terminal(self):
    
        if self.winner != 0:  # find winner
            return True
        elif self.current_round_index == MAX_ROUND:  # too many round and no winner
            return True
        else:
            return False

    def __repr__(self):
        return "State: {}, value: {}, round: {}, choices: {}".format(hash(self), self.current_value,
                                                                     self.current_round_index,
                                                                     self.cumulative_choices)


class TreeNode:
    def __init__(self):
        self.parent = None
        self.children = {}
        self.visit_number = 0
        self.quality_value = 0.0
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_state().get_pieces())

    def get_children(self):
        return self.children

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def get_visit_number(self):
        return self.visit_number

    def get_quality_value(self):
        return self.quality_value

    def quality_value_add(self, n):
        self.quality_value += n

    def set_quality_value(self, value):
        self.quality_value = value

    def set_visit_number(self, number):
        self.visit_number = number

    def visit_number_add_one(self):
        self.visit_number += 1

    def __repr__(self):
        return "TreeNode: {}, Q/N:{}/{}, state: {}".format(hash(self), self.quality_value, self.visit_number,
                                                           self.state)


def tree_policy(node):
    while not node.get_state().is_terminal():
        if node.is_fully_expanded():
            node = best_child(node, True)
        else:
            return expand(node)
    return node


def expand(node):
    tried_sub_node_states = [
        sub_node.get_state() for sub_node in node.get_children()
    ]
    new_state = node.get_state().get_next_state()
    while new_state in tried_sub_node_states:
        new_state = node.get_state().get_next_state()
    sub_node = TreeNode()
    sub_node.set_state(new_state)
    node.add_child(sub_node)
    return sub_node


def play_out(node):  # need evaluation function for reward
    current_state = node.get_state()
    height = 1
    while not current_state.is_terminal():
        height += 1
        current_state = current_state.get_next_state()
    final_state_reward = current_state.compute_reward()/height
    # final reward = winorlose / height
    return final_state_reward


def best_child(node, is_exploration):
    best_score = -sys.maxsize
    best_sub_node = None

    for child in node.get_children():
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0
        left = child.get_quality_value() / child.get_vistit_number()
        right = 2.0 * math.log(node.get_visit_number()) / child.get_vistit_number()
        score = left + C * math.sqrt(right)
        #log_total = log(sum(Psteps[(player, S)])for player,S in moves_state)
        #score = (wins_list[(player,S)] / Psteps[(player,S)]) + C * sqrt(log_total / Psteps[(player,S)]), for player,S in moves_state)
        if score > best_score:
            best_score = score
            best_sub_node = child
    return best_sub_node


def back_propagation(node, reward):
    while node is not None:
        node.visit_number_add_one()
        node.quality_value_add(reward)
        node = node.parent


def MCTS(node):
    computation_budget = 2  #
    for i in range(computation_budget):
        expand_node = tree_policy(node)
        reward = play_out(expand_node)
        back_propagation(expand_node, reward)
    best_next_node = best_child(node, False)
    return best_next_node


def MCT_step():#need varibles:
               #board_situation,balck
    init_state = State()
    bot_player = 1  # set white
    init_state.set_player(1) #bot player
    init_state.set_current_board(board_situation)
    init_state.set_pieces()
    init_node = TreeNode()
    init_node.set_state(init_state)
    current_node = init_node
    for i in range(10): # set round
        current_node = MCTS(current_node)
        best_move = current_node.get_state().get_cumulative_choices()[-1]
        # tell board to apply the best move
        # human play
        current_node.get_state().set_current_board(LineOfA.board_situation) # update node board for human's move
        current_node.set_pieces()
