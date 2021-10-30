import time
import json
import copy
from modules.utils import removeElementFromArray, printTree
from modules.node_node_costing import NodeToNodeCostCalc
from modules.node_to_group_costing import NodeToGroupCostCalc
start = time.time()


with open('./samples/students/12_4.json', encoding='utf-8') as F:
    json_data = json.loads(F.read())
# read sample data and alg_params
COSTING = json_data['costing_params']
NODES = json_data['nodes']
GROUPS = json_data['groups']
NUMBER_OF_GROUPS = len(GROUPS)

# algorithm params
alg_params = json_data['alg_params']
# pruning params
TREE_PRUNE_TRESHOLD = alg_params['TREE_PRUNE_TRESHOLD']
STEP_MAX_COST = alg_params['STEP_MAX_COST']
MINIMUM_ACCEPTABLE_SOLUTION = alg_params['MINIMUM_ACCEPTABLE_SOLUTION']

# costing params
GROUP_BASE_COST = alg_params['GROUP_BASE_SCORE']

# initialize costing modules
NODE_NODE_COST_CALC = NodeToNodeCostCalc(NODES, COSTING['node-node'])  # nopep8
NODE_GROUP_COST_CALC = NodeToGroupCostCalc(NODES, GROUPS, COSTING['node-group'])  # nopep8


# main recursive path finding function
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

                # if returned tree contains all nodes and is bellow the minimum acceptable cost, stop execution
                if (len(childTree['nodes']) == len(NODES)):
                    if (childTree['cost'] <= MINIMUM_ACCEPTABLE_SOLUTION):
                        return returnTrees

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
    cost += NODE_GROUP_COST_CALC.getNodeToGroupCost(nodesInGroup, el['groupID'], el['id'])  # nopep8

    # calculate cost for nodes in grouping
    cost += NODE_NODE_COST_CALC.getNodeToNodesCost(nodesInGroup, el['id'])

    return cost


# instantiate tree and nodes to be explored
currentTree = {
    "nodes": [{"groupID": 1, "id": NODES[0]['id']}],
    "cost": 0
}
remainginNodes = []
for node in NODES:
    remainginNodes.append(node['id'])

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
