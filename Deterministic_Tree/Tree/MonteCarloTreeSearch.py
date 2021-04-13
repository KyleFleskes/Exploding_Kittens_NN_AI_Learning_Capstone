# This is a modified version of the online available Monte Carlo Search Tree 
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
class MonteCarloTreeSearch(object):

    # Creates a tree with the passed node as the root.
    def __init__(self, node):
        """
        MonteCarloTreeSearchNode
        Parameters
        ----------
        node : mctspy.tree.nodes.MonteCarloTreeSearchNode
        """
        self.root = node

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
            reward = v.rollout()
            # update the tree with the simulated game result.
            v.backpropagate(reward)
        # to select best child with no exploitation.
        return self.root.best_child(c_param=0.)

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

    