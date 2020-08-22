import random
import numpy as np
import time
from Shared import tourCost, stochasticTwoOpt, constructInitialSolution


def load_data(file):
    data = np.loadtxt(file, skiprows=6)
    data = np.delete(data, 0, 1).tolist()
    return data


def perturbation(aSol):
    # uses a 'double bridge move' for perturbation
    newSol = doubleBridgeMove(aSol)
    newSolCost = tourCost(newSol)
    return newSol, newSolCost


# the double bridge move involves partitioning a permutation into 4 pieces
# (a, b, c, d) and putting it back together in a specific and jumbled ording
# (a, b, c, d) - this is equivalent to a 4-opt move
def doubleBridgeMove(perm):
    # make four slices
    sliceLength = int(len(perm) / 4)
    p1 = 1 + random.randrange(0, sliceLength)
    p2 = p1 + 1 + random.randrange(0, sliceLength)
    p3 = p2 + 1 + random.randrange(0, sliceLength)
    # combine first and fourth slice in order
    # combine third and second slice in order
    # return the combination of the above two combined slices
    return perm[0:p1] + perm[p3:] + perm[p2:p3] + perm[p1:p2]


def localSearch(aSol, aCost, maxIter):
    while maxIter > 0:
        maxIter -= 1
        newSol = stochasticTwoOpt(aSol)
        newCost = tourCost(newSol)
        if newCost < aCost:
            aSol = newSol
            aCost = newCost
    return aSol, aCost


if __name__ == "__main__":
    """ALGORITHM FRAMEWORK"""
    algorithmName = "ILS"
    print("Best sol by" + algorithmName + "...")
    file = "wi29.txt"

    # problem configuration
    inputsTSP = load_data(file)


    cost = 0
    time_ = 0
    for i in range(0, 5):
        maxIteration = 15000
        maxNoImprove = 100
        start = time.perf_counter()

        # 1. generate an initial solution. we use a random permutation as the initial solution
        bestSol = constructInitialSolution(inputsTSP)
        bestCost = tourCost(bestSol)
        # 2. refine this using a local search for getting to the local optima
        bestSol, bestCost = localSearch(bestSol, bestCost, maxNoImprove)
        # 3. iterate
        while maxIteration > 0:
            maxIteration -= 1
            newSol, newCost = perturbation(bestSol)
            newSol, newCost = localSearch(newSol, newCost, maxNoImprove)
            if newCost < bestCost:
                bestSol = newSol
                bestCost = newCost
                # print(bestCost, maxIteration)
        # 4. stop clock and return outputs
        stop = time.perf_counter()
        cost += bestCost
        time_ += (stop - start)
        print(bestCost)
    print(cost)
    with open(algorithmName + "_" + file, "w") as out:
        out.write("Best sol by" + algorithmName + "... \n")
        out.write("Average Cost = {}\n".format(cost / 5))
        out.write("Average Elapsed = {}\n ".format(time_ / 5))