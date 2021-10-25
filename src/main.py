import time
import json
import copy
from utils import removeElementFromArray, printTree
start = time.time()


with open('sample_data_1.json', encoding='utf-8') as F:
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
# memoization paramaters
LEVELS_TO_MEMOIZE = 2
# memoization variables
NODE_PAIRING_COSTS = []
NODE_GROUPING_IDS = []
NODE_GROUPING_COSTS = [[1], [[2, 3], [3, 4]]]


def generateTree(currentTree, remainingElements):
    elementToAdd = {
        'groupID': None,
        'id': remainingElements[0]
    }

    remainingElementsCopy = removeElementFromArray(
        remainingElements, remainingElements[0])

    possibleTrees = []
    returnTrees = []

    if (len(remainingElementsCopy) > 0):
        for i in range(0, NUMBER_OF_GROUPS):
            # instanciate element copy
            elementToAddCopy = copy.deepcopy(elementToAdd)
            elementToAddCopy['groupID'] = i
            # instanciate tree copy
            currentTreeCopy = copy.deepcopy(currentTree)

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTreeCopy['cost'] + costToAdd

            # add info to currentTreeCopy
            if (costToAdd < STEP_MAX_COST):
                if (totalTreeCost < TREE_PRUNE_TRESHOLD):
                    currentTreeCopy['nodes'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                possibleTrees.append(currentTreeCopy)

        for tree in possibleTrees:
            # print(tree, remainingElementsCopy)
            childTrees = generateTree(tree, remainingElementsCopy)
            for childTree in childTrees:
                # print(childTree)
                returnTrees.append(childTree)

        return returnTrees
    else:
        for i in range(0, NUMBER_OF_GROUPS):
            # instanciate element copy
            elementToAddCopy = copy.deepcopy(elementToAdd)
            elementToAddCopy['groupID'] = i
            # instanciate tree copy
            currentTreeCopy = copy.deepcopy(currentTree)

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTreeCopy['cost'] + costToAdd

            # add info to currentTreeCopy
            if (costToAdd < STEP_MAX_COST):
                if (totalTreeCost < TREE_PRUNE_TRESHOLD):
                    currentTreeCopy['nodes'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                    possibleTrees.append(currentTreeCopy)

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

# run binary search alg
remainginNodes = removeElementFromArray(remainginNodes, NODES[0]['id'])
possible_trees = generateTree(currentTree, remainginNodes)

# print readable results
if (alg_params['PRINT_RESULTS']):
    for tree in possible_trees:
        printTree(tree)
        print('\n')

print("Viable solutions found: " + str(len(possible_trees)))
if len(possible_trees) > 0:
    best_tree = possible_trees[0]
    for tree in possible_trees:
        if tree['cost'] <= best_tree['cost']:
            best_tree = tree

    printTree(best_tree)

# profiling/ calculate execution time of program
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
