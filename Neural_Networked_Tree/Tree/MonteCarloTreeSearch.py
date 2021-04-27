# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Activation, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
import os.path
import numpy as np
import tensorflow as tf
config = tf.compat.v1.ConfigProto(gpu_options=tf.compat.v1.GPUOptions(
    per_process_gpu_memory_fraction=0.8)
    # device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(session)


class MonteCarloTreeSearch(object):

    # Creates a tree with the passed node as the root.
    def __init__(self, node, fpath):
        """
        MonteCarloTreeSearchNode
        Parameters
        ----------
        node : mctspy.tree.nodes.MonteCarloTreeSearchNode
        """
        self.root = node
        self.fpath = fpath

        # if a neural network does not exist then create one.
        if os.path.isfile(fpath) is False:
            print("!!!Creating new model!!!")
            self.model = self.create_model()
            self.save_model()

        # load previously created model.
        else:
            self.model = tf.keras.models.load_model(fpath, compile=False)
            print("!!!!Loading model from file!!!!")

    # creates a new model with an input layer with 12 nodes, 2 hiddens layers each with size 11 and 10 respectively
    # and 1 output layers each with size 10.
    def create_model(self):
        model = Sequential([
            # creates first hidden layer(Second overall layer),
            Dense(units=15, input_shape=(15,), activation='relu'),
            # with 15 nodes,
            # with an input layer of shape (1,).
            Dense(units=15, activation='relu'),
            Dropout(0.25),
            Dense(units=15, activation='relu'),
            # create an output layer with 13 output nodes.
            Dense(units=13, activation='sigmoid')
        ])
        #model.compile(optimizer=Adam(learning_rate=0.1),
        #              loss='categorical_crossentropy', metrics=['accuracy'])
        model.compile(optimizer=Adam(learning_rate=0.0001),
                      loss='mean_squared_error',
                      metrics=['accuracy'])

        return model

    # saves the current state of the model.
    def save_model(self):
        self.model.save(self.fpath)
        print("!!!Model saved!!!")

    # Explores the gamespace using MCTS where the number of games is specified by the parameter.
    # Returns what the tree thinks is the "best" next action based upon the tree exploration.
    def best_action(self, simulations_number):
        """
        Parameters
        ----------
        simulations_number : int
            number of simulations performed to get the best action
        Returns
        -------
        """
        # simulate "simulations_number" of games in the tree.
        for _ in range(0, simulations_number):

            # get the node that the MCTS wants to explore.
            v = self._tree_policy()
            # simulate the game until a win or a loss.
            reward = v.rollout(self.model)
            #print("Reward: ", reward)
            # update the tree with the simulated game result.
            # print("Backpropagating....")
            v.backpropagate(reward)
        # to select best child with no exploitation.
        return self.root.best_child(c_param=0.).action

    # Starts at the root of the tree and finds the first unexplored action of the most
    # profitable nodes in the tree.
    def _tree_policy(self):
        """
        selects node to run rollout/playout for
        Returns
        -------
        """
        current_node = self.root
        # while current node is not a game ending state.
        while not current_node.is_terminal_node():
            # if current node has not explored all available actions,
            # then create and return a child node from one those actions.
            if not current_node.is_fully_expanded():
                return current_node.expand()
            # if current node has explored all available actions,
            # then pick the most profitable action and make it the new current node.
            else:
                current_node = current_node.best_child()
        return current_node
