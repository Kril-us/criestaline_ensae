from grid import Grid
from solver import *
import timeit

grid = Grid(2, 3)
print(grid)

#krillpath = "/home/krill//criestaline_ensae/projet_python_ensae_2025/input/"
data_path = "C:/Users/pakin/Desktop/boulot/info/projet ENSAE 1A/criestaline_ensae/projet_python_ensae_2025/input/"

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name)
print(grid)

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

solver = SolverGreedy(grid)
start = timeit.timeit()
solver.run()
end = timeit.timeit()
print("The final score of SolverGreedy is:", solver.score()," it was calculated in:", end - start, "seconds")

grid.plot()