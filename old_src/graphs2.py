import time
import json
import copy
start = time.time()


with open('sample_data_2.json', encoding='utf-8') as F:
    json_data = json.loads(F.read())
# read sample data and alg_params
sample = json_data['data']
alg_params = json_data['alg_params']


NUMBER_OF_GROUPS = alg_params['NUMBER_OF_GROUPS']
GROUP_SIZE = alg_params['GROUP_SIZE']
# pruning params
TREE_PRUNE_TRESHOLD = alg_params['TREE_PRUNE_TRESHOLD']
STEP_MAX_COST = alg_params['STEP_MAX_COST']
# costing params
GROUP_BASE_SCORE = alg_params['GROUP_BASE_SCORE']
LARGE_GROUP_PENALTY = alg_params['LARGE_GROUP_PENALTY']
AFFINITY_BONUS = alg_params['AFFINITY_BONUS']


def generateTree(currentTree, remainingElements):
    treePruneThreshold = TREE_PRUNE_TRESHOLD
    stepMaxCost = STEP_MAX_COST
    numberOfGroups = NUMBER_OF_GROUPS

    elementToAdd = {
        'groupID': None,
        'properties': remainingElements[0]
    }

    remainingElementsCopy = removeElementFromArray(
        remainingElements, remainingElements[0])

    possibleTrees = []
    if (len(remainingElementsCopy) > 0):
        for i in range(0, numberOfGroups):
            # instanciate element copy
            elementToAddCopy = copy.deepcopy(elementToAdd)
            elementToAddCopy['groupID'] = i
            # instanciate tree copy
            currentTreeCopy = copy.deepcopy(currentTree)

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTreeCopy['cost'] + costToAdd

            # add info to currentTreeCopy
            if (costToAdd < stepMaxCost):
                if (totalTreeCost < treePruneThreshold):
                    currentTreeCopy['elements'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                    possibleTrees.append(currentTreeCopy)

        returnTrees = []
        for tree in possibleTrees:
            childTrees = generateTree(tree, remainingElementsCopy)
            for childTree in childTrees:
                returnTrees.append(childTree)

        return returnTrees
    else:
        returnTrees = []

        for i in range(0, numberOfGroups):
            possibleTrees = []
            # instanciate element copy
            elementToAddCopy = copy.deepcopy(elementToAdd)
            elementToAddCopy['groupID'] = i
            # instanciate tree copy
            currentTreeCopy = copy.deepcopy(currentTree)

            # get cost to add
            costToAdd = getCost(currentTree, elementToAddCopy)
            totalTreeCost = currentTreeCopy['cost'] + costToAdd

            # add info to currentTreeCopy
            if (costToAdd < stepMaxCost):
                if (totalTreeCost < treePruneThreshold):
                    currentTreeCopy['elements'].append(elementToAddCopy)
                    currentTreeCopy['cost'] = totalTreeCost

                    possibleTrees.append(currentTreeCopy)

            for tree in possibleTrees:
                returnTrees.append(tree)

        return returnTrees


def getCost(currentTree, el):
    score = GROUP_BASE_SCORE
    group_size_limit = GROUP_SIZE
    large_group_penalty = LARGE_GROUP_PENALTY
    affinity_bonus = AFFINITY_BONUS

    # check if group size limit hasn't been exceeded
    group_size = 0
    group_members = []

    for node in currentTree['elements']:
        if (int(node['groupID']) == int(el['groupID'])):
            group_size += 1
            group_members.append(node)

            if (group_size >= group_size_limit):
                # increase the cost of having larger groups
                score += large_group_penalty

    # check if there is an (mutual) affinity specified in the node properties
    el_properties = el['properties']
    for node in group_members:
        # check if other nodes pair with current element
        node_properties = node['properties']
        for affinity in node_properties['affinities']:
            if (el_properties['id'] == affinity):
                score -= affinity_bonus

        # check if current element pairs with other nodes
        for affinity in el_properties['affinities']:
            if (affinity == node_properties['id']):
                score -= affinity_bonus

    return score


def removeElementFromArray(arr, el):
    arr_copy = copy.deepcopy(arr)

    for i in range(0, len(arr)):
        if arr[i]['id'] == el['id']:
            arr_copy.pop(i)
            break

    return arr_copy


def printTree(tree):
    string1 = ""
    string2 = ""

    for element in tree['elements']:
        string1 += str(element['properties']['id']) + " "
    for element in tree['elements']:
        string2 += str(element['groupID']) + " "

    print(string1)
    print(string2)
    print(tree['cost'])


currentTree = {
    'elements': [
        {
            'groupID': 1,
            'properties': sample[0]
        }
    ],
    "cost": 0
}

el = {
    'groupID': 1,
    'properties': sample[2]
}

possible_trees = generateTree(
    currentTree, removeElementFromArray(sample, sample[0]))


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

# element def
# {
#     'groupID': 1,
#     'properties': {
#         'id': 1,
#         'affinities': [0, 3]
#     }
# }

# tree def
# {
#     "elements": [elements],
#     "cost": ints
# }
