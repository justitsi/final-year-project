class NodeToNodeCostCalc:
    def __init__(self, NODES, COSTING_PARAMS):
        self.NODES = NODES
        self.COSTING_PARAMS = COSTING_PARAMS["pre-run-costs"]

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
        costParams = self.COSTING_PARAMS
        cost = 0

        for costParam in costParams:
            node1Property = node1[costParam['node_property_name']]
            node2Property = node2[costParam['node_property_name']]

            # handle includes_node_id operation
            if (costParam['operation'] == 'includes_node_id'):
                if (node1Property):
                    for item in node1Property:
                        if (item == node2['id']):
                            cost -= costParam['multiplier']

                if (node2Property):
                    for item in node2Property:
                        if (item == node1['id']):
                            cost -= costParam['multiplier']

            # handle similiarity_float operation
            if (costParam['operation'] == 'similiarity_float'):
                if (node1Property and node2Property):
                    difference = 1
                    if (node1Property > node2Property):
                        difference = node2Property/node1Property
                    else:
                        difference = node1Property/node2Property

                    cost += costParam['multiplier'] * difference

            # handle is_equal operation
            if (costParam['operation'] == 'is_equal'):
                if (node1Property and node2Property):
                    if (node1Property == node2Property):
                        cost += costParam['multiplier']

        return cost

    # lookup full node properties by id
    def getNodeProperties(self, nodeID):
        for node in self.NODES:
            if nodeID == node['id']:
                return node
        return {'id': -1}

    # precalculate costs for each node-to-node pairing
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
