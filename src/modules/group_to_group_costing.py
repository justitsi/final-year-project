class GroupToGroupCostCalc:
    def __init__(self, NODES, GROUPS, COSTING_PARAMS):
        self.NUMBER_OF_GROUPS = len(GROUPS)
        self.GROUPS = GROUPS
        self.NODES = NODES
        self.COSTING_PARAMS = COSTING_PARAMS

    def getNodesByGroups(self, path):
        groups = []
        for i in range(self.NUMBER_OF_GROUPS):
            groups.append([])

        for item in path["nodes"]:
            groups[item["groupID"]].append(item["id"])

        return groups

    def calculateGroupToGroupCost(self, group1, group2):
        # add 100 cost for each difference in len
        return (len(group1) - len(group2)) * 100
