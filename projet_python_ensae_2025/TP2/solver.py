import numpy as np
from grid import Grid

class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the score of the list of pairs in self.pairs
        """
        output = 0
        for pair in self.pairs:
            output += abs(pair[0]-pair[1])
        return output

class SolverEmpty(Solver):
    def run(self):
        pass

class SolverGreedy(Solver):
    def run(self):
        if self.grid.all_pairs == [] :
            return self.pairs
        else :
            list_cost = [self.cost(pair) for pair in self.grid.all_pairs]
            pair_min = self.grid.all_pairs[np.argmin(list_cost)]
            self.pairs.append(pair_min)
            self.grid.color[pair_min[0][0]][pair_min[0][1]] == 4
            self.grid.color[pair_min[1][0]][pair_min[1][1]] == 4
            return self.run


        






