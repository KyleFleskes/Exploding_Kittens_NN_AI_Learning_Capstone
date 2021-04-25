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
        
        self.blockPrint()
        self.tree.best_action(100)
        self.enablePrint()

        self.pprint_tree(root)
        
        self.build_data(root, 10)
        
    # Does a pretty print of the search tree.
    def pprint_tree(self, n, file=None, _prefix="", _last=True):
        print(_prefix, "`- " if _last else "|- ", "P:", n.state.game.currentPlayer, " ",
            n.state.get_obsersavtion_space(), "#'s visited: ", n.n, " #'s wins: ", list(n._results.values())[n.state.game.currentPlayer], " #'s loses: ", list(n._results.values())[n.state.game.currentPlayer - 1], " Action: ", n.action,sep="", file=file)
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


    # This uses the generated MCTS and extracts data for NN to train on.
    def build_data(self, node, entries):
        visited = []   # List to keep track of visited nodes.
        queue = []     # Initialize a queue
        
        visited.append(node)
        queue.append(node)
        with open(self.csv_fpath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Attack", "Skip", "Favor",\
                "Shuffle", "See-The-Future", "Draw-From-Bottom", "Defuse", "Taco", "Watermelon",\
                "Potato", "Beard", "Rainbow", "Draw", "Last Card Played Index", "Cards in Deck",\
                "Attack Winrate", "Skip Winrate", "Favor Winrate", "Shuffle Winrate",\
                "See-The-Future Winrate", "Draw-From-Bottom Winrate", "Defuse Winrate",\
                "Taco Winrate", "Watermelon Winrate", "Potato Winrate", "Beard Winrate",\
                "Rainbow Winrate", "Draw Winrate"])

            counter = 0
            #do a breadth first search of the MCTS.
            while queue:

                # if generated specificed entries.
                if counter is entries:
                    return
                
                node = queue.pop(0)

                #print(node.state.get_obsersavtion_space(), end = " ") 
                row = node.state.get_obsersavtion_space()
                winrates = [0,0,0,0,0,0,0,0,0,0,0,0,0]

                # for each child of current node.
                for child in node.children:
                    # check if that action to get to child is the card types.
                    for key in node.state.indexToChoice:
                        # if card type makes card index.
                        if node.state.indexToChoice[key] is child.action:
                            
                            wins = list(child._results.values())[child.state.game.currentPlayer]
                            loses = list(child._results.values())[child.state.game.currentPlayer - 1]
                            #print(key, " = ",child.action)
                            #print(wins, " ", loses) 
                            if wins + loses is not 0:
                                winrates[key - 1] = wins / (wins + loses)

                        

                for child in node.children: 
                    if child not in visited:
                        visited.append(child)
                        queue.append(child)
                row = row + winrates
                writer.writerow(row)
                counter = counter + 1
        
       