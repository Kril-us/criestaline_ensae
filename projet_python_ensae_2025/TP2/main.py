from grid import Grid
from solver import *
import timeit


grid = Grid(2, 3)
print(grid)

data_path = "projet_python_ensae_2025/input/"

file_name = data_path + "grid15.in"
grid = Grid.grid_from_file(file_name)
print(grid)

file_name = data_path + "grid15.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

solver = SolverGreedy(grid)
start = timeit.timeit()
solver.run()
end = timeit.timeit()
print("The final score of SolverGreedy is:", solver.score()," it was calculated in:", end - start, "seconds")

print(grid.all_pairs())

grid.plot()


# solver ford fulkerson
# problème réglé : après des test la recursion est trop lourde pour python sur mon ordi 
# ne pas tester avec les grid20 ou plus sinon ça crash
# après des test solverMaxMatching est moins performant que le greedy (tester grid17)
solver_max = SolverMaxMatching(grid)
start = timeit.timeit()
solver_max.run()
end = timeit.timeit()
print("The final score of SolverMaxMatching is:", solver_max.score(), " it was calculated in:", end - start, "seconds")

