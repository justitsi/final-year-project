import time
import json
import copy
import concurrent.futures
from utils import removeElementFromArray, printTree
start = time.time()


with open('sample_data_2.json', encoding='utf-8') as F:
    json_data = json.loads(F.read())
# read sample data and alg_params
NODES = json_data['data']
alg_params = json_data['alg_params']


NUMBER_OF_GROUPS = alg_params['NUMBER_OF_GROUPS']
GROUP_SIZE = alg_params['GROUP_SIZE']
# pruning params
TREE_PRUNE_TRESHOLD = alg_params['TREE_PRUNE_TRESHOLD']
STEP_MAX_COST = alg_params['STEP_MAX_COST']
# costing params
GROUP_BASE_COST = alg_params['GROUP_BASE_SCORE']
LARGE_GROUP_PENALTY = alg_params['LARGE_GROUP_PENALTY']
AFFINITY_BONUS = alg_params['AFFINITY_BONUS']
# memoization variables
NODE_PAIRING_COSTS = []
NODE_GROUPING_IDS = []
# multithreading params
NUMBER_OF_LEVELS_BEFORE_MULTITHREADING = 4
NUMBER_OF_THREADS_TO_USE = 8


def generateTree(currentTree, remainingElements):
    # take out id that will be added to the array
    idToAdd = remainingElements[0]
    remainingElementsCopy = removeElementFromArray(remainingElements, remainingElements[0])  # nopep8

    possibleTrees = []
    returnTrees = []

    if (len(remainingElementsCopy) > 0):
        for i in range(0, NUMBER_OF_GROUPS):
            # instanciate element to add
            elementToAddCopy = {
                'groupID': i,
                'id': idToAdd
            }

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTree['cost'] + costToAdd

            # add info to possible trees if tested tree is OK
            if (costToAdd < STEP_MAX_COST):
                if (totalTreeCost < TREE_PRUNE_TRESHOLD):
                    # instanciate copy of currently tested tree
                    currentTreeCopy = copy.deepcopy(currentTree)

                    currentTreeCopy['nodes'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                    possibleTrees.append(currentTreeCopy)

        # re-run the function for valid candidate trees
        for tree in possibleTrees:
            childTrees = generateTree(tree, remainingElementsCopy)
            for childTree in childTrees:
                returnTrees.append(childTree)

        return returnTrees

    else:
        for i in range(0, NUMBER_OF_GROUPS):
            # instanciate element to add
            elementToAddCopy = {
                'groupID': i,
                'id': idToAdd
            }

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTree['cost'] + costToAdd

            # add info to possible trees if tested tree is OK
            if (costToAdd < STEP_MAX_COST):
                if (totalTreeCost < TREE_PRUNE_TRESHOLD):
                    # instanciate copy of currently tested tree
                    currentTreeCopy = copy.deepcopy(currentTree)

                    currentTreeCopy['nodes'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                    possibleTrees.append(currentTreeCopy)

        # return bottom-level path costs
        return possibleTrees


# returns the cost of adding an element to a specific path
def getCost(currentTree, el):
    cost = GROUP_BASE_COST

    # get nodeIDs for nodes in group
    nodesInGroup = []
    for node in currentTree['nodes']:
        if (node['groupID'] == el['groupID']):
            nodesInGroup.append(node['id'])

    # calculate cost for group in grouping
    cost += getNodeToGroupCost(nodesInGroup, el['groupID'], el['id'])

    # calculate cost for nodes in grouping
    cost += getNodeToNodesCost(nodesInGroup, el['id'])

    return cost


# array of node ids from path ([int]) and id (int)
def getNodeToNodesCost(nodesInGroup, nodeToAddID):
    cost = 0
    # check for affinities
    for groupNode in nodesInGroup:
        cost += getNodeToNodeCost(groupNode, nodeToAddID)

    return cost


# lookup results for node-node pairing in NODE_PAIRING_COSTS
def getNodeToNodeCost(nodeID1, nodeID2):
    return NODE_PAIRING_COSTS[nodeID1][nodeID2]


# both arguments contain full node data dictionaries
def calculateNodeToNodeCost(node1, node2):
    cost = 0

    if (node1['affinities']):
        for affinity in node1['affinities']:
            if (affinity == node2['id']):
                cost -= AFFINITY_BONUS

    if (node2['affinities']):
        for affinity in node2['affinities']:
            if (affinity == node1['id']):
                cost -= AFFINITY_BONUS

    return cost


# array of node ids from path ([int]), id(int) and id (int)
def getNodeToGroupCost(nodesInGroup, groupID, nodeToAddID):
    cost = 0
    groupSize = len(nodesInGroup) + 1

    # check if group size limit hasn't been exceeded
    if (groupSize >= GROUP_SIZE):
        cost += LARGE_GROUP_PENALTY * ((groupSize) - GROUP_SIZE)

    return cost


# returns full node properties as dictionary
def getNodeProperties(nodeID):
    for node in NODES:
        if nodeID == node['id']:
            return node
    return {}


# precalculate costs for each node-to-node pairings
# assumes that nodes are sorted by id
def preCalculateNodeToNodeCosts(nodes):
    costs = []

    for i in range(0, len(nodes)):
        currentNode = getNodeProperties(nodes[i])
        currentCosts = []

        for j in range(0, len(nodes)):
            comparisonNode = getNodeProperties(nodes[j])
            currentCosts.append(calculateNodeToNodeCost(currentNode, comparisonNode))  # nopep8

        costs.append(currentCosts)

    return costs


if __name__ == '__main__':
    # instantiate tree and nodes to be explored
    currentTree = {
        "nodes": [{"groupID": 1, "id": NODES[0]['id']}],
        "cost": 0
    }

    remainginNodes = []
    for node in NODES:
        remainginNodes.append(node['id'])

    # pre-calculate node pairing costs
    NODE_PAIRING_COSTS = preCalculateNodeToNodeCosts(remainginNodes)

    # remove 0th node from array of all nodes
    remainginNodes = removeElementFromArray(remainginNodes, NODES[0]['id'])

    # pre-run certain paths to allow for multhithreading - this generates a batch of jobs to run on seperate threads
    preRunNodes = []
    for i in range(0, NUMBER_OF_LEVELS_BEFORE_MULTITHREADING):
        preRunNodes.append(remainginNodes[i])
        remainginNodes = removeElementFromArray(
            remainginNodes, remainginNodes[i])

    # pre run several paths to create a batch of jobs
    preRunTrees = generateTree(currentTree, preRunNodes)

    # run jobs on seperate threads and store results in possible_paths[]
    possible_paths = []

    # code to run job batch one by one
    # for preRunTree in preRunTrees:
    #     solutions = generateTree(preRunTree, remainginNodes)
    #     for solution in solutions:
    #         possible_paths.append(solution)

    # code to run job batch in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=NUMBER_OF_THREADS_TO_USE) as executor:
        futures = []
        for preRunTree in preRunTrees:
            futures.append(executor.submit(generateTree, currentTree=preRunTree, remainingElements=remainginNodes))  # nopep8

        for future in concurrent.futures.as_completed(futures):
            solutions = future.result()
            for solution in solutions:
                possible_paths.append(solution)

    # print readable results
    if (alg_params['PRINT_RESULTS']):
        for tree in possible_paths:
            printTree(tree)
            print('\n')

    print("Viable solutions found: " + str(len(possible_paths)))
    if len(possible_paths) > 0:
        best_tree = possible_paths[0]
        for tree in possible_paths:
            if tree['cost'] <= best_tree['cost']:
                best_tree = tree

        printTree(best_tree)

    # # profiling/ calculate execution time of program
    end = time.time()
    print(f"Runtime of the program is {end - start}")

    # Data structures reference
    # tree element def
    # {
    #     'groupID': 1,
    #     'id': 1
    # }

    # element def
    # {
    #     'groupID': 1,
    #     'properties': {
    #          'id' : 1,
    #          'affinities': [2, 3]
    #      }
    # }

    # tree def
    # {
    #     "nodes": [elements],
    #     "cost": ints
    # }
