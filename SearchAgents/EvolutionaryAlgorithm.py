from random import betavariate
from utils import EvolutionaryAlgorithm, Drawer

solution = EvolutionaryAlgorithm(50)
best = solution.best()
print("Initial state")
print("Number of sheets: {}".format(best.f()))
print("Number of overlaps: {}".format(best.g()))
print("Number of cells out of the sheet: {}".format(best.h()))
print("Average white cells: {}".format(best.i()))
print("Number white cells: {}".format(best.j()))
print("Fitness: {}".format(best.fitness()))

solution.findSolution(12)

best = solution.best()
print("Final state")
print("Number of sheets: {}".format(best.f()))
print("Number of overlaps: {}".format(best.g()))
print("Number of cells out of the sheet: {}".format(best.h()))
print("Average white cells: {}".format(best.i()))
print("Number white cells: {}".format(best.j()))
print("Fitness: {}".format(best.fitness()))

canva = Drawer()
canva.draw(best)