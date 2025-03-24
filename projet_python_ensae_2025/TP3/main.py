from grid import Grid
from solver import *
import timeit


data_path = "projet_python_ensae_2025/input/"

file_name = data_path + "grid02.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)
#print(grid.all_pairs())
#grid.plot()

"""
solver = SolverGreedy(grid)
start = timeit.timeit()
solver.run()
end = timeit.timeit()
print("The final score of SolverGreedy is:", solver.score()," it was calculated in:", end - start, "seconds")
"""

"""
solver_max = SolverFordNetworkx(grid)
start = timeit.timeit()
solver_max.run()
end = timeit.timeit()
print("The final score of SolverFordNetworkx is:", solver_max.score(), " it was calculated in:", end - start, "seconds")
"""


solver_hung = SolverHungarianNetworkx(grid)
start = timeit.timeit()
solver_hung.run()
end = timeit.timeit()
print("The final score of SolverHungarianNetworkx is:", solver_hung.score(), " it was calculated in:", end - start, "seconds")
