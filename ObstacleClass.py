from static import Colours
import pygame
from CollisionClass import Line
import numpy as np

objectSprites = pygame.sprite.Group()
collisionObj = []


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, coord, cell, obstacleType, addObjects):
        super().__init__()
        self.width = gameMap.blockSize[0]
        self.height = gameMap.blockSize[1]
        self.x1 = coord[0] - self.width
        self.y1 = coord[1] - self.height
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.cell = cell
        self.offsets = []
        self.adjacencyMatrix = np.zeros((3, 3), dtype=int)
        self.adjacencyMatrix[1, 1] = 1
        self.obstacleType = obstacleType
        self.image = pygame.Surface((self.width - 15, self.height - 15))
        if addObjects:
            objectSprites.add(self)
        self.rect = self.image.fill(Colours.white)
        self.rect = pygame.rect.Rect(self.x1 + 15, self.y1 + 15, self.width - 30, self.height - 30)
        self.center = self.rect.center

    @classmethod
    def createLines(cls, objects):
        for obstacle in objects:
            left, right, up, down = 0, 0, 0, 0
            if (-1, 0) in obstacle.offsets:
                up = 30
            if (0, -1) in obstacle.offsets:
                left = 30
            if (0, 1) in obstacle.offsets:
                right = 30
            if (1, 0) in obstacle.offsets:
                down = 30

            if (-1, 1) in obstacle.offsets or (1, 1) in obstacle.offsets and right != 0:
                right = 0
            if (-1, -1) in obstacle.offsets or (1, -1) in obstacle.offsets and left != 0:
                left = 0
            if (-1, 1) in obstacle.offsets or (-1, -1) in obstacle.offsets and up != 0:
                up = 0
            if (1, 1) in obstacle.offsets or (1, -1) in obstacle.offsets and down != 0:
                down = 0

            if not up:
                collisionObj.append(Line(obstacle.x1 + 15 - left, obstacle.y1 + 15, obstacle.x2 - 15 + right, obstacle.y1 + 15, 1))
            if not left:
                collisionObj.append(Line(obstacle.x1 + 15, obstacle.y1 + 15 - up, obstacle.x1 + 15, obstacle.y2 - 15 + down, 2))
            if not down:
                collisionObj.append(Line(obstacle.x1 + 15 - left, obstacle.y2 - 15, obstacle.x2 - 15 + right, obstacle.y2 - 15, 3))
            if not right:
                collisionObj.append(Line(obstacle.x2 - 15, obstacle.y1 + 15 - up, obstacle.x2 - 15, obstacle.y2 - 15 + down, 4))

    @classmethod
    def drawObstacle(cls, objects, screen):
        for obstacle in objects:
            if obstacle.cell[0] == 0 or obstacle.cell[1] == 0 or obstacle.cell[0] == gameMap.height-1 or obstacle.cell[1] == gameMap.width-1:
                continue
            adjacencyList = obstacle.adjacencyMatrix.tolist()
            name = "[" + " ".join(["[{} {} {}]".format(row[0], row[1], row[2]) for row in adjacencyList]) + "]"
            image = pygame.image.load(f'ObstacleImages/{name}.xcf')
            screen.blit(image, (obstacle.x1, obstacle.y1))

    def getNeighbors(self, gameGrid):
        # calculate what neighbors each cell has
        offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]
        for offset in offsets:
            row = self.cell[0] + offset[0]
            col = self.cell[1] + offset[1]
            if 0 <= row < gameGrid.height and 0 <= col < gameGrid.width and gameGrid.grid[row, col] == 1:
                self.offsets.append(offset)


class Map:
    def __init__(self, blockSize, width, height, draw=True):
        self.blockSize = blockSize
        self.width = width
        self.height = height
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1
        self.grid[1, :] = 1
        self.grid[-2, :] = 1
        self.grid[:, 1] = 1
        self.grid[:, -2] = 1
        self.obstacles = []
        self.draw = draw

    def setObstacle(self, obstacleType, *cells):
        for cell in cells:
            x1, y1 = cell[0] * self.blockSize[0], cell[1] * self.blockSize[1]
            if obstacleType >= 1:
                self.obstacles.append(ObstacleSprite((x1, y1), (cell[1], cell[0]), obstacleType, self.draw))
            self.grid[cell[1], cell[0]] = obstacleType

    def createObstacles(self):
        # Create obstacles based on the game map
        for row, col in zip(*self.grid.nonzero()):
            # Create an obstacle at the current cell
            self.setObstacle(1, (col, row))
        for obstacle in self.obstacles:
            obstacle.getNeighbors(self)
        for obstacle in self.obstacles:
            for offset in obstacle.offsets:
                obstacle.adjacencyMatrix[offset[0] + 1, offset[1] + 1] = 1
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for i, j in corners:
                if i == 0 and j == 0 and (obstacle.adjacencyMatrix[0, 1] + obstacle.adjacencyMatrix[1, 0]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 0 and j == 2 and (obstacle.adjacencyMatrix[0, 1] + obstacle.adjacencyMatrix[1, 2]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 2 and j == 0 and (obstacle.adjacencyMatrix[1, 0] + obstacle.adjacencyMatrix[2, 1]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0
                elif i == 2 and j == 2 and (obstacle.adjacencyMatrix[2, 1] + obstacle.adjacencyMatrix[1, 2]) < 2:
                    obstacle.adjacencyMatrix[i, j] = 0


class FinishLine(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.fill(Colours.white)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def drawFlag(self, screen):
        image = pygame.image.load(f'ObstacleImages/flag.xcf')
        screen.blit(image, (self.x, self.y))


gameMap = Map((101, 108), 21, 12)
menuMap = Map((101, 108), 21, 12, False)
gameMap.setObstacle(1, (3, 3), (6, 1), (5, 4), (5, 7), (5, 8), (5, 5), (5, 6), (4, 5), (6, 5), (8, 8))
gameMap.setObstacle(0, (1, 8), (19, 9))
gameMap.createObstacles()
menuMap.createObstacles()
finishLine = FinishLine(1818, 864, 101, 108)

ObstacleSprite.createLines(gameMap.obstacles)
