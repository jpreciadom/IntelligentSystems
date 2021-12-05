from utils import HillClimbing, Drawer, SimulatedAnnealing
from math import ceil

def L(t):
    return ceil((5000 / t) - 9)

solution = SimulatedAnnealing(500, 1, L, 1)
print("Initial state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Number white cells: {}".format(solution.currentState.i()))
print("Heuristic: {}\n".format(solution.currentState.heuristic()))
solution.findSolution()

print("Final state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Number white cells: {}".format(solution.currentState.i()))
print("Heuristic: {}".format(solution.currentState.heuristic()))

canva = Drawer(30)
canva.draw(solution.currentState)

state = solution.currentState
solution = HillClimbing()
solution.currentState = state
solution.findSolution()
print("Improve using HillClimbing state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Number white cells: {}".format(solution.currentState.i()))
print("Heuristic: {}".format(solution.currentState.heuristic()))

canva = Drawer(30)
canva.draw(solution.currentState)