import time
import copy
import json
from modules.utils import removeElementFromArray, printTree
from modules.node_node_costing import NodeToNodeCostCalc
from modules.node_to_group_costing import NodeToGroupCostCalc


class jobRunner:
    def __init__(self, job_spec):
        # read sample data and alg_params
        self.COSTING = job_spec['costing_params']
        self.NODES = job_spec['nodes']
        self.GROUPS = job_spec['groups']
        self.NUMBER_OF_GROUPS = len(self.GROUPS)

        # algorithm params
        alg_params = job_spec['alg_params']
        # pruning params
        self.TREE_PRUNE_TRESHOLD = alg_params['TREE_PRUNE_TRESHOLD']
        self.STEP_MAX_COST = alg_params['STEP_MAX_COST']
        self.MINIMUM_ACCEPTABLE_SOLUTION = alg_params['MINIMUM_ACCEPTABLE_SOLUTION']

        # initialize costing modules
        self.NODE_NODE_COST_CALC = NodeToNodeCostCalc(self.NODES, self.COSTING['node-node'])  # nopep8
        self.NODE_GROUP_COST_CALC = NodeToGroupCostCalc(self.NODES, self.GROUPS, self.COSTING['node-group'])  # nopep8

    # main recursive path finding function
    def generateTree(self, currentTree, remainingElements):
        # take out id that will be added to the array
        idToAdd = remainingElements[0]
        remainingElementsCopy = removeElementFromArray(remainingElements, remainingElements[0])  # nopep8

        possibleTrees = []
        returnTrees = []

        if (len(remainingElementsCopy) > 0):
            for i in range(0, self.NUMBER_OF_GROUPS):
                # instanciate element to add
                elementToAddCopy = {
                    'groupID': i,
                    'id': idToAdd
                }

                # get cost to add
                costToAdd = self.getCost(currentTree, elementToAddCopy)
                totalTreeCost = currentTree['cost'] + costToAdd

                # add info to possible trees if tested tree is OK
                if (costToAdd < self.STEP_MAX_COST):
                    if (totalTreeCost < self.TREE_PRUNE_TRESHOLD):
                        # instanciate copy of currently tested tree
                        currentTreeCopy = copy.deepcopy(currentTree)

                        currentTreeCopy['nodes'].append(elementToAddCopy)
                        currentTreeCopy['cost'] = totalTreeCost

                        possibleTrees.append(currentTreeCopy)

            # re-run the function for valid candidate trees
            for tree in possibleTrees:
                childTrees = self.generateTree(tree, remainingElementsCopy)
                for childTree in childTrees:
                    returnTrees.append(childTree)

                    # if returned tree contains all nodes and is bellow the minimum acceptable cost, stop execution
                    if (len(childTree['nodes']) == len(self.NODES)):
                        if (childTree['cost'] <= self.MINIMUM_ACCEPTABLE_SOLUTION):
                            return returnTrees

            return returnTrees

        else:
            for i in range(0, self.NUMBER_OF_GROUPS):
                # instanciate element to add
                elementToAddCopy = {
                    'groupID': i,
                    'id': idToAdd
                }

                # get cost to add
                costToAdd = self.getCost(currentTree, elementToAddCopy)
                totalTreeCost = currentTree['cost'] + costToAdd

                # add info to possible trees if tested tree is OK
                if (costToAdd < self.STEP_MAX_COST):
                    if (totalTreeCost < self.TREE_PRUNE_TRESHOLD):
                        # instanciate copy of currently tested tree
                        currentTreeCopy = copy.deepcopy(currentTree)

                        currentTreeCopy['nodes'].append(elementToAddCopy)
                        currentTreeCopy['cost'] = totalTreeCost

                        possibleTrees.append(currentTreeCopy)

            # return bottom-level path costs
            return possibleTrees

    # returns the cost of adding an element to a specific path
    def getCost(self, currentTree, el):
        cost = 0

        # get nodeIDs for nodes in group
        nodesInGroup = []
        for node in currentTree['nodes']:
            if (node['groupID'] == el['groupID']):
                nodesInGroup.append(node['id'])

        # calculate cost for group in grouping
        cost += self.NODE_GROUP_COST_CALC.getNodeToGroupCost(nodesInGroup, el['groupID'], el['id'])  # nopep8

        # calculate cost for nodes in grouping
        cost += self.NODE_NODE_COST_CALC.getNodeToNodesCost(
            nodesInGroup, el['id'])

        return cost

    # run job
    def run(self):
        # instantiate tree and nodes to be explored
        currentTree = {
            "nodes": [{"groupID": 1, "id": self.NODES[0]['id']}],
            "cost": 0
        }
        remainginNodes = []
        for node in self.NODES:
            remainginNodes.append(node['id'])

        # run binary search alg
        remainginNodes = removeElementFromArray(remainginNodes, self.NODES[0]['id'])  # nopep8
        possible_trees = self.generateTree(currentTree, remainginNodes)

        return possible_trees


def main():
    start = time.time()
    with open('./samples/students/12_4.json', encoding='utf-8') as F:
        json_data = json.loads(F.read())

    runner = jobRunner(json_data)

    possible_trees = runner.run()

    # print readable results
    if (json_data['alg_params']['PRINT_RESULTS']):
        for tree in possible_trees:
            printTree(tree)
            print('\n')

    print("Viable solutions found: " + str(len(possible_trees)))
    if len(possible_trees) > 0:
        tree_cost_sum = 0
        best_tree = possible_trees[0]

        for tree in possible_trees:
            tree_cost_sum += tree['cost']
            if tree['cost'] <= best_tree['cost']:
                best_tree = tree

        printTree(best_tree)

        print()
        print(f"Avg. cost: {str(tree_cost_sum/len(possible_trees))}")

    # profiling/ calculate execution time of program
    end = time.time()
    print(f"Runtime:   {end - start}")


main()
