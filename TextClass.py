import pygame  # Import Pygame module
from static import Colours  # Import Colours from static module
from PlayerClass import player  # Import player from PlayerClass module


class Text:
    def __init__(self, font, colour, name, x, y, button=False, function=None):
        # Initialize the Text object with font, colour, name, x, y, button, and function parameters
        self.name = name
        self.font = font
        self.text = font.render(self.name, True, colour)
        self.colour = Colours.black
        self.resetColour = self.colour
        self.textColour = colour
        self.width = max(250, self.text.get_width())
        self.height = self.text.get_height()
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.function = function
        self.button = button
        self.active = False
        self.used = False
        self.minWidth = 250

    # Renders the text and draws it to the screen
    def write(self, screen):
        if self.name and len(self.name) > 2:
            self.used = True
        else:
            self.used = False
        self.width = max(self.minWidth, self.text.get_width() + 10)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.button:
            pygame.draw.rect(screen, self.colour, self.rect, 2)
        self.text = self.font.render(self.name, True, self.textColour)
        screen.blit(self.text, (self.x, self.y))

    # Updates the text
    def setText(self, text):
        self.name = str(text)

    # Adds string to the end of the text
    def addText(self, text):
        if len(self.name) + 1 > 15:
            return
        self.name += text

    # Removes text from the end
    def deleteText(self):
        self.name = self.name[:-1]

    # Updates the position of the text
    def updatePos(self, x, y):
        self.x = x
        self.y = y

    def buttonPress(self, mx, my, colourChange, click, otherButtons, canUse=True):
        # Check if the button has been clicked
        if not self.rect.collidepoint(mx, my):
            self.colour = self.resetColour
            return
        # Deactivate other buttons and activate this button

        self.colour = colourChange
        if not player.leftMouse:
            return
        for button in otherButtons:
            button.active = False
        self.active = True
        # Play a click sound and wait a little before performing the button's function
        click.play()
        pygame.time.wait(160)
        if self.function and canUse:
            self.function()
        else:
            return True

    @classmethod
    def stopDraw(cls, buttons):
        # Stop drawing the buttons
        for button in buttons:
            button.draw = False
