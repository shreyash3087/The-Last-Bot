import sys
import pygame
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set the window's name
pygame.display.set_caption("The Last Bot")

# Set an icon
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))

# Set up the clock
clock = pygame.time.Clock()

# Window's Size
screen = pygame.display.set_mode((1366, 740))

# Load images
BG1 = pygame.image.load('Assets/BG1.jpg').convert()
BG2 = pygame.image.load('Assets/BG2.png').convert()
BG3 = pygame.image.load('Assets/BG3.png').convert()

# Stores the time at which the application starts
start_time = time.time()

# Background Music
pygame.mixer.music.load('Assets/MenuMusic.mp3')

# Repeat Background Music
pygame.mixer.music.play(-1)

# Defined class for button1
class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = (248, 248, 255)
    
    def draw(self, screen, outline=None):
        if self.text != '':
            font = pygame.font.SysFont('Berlin Sans FB', 70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# Defined class for button2
class Button2():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = (248, 248, 255)
    
    def draw(self, screen, outline=None):
        if self.text != '':
            font = pygame.font.SysFont('Berlin Sans FB', 70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# Improved fade function with parameters for color and speed
def fade(screen, fade_color=(0, 0, 0), fade_speed=5):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(fade_color)
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.Clock().tick(60)  # Maintain 60 FPS

# Background and calling other stuff
def redrawWindow():
    Button.draw(screen, (0, 0, 0))
    Button2.draw(screen, (0, 0, 0))
    font = pygame.font.SysFont('Berlin Sans FB', 70)
    text = font.render('LAST BOT', 1, (140, 34, 255, 0))
    screen.blit(text, (1366 / 2 - (text.get_width() / 2), 670))

Button = Button((0, 255, 0), 50, 660, 150, 100, 'Start')
Button2 = Button2((0, 255, 0), 1100, 660, 200, 100, 'Credits')

# Main loop
while True:
    # Maintains 60 FPS
    clock.tick(60)

    # Updates the Window
    pygame.display.update()

    # Event loop
    for event in pygame.event.get():
        # Mouse Position
        pos = pygame.mouse.get_pos()
        pos1 = pygame.mouse.get_pos()

        # Checking for Buttons
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # Stop pygame
            pygame.quit()
            # Stop script
            sys.exit()

        # Importing Stage1
        if event.type == MOUSEBUTTONDOWN:
            if Button.isOver(pos):
                fade(screen)
                import Stage1

        # Changing Button's Color
        if event.type == MOUSEMOTION:
            if Button.isOver(pos):
                Button.textColor = (255, 34, 34)
            else:
                Button.textColor = (248, 248, 255)

        # Importing Credits
        if event.type == MOUSEBUTTONDOWN:
            if Button2.isOver(pos1):
                fade(screen)
                import Credits

        # Changing Button's Color
        if event.type == MOUSEMOTION:
            if Button2.isOver(pos1):
                Button2.textColor = (255, 34, 34)
            else:
                Button2.textColor = (248, 248, 255)

    # Stores current time in end_time variable
    end_time = time.time()
    Result = end_time - start_time

    # Changing Background image after 5 sec interval
    if 0 <= Result < 5:
        screen.blit(BG1, (0, 0))
        redrawWindow()
    elif 5 < Result < 5.5:
        fade(screen)
        redrawWindow()
    elif 5.5 <= Result < 10.5:
        screen.blit(BG2, (0, 0))
        redrawWindow()
    elif 10.5 < Result < 11:
        fade(screen)
        redrawWindow()
    elif 11 <= Result < 15:
        screen.blit(BG3, (0, 0))
        redrawWindow()
    elif Result >= 15:
        fade(screen)
        start_time = end_time
