import numpy as np

class HungarianAlg(object):
        
    def __init__(self, cost_matrix):
        '''
        This creates a HungarianAlg object with the cost matrix associated to it. It stores a copy of the matrix as well as the original.
        It then records the shape and initiates some helper variables, like the covers for the rows and columns and the markings.
        '''
        self.O = cost_matrix
        self.C = cost_matrix.copy()  # Removed deep=True
        self.n, self.m = self.C.shape
        self.row_covered = np.zeros(self.n, dtype=bool)
        self.col_covered = np.zeros(self.m, dtype=bool)
        self.marked = np.zeros((self.n, self.m), dtype=int)

    def _clear_covers(self):
        '''
        This clears any covers, as they can change meaning from one step to another
        '''
        self.row_covered[:] = False
        self.col_covered[:] = False
    
    def _clear_marks(self):
        '''
        Clears marks when trying new solutions
        '''
        self.marked[:,:] = 0

    def solve(self):
        '''
        This chooses an initial step for the process and then begins following the appropriate steps.
        It saves the assignment solution to self.solution and the final cost found to self.minimum_cost.
        '''
        initial_step = _step0
        if(self.n==self.m):
            initial_step = _step1

        step = initial_step

        while type(step) is not tuple:
            step = step(self)

        if(step[0]):
            self.solution = step[2]
            self.minimum_cost = step[1]
        return step[0]

    def print_results(self):
        '''
        Just a pretty print for the results
        '''
        if self.solution == None:
            raise Exception("No solution was computed yet or there is no solution. Run the solve method or try another cost matrix.")
        for k,v in self.solution.items():
            print("For {} is assignes {}".format(v,k))
        print("The final total cost was {}".format(self.minimum_cost))

def _step0(state):
    '''
    This step pads the matrix so that it's squared
    '''
    matrix_size = max(state.n, state.m)
    pad_columns = matrix_size - state.n
    pad_rows = matrix_size - state.m
    state.C = np.pad(state.C, ((0,pad_columns),(0,pad_rows)), 'constant', constant_values=(0))
    
    state.row_covered = np.zeros(state.C.shape[0], dtype=bool)
    state.col_covered = np.zeros(state.C.shape[1], dtype=bool)
    state.marked = np.zeros((state.C.shape[0], state.C.shape[1]), dtype=int)
    return _step1

def _step1(state):
    '''
    Subtracts the minimum value per column for each cell of that column
    '''
    # Replace np.inf with np.nan to ignore them in the minimum calculation
    temp_C = np.where(np.isinf(state.C), np.nan, state.C)
    
    # Check if any row is entirely NaN
    if np.any(np.all(np.isnan(temp_C), axis=1)):
        # If a row is entirely NaN, no solution exists
        return (False, np.inf, None)
    
    # Subtract the minimum value per row, ignoring np.inf
    row_min = np.nanmin(temp_C, axis=1)
    state.C = state.C - row_min[:, np.newaxis]
    return _step2

def _step2(state):
    '''
    Subtracts the minimum value per row for each cell of that row
    '''
    # Replace np.inf with np.nan to ignore them in the minimum calculation
    temp_C = np.where(np.isinf(state.C), np.nan, state.C)
    
    # Check if any column is entirely NaN
    if np.any(np.all(np.isnan(temp_C), axis=0)):
        # If a column is entirely NaN, no solution exists
        return (False, np.inf, None)
    
    # Subtract the minimum value per column, ignoring np.inf
    col_min = np.nanmin(temp_C, axis=0)
    state.C = state.C - col_min[np.newaxis, :]
    return _step3

def _step3(state):
    '''
    This step tries to find a coverage of all zeroes in the matrix using the minimum amount of row/column covers.
    It then uses this coverage to check for a solution. If one is found, the algorithm stops. Otherwise, it goes to step 4 and back to step 3.
    '''
    row_marked = np.zeros(state.C.shape[0], dtype=bool)
    col_marked = np.zeros(state.C.shape[1], dtype=bool)
    
    for j in range(state.C.shape[1]):
        for i in range(state.C.shape[0]):
            if(not state.row_covered[i] and not state.col_covered[j] and state.C[i][j]==0):
                state.marked[i][j] = 1
                state.row_covered[i] = True
                state.col_covered[j] = True
                
    state._clear_covers()
    
    for i in range(state.C.shape[0]):
        if np.sum(state.marked[i,:])==0:
            row_marked[i] = True
            for j in range(state.C.shape[1]):
                if not col_marked[j] and state.C[i][j] ==0:
                    col_marked[j] = True
                    for k in range(state.C.shape[0]):
                        if not row_marked[k] and state.marked[k][j]==1:
                            row_marked[k]=True
    
    state.row_covered = np.logical_not(row_marked)
    state.col_covered = col_marked
    num_lines = np.sum(state.row_covered) + np.sum(state.col_covered)
    
    if num_lines == state.C.shape[0]:
        sol = _check_for_solution(state)
        return sol
    else:
        return _step4

def _step4(state):
    '''
    If no solution was found in step 3, this step changes some values in the matrix so that we may now find some coverage.
    The algorithm may be stuck in a step 3 - step 4 loop. If it happens, there is no solution or the wrong matrix was given.
    '''
    smallest_uncovered = np.inf
    for i in range(state.C.shape[0]):
        for j in range(state.C.shape[1]):
            if not state.row_covered[i] and \
               not state.col_covered[j] and \
               state.C[i][j] < smallest_uncovered:
                smallest_uncovered = state.C[i][j]
                
    for i in range(state.C.shape[0]):
        for j in range(state.C.shape[1]):
            if not state.row_covered[i] and not state.col_covered[j]:
                state.C[i][j] -= smallest_uncovered
            elif state.row_covered[i] and state.col_covered[j]:
                state.C[i][j] += smallest_uncovered
                
    state._clear_covers()
    state._clear_marks()
    return _step3

def _check_for_solution(state):
    '''
    This method uses the coverage of the cost matrix to try and find a solution.
    '''
    for j in range(state.C.shape[1]):
        for i in range(state.C.shape[0]):
            if(not state.row_covered[i] and not state.col_covered[j] and state.C[i][j]==0):
                state.marked[i][j] = 1
                state.row_covered[i] = True
                state.col_covered[j] = True
    sol = {}
    cost = 0
    for i in range(state.n):
        for j in range(state.m):
            if(state.marked[i][j]==1):
                sol[j] = i
                cost = cost + state.O[i][j]
                
    state._clear_covers()

    return len(sol)==state.m, cost, sol



def build_bipartite_graph(grid):
    """
    Construit la structure d’un graphe biparti sous forme d’un dictionnaire à partir d’un objet grid.
    
    Retourne :
        {
            "left_nodes": liste des cellules côté gauche,
            "right_nodes": liste des cellules côté droit,
            "weights": dictionnaire {(cell_gauche, cell_droite): weight}
        }
    """
    left_nodes, right_nodes = list(), list()
    
    max_val = max(max(row) for row in grid.value) + 1
    weights = {}

    for (i1, j1), (i2, j2) in grid.all_pairs():
        diff = abs(grid.value[i1][j1] - grid.value[i2][j2])
        weight = max_val - diff
        if (i1 + j1) % 2 == 0 :
            left_nodes.append((i1,j1))
            right_nodes.append((i2,j2))
            weights[((i1, j1), (i2, j2))] = weight
        else :
            left_nodes.append((i2,j2))
            right_nodes.append((i1,j1))
            weights[((i2, j2), (i1, j1))] = weight

    return {
        "left_nodes": left_nodes,
        "right_nodes": right_nodes,
        "weights": weights
    }



def build_cost_matrix(bipartite_graph):
    """
    Construit la matrice de coût à partir du dictionnaire bipartite_graph.
    
    Retourne :
        - cost_matrix : matrice numpy (2D) avec les poids
        - left_nodes, right_nodes : listes pour retrouver les coordonnées
    """
    left_nodes = bipartite_graph["left_nodes"]
    right_nodes = bipartite_graph["right_nodes"]
    weights = bipartite_graph["weights"]

    n_left = len(left_nodes)
    n_right = len(right_nodes)
    cost_matrix =np.asarray( np.inf * np.ones((n_left, n_right)))  # Valeurs impossibles par défaut

    # Remplissage de la matrice
    for (u, v), w in weights.items():
        i = left_nodes.index(u)
        j = right_nodes.index(v)
        cost_matrix[i, j] = w

    return cost_matrix, left_nodes, right_nodes