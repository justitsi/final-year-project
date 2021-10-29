class NodeToNodeCostCalc:
    def __init__(self, NODES, AFFINITY_BONUS):
        self.NODES = NODES
        self.AFFINITY_BONUS = AFFINITY_BONUS

        nodeIDs = []
        for node in NODES:
            nodeIDs.append(node['id'])

        # pre-calculate costs and store them in lookup table (memoization)
        self.NODE_PAIRING_COSTS = self.preCalculateNodeToNodeCosts(nodeIDs)  # nopep8

    # array of node ids from path ([int]) and id (int)
    def getNodeToNodesCost(self, nodesInGroup, nodeToAddID):
        cost = 0
        # check for affinities
        for groupNode in nodesInGroup:
            cost += self.getNodeToNodeCost(groupNode, nodeToAddID)

        return cost

    # lookup results for node-node pairing in NODE_PAIRING_COSTS
    def getNodeToNodeCost(self, nodeID1, nodeID2):
        return self.NODE_PAIRING_COSTS[nodeID1][nodeID2]

    # both arguments contain full node data dictionaries
    def calculateNodeToNodeCost(self, node1, node2):
        cost = 0

        if (node1['affinities']):
            for affinity in node1['affinities']:
                if (affinity == node2['id']):
                    cost -= self.AFFINITY_BONUS

        if (node2['affinities']):
            for affinity in node2['affinities']:
                if (affinity == node1['id']):
                    cost -= self.AFFINITY_BONUS

        return cost

    # returns full node properties as dictionary
    def getNodeProperties(self, nodeID):
        for node in self.NODES:
            if nodeID == node['id']:
                return node
        return {}

    # precalculate costs for each node-to-node pairings
    # assumes that nodes are sorted by id
    def preCalculateNodeToNodeCosts(self, nodes):
        costs = []

        for i in range(0, len(nodes)):
            currentNode = self.getNodeProperties(nodes[i])
            currentCosts = []

            for j in range(0, len(nodes)):
                comparisonNode = self.getNodeProperties(nodes[j])
                currentCosts.append(self.calculateNodeToNodeCost(currentNode, comparisonNode))  # nopep8

            costs.append(currentCosts)

        return costs
