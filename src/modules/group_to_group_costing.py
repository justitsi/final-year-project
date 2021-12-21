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
        return cost
