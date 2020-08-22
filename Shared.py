import math
import random
import numpy as np 


# evaluates the total length of a TSP solution (permutation of nodes)
def tourCost(perm):
    # is the sum of the Euclidean distance between consecutive points in the path
    totalDistance = 0.0
    size = len(perm)
    for index in range(size):
        startNode = perm[index]
        # select the end point for calculating the segment length
        if index == size - 1:
            # in order to complete the 'tour' we need to reach the starting point
            endNode = perm[0]
        else:
            endNode = perm[index + 1]

        totalDistance += euclideanDistance(startNode, endNode)
    return totalDistance


# calculates the euclidean distance between two points
def euclideanDistance(xNode, yNode):
    sum = 0.0
    # use Zip to iterate over the two vectors (nodes)
    for xi, yi in zip(xNode, yNode):
        sum += pow((xi - yi), 2)
    return math.sqrt(sum)


def getBRA(beta, size):
    t1 = random.random()
    index = math.log(t1) / math.log(1 - beta)
    index = int(index) % size

    return index


# deletes two edges and reverse the sequence in between the deleted edges
def stochasticTwoOpt(perm):
    result = perm[:]  # to avoide changing the original sol (perm), make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0, size), random.randrange(0, size)
    # do this as not to overshoot tour boundaries
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size - 1)
    else:
        exclude.add(p1 - 1)

    if p1 == size - 1:
        exclude.add(0)
    else:
        exclude.add(p1 + 1)

    while p2 in exclude:
        p2 = random.randrange(0, size)

    # to ensure we always have p1 < p2
    if p2 < p1:
        p1, p2 = p2, p1
    
    # now reverse the tour segment between p1 and p2
    result[p1:p2] = reversed(result[p1:p2])

    return result


# creates a random sol (permutation) from an initial permutation by shuffling its elements
def constructInitialSolution(initPerm):
    # randomise the initial permutation
    permutation = initPerm[:]  # make a copy of the initial permutation
    size = len(permutation)
    for index in range(size):
        # shuffle the values of the initial permytation randomly
        # get a random index and exchange values
        shuffleIndex = random.randrange(index, size)  # randange excludes upper bound
        permutation[shuffleIndex], permutation[index] = permutation[index], permutation[shuffleIndex]
    return permutation