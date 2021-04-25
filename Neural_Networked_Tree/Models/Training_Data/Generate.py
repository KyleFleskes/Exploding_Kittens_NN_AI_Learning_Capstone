# This class creates .csv files to be used with training the neural network. 
from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs
import sys
import os
import csv

class Generate:

    def __init__(self, model_fpath, csv_fpath):
        self.model_fpath = model_fpath
        self.csv_fpath = csv_fpath
        self.tree = None

    def gen_data(self):
        board_state = gs(make_data=True)
        root = node(board_state)
        self.tree = tree(root, self.model_fpath)
        print(board_state.get_obsersavtion_space())
        self.blockPrint()
        self.tree.best_action(10000)
        self.enablePrint()
        self.pprint_tree(root)
        with open(self.csv_fpath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Kitten Card(Should always be zero)", "Attack", "Skip", "Favor",\
                "Shuffle", "See-The-Future", "Draw-From-Bottom", "Defuse", "Taco", "Watermelon",\
                "Potato", "Beard", "Rainbow", "Draw", "Last Card Played Index", "Cards in Deck",\
                "Kitten Card Winrate",\
                "Attack Winrate", "Skip Winrate", "Favor Winrate", "Shuffle Winrate",\
                "See-The-Future Winrate", "Draw-From-Bottom Winrate", "Defuse Winrate",\
                "Taco Winrate", "Watermelon Winrate", "Potato Winrate", "Beard Winrate",\
                "Rainbow Winrate", "Draw Winrate"])
    
    # Does a pretty print of the search tree.
    def pprint_tree(self, n, file=None, _prefix="", _last=True):
        print(_prefix, "`- " if _last else "|- ", "P:", n.state.game.currentPlayer, " ",
            n.state.get_obsersavtion_space(), "#'s visited: ", n.n, " #'s wins: ", list(n._results.values())[n.state.game.currentPlayer], " #'s loses: ", list(n._results.values())[n.state.game.currentPlayer - 1], sep="", file=file)
        _prefix += "   " if _last else "|  "
        child_count = len(n.children)
        for i, child in enumerate(n.children):
            _last = i == (child_count - 1)
            self.pprint_tree(child, file, _prefix, _last)

    # Disable
    def blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint(self):
        sys.stdout = sys.__stdout__