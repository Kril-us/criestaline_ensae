echo "# criestaline_ensae" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Kril-us/criestaline_ensae.git
git push -u origin main

from grid import Grid
from solver import *

grid = Grid(2, 3)
print(grid)

data_path = "../input/"

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name)
print(grid)

file_name = data_path + "grid01.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

solver = SolverEmpty(grid)
solver.run()
print("The final score of SolverEmpty is:", solver.score())


