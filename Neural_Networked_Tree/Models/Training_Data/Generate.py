# This class creates .csv files to be used with training the neural network. 
from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs

class Generate:

    def __init__(self, model_fpath, csv_fpath):
        self.model_fpath = model_fpath
        self.csv_fpath = csv_fpath
        self.tree = None

    def gen_data():
        board_state = gs()
        root = node(board_state)
        self.tree = tree(root, self.fpath)