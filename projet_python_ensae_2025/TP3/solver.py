import numpy as np
from grid import Grid
import copy
import networkx as nx


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
        self.test_score = False #renvoie true si le solver est celui de ford fulkersen
        self.score_int = 0

    def score(self):
        """
        Computes the score of the list of pairs in self.pairs
        """
        if self.test_score :
            return self.score
        else :
            output = 0
            for pair in self.pairs:
                output += abs(self.grid.value[pair[0][0]][pair[0][1]] - self.grid.value[pair[1][0]][pair[1][1]])
            sommets_atteints = [u for (u,v) in self.pairs] + [v for (u,v) in self.pairs]
            for i in range(self.grid.n):
                for j in range(self.grid.m):
                    if (i,j) not in sommets_atteints and self.grid.color[i][j] != 4:
                        output += self.grid.value[i][j]
            return output

class SolverEmpty(Solver):
    def run(self):
        pass

class SolverGreedy(Solver):
    def run(self):
        copie = copy.deepcopy(self)
        #un défaut de cette implémentation est qu'elle modifie les couleurs de grid, c'est porquoi on le copie
        def boucle(solver: Solver) : 
            all_pairs = solver.grid.all_pairs()
            if all_pairs == [] :
                return solver.pairs
            else :
                list_cost = [solver.grid.cost(pair) for pair in all_pairs]
                pair_min = all_pairs[np.argmin(list_cost)]
                self.pairs.append(pair_min) #l'objectif est de remplir self.pairs
                solver.grid.color[pair_min[0][0]][pair_min[0][1]] = 4
                solver.grid.color[pair_min[1][0]][pair_min[1][1]] = 4
                return boucle(solver)   
        boucle(copie)    

        
"""
A propos de la complexité de la solution gloutonne :

Soit n et m les dimensions de la grille, on remarque que all_pairs() a une complexité en O(n*m).

Admettons que la fonction np.argmin(liste) a une complexité proportionnelle à len(liste) alors les 
opérations sous la condition "else" sont toutes négligeables par rapport à all.pairs car de complexité 
d'ordre plus petite que n*m.

Or à chaque itération on élimine 2 cases, donc à la k-ème itération la complexité augmente 
d'une valeure proportionnelle à n*m - k

En sommant on obtient que la complexité totale est en O((n*m)**2)
"""



class SolverFordNetworkx(Solver):
    def run(self):

        def pairs_for_ford(list):
            pairs_ford = [] # liste of pairs with their capacity compatible with ford-fulkerson
            for couple_de_pairs in list : 
                pairs_ford += [(couple_de_pairs[0],couple_de_pairs[1],{"capacity":1})]
            return pairs_ford
    
        G = nx.DiGraph()
        #G.add_nodes_from(grid.graph())
        # [("u", "v",{"capacity":12})]

        edges = pairs_for_ford(self.grid.graph())
        G.add_edges_from(edges)

        from networkx.algorithms.flow import shortest_augmenting_path

        flow_value, flow_dict = nx.maximum_flow(G,(-1,-1),(-2,-2),flow_func=shortest_augmenting_path)

        #flow_dict = [elt for elt in flow_dict if flow_dict[elt]!=0]

        for source, destinations in flow_dict.items():
            for target, flow in destinations.items():
                if flow > 0:
                    self.pairs.append((source, target))



class SolverHungarian(Solver):
    def run(self):
        
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
            cost_matrix = -np.inf * np.ones((n_left, n_right))  # Valeurs impossibles par défaut

            # Remplissage de la matrice
            for (u, v), w in weights.items():
                i = left_nodes.index(u)
                j = right_nodes.index(v)
                cost_matrix[i, j] = w

            return cost_matrix, left_nodes, right_nodes

