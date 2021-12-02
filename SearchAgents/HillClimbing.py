import Utils as utils

class HillClimbing:
    def __init__(self):
        self.currentState = utils.State(utils.generateRandomPieces(utils.piecesDimensions))

    def next(self):
        neighbors = self.currentState.findNeighbors()

        minHeuristic = (self.currentState.heuristic(), -1)
        for idx, state in enumerate(neighbors):
            currentHuristic = state.heuristic()
            if currentHuristic < minHeuristic[0]:
                minHeuristic = (currentHuristic, idx)

        if (minHeuristic[1] != -1):
            self.currentState = neighbors[minHeuristic[1]]
            return True
        return False

    def findSolution(self):
        canContinue = True
        i = 0
        while canContinue:
            canContinue = self.next()
            i += 1
        print("\nA solution has found in {} iterations\n".format(i))

solution = HillClimbing()
print("Initial state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Number white cells: {}".format(solution.currentState.i()))
print("Heuristic: {}".format(solution.currentState.heuristic()))
solution.findSolution()

print("Final state")
print("Number of sheets: {}".format(solution.currentState.f()))
print("Number of overlaps: {}".format(solution.currentState.g()))
print("Number of cells out of the sheet: {}".format(solution.currentState.h()))
print("Number white cells: {}".format(solution.currentState.i()))
print("Heuristic: {}".format(solution.currentState.heuristic()))

canva = utils.Drawer()
canva.draw(solution.currentState)