from static import Colours
from AStarClass import Node


class Dijkstra:
    def __init__(self, nodes, firstNode):
        self.previousNode = None
        self.shortestPath = None
        self.graph = None
        self.shortest = None
        self.firstNode = firstNode
        self.finalNode = None
        self.iteration = 0
        self.nodes = nodes

    def findClosestNode(self):
        self.shortest = None
        for node in self.graph:
            if self.shortest is None:
                self.shortest = node
            elif node.fCost < self.shortest.fCost:
                self.shortest = node

    # finds the path between two given nodes
    def findPath(self, player):
        self.graph = self.nodes.copy()
        self.shortestPath = []
        self.previousNode = {}
        self.finalNode = self.graph[-1]
        self.firstNode.x = player.x
        self.firstNode.y = player.y
        for node in self.graph:
            node.reset()
            node.setFCost()

        self.firstNode.setGCost()
        self.firstNode.findAdj(self.graph)

        while self.finalNode in self.graph:
            self.iteration += 1
            self.findClosestNode()
            for adjNode in self.shortest.adjNodes:
                if adjNode not in self.graph or self.shortest.adjNodes[adjNode] + self.shortest.gCost > adjNode.fCost:
                    continue
                adjNode.gCost = self.shortest.adjNodes[adjNode] + self.shortest.gCost
                adjNode.setFCost()
                self.previousNode.update({adjNode: self.shortest})

            self.graph.remove(self.shortest)
        node = self.finalNode
        self.firstNode.colour = Colours.red
        while node != self.firstNode:
            node.colour = Colours.red
            self.shortestPath.insert(0, node)
            node = self.previousNode[node]
        self.shortestPath.insert(0, self.firstNode)


def createPath(nodesMap):
    Path = Dijkstra(nodesMap, Node(0, 0, "Player"))
    return Path
