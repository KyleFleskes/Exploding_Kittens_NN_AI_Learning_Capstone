
import random
import numpy as np
import sys
import os
import pickle
import json
import time

from Neural_Networked_Tree.Game.Exploding_Kittens import Game as ek
from Neural_Networked_Tree.Game.Gamestate import ExplodingKittensAbstractGameState as gs

from Neural_Networked_Tree.Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as NNnode
from Vanilia_Tree.Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as Vnode
from Neural_Networked_Tree.Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as NNtree
from Vanilia_Tree.Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as Vtree

# Disable


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore


def enablePrint():
    sys.stdout = sys.__stdout__


winsLosses = []
p0Time = 0
p1Time = 0

p0_search = 6  # used by AI and NN
p1_search = 6
iterations = 100  # https://en.wikipedia.org/wiki/Checking_whether_a_coin_is_fair
player = 'NN'  # can use NN, AI, or random
opponent = 'AI'
for i in range(iterations):
    board_state = gs()
    t0 = None
    t1 = None
    print(i)

    while not board_state.is_game_over():
        turnTimeStart = time.time()

        while board_state.game.currentPlayer == 0:
            if board_state.is_game_over():
                break

            if player == 'AI':
                root = Vnode(board_state)
                if t0:
                    t0.root = root
                else:
                    t0 = Vtree(root)
                blockPrint()
                action = t0.best_action(p1_search)
                enablePrint()
                board_state = board_state.move(action)
                # enablePrint()

            elif player == 'NN':
                root = NNnode(board_state)
                if t0:
                    t0.root = root
                else:
                    t0 = NNtree(
                        root, 'C:/Users/flesk/Desktop/qlearning/Git Exploding Kittens/Reinforcement_Learning_Capstone/Neural_Networked_Tree/Models/Exploding_Cat_Model-big.h5')
                blockPrint()
                action = t0.best_action(p1_search)
                enablePrint()
                board_state = board_state.move(action)
                # enablePrint()

            elif player == 'random':
                blockPrint()
                board_state = board_state.move(random.choice(
                    board_state.get_legal_actions()))
                enablePrint()

            else:
                print('please choose AI or random')

            p0Time += (time.time() - turnTimeStart)

        while board_state.game.currentPlayer == 1:
            if board_state.is_game_over():
                break

            if opponent == 'AI':
                root = Vnode(board_state)
                if t1:
                    t1.root = root
                else:
                    t1 = Vtree(root)
                blockPrint()
                action = t1.best_action(p1_search)
                enablePrint()
                board_state = board_state.move(action)
                # enablePrint()

            elif opponent == 'NN':
                root = NNnode(board_state)
                if t1:
                    t1.root = root
                else:
                    t1 = NNtree(
                         root, 'C:/Users/flesk/Desktop/qlearning/Git Exploding Kittens/Reinforcement_Learning_Capstone/Neural_Networked_Tree/Models/Exploding_Cat_Model-big.h5')
                blockPrint()
                action = t1.best_action(p1_search)
                enablePrint()
                board_state = board_state.move(action)
                # enablePrint()

            elif opponent == 'random':
                blockPrint()
                board_state = board_state.move(random.choice(
                    board_state.get_legal_actions()))
                enablePrint()

            else:
                print('please choose AI or random')

            p1Time += (time.time() - turnTimeStart)

    # print('winner', board_state.game_result())
    winsLosses.append(board_state.game_result())

# print(winsLosses)
entry = {
    'p0_search': p0_search,
    'p1_search': p1_search,
    'iterations': iterations,
    'p0_time': p0Time,
    'p1_time': p1Time,
    'wins': iterations - sum(winsLosses),
    'loss': sum(winsLosses),
    'ratio': ((iterations - sum(winsLosses))/sum(winsLosses) if sum(winsLosses) > 0 else 'NA'),
    'raw': str(winsLosses),
}

fname = 'wins&losses-'+str(iterations)+'-' + \
    str(p0_search)+'-'+str(p1_search)+player+'-vs-'+opponent + '.json'
a = []
if not os.path.isfile(fname):
    a.append(entry)
    with open(fname, mode='w') as f:
        f.write(json.dumps(a, indent=2))
else:
    with open(fname) as feedsjson:
        feeds = json.load(feedsjson)

    feeds.append(entry)
    with open(fname, mode='w') as f:
        f.write(json.dumps(feeds, indent=2))
