from utils import HillClimbing, Drawer

solution = HillClimbing()
print("Initial state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Average white cells: {}".format(solution.currentState.i()))
print("Number white cells: {}".format(solution.currentState.j()))
print("Heuristic: {}".format(solution.currentState.heuristic()))
solution.findSolution()

print("Final state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Average white cells: {}".format(solution.currentState.i()))
print("Number white cells: {}".format(solution.currentState.j()))
print("Heuristic: {}".format(solution.currentState.heuristic()))

canva = Drawer()
canva.draw(solution.currentState)