class NodeToGroupCostCalc:
    def __init__(self, GROUP_SIZE, LARGE_GROUP_PENALTY):
        self.GROUP_SIZE = GROUP_SIZE
        self.LARGE_GROUP_PENALTY = LARGE_GROUP_PENALTY

    # array of node ids from path ([int]), id(int) and id (int)
    def getNodeToGroupCost(self, nodesInGroup, groupID, nodeToAddID):
        cost = 0
        groupSize = len(nodesInGroup) + 1

        # check if group size limit hasn't been exceeded
        if (groupSize >= self.GROUP_SIZE):
            cost += self.LARGE_GROUP_PENALTY * ((groupSize) - self.GROUP_SIZE)

        return cost
