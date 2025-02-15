import math, sys
import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set window properties
pygame.display.set_caption("The Last Bot - Enhanced")
screen = pygame.display.set_mode((1366, 768), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Load assets efficiently
def load_image(path, alpha=True):
    return pygame.image.load(path).convert_alpha() if alpha else pygame.image.load(path).convert()

def load_sound(path):
    return pygame.mixer.Sound(path)

# Background & UI Elements
loading_screen = load_image("Assets/loading.png")
bg = load_image("Assets/Background3.jpg")
ground = load_image("Assets/Ground.png")
portal1 = load_image("Assets/P1.png")
portal2 = load_image("Assets/P2.png")
health_bar = load_image("Assets/Health1.png")
energy_states = [load_image(f"Assets/Energy{i}.png") for i in range(1, 8)]

# Sounds
bullet_sound = load_sound('Assets/BulletSound.wav')
hit_sound = load_sound('Assets/LaserHit.wav')
pygame.mixer.music.load('Assets/BossMusic.mp3')
pygame.mixer.music.play(-1)

# UI Text Rendering
font = pygame.font.SysFont('Berlin Sans FB', 50)
def draw_text(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont('Berlin Sans FB', size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Particle System for effects
particles = []
def create_particles(x, y):
    for _ in range(5):
        particles.append([[x, y], [random.randint(-3, 3), random.randint(-3, 3)], random.randint(4, 6)])

def update_particles():
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        pygame.draw.circle(screen, (255, 100, 0), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))
    particles[:] = [p for p in particles if p[2] > 0]

# Player Class
class Player:
    def __init__(self):
        self.x, self.y = 50, 505
        self.vel, self.jump_power = 11, 10
        self.is_jump, self.left, self.right = False, False, False
        self.health, self.energy = 100, 1
        self.standing, self.shoot, self.visible = True, False, True
        self.dash_cooldown = 0

    def draw(self):
        color = (0, 255, 0) if self.health > 50 else (255, 0, 0)
        pygame.draw.rect(screen, color, (self.x + 30, self.y - 20, self.health, 5))
        screen.blit(health_bar, (0, 0))
        screen.blit(energy_states[min(self.energy // 3, 6)], (0, 60))

    def move(self, keys):
        if keys[pygame.K_LSHIFT] and self.dash_cooldown == 0:
            self.vel = 20
            self.dash_cooldown = 20
        else:
            self.vel = 11

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(self.x - self.vel, 0)
            self.left, self.right = True, False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(self.x + self.vel, 1366 - 50)
            self.left, self.right = False, True
        else:
            self.standing = True

        if not self.is_jump:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.is_jump = True
        else:
            self.y -= (self.jump_power ** 2) * 0.3
            self.jump_power -= 1
            if self.jump_power < -10:
                self.is_jump, self.jump_power = False, 10

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

player = Player()

# Pause Menu
paused = False
def pause_menu():
    global paused
    paused = True
    while paused:
        screen.blit(bg, (0, 0))
        draw_text("Paused", 80, 600, 300)
        draw_text("Press 'R' to Resume", 40, 550, 400)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                paused = False

# FPS Counter
fps_font = pygame.font.SysFont("Arial", 20)
def show_fps():
    fps = str(int(clock.get_fps()))
    fps_surface = fps_font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_surface, (10, 740))

# Game Loop
running = True
while running:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    player.draw()
    update_particles()
    show_fps()
    
    draw_text(f"Health: {player.health}", 30, 10, 10)
    draw_text(f"Energy: {player.energy}", 30, 10, 50)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        pause_menu()
    player.move(keys)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
pygame.quit()
