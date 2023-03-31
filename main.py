import AStarClass
import Dijkstra
from static import *
from ProjectileClass import *
from VectorClass import *
from CollisionClass import *
from PortalClass import *
from ObstacleClass import *
import pygame
from pygame import mixer
from TextClass import Text
from DatabaseClass import db

pygame.init()

# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
size = pygame.display.Info()
screen = pygame.display.set_mode((size.current_w, size.current_h))

screenW = size.current_w
screenH = size.current_h

menuFont = pygame.font.Font('static/MainFont.otf', int(screenW / 6.5))
nodeFont = pygame.font.Font('static/MainFont.otf', int(screenW / 32.5))
buttonFont = pygame.font.Font('static/MainFont.otf', 150)
enterFont = pygame.font.Font('static/MainFont.otf', 50)
firstPageFont = pygame.font.Font('static/MainFont.otf', 70)

menuText = Text(menuFont, Colours.orange, 'Wormhole', screenW/2, screenH/5)
menuText2 = Text(menuFont, Colours.orange, 'Game', screenW/2, screenH/4 + menuText.height/2)

BackgroundNoise = mixer.Sound('static/Still Alive.mp3')
click = mixer.Sound('static/buttonClick.wav')


# event loop
def eventLoop(buttons=None):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.leftMouse = event.button == pygame.BUTTON_LEFT
            player.rightMouse = event.button == pygame.BUTTON_RIGHT
        elif event.type == pygame.KEYDOWN and buttons:
            for button in buttons:
                if not button.active:
                    continue
                if event.key == pygame.K_ESCAPE:
                    quit()
                elif event.key == pygame.K_RETURN:
                    button.active = False
                elif event.key == pygame.K_BACKSPACE:
                    button.deleteText()
                elif event.unicode.isprintable():
                    button.addText(event.unicode)


def Play():
    # variables
    Text.stopDraw((startButton, loginPageButton, menuText, menuText2))
    PathA, nodesMap = AStarClass.createNodes()
    PathD = Dijkstra.createPath(nodesMap)
    frame = 0
    player.reset()
    while True:
        screen.fill(Colours.darkGrey)
        # set fps
        clock.tick(fps)
        frame += 1
        # check for mouse attributes
        eventLoop()
        mx, my = pygame.mouse.get_pos()

        finishLine.drawFlag(screen)
        if player.finishLine(finishLine):
            print(player.name)
            db.insertScores(9.6, player.name)

        # find facing angle
        angle = player.findAngle(mx, my)
        xChange = cos(angle)
        yChange = -sin(angle)

        player.facingLine(20, screen)
        ObstacleSprite.drawObstacle(gameMap.obstacles, screen)

        if frame % 10 == 0:
            PathA.findPath(player)
            # PathD.findPath(player)
        for node in nodesMap:
            node.drawNode(screen, nodeFont, PathA, nodesMap[-1])

        L1.setCoord(posVec.i + xChange, posVec.j + yChange, xChange * mL + posVec.i, yChange * mL + posVec.j)

        # check if player moves left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            vel.add(acceleration, 'i')

        if keys[pygame.K_a]:
            vel.subtract(acceleration, 'i')

        if vel.i > 0.01:
            player.movingRight = True
            player.lastMoved = 'right'

        if vel.i < -0.01:
            player.movingLeft = True
            player.lastMoved = 'left'

        # add gravity vector to velocity
        vel.add(gravity, 'j')

        # check if player stops moving
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            vel.scale(deceleration, 'i', player)

        # check for collisions
        collide = player.objectCollide(objectSprites)
        posVec.add(vel, 'i')
        posVec.add(vel, 'j')
        player.setPos(posVec.i, posVec.j)
        vel.limit('i')

        if player.canJump and keys[pygame.K_w] or keys[pygame.K_SPACE]:
            vel.j = -16
            player.canJump = False
        # if player presses w or space and can jump they jump
        if collide:
            player.canJump = True

        # draw projectile to the screen
        projectile.drawProjectile(speed, screen)
        projectile2.drawProjectile(speed, screen)
        portalSprites.update(screen)
        objectSprites.update(screen)
        projectile.update()
        projectile2.update()
        player.update(screen)
        projectile.startProjectile(angle, 'left', L1, Colours.blue)
        projectile2.startProjectile(angle, 'right', L1, Colours.orange)
        vel.limit('i')
        # if portal makes collision draw a portal
        projectile.collision('left', portal, objectSprites)
        # if portal makes collision draw a portal
        projectile2.collision('right', portal2, objectSprites)

        xButton.write(screen)
        xButton.buttonPress(mx, my, Colours.darkGrey, click, menuButtons)

        # if player can teleport then check for collisions and teleport
        player.portalCollide()
        player.reset()
        pygame.display.update()


def Title():
    # one time statements
    backgroundY = 0
    BackgroundNoise.play()
    BackgroundNoise.set_volume(0.00)
    while True:
        screen.fill(Colours.darkGrey)
        ObstacleSprite.drawObstacle(menuMap.obstacles, screen)
        eventLoop()
        mx, my = pygame.mouse.get_pos()
        clock.tick(fps)

        # draw static portals
        pygame.draw.ellipse(screen, Colours.blue, [screenW / 2 - depth, screenH - 69, 60, 35], 5)
        pygame.draw.ellipse(screen, Colours.orange, [screenW / 2 - depth, 34, 60, 35], 5)

        # draw falling character
        screen.blit(fallSprite, (screenW/2 - fsWidth/1.5, backgroundY))
        screen.blit(fallSprite, (screenW/2 - fsWidth/1.5, -screenH + backgroundY))

        if backgroundY >= screenH - fsWidth:
            screen.blit(fallSprite, (screenW/2 - fsWidth, -screenH + backgroundY))
            backgroundY = 0

        for button in menuButtons:
            button.write(screen)
            button.buttonPress(mx, my, Colours.darkGrey, click, menuButtons)

        backgroundY += 25
        player.reset()
        pygame.display.update()


def Choices():
    canContinue1 = False
    canContinue2 = False
    db.allScores()
    while True:
        screen.fill(Colours.darkGrey)
        ObstacleSprite.drawObstacle(menuMap.obstacles, screen)
        eventLoop(firsPageButtons1)
        mx, my = pygame.mouse.get_pos()
        clock.tick(fps)
        for button in firsPageButtons1:
            if button.buttonPress(mx, my, Colours.blue, click, firsPageButtons1):
                button.name = ''
        xButton.buttonPress(mx, my, Colours.red, click, menuButtons)

        for button in firsPageButtons:
            button.write(screen)

        if all(button.used for button in signUpButtons):
            canContinue1 = True
        if all(button.used for button in loginButtons):
            canContinue2 = True

        continueButton1.buttonPress(mx, my, Colours.blue, click, menuButtons, canContinue1)
        continueButton2.buttonPress(mx, my, Colours.blue, click, menuButtons, canContinue2)
        player.reset()
        pygame.display.update()


def Scores():
    db.sortScores()
    db.allScores()


def SignUp():
    db.newUser(signUpButton.name, signUpButton1.name, signUpButton2.name, Title)


def Login():
    db.login(loginButton.name, loginButton1.name, Title)


xButton = Text(enterFont, Colours.red, 'X', screenW + 91, 23, True, quit)
xButton.minWidth = 20
startButton = Text(buttonFont, Colours.orange, 'Start', screenW/4, 2*screenH/3, True, Play)
loginPageButton = Text(buttonFont, Colours.blue, 'Login', 3*screenW/4, 2*screenH/3, True, Login)

signUpText = Text(firstPageFont, Colours.orange, 'Sign Up', screenW / 4, screenH / 3)
loginText = Text(firstPageFont, Colours.orange, 'Login', screenW / 2, screenH / 3)
guestText = Text(firstPageFont, Colours.orange, 'Guest', 3 * screenW / 4, screenH / 3)

signUpButton = Text(enterFont, Colours.blue, 'Username', screenW / 4, screenH / 2, True)
signUpButton1 = Text(enterFont, Colours.blue, 'Real Name', screenW / 4, screenH / 2 + 50, True)
signUpButton2 = Text(enterFont, Colours.blue, 'Password', screenW / 4, screenH / 2 + 100, True)

signUpButtons = [signUpButton, signUpButton1, signUpButton2]

loginButton = Text(enterFont, Colours.blue, 'Username', screenW/2, screenH/2, True)
loginButton1 = Text(enterFont, Colours.blue, 'Password', screenW/2, screenH/2 + 50, True)

loginButtons = [loginButton, loginButton1]

continueButton1 = Text(enterFont, Colours.blue, 'Continue', screenW / 4, 2 * screenH / 3, True, SignUp)
continueButton2 = Text(enterFont, Colours.blue, 'Continue', screenW / 2, 2 * screenH / 3, True, Login)
continueButton3 = Text(enterFont, Colours.blue, 'Continue', 3 * screenW / 4, 2 * screenH / 3, True, Title)

firsPageButtons = [xButton, signUpText, loginText, guestText, signUpButton, signUpButton1, signUpButton2, loginButton, loginButton1, continueButton1, continueButton2, continueButton3]
firsPageButtons1 = [signUpButton, signUpButton1, signUpButton2, loginButton, loginButton1, continueButton3]
continueButtons = [continueButton1, continueButton2, continueButton3]
menuButtons = [xButton, startButton, loginPageButton, menuText, menuText2]


if __name__ == '__main__':
    Choices()
