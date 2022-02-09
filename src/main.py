import time
import copy
import json
from modules.utils import removeElementFromArray, printTree
from modules.node_node_costing import NodeToNodeCostCalc
from modules.node_to_group_costing import NodeToGroupCostCalc
from modules.group_to_group_costing import GroupToGroupCostCalc


class jobRunner:
    def __init__(self, job_spec):
        # read sample data and alg_params
        self.COSTING = job_spec["costing_params"]
        self.NODES = job_spec["nodes"]
        self.GROUPS = job_spec["groups"]
        self.NUMBER_OF_GROUPS = len(self.GROUPS)

        # algorithm params
        alg_params = job_spec["alg_params"]
        # pruning params
        self.TREE_PRUNE_TRESHOLD = alg_params["TREE_PRUNE_TRESHOLD"]
        self.STEP_MAX_COST = alg_params["STEP_MAX_COST"]
        self.MINIMUM_ACCEPTABLE_SOLUTION = alg_params["MINIMUM_ACCEPTABLE_SOLUTION"]

        # initialize costing modules
        self.NODE_NODE_COST_CALC = NodeToNodeCostCalc(self.NODES, self.COSTING["node-node"])  # nopep8
        self.NODE_GROUP_COST_CALC = NodeToGroupCostCalc(self.NODES, self.GROUPS, self.COSTING["node-group"])  # nopep8
        self.GROUP_GROUP_COST_CALC = GroupToGroupCostCalc(self.NODES, self.GROUPS, self.COSTING["group-group"])  # nopep8

    # main recursive path finding function
    def pairNodes(self, currentTree, remainingElements):
        # take out id that will be added to the array
        idToAdd = remainingElements[0]
        remainingElementsCopy = removeElementFromArray(remainingElements, remainingElements[0])  # nopep8

        possibleTrees = []
        returnTrees = []

        if len(remainingElementsCopy) > 0:
            for i in range(0, self.NUMBER_OF_GROUPS):
                # instanciate element to add
                elementToAddCopy = {"groupID": i, "id": idToAdd}

                # get cost to add
                costToAdd = self.getNodeCost(currentTree, elementToAddCopy)
                totalTreeCost = currentTree["cost"] + costToAdd

                # add info to possible trees if tested tree is OK
                if costToAdd < self.STEP_MAX_COST:
                    if totalTreeCost < self.TREE_PRUNE_TRESHOLD:
                        # instanciate copy of currently tested tree
                        currentTreeCopy = copy.deepcopy(currentTree)

                        currentTreeCopy["nodes"].append(elementToAddCopy)
                        currentTreeCopy["cost"] = totalTreeCost

                        possibleTrees.append(currentTreeCopy)

            # re-run the function for valid candidate trees
            for tree in possibleTrees:
                childTrees = self.pairNodes(tree, remainingElementsCopy)
                for childTree in childTrees:
                    returnTrees.append(childTree)

                    # if returned tree contains all nodes and is bellow the minimum acceptable cost, stop execution
                    if len(childTree["nodes"]) == len(self.NODES):
                        if childTree["cost"] <= self.MINIMUM_ACCEPTABLE_SOLUTION:
                            return returnTrees

            return returnTrees

        else:
            for i in range(0, self.NUMBER_OF_GROUPS):
                # instanciate element to add
                elementToAddCopy = {"groupID": i, "id": idToAdd}

                # get cost to add
                costToAdd = self.getNodeCost(currentTree, elementToAddCopy)
                totalTreeCost = currentTree["cost"] + costToAdd

                # add info to possible trees if tested tree is OK
                if costToAdd < self.STEP_MAX_COST:
                    if totalTreeCost < self.TREE_PRUNE_TRESHOLD:
                        # instanciate copy of currently tested tree
                        currentTreeCopy = copy.deepcopy(currentTree)

                        currentTreeCopy["nodes"].append(elementToAddCopy)
                        currentTreeCopy["cost"] = totalTreeCost

                        possibleTrees.append(currentTreeCopy)

            # return bottom-level path costs
            return possibleTrees

    # returns the cost of adding an element to a specific path
    def getNodeCost(self, currentTree, el):
        cost = 0

        # get nodeIDs for nodes in group
        nodesInGroup = []
        for node in currentTree["nodes"]:
            if node["groupID"] == el["groupID"]:
                nodesInGroup.append(node["id"])

        # calculate cost for group in grouping
        cost += self.NODE_GROUP_COST_CALC.getNodeToGroupCost(nodesInGroup, el["groupID"], el["id"])  # nopep8

        # calculate cost for nodes in grouping
        cost += self.NODE_NODE_COST_CALC.getNodeToNodesCost(
            nodesInGroup, el["id"])

        return cost

    # recursive function for ordering nodes
    def orderGroups(self, groupsOrdered, groupsRemaining):
        # groupsOrdered is empty, populate it!
        if len(groupsOrdered["groups"]) == 0:
            possible_results = []
            for i in range(0, len(groupsRemaining)):
                # create new instances of funciton objects
                groupsRemainingCopy = groupsRemaining.copy()

                groupToEvaluate = groupsRemainingCopy[i]
                del groupsRemainingCopy[i]

                groupsOrderedCopy = copy.deepcopy(groupsOrdered)
                groupsOrderedCopy["groups"] = [groupToEvaluate]

                # get all possible solutions
                results = self.orderGroups(groupsOrderedCopy, groupsRemainingCopy)  # nopep8

                for result in results:
                    possible_results.append(result)

            return possible_results
        else:
            # init last group in groupsOrdered
            lastInList = groupsOrdered["groups"][len(groupsOrdered["groups"]) - 1]  # nopep8

            # if there's groups to be ordered call orderGroups function
            if len(groupsRemaining) > 1:

                possible_results = []
                for i in range(0, len(groupsRemaining)):
                    # get group to evaluate
                    groupToEvaluate = groupsRemaining[i]

                    # create a copy of the remaining groups array to pass to the recursive function
                    groupsRemainingCopy = groupsRemaining.copy()
                    del groupsRemainingCopy[i]

                    # create a copy of the object that holds the current order data
                    groupsOrderedCopy = copy.deepcopy(groupsOrdered)
                    # add the cost of adding the current group to this ordering to the order data object
                    groupsOrderedCopy['cost'] += self.groupToGroupCost(lastInList, groupToEvaluate)  # nopep8
                    groupsOrderedCopy['groups'].append(groupToEvaluate)  # nopep8

                    # call recusrsive function to get cost at bottom
                    results = self.orderGroups(groupsOrderedCopy, groupsRemainingCopy)  # nopep8

                    for result in results:
                        possible_results.append(result)

                return possible_results
            # if array has only one item then it's a leaf, add it to the end and return the full ordering
            else:
                # get the first unordered group from the list
                groupToEvaluate = groupsRemaining[0]
                del groupsRemaining[0]

                # add element to groupsOrdered and calculate new cost
                groupsOrdered["cost"] += self.groupToGroupCost(lastInList, groupToEvaluate)  # nopep8
                groupsOrdered["groups"].append(groupToEvaluate)  # nopep8

                return [groupsOrdered]

    # returns the cost of putting group2 after group1
    def groupToGroupCost(self, group1, group2):
        return self.GROUP_GROUP_COST_CALC.calculatePostRunCost(group1, group2)

    # run node pairing job
    def getBestPairings(self):
        # instantiate tree and nodes to be explored
        currentTree = {"nodes": [{"groupID": 1, "id": self.NODES[0]["id"]}], "cost": 0}  # nopep8
        remainginNodes = []
        for node in self.NODES:
            remainginNodes.append(node["id"])

        # run binary search alg
        remainginNodes = removeElementFromArray(remainginNodes, self.NODES[0]["id"])  # nopep8
        possible_trees = self.pairNodes(currentTree, remainginNodes)

        return possible_trees

    # run group ordering job
    def getOptimalGroupOrder(self, path):
        best_groups = self.GROUP_GROUP_COST_CALC.getNodesByGroups(path)
        order_object = {"groups": [], "cost": 0}

        possible_orders = self.orderGroups(order_object, best_groups)
        best_order = possible_orders[0]

        for order in possible_orders:
            if order['cost'] < best_order['cost']:
                best_order = order

        return best_order


def main():
    start = time.time()
    output_location = './tmp_output.json'
    marketing_loc = './samples/marketing/20_2.json'
    mentoring_loc = './samples/mentoring/job.json'
    real_students_loc = './samples/students_excel/job.json'

    with open(real_students_loc, encoding="utf-8") as F:
        json_data = json.loads(F.read())

    runner = jobRunner(json_data)
    possible_trees = runner.getBestPairings()

    # print readable results
    if json_data["alg_params"]["PRINT_RESULTS"]:
        for tree in possible_trees:
            printTree(tree)
            print("\n")

    print("Viable solutions found: " + str(len(possible_trees)))
    if len(possible_trees) > 0:
        tree_cost_sum = 0
        best_tree = possible_trees[0]

        for tree in possible_trees:
            tree_cost_sum += tree["cost"]
            if tree["cost"] <= best_tree["cost"]:
                best_tree = tree

        printTree(best_tree)
        print()

        # best_order = runner.getOptimalGroupOrder(best_tree)

        # print(best_order['groups'])
        # print()
        print(f"Number of solutions: {len(possible_trees)}")
        print(f"Avg. cost: {str(tree_cost_sum/len(possible_trees))}")

        # save results as json file
        # delete job file and generate new one
        with open(output_location, 'w') as f:
            json.dump(best_tree, f)

    # profiling/ calculate execution time of program
    end = time.time()
    print(f"Runtime:   {end - start}")


main()
