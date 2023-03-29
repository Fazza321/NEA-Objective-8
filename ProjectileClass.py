from math import sin, cos
import pygame
from PlayerClass import player
from ObstacleClass import collisionObj


class ProjectileSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.angle = None
        self.x = None
        self.y = None
        self.colour = None
        self.xi = None
        self.yi = None
        self.intersectionLine = None
        self.image = pygame.Surface([5, 5])
        self.rect = self.image.get_rect()
        self.time = 0

    # returns a specific attribute of the projectile
    def getAttr(self, attribute):
        return self.__getattribute__(attribute)

    def update(self):
        if not self.x and not self.y:
            return
        self.rect.center = (self.x, self.y)

    # sets the initial angle of motion
    def setAngle(self, newAngle):
        self.angle = newAngle

    # draws the portal to the screen and calls the update position method, passing in a speed
    def drawProjectile(self, speedCoefficient, screen):
        if self.x is None or self.y is None:
            return
        self.updatePos(speedCoefficient)
        pygame.draw.rect(screen, self.colour, self.rect, 2)
        pygame.draw.circle(screen, self.colour, [self.x, self.y], 5)

    def setAttributes(self, angle, x, y, col, intersectionLine):
        self.angle = angle
        self.x = x
        self.y = y
        self.colour = col
        self.intersectionLine = intersectionLine

    def reset(self):
        self.x, self.y = -1000, -1000
        self.intersectionLine = None

    # updates the position of the projectile on the y and x-axis
    def updatePos(self, speedCoefficient):
        if not self.angle:
            return
        self.y -= sin(self.angle) * speedCoefficient
        self.x += cos(self.angle) * speedCoefficient

    # detects for collisions
    def collision(self, side, portalType, *sprites):
        if not any(pygame.sprite.spritecollide(self, spriteGroup, False) for spriteGroup in sprites):
            return
        self.time = 0
        player.setCanShoot(side, True)
        if not self.intersectionLine:
            return
        portalType.setPos(self)
        portalType.setLine(self.intersectionLine)
        self.x, self.y = -1000, -1000

    def startProjectile(self, angle, side, line, colour):
        # if mouse button is pressed a projectile is created
        if player.getMousePress(side) and player.getCanShoot(side):
            intersectionLine = line.intersection(collisionObj, self)
            self.setAttributes(angle, player.x + player.xChange, player.y + player.yChange, colour, intersectionLine)
            player.setCanShoot(side, False)


projectileSprites = pygame.sprite.Group()
projectile = ProjectileSprite(1)
projectile2 = ProjectileSprite(2)
