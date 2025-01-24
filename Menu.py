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

# Defined class for button
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
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def highlight(self, pos):
        self.textColor = (255, 34, 34) if self.isOver(pos) else (248, 248, 255)

# Fade function for smooth transitions
def fade(screen, fade_color=(0, 0, 0), fade_speed=5):
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(fade_color)
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.Clock().tick(60)

# Create button instances
start_button = Button((0, 255, 0), 50, 660, 150, 100, 'Start')
credits_button = Button((0, 255, 0), 1100, 660, 200, 100, 'Credits')
instructions_button = Button((0, 255, 0), 650, 660, 250, 100, 'Instructions')
back_button = Button((200, 0, 0), 50, 660, 200, 100, 'Back')

# Redraw buttons
def redrawWindow():
    start_button.draw(screen)
    credits_button.draw(screen)
    instructions_button.draw(screen)
    font = pygame.font.SysFont('Berlin Sans FB', 70)
    text = font.render('LAST BOT', 1, (140, 34, 255))
    screen.blit(text, (1366 / 2 - (text.get_width() / 2), 60))

# States
current_state = "menu"

# Main loop
while True:
    clock.tick(60)
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if current_state == "menu":
                if start_button.isOver(pos):
                    fade(screen)
                    current_state = "stage1"
                elif credits_button.isOver(pos):
                    fade(screen)
                    current_state = "credits"
                elif instructions_button.isOver(pos):
                    fade(screen)
                    current_state = "instructions"
            elif current_state in ["credits", "instructions"]:
                if back_button.isOver(pos):
                    fade(screen)
                    current_state = "menu"

        if event.type == MOUSEMOTION:
            if current_state == "menu":
                start_button.highlight(pos)
                credits_button.highlight(pos)
                instructions_button.highlight(pos)
            elif current_state in ["credits", "instructions"]:
                back_button.highlight(pos)

    # Render based on the current state
    if current_state == "menu":
        screen.blit(BG1, (0, 0))
        redrawWindow()

    elif current_state == "stage1":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        text = font.render("Stage 1 - Gameplay Placeholder", True, (255, 255, 255))
        screen.blit(text, (400, 300))
        pygame.display.update()
        pygame.time.wait(3000)  # Placeholder logic
        current_state = "menu"  # Return to menu after stage1 ends

    elif current_state == "credits":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        text = font.render("Credits - Placeholder", True, (255, 255, 255))
        screen.blit(text, (500, 300))
        back_button.draw(screen)

    elif current_state == "instructions":
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.SysFont('Berlin Sans FB', 50)

        # Display the instructions
        title_text = font.render("Instructions for the game:", True, (255, 255, 255))
        controls_text = font.render("Use 'A' or Left Arrow to move left", True, (255, 255, 255))
        right_text = font.render("Use 'D' or Right Arrow to move right", True, (255, 255, 255))
        jump_text = font.render("Press 'W' or Up Arrow to jump", True, (255, 255, 255))
        shoot_text = font.render("Press Spacebar to shoot", True, (255, 255, 255))

        # Blit the instructions text onto the screen
        screen.blit(title_text, (400, 100))
        screen.blit(controls_text, (400, 200))
        screen.blit(right_text, (400, 260))
        screen.blit(jump_text, (400, 320))
        screen.blit(shoot_text, (400, 380))

        # Draw the back button
        back_button.draw(screen)


    pygame.display.update()