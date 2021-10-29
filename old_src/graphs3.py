import time
import json
import copy
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
    nodeToAdd = getNodeProperties(nodeToAddID)

    # check for affinities
    for groupNode in nodesInGroup:
        groupNodeProperties = getNodeProperties(groupNode)

        if (groupNodeProperties['affinities']):
            for affinity in groupNodeProperties['affinities']:
                if (affinity == nodeToAddID):
                    cost -= AFFINITY_BONUS

        if (nodeToAdd['affinities']):
            for affinity in nodeToAdd['affinities']:
                if (affinity == groupNode):
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


def removeElementFromArray(arr, el):
    arr_copy = arr.copy()

    for i in range(0, len(arr)):
        if arr[i] == el:
            arr_copy.pop(i)
            break

    return arr_copy


def printTree(tree):
    string1 = ""
    string2 = ""

    for element in tree['nodes']:
        string1 += str(element['id']) + " "
    for element in tree['nodes']:
        string2 += str(element['groupID']) + " "

    print(string1)
    print(string2)
    print(tree['cost'])


def getNodeProperties(nodeID):
    for node in NODES:
        if nodeID == node['id']:
            return node
    return {}


currentTree = {
    "nodes": [{"groupID": 1, "id": NODES[0]['id']}],
    "cost": 0
}

remainginNodes = []
for node in NODES:
    remainginNodes.append(node['id'])

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
#          'id' : 1
#      }
# }

# tree def
# {
#     "nodes": [elements],
#     "cost": ints
# }
