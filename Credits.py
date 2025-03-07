import math, sys
import pygame
import time
from pygame.locals import *
# Initialize pygame
pygame.init()
pygame.mixer.init()
# Set up the clock
clock = pygame.time.Clock()
# Set the windows name
pygame.display.set_caption("The Last Bot")
# Set a icon
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
# Window's Size
screen = pygame.display.set_mode((1366,740))
# Load images
BG = pygame.image.load('Assets/credits.png').convert()
bg_width = screen.get_width()
bg_height = BG.get_height() * (bg_width / BG.get_width())
BG = pygame.transform.scale(BG, (int(bg_width), int(bg_height)))
# Stores the time at which Application starts
start_time = time.time()
# Background Music
BackgroundMusic = pygame.mixer.music.load('Assets/MenuMusic.mp3')
# Repeat Background Music
pygame.mixer.music.play(-1)
# Defined class for button1
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = (248,248,255)
    def draw(self, screen, outline=None):
        if self.text != '':
            font = pygame.font.SysFont('Berlin Sans FB',70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

# Defined class for button2
class button2():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = (248,248,255)
    def draw(self, screen, outline=None):
        if self.text != '':
            font = pygame.font.SysFont('Berlin Sans FB',70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos1):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos1[0] > self.x and pos1[0] < self.x + self.width:
            if pos1[1] > self.y and pos1[1] < self.y + self.height:
                return True

        return False

# Fade a surface
def fade():
    fade = pygame.Surface((1366,680))
    fade.fill((0,0,0))
    for alpha in range(0,40):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)

# Background and calling other stuff
def redrawWindow():
    screen.blit(BG,(0,0))
    Button.draw(screen, (0,0,0))
    Button2.draw(screen, (0, 0, 0))
    font = pygame.font.SysFont('Berlin Sans FB', 70)
    text = font.render('LAST BOT', 1, (140, 34, 255, 0))
    screen.blit(text, (1366/2 - (text.get_width()/2), 670))

Button = button((0,255,0), 50,660,150,100,'Start')
Button2 = button2((0,255,0), 1100,660,200,100,'Menu')

# Main loop
while True:
    # Maintains 60 FPS
    clock.tick(60)
    # Calling redrawWindow
    redrawWindow()
    # Updates the Window
    pygame.display.update()

    # Event loop
    for event in pygame.event.get():
        # Mouse Position
        pos = pygame.mouse.get_pos()
        pos1 = pygame.mouse.get_pos()
        # Checking for Buttons
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):#Check for buttons
            # stop pygame
            pygame.quit()
            # stop script
            sys.exit()

        # Importing Stage1
        if event.type == MOUSEBUTTONDOWN:
            if Button.isOver(pos):
                fade()
                import Stage1

        # Changing Button's Color
        if event.type == MOUSEMOTION:
            if Button.isOver(pos):
                Button.textColor = (255,34,34)
            else:
                Button.textColor = (248,248,255)
        if event.type == MOUSEBUTTONDOWN:
            if Button2.isOver(pos1):
                import Menu

        # Changing Button's Color
        if event.type == MOUSEMOTION:
            if Button2.isOver(pos1):
                Button2.textColor = (255,34,34)
            else:
                Button2.textColor = (248,248,255)


