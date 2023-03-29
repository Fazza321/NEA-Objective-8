from math import sin, cos, atan2, ceil, floor
from static import Colours
import pygame
from VectorClass import posVec, vel
from PortalClass import portal, portal2, portalSprites


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.index = 0
        self.counter = 0
        self.width = 54
        self.height = 66
        self.state = "right"
        self.images = pygame.image.load('SpriteImages/SpritesRunRight/PunkRun.xcf')
        self.images = pygame.transform.scale(self.images, (self.images.get_width() * 2, self.images.get_height() * 2))
        self.image = pygame.Surface([self.width, self.height])
        self.image.set_colorkey(Colours.black)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.facingAngle = 0
        self.xChange = None
        self.yChange = None
        self.canJump = True
        self.movingRight = False
        self.movingLeft = False
        self.lastMoved = None
        self.canShootLeft = True
        self.canShootRight = True
        self.canTeleport = False
        self.leftMouse = False
        self.rightMouse = False
        self.name = ""
        self.col = Colours.black

    def getImage(self):
        surface = pygame.Surface((self.width, self.height))
        self.image = surface
        self.image.set_colorkey(Colours.black)
        surface.blit(self.images, (0, 0), ((self.index * self.width), 0, self.width, self.height))

    def update(self, screen):
        if not self.x and not self.y:
            return

        self.rect.center = (self.x, self.y)
        self.drawPlayer(screen)
        animationCooldown = 5

        self.counter += 1

        if self.counter > animationCooldown:
            self.counter, self.index = 0, self.index + 1
        if self.index == 5:
            self.index = 0
        if not self.movingRight and not self.movingLeft:
            self.index = 2
            return
        if self.movingLeft and self.state == "right":
            self.images, self.state = pygame.transform.flip(self.images, True, False), "left"
        if self.movingRight and self.state == "left":
            self.images, self.state = pygame.transform.flip(self.images, True, False), "right"
        self.getImage()

    def getCanShoot(self, side):
        if side == "left":
            return self.canShootLeft
        elif side == "right":
            return self.canShootRight

    def setCanShoot(self, side, state):
        if side == "left":
            self.canShootLeft = state
        elif side == "right":
            self.canShootRight = state

    def getMousePress(self, side):
        if side == "left":
            return self.leftMouse
        elif side == "right":
            return self.rightMouse

    def setCanTeleport(self, state):
        self.canTeleport = state

    def setPos(self, newX, newY):
        self.x, self.y = newX, newY

    def drawPlayer(self, screen):
        screen.blit(self.image, self.rect)

    def finishLine(self, finalSprite):
        if finalSprite.rect.colliderect(self.rect):
            return True

    def objectCollide(self, sprites):
        if not self.canTeleport:
            return
        for sprite in sprites:
            if vel.i > 0 and sprite.rect.colliderect(self.rect.x + ceil(vel.i), self.rect.y, self.width, self.height):
                vel.i = 0
            elif vel.i <= 0 and sprite.rect.colliderect(self.rect.x + floor(vel.i), self.rect.y, self.width, self.height):
                vel.i = 0

            if not sprite.rect.colliderect(self.rect.x, self.rect.y + vel.j, self.width, self.height):
                continue

            if vel.j < 0:
                vel.j = sprite.rect.bottom - self.rect.top
            else:
                vel.j = sprite.rect.top - self.rect.bottom
                self.canJump = True

    def portalCollide(self):
        collision = None
        for sprite in portalSprites:
            if sprite.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                collision = sprite
        if not collision:
            self.setCanTeleport(True)
        if not self.canTeleport:
            return
        if collision and portal.x and portal2.x:
            self.teleport(collision)
            self.setCanTeleport(False)

    def teleport(self, portalType):
        if portalType.name == 1:
            posVec.setVec(portal2.x, portal2.y)
            vel.vecAngleChange(portal, portal2)
        elif portalType.name == 2:
            posVec.setVec(portal.x, portal.y)
            vel.vecAngleChange(portal2, portal)

    def changeCol(self, newCol):
        self.col = newCol

    # draw players pointer
    def facingLine(self, length, screen):
        self.yChange = -sin(self.facingAngle) * length
        self.xChange = cos(self.facingAngle) * length
        pygame.draw.aaline(screen, Colours.black, [self.x, self.y],
                           [self.x + self.xChange, self.y + self.yChange], 3)

    # finds what angle the player is facing
    def findAngle(self, mx, my):
        opposite, adjacent = mx - self.x, my - self.y
        self.facingAngle = -atan2(adjacent, opposite)
        return self.facingAngle

    def reset(self):
        self.leftMouse, self.movingLeft, self.movingRight, self.rightMouse = False, False, False, False


playerSprites = pygame.sprite.Group()
player = PlayerSprite(posVec.i, posVec.j)
playerSprites.add(player)
