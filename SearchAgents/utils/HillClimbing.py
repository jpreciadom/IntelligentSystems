from .Utils import State, generateRandomPieces, piecesDimensions

class HillClimbing:
    def __init__(self):
        self.currentState = State(generateRandomPieces(piecesDimensions))

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
        print("\nHill Climbing:")
        print("A solution has been found in {} iterations\n".format(i))