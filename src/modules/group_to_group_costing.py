class GroupToGroupCostCalc:
    def __init__(self, NODES, GROUPS, COSTING_PARAMS):
        self.NUMBER_OF_GROUPS = len(GROUPS)
        self.GROUPS = GROUPS
        self.NODES = NODES
        self.POST_RUN_COSTING_PARAMS = COSTING_PARAMS['post-run-costs']

    def getNodesByGroups(self, path):
        groups = []
        for i in range(self.NUMBER_OF_GROUPS):
            groups.append([])

        for item in path["nodes"]:
            groups[item["groupID"]].append(item["id"])

        return groups

    def calculatePostRunCost(self, group1, group2):
        cost = 0

        for operation in self.POST_RUN_COSTING_PARAMS:
            if operation['operation'] == 'difference_count_nodes':
                cost += (len(group1) - len(group2)) * operation['multiplier']
            if operation['operation'] == 'nodes_inlcude_property':
                # get the full about the nodes in both groups
                nodesG1 = []
                for entry in group1:
                    nodesG1.append(self.getNodeProperties(entry))

                nodesG2 = []
                for entry in group2:
                    nodesG2.append(self.getNodeProperties(entry))

                # check nodes from both groups/labels for repeating attributes
                for node1 in nodesG1:
                    for node2 in nodesG2:
                        if (node1[operation['node_propery_to_check']] == node2[operation['node_propery_to_check']]):
                            cost += operation['multiplier']

        return cost

    # lookup full node properties by id
    def getNodeProperties(self, nodeID):
        for node in self.NODES:
            if nodeID == node['id']:
                return node
        return {'id': -1}

    # lookup full group properties by id
    def getGroupProperties(self, groupID):
        for group in self.GROUPS:
            if groupID == group['id']:
                return group
        return {'id': -1}
