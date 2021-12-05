from numpy import mat
from .Utils import State, generateRandomPieces, piecesDimensions
import random
import math

class SimulatedAnnealing:
    def __init__(self, t0, a, l, tf):
        self.currentState = State(generateRandomPieces(piecesDimensions))
        self.t0 = t0
        self.a = a
        self.l = l
        self.tf = tf

    def next(self, t):
        candidate = self.currentState.getRandomNeighbor()
        d = candidate.heuristic() - self.currentState.heuristic()
        if d < 0 or probability(d, t):
            return candidate
        else:
            return self.currentState

    def findSolution(self):
        t = self.t0
        while t >= self.tf:
            for i in range(0, self.l(t)):
                self.currentState = self.next(t)
            t -= self.a

def probability(d, t):
    a = random.uniform(0, 1)
    reg = (d * -1) / t
    reg = math.e ** reg
    reg = a < reg
    return reg