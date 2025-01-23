import pygame
import sys

pygame.init()

# Set up the window
screen = pygame.display.set_mode((1366, 740))
pygame.display.set_caption("Instructions")

# Define text and instructions
font = pygame.font.SysFont('Berlin Sans FB', 50)
title_text = font.render("Instructions for the game:", True, (255, 255, 255))
controls_text = font.render("Use 'A' or Left Arrow to move left", True, (255, 255, 255))
right_text = font.render("Use 'D' or Right Arrow to move right", True, (255, 255, 255))
jump_text = font.render("Press 'W' or Up Arrow to jump", True, (255, 255, 255))
shoot_text = font.render("Press Spacebar to shoot", True, (255, 255, 255))

# Define the back button
button_font = pygame.font.SysFont('Berlin Sans FB', 40)
back_button = pygame.Rect(50, 650, 200, 60)  # x, y, width, height
back_text = button_font.render("Back", True, (0, 0, 0))

def instructions_screen():
    """Instructions screen loop."""
    while True:
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Render all text on the screen
        screen.blit(title_text, (500, 100))
        screen.blit(controls_text, (500, 200))
        screen.blit(right_text, (500, 250))
        screen.blit(jump_text, (500, 300))
        screen.blit(shoot_text, (500, 350))

        # Draw the back button
        pygame.draw.rect(screen, (200, 200, 200), back_button)  # Button background
        screen.blit(back_text, (back_button.x + 50, back_button.y + 10))  # Button text

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos): 
                    return  

        pygame.display.update()