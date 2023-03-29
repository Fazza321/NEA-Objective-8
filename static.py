import pygame
fps = 60

characterWidth = 10
characterHeight = 30
speed = 20
left = 1
right = 3
depth = 52
mL = 2500

fallSprite = pygame.image.load("SpriteImages/SpritesIdle/Punk_run6.png")
fsWidth, fsHeight = fallSprite.get_width() * 2.5, fallSprite.get_height() * 2.5
fallSprite = pygame.transform.scale(fallSprite, (fsWidth, fsHeight))


class Colours:
    black = (0, 0, 0)
    orange = (255, 180, 0)
    blue = (0, 0, 255)
    lightGrey = (130, 130, 130)
    darkGrey = (100, 100, 100)
    red = (255, 0, 0)
    white = (255, 255, 255)
