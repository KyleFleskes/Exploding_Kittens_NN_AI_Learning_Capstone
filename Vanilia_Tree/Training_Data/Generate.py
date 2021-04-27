# This class creates .csv files to be used with training the neural network. 
from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs
import sys
import os
import csv

class Generate:

    def __init__(self, csv_fpath):
        self.csv_fpath = csv_fpath
        self.tree = None

    def gen_data(self):
        
        board_state = gs()
        root = node(board_state)
        self.tree = tree(root)
        
        self.blockPrint()
        self.tree.best_action(1000000)
        self.enablePrint()

        pprint_tree(root)
        
        self.build_data(root)
        


    # Disable
    def blockPrint(self):
        sys.stdout = open(os.devnull, 'w')

    # Restore
    def enablePrint(self):
        sys.stdout = sys.__stdout__


    # This uses the generated MCTS and extracts data for NN to train on.
    def build_data(self, node):
        visited = []   # List to keep track of visited nodes.
        queue = []     # Initialize a queue
        
        visited.append(node)
        queue.append(node)
        with open(self.csv_fpath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Exploding Kitten", "Attack", "Skip", "Favor",\
                "Shuffle", "See-The-Future", "Draw-From-Bottom", "Defuse", "Taco", "Watermelon",\
                "Potato", "Beard", "Rainbow", "Last Card Played Index", "Cards in Deck",\
                "Attack Winrate", "Skip Winrate", "Favor Winrate", "Shuffle Winrate",\
                "See-The-Future Winrate", "Draw-From-Bottom Winrate", "Defuse Winrate",\
                "Taco Winrate", "Watermelon Winrate", "Potato Winrate", "Beard Winrate",\
                "Rainbow Winrate", "Draw Winrate"])

            counter = 0
            #do a breadth first search of the MCTS.
            while queue:
                
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
                
                count = 0

                for win in winrates:
                    if win > 0:
                        count = count + 1

                if count > 4:
                    writer.writerow(row)
                
        
# Does a pretty print of the search tree.
def pprint_tree( node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", "P:", node.state.game.currentPlayer, " ",
        node.state.get_obsersavtion_space(), "#'s visited: ", node.n, " #'s wins: ",\
        list(node._results.values())[node.state.game.currentPlayer], " #'s loses: ",\
        list(node._results.values())[node.state.game.currentPlayer - 1], " Action: ",\
        node.action, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)