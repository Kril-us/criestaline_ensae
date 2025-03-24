from grid import Grid
from solver import *
import timeit


data_path = "projet_python_ensae_2025/input/"

file_name = data_path + "grid02.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

"""
solver = SolverGreedy(grid)
start = timeit.timeit()
solver.run()
end = timeit.timeit()
print("The final score of SolverGreedy is:", solver.score()," it was calculated in:", end - start, "seconds")
"""

#print(grid.all_pairs())

solver_max = SolverMaxMatching(grid)
start = timeit.timeit()
solver_max.run()
end = timeit.timeit()
print("The final score of SolverMaxMatching is:", solver_max.score(), " it was calculated in:", end - start, "seconds")
