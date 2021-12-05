from python_datastructures import MaxHeap
from .Utils import piecesDimensions, generateRandomPieces, Chromosome

class EvolutionaryAlgorithm:
    def __init__(self, initialPopulation = 2, maxPopulation = 500):
        self.population = []
        for i in range(initialPopulation):
            self.population.append(Chromosome(generateRandomPieces(piecesDimensions)))
        self.maxPopulation = maxPopulation
        self.population = MaxHeap(self.population)

    def next(self):
        reg = MaxHeap([])
        while len(self.population.heap) > 1:
            parentA = self.population.remove()
            parentB = self.population.remove()

            childs = parentA.merge(parentB)
            childs[0].mutate()
            childs[1].mutate()

            reg.add(parentA)
            reg.add(parentA)
            reg.add(childs[0])
            reg.add(childs[1])

        while len(self.population.heap) > 0:
            reg.add(self.population.remove())

        while len(reg.heap) > 0 and len(self.population.heap) < self.maxPopulation:
            self.population.add(reg.remove())

    def findSolution(self, iterations):
        print()
        for i in range(1, iterations + 1):
            print("Iteration {}:".format(i))
            print("Population size: {}".format(len(self.population.heap)))
            self.next()
        print()

    def best(self):
        return self.population.peek()