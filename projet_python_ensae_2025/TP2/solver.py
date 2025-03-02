import numpy as np
from grid import Grid
import copy


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
            output += abs(self.grid.value[pair[0][0]][pair[0][1]] - self.grid.value[pair[1][0]][pair[1][1]])
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

Soit n le nombre de cases, si on met de côté les contraintes de couleur pour se donner une idée
de la complexité du programme, il y a environ 2**(n/2) possibilités pour former les paires.
On obtient ce résultat en partant d'un coin, disons en bas à gauche on a alors deux possibilité 
pour former une paire si on impose de choisir la 2ème case au dessus ou à droite de la première.
On choisit ensuite que la première case de la paire suivante doit être le plus bas possible puis
le plus à gauche possible, ainsi la laigne en dessous est complète et la case à droite n'est pas
disponible, on peut donc approximer qu'il y a deux possibilités pour former une paire.

Admettons que la fonction np.argmin(liste) a une complexité proportionnelle à len(liste) (les
autres opérations sont négligeables) car elle parcours la liste pour repérer l'indice du min. 
Alors à chaque itération qui diminue n de 2, donc à la k-ème itération la complexité augmente 
d'une valeure proportionnelle à 2**(n/2 -k)

En sommant on obtient que la complexité totale est proportionnelle à 2**(n/2) 
"""




from ford_fulkerson import ford_fulkerson, construire_réseau



class SolverMaxMatching(Solver):
    def run(self):
        """
        Runs the solver using the maximum matching approach.
        """
        nodes_left, nodes_right, edges = self.grid.graph()
        
        # Convert to a network for Ford-Fulkerson
        edge_list = [((str(u), str(v)), 1) for u, v in edges]
        graph, capacity = construire_réseau(edge_list)
        
        # Add a source 's' connected to all left nodes, and a sink 't' from all right nodes
        for node in nodes_left:
            graph['s'].add(str(node))
            capacity[("s", str(node))] = 1
        for node in nodes_right:
            graph[str(node)].add('t')
            capacity[(str(node), "t")] = 1
        
        # Compute maximum matching
        flow = ford_fulkerson(graph, capacity, 's', 't')
        
        # Extract matching pairs
        self.pairs = []
        for (u, v), f in flow.items():
            if f == 1 and u != 's' and v != 't':
                self.pairs.append((eval(u), eval(v)))
        
        # Print selected pairs
        print("Selected pairs:", self.pairs)


# 2eme essai
"""
class SolverFordFulkerson(Solver):
    def run(self):
        
        # Solve the grid pairing problem using the Ford-Fulkerson algorithm.
        
        # Convert grid into a bipartite graph
        edges = self.grid.all_pairs()
        graph, capacity = construire_réseau([(edge, 1) for edge in edges])
        
        # Define source ('s') and terminus ('t')
        source = 's'
        terminus = 't'
        
        # Add source and terminus nodes to the graph
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                cell = (i, j)
                if (i + j) % 2 == 0:  # Left side of bipartite graph
                    graph[source].add(cell)
                    capacity[(source, cell)] = 1
                else:  # Right side of bipartite graph
                    graph[cell].add(terminus)
                    capacity[(cell, terminus)] = 1
        
        # Run Ford-Fulkerson to find max matching
        flow = ford_fulkerson(graph, capacity, source, terminus)
        
        # Extract pairs from the flow result
        for (u, v), f in flow.items():
            if f == 1 and isinstance(u, tuple) and isinstance(v, tuple):
                self.pairs.append((u, v))
"""