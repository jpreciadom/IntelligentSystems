from python_datastructures import MaxHeap
from .Utils import piecesDimensions, generateRandomPieces, Chromosome

class EvolutionaryAlgorithm:
    def __init__(self, initialPopulation = 2):
        self.population = []
        for i in range(initialPopulation):
            self.population.append(Chromosome(generateRandomPieces(piecesDimensions)))
        self.population = MaxHeap(self.population)

    def next(self):
        reg = MaxHeap([])
        while len(self.population.heap) > 1:
            parentA = self.population.remove()
            parentB = self.population.remove()

            childs = parentA.merge(parentB)
            childs[0].mutate()
            childs[1].mutate()
            
            reg.add(childs[0])
            reg.add(childs[1])

        while len(self.population.heap) > 0:
            reg.add(self.population.remove())

        self.population = reg

    def findSolution(self, iterations):
        print()
        for i in range(1, iterations + 1):
            print("Iteration {}:".format(i))
            print("Population size: {}".format(len(self.population.heap)))
            self.next()
        print()

    def best(self):
        return self.population.peek()