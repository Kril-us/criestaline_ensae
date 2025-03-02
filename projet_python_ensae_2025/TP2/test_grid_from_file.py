# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from parameterized import parameterized

class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=True)
        self.assertEqual(grid.n, 2,"erreur test_grid0 : n")
        self.assertEqual(grid.m, 3,"erreur test_grid0 : m")
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]],"erreur test_grid0 : color")
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]],"erreur test_grid0 : value")


    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=False)
        self.assertEqual(grid.n, 2,"erreur test_grid0_novalues : n")
        self.assertEqual(grid.m, 3,"erreur test_grid0_novalues : m")
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]],"erreur test_grid0_novalues : color")
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]],"erreur test_grid0_novalues : value")


    def test_grid1(self):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2,"erreur test_grid1 : n")
        self.assertEqual(grid.m, 3,"erreur test_grid1 : m")
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]],"erreur test_grid1 : color")
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]],"erreur test_grid1 : value")
    

    def test_grid2(self):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in",read_values=True)
        self.assertEqual(grid.n, 2,"erreur test_grid2 : n")
        self.assertEqual(grid.m, 3,"erreur test_grid2 : m")
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]],"erreur test_grid2 : color")
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]],"erreur test_grid2 : value")



    @parameterized.expand([
        ("test1",0,0),
        ("test2",1,0),
        ("test3",1,1),
        ("test4",0,1),
    ]) #permet de tester une série couples i, j
    def test_is_forbidden_all_grid(self,num_test,i,j):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=True)
        self.assertFalse(grid.is_forbidden(i,j),"erreur test_is_forbidden_grid0 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid01.in",read_values=True)
        #on fait un dictionnaire qui prévoit pour chaque entrée la réponse attendue
        dic_1 = {(0,0):False, (0,1):True, (1,0):False, (1,1):False}
        self.assertEqual(grid.is_forbidden(i,j),dic_1[(i,j)],"erreur test_is_forbidden_grid1 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in",read_values=True)
        dic_2 = {(0,0):False, (0,1):True, (1,0):False, (1,1):False}
        self.assertEqual(grid.is_forbidden(i,j),dic_1[(i,j)],"erreur test_is_forbidden_grid2 "+num_test)



    @parameterized.expand([
        ("test1",0,0,0,1),
        ("test2",0,0,1,0),
        ("test3",1,1,0,1),
        ("test4",1,1,1,0),
    ])
    def test_cost_all_grid(self,num_test,i1,j1,i2,j2):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=True)
        #une entrée est définie par i1 et i2
        dic_1 = {(0,0):3, (0,1):6, (1,0):7, (1,1):10}
        self.assertEqual(grid.cost(((i1,j1),(i2,j2))),dic_1[(i1,i2)],"erreur test_cost_grid0 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid01.in",read_values=True)
        self.assertEqual(grid.cost(((i1,j1),(i2,j2))),dic_1[(i1,i2)],"erreur test_cost_grid0 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in",read_values=True)
        #tous les coûts sont égaux à 0
        self.assertEqual(grid.cost(((i1,j1),(i2,j2))),0,"erreur test_cost_grid0 "+num_test)



    @parameterized.expand([
        ("test1",0,0,0,1),
        ("test2",0,0,1,0),
        ("test3",1,1,0,1),
        ("test4",1,1,1,0),
    ])
    def test_is_compatible_all_grid(self,num_test,i1,j1,i2,j2):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=True)
        self.assertTrue(grid.is_compatible(i1,j1,i2,j2),"erreur test_is_compatible_grid0 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid01.in",read_values=True)
        dic_1 = {(0,0):False, (0,1):True, (1,0):False, (1,1):True}
        self.assertEqual(grid.is_compatible(i1,j1,i2,j2),dic_1[(i1,i2)],"erreur test_is_compatible_grid1 "+num_test)

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in",read_values=True)
        dic_2 = {(0,0):False, (0,1):True, (1,0):False, (1,1):True}
        self.assertEqual(grid.is_compatible(i1,j1,i2,j2),dic_2[(i1,i2)],"erreur test_is_compatible_grid2 "+num_test)



    def test_all_pairs(self):

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid00.in",read_values=True)
        #il faut prendre en compte l'ordre des couples de coordonnées selon comment on a construit all_pairs
        result_0 = [((0, 1), (0, 0)), ((0, 2), (0, 1)), ((1, 0), (0, 0)), ((1, 1), 
                    (0, 1)), ((1, 1), (1, 0)), ((1, 2), (0, 2)), ((1, 2), (1, 1))]
        self.assertEqual(grid.all_pairs(),result_0,"erreur test_all_pairs grid0")

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid01.in",read_values=True)
        result_1 = [((1, 0), (0, 0)), ((1, 1), (1, 0)), ((1, 2), (0, 2)), ((1, 2), (1, 1))]
        self.assertEqual(grid.all_pairs(),result_1,"erreur test_all_pairs grid1")

        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in",read_values=True)
        self.assertEqual(grid.all_pairs(),result_1,"erreur test_all_pairs grid2")


if __name__ == '__main__':
    unittest.main()



# test pour solver for fulkerson

class Test_SolverMaxMatching(unittest.TestCase):
    def test_solver_max_matching(self):
        grid = Grid.grid_from_file("projet_python_ensae_2025/input/grid02.in", read_values=True)
        solver = SolverMaxMatching(grid)
        solver.run()
        expected_pairs = [((0, 0), (1, 0)), ((0, 2), (1, 2))]  # Example expected pairs
        self.assertEqual(set(solver.pairs), set(expected_pairs), "Mismatch in matching pairs")
