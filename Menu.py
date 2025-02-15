import sys
import pygame
import time
from pygame.locals import *

# Initialize pygame and its mixer
pygame.init()
pygame.mixer.init()

# Window settings
WIDTH, HEIGHT = 1366, 740
pygame.display.set_caption("The Last Bot Enhanced Menu")
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background images
BG1 = pygame.image.load('Assets/BG1.jpg').convert()
BG2 = pygame.image.load('Assets/BG2.png').convert()  # Not used, but available
BG3 = pygame.image.load('Assets/BG3.png').convert()  # Not used, but available

# Load background music and play it in a loop
pygame.mixer.music.load('Assets/MenuMusic.mp3')
pygame.mixer.music.play(-1)

# Load sound effect for button click (wrapped in try/except)
try:
    click_sound = pygame.mixer.Sound('Assets/click.wav')
except FileNotFoundError:
    print("click.wav not found, skipping click sound.")
    click_sound = None

# Define some colors
WHITE = (248, 248, 255)
HOVER_COLOR = (255, 34, 34)
BUTTON_COLOR = (0, 255, 0)
BUTTON_BG_COLOR = (50, 50, 50)
BACK_BUTTON_COLOR = (200, 0, 0)

# Enhanced Button class with hover effects and a rounded rectangle background
class Button:
    def __init__(self, x, y, width, height, text='', base_color=BUTTON_COLOR, hover_color=HOVER_COLOR, font_size=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.font = pygame.font.SysFont('Berlin Sans FB', font_size)
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        # Draw button background with rounded corners
        pygame.draw.rect(screen, BUTTON_BG_COLOR, self.rect, border_radius=12)
        # Draw the button border
        pygame.draw.rect(screen, self.current_color, self.rect, 3, border_radius=12)
        # Render and blit the button text centered within the button
        if self.text:
            text_surface = self.font.render(self.text, True, self.current_color)
            screen.blit(
                text_surface,
                (self.x + (self.width - text_surface.get_width()) / 2,
                 self.y + (self.height - text_surface.get_height()) / 2)
            )
    
    def is_over(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, pos):
        if self.is_over(pos):
            self.current_color = self.hover_color
            self.hovered = True
        else:
            self.current_color = self.base_color
            self.hovered = False

# Create main menu buttons
start_button = Button(50, 660, 150, 60, 'Start', font_size=40)
credits_button = Button(250, 660, 150, 60, 'Credits', font_size=40)
instructions_button = Button(450, 660, 200, 60, 'Instructions', font_size=40)
settings_button = Button(700, 660, 150, 60, 'Settings', font_size=40)
exit_button = Button(900, 660, 150, 60, 'Exit', font_size=40)

# Create a back button for sub-menus
back_button = Button(50, 660, 150, 60, 'Back', base_color=BACK_BUTTON_COLOR, hover_color=(255,100,100), font_size=40)

# Volume setting (for the Settings screen)
volume = 0.5  # Initial volume (50%)
pygame.mixer.music.set_volume(volume)

# Function to draw a volume slider
def draw_volume_slider(screen, x, y, width, height, volume):
    # Draw slider background
    pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), border_radius=5)
    # Draw the filled portion representing the current volume level
    fill_width = int(volume * width)
    pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_width, height), border_radius=5)
    # Draw an outline
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=5)
    # Draw the volume percentage text
    font = pygame.font.SysFont('Berlin Sans FB', 30)
    vol_text = font.render(f'Volume: {int(volume * 100)}%', True, WHITE)
    screen.blit(vol_text, (x, y - 35))

# Fade transition function
def fade(screen, fade_color=(0, 0, 0), fade_speed=5):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(fade_color)
    for alpha in range(0, 256, fade_speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)

# Title animation variables
title_font = pygame.font.SysFont('Berlin Sans FB', 90)
title_text = title_font.render('LAST BOT', True, (140, 34, 255))
title_rect = title_text.get_rect(center=(WIDTH / 2, 100))
title_alpha = 0
title_fade_in = True

# Define game states: "menu", "stage1", "credits", "instructions", "settings"
current_state = "menu"

# Variables for an animated background (a slow horizontal scroll)
bg_x = 0

# Main loop
running = True
while running:
    clock.tick(60)
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        
        if event.type == MOUSEBUTTONDOWN:
            # In the main menu, check which button was pressed
            if current_state == "menu":
                if start_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    current_state = "stage1"
                elif credits_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    current_state = "credits"
                elif instructions_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    current_state = "instructions"
                elif settings_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    current_state = "settings"
                elif exit_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    running = False
            # In sub-menus, use the back button to return to the main menu
            elif current_state in ["credits", "instructions", "settings"]:
                if back_button.is_over(pos):
                    if click_sound:
                        click_sound.play()
                    fade(screen)
                    current_state = "menu"
            
            # In the Settings state, allow volume adjustment via the slider
            if current_state == "settings":
                slider_rect = pygame.Rect(600, 300, 300, 30)
                if slider_rect.collidepoint(pos):
                    # Calculate new volume based on the click position
                    new_volume = (pos[0] - slider_rect.x) / slider_rect.width
                    volume = max(0, min(new_volume, 1))
                    pygame.mixer.music.set_volume(volume)

        if event.type == MOUSEMOTION:
            if current_state == "menu":
                start_button.update(pos)
                credits_button.update(pos)
                instructions_button.update(pos)
                settings_button.update(pos)
                exit_button.update(pos)
            elif current_state in ["credits", "instructions", "settings"]:
                back_button.update(pos)
        
        if event.type == KEYDOWN:
            if current_state == "settings":
                # Allow volume adjustments using the left/right arrow keys
                if event.key == K_LEFT:
                    volume = max(0, volume - 0.05)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == K_RIGHT:
                    volume = min(1, volume + 0.05)
                    pygame.mixer.music.set_volume(volume)
    
    # Render different screens based on the current state
    if current_state == "menu":
        # Animate a scrolling background
        bg_x -= 0.5
        if bg_x <= -WIDTH:
            bg_x = 0
        screen.blit(BG1, (bg_x, 0))
        screen.blit(BG1, (bg_x + WIDTH, 0))

        # Animate title fade-in
        if title_fade_in and title_alpha < 255:
            title_alpha += 3
            # Recreate the title surface with the new alpha value
            title_text = title_font.render('LAST BOT', True, (140, 34, 255))
            title_text.set_alpha(title_alpha)
        screen.blit(title_text, title_rect)

        # Draw main menu buttons
        start_button.draw(screen)
        credits_button.draw(screen)
        instructions_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

    elif current_state == "stage1":
        # Stage 1: Gameplay placeholder
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        stage_text = font.render("Stage 1 - Gameplay Placeholder", True, (255, 255, 255))
        screen.blit(stage_text, (400, 300))
        pygame.display.update()
        pygame.time.wait(3000)
        current_state = "menu"

    elif current_state == "credits":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        credits_text = font.render("Credits - Placeholder", True, (255, 255, 255))
        screen.blit(credits_text, (500, 300))
        back_button.draw(screen)

    elif current_state == "instructions":
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        title_inst = font.render("Instructions:", True, (255, 255, 255))
        screen.blit(title_inst, (400, 100))
        instructions_lines = [
            "Use 'A' or Left Arrow to move left",
            "Use 'D' or Right Arrow to move right",
            "Press 'W' or Up Arrow to jump",
            "Press Spacebar to shoot"
        ]
        for i, line in enumerate(instructions_lines):
            line_text = font.render(line, True, (255, 255, 255))
            screen.blit(line_text, (400, 180 + i * 60))
        back_button.draw(screen)

    elif current_state == "settings":
        screen.fill((20, 20, 20))
        font = pygame.font.SysFont('Berlin Sans FB', 50)
        settings_title = font.render("Settings", True, (200, 200, 255))
        screen.blit(settings_title, (WIDTH / 2 - settings_title.get_width() / 2, 100))
        # Draw the volume slider
        draw_volume_slider(screen, 600, 300, 300, 30, volume)
        # Display instructions for adjusting volume
        font_small = pygame.font.SysFont('Berlin Sans FB', 30)
        vol_instr = font_small.render("Click slider or use LEFT/RIGHT arrows to adjust volume", True, WHITE)
        screen.blit(vol_instr, (WIDTH / 2 - vol_instr.get_width() / 2, 350))
        back_button.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
