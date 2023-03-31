from static import Colours
from math import inf, dist
import pygame
from TextClass import Text
from ObstacleClass import gameMap


class Node:
    def __init__(self, X, Y, name=None, colour=Colours.black, gCost=inf, hCost=inf, fCost=inf, closestNode=None):
        self.name = name
        self.fCost = fCost
        self.gCost = gCost
        self.hCost = hCost
        self.x = X
        self.y = Y
        self.colour = colour
        self.adjNodes = {}
        self.closestNode = closestNode

    def setFCost(self):
        self.fCost = self.gCost + self.hCost

    # sets H cost to the heuristic distance from the node to the destination
    def setHCost(self, finalNode):
        self.hCost = dist((self.x, self.y), (finalNode.x, finalNode.y))

    def setGCost(self, val=0):
        self.gCost = val

    # finds the distance between two nodes
    def findDist(self, finalNode):
        return dist((self.x, self.y), (finalNode.x, finalNode.y))

    # draws nodes to the screen and changes their colour to red
    # draws lines between each node and red lines between the nodes in the path
    def drawNode(self, screen, font, Path, last):
        # pygame.draw.circle(screen, self.colour, [self.X, self.Y], 10)
        for adjNode in self.adjNodes:
            if Path.shortestPath and adjNode in Path.shortestPath and self in Path.shortestPath:
                pygame.draw.aaline(screen, Colours.red, [self.x, self.y], [adjNode.x, adjNode.y], 2)
                continue
        pygame.draw.circle(screen, Colours.red, [self.x, self.y], 5)
        pygame.draw.circle(screen, Colours.blue, [last.x, last.y], 10)
        # writes the name for each node on top
        nameText = Text(font, Colours.red, self.name, self.x, self.y)
        nameText.write(screen)

    # sets the coordinates of a node to a new coordinate
    def setCoord(self, newCoord):
        self.x = newCoord[0]
        self.y = newCoord[1]

    # rests the cost for each node and sets the colour back to black
    # runs every time a new path is created
    def reset(self):
        self.fCost = inf
        self.gCost = inf
        self.hCost = inf
        self.colour = Colours.black

    # used to add an adjacent node
    def addAdj(self, *nodes):
        for item in nodes:
            if not item:
                continue
            self.adjNodes.update({item: self.findDist(item)})

    # creates a dictionary of adjacent nodes and adds these to itself
    def findAdj(self, nodes):
        self.adjNodes = {}
        for item in nodes:
            if self.closestNode is None or self.closestNode is nodes[0]:
                self.closestNode = item
            if self.findDist(item) < self.findDist(self.closestNode):
                self.closestNode = item
        self.addAdj(self.closestNode)

    # this method creates a grid of nodes the size of the screen
    # it creates a node where there are blank spaces
    # it adds horizontal and diagonal adjacency's for each node
    @classmethod
    def dynamicNodes(cls):
        gap = (101, 108)
        nodesMap = []
        playerNode = Node(0, 0, "")
        nodesMap.append(playerNode)

        # create a temporary array of nodes where there are blank spaces on the gameMap array
        tempArray = [[Node((j * gap[0]) - 51, (i * gap[1]) - 54) if gameMap.grid[i, j] != 1 else None for j in range(gameMap.width)] for i in
                     range(gameMap.height)]
        for i, row in enumerate(tempArray):
            for j, node in enumerate(row):
                if not node:
                    continue
                # make sure not adding adjacency's off the screen
                if j < gameMap.width - 1:
                    node.addAdj(tempArray[i][j + 1])
                if i < gameMap.height - 1:
                    node.addAdj(tempArray[i + 1][j])

                # add adjacent nodes in all directions where a node is present
                if i > 0 and j > 0 and tempArray[i - 1][j - 1]:
                    node.addAdj(tempArray[i - 1][j - 1])
                if i > 0 and j < gameMap.width - 1 and tempArray[i - 1][j + 1]:
                    node.addAdj(tempArray[i - 1][j + 1])
                if i < gameMap.height - 1 and j > 0 and tempArray[i + 1][j - 1]:
                    node.addAdj(tempArray[i + 1][j - 1])
                if i < gameMap.height - 1 and j < gameMap.width - 1 and tempArray[i + 1][j + 1]:
                    node.addAdj(tempArray[i + 1][j + 1])

                nodesMap.append(node)
        return nodesMap, playerNode


class AStar:
    def __init__(self, nodes, firstNode):
        self.previousNode = None
        self.shortestPath = None
        self.graph = None
        self.shortest = None
        self.firstNode = firstNode
        self.finalNode = None
        self.iteration = 0
        self.nodes = nodes

    # used to find which node has the lowest fCost
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
        # when finding the path reset nodes and set hCosts
        for node in self.graph:
            node.reset()
            node.setHCost(self.finalNode)
            node.setFCost()
        # find distance to start of first node (player)
        self.firstNode.setGCost()
        # use the findAdj method to find the closest node to player
        self.firstNode.findAdj(self.graph)

        # run until shortest path is found
        while self.finalNode in self.graph:
            self.iteration += 1
            # find the closest neighbour
            self.findClosestNode()
            # loop through this node's neighbours
            for adjNode in self.shortest.adjNodes:
                # if a node isn't in the graph or if the path it creates is longer than the current path then go to next node
                if adjNode not in self.graph or self.shortest.adjNodes[adjNode] + self.shortest.gCost + adjNode.hCost > adjNode.fCost:
                    continue
                # set the gCost of the node to its current distance plus the previous node's gCost
                adjNode.gCost = self.shortest.adjNodes[adjNode] + self.shortest.gCost
                adjNode.setFCost()
                # update the path to contain this node
                self.previousNode.update({adjNode: self.shortest})
            # remove this node and go onto the next
            self.graph.remove(self.shortest)
        # start from the last node
        node = self.finalNode
        # set the first node to red
        self.firstNode.colour = Colours.red
        # loop through all nodes in the previousNode dictionary
        while node != self.firstNode:
            # set all the nodes to red
            node.colour = Colours.red
            # insert the current node to the path
            self.shortestPath.insert(0, node)
            # go onto the next node
            node = self.previousNode[node]
        # add the first node into the shortest path
        self.shortestPath.insert(0, self.firstNode)


def createNodes():
    nodesMap, playerNode = Node.dynamicNodes()
    Path = AStar(nodesMap, playerNode)
    return Path, nodesMap
