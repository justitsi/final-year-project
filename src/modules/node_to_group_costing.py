class NodeToGroupCostCalc:
    def __init__(self, NODES, GROUPS, COSTING_PARAMS):
        self.GROUPS = GROUPS
        self.NODES = NODES
        self.PRERUN_COSTING_PARAMS = COSTING_PARAMS['pre-run-costs']
        self.RUNTIME_COSTING_PARAMS = COSTING_PARAMS['runtime-costs']

        # extract node and group IDs
        groupIDs = []
        for group in GROUPS:
            groupIDs.append(group['id'])

        nodeIDs = []
        for node in NODES:
            nodeIDs.append(node['id'])

        # pre-calculate costs and store them in lookup table (memoization)
        self.GROUP_NODE_PAIRING_COSTS = self.preCalculateGroupToNodeCosts(groupIDs, nodeIDs)  # nopep8

    # array of node ids from path ([int]), id(int) and id (int)
    def getNodeToGroupCost(self, nodesInGroup, groupID, nodeToAddID):
        cost = 0

        # get runtime cost of adding node to group
        cost = self.calculateRuntimeGroupToNodeCost(groupID, nodesInGroup, nodeToAddID)  # nopep8
        # get pre-calculated static costs
        cost += self.getGroupToNodeCost(groupID, nodeToAddID)

        return cost

    def calculateRuntimeGroupToNodeCost(self, groupID, groupNodesIDs, nodeToAddID):
        cost = 0
        group_info_full = self.getGroupProperties(groupID)

        for param in self.RUNTIME_COSTING_PARAMS:
            if (param['operation'] == 'count_all_over'):
                groupSize = len(groupNodesIDs) + 1
                if (groupSize >= group_info_full[param['group_property_name']]):
                    cost += param['multiplier'] * ((groupSize) - group_info_full[param['group_property_name']])  # nopep8

            if (param['operation'] == 'count_all_under'):
                groupSize = len(groupNodesIDs) + 1
                if (groupSize <= group_info_full[param['group_property_name']]):
                    cost += param['multiplier'] * (group_info_full[param['group_property_name']] - (groupSize))  # nopep8

            if (param['operation'] == 'add_once'):
                if (len(groupNodesIDs) == 0):
                    cost += param['multiplier'] * group_info_full[param['group_property_name']]  # nopep8

        return cost

    # lookup results for group-node pairing in GROUP_NODE_PAIRING_COSTS
    def getGroupToNodeCost(self, groupID, nodeID):
        return self.GROUP_NODE_PAIRING_COSTS[groupID][nodeID]

    # precalculate costs for each group-to-node pairing
    # assumes that nodes and groups are sorted by id
    def preCalculateGroupToNodeCosts(self, groups, nodes):
        costs = []

        for i in range(0, len(groups)):
            currentGroup = self.getGroupProperties(groups[i])
            currentCosts = []

            for j in range(0, len(nodes)):
                comparisonNode = self.getNodeProperties(nodes[j])
                currentCosts.append(self.calculatePreRunGroupToNodeCost(currentGroup, comparisonNode))  # nopep8

            costs.append(currentCosts)

        return costs

    # both arguments contain full group/node data dictionaries
    def calculatePreRunGroupToNodeCost(self, group, node):
        preRunCostParams = self.PRERUN_COSTING_PARAMS
        cost = 0

        for costParam in preRunCostParams:
            groupProperty = group[costParam['group_property_name']]
            nodeProperty = node[costParam['node_property_name']]

            if (costParam['operation'] == 'difference_absolute'):
                cost = abs(groupProperty - nodeProperty) * costParam['multiplier']  # nopep8

            if (costParam['operation'] == 'difference_over'):
                difference = groupProperty - nodeProperty
                if (difference < 0):
                    cost = (-difference) * costParam['multiplier']

            if (costParam['operation'] == 'difference_under'):
                difference = groupProperty - nodeProperty
                if (difference > 0):
                    cost = difference * costParam['multiplier']

            if (costParam['operation'] == 'binary_group_array_excludes'):
                includes = False
                for i in range(0, len(groupProperty)):
                    if groupProperty[i] == 1:
                        if nodeProperty[i] == groupProperty[i]:
                            includes = True
                            break

                if (not includes):
                    cost = costParam['multiplier']

            if (costParam['operation'] == 'affinities_list_prioritised'):
                pass
        return cost

    # lookup full group properties by id
    def getGroupProperties(self, groupID):
        for group in self.GROUPS:
            if groupID == group['id']:
                return group
        return {'id': -1}

    # lookup full node properties by id
    def getNodeProperties(self, nodeID):
        for node in self.NODES:
            if nodeID == node['id']:
                return node
        return {'id': -1}
