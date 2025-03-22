import networkx as nx
from grid import Grid

data_path = "projet_python_ensae_2025/input/"

file_name = data_path + "grid03.in"
grid = Grid.grid_from_file(file_name, read_values=True)
#print(grid)


def pairs_for_ford(list):
        pairs_ford = [] # liste of pairs with their capacity compatible with ford-fulkerson
        for couple_de_pairs in list : 
            pairs_ford += [(couple_de_pairs[0],couple_de_pairs[1],{"capacity":1})]
        return pairs_ford

#def solver_ford_fulkerson():
       

#print(pairs_for_ford(grid.graph()))


G = nx.DiGraph()

#G.add_nodes_from(grid.graph())
# [("u", "v",{"capacity":12})]



edges = pairs_for_ford(grid.graph())
G.add_edges_from(edges)

from networkx.algorithms.flow import shortest_augmenting_path

flow_value, flow_dict = nx.maximum_flow(G,(-1,-1),(-2,-2),flow_func=shortest_augmenting_path)

#flow_dict = [elt for elt in flow_dict if flow_dict[elt]!=0]

print (flow_value)
print("\n" + "===================================="+"\n")
print(flow_dict)





