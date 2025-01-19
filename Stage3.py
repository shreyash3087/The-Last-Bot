import math, sys, random
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("The Last Bot")
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
screen = pygame.display.set_mode((1366, 768))
font = pygame.font.SysFont('Berlin Sans FB', 30)

bg = pygame.image.load("Assets/Background2.jpg").convert()
ground = pygame.image.load("Assets/Ground.png")
walkRight = [pygame.image.load(f'Assets/run{i}.png') for i in range(1, 9)]
walkLeft = [pygame.image.load(f'Assets/rleft{i}.png') for i in range(1, 9)]
ShootRight = [pygame.image.load(f'Assets/runshoot{i}.png') for i in range(1, 9)]
ShootLeft = [pygame.image.load(f'Assets/rsleft{i}.png') for i in range(1, 9)]
IdleShoot = pygame.image.load('Assets/Shoot1.png')
IdleShootLeft = pygame.image.load('Assets/sleft1.png')
portal1 = pygame.image.load('Assets/P1.png')
portal2 = pygame.image.load('Assets/P2.png')
Char = pygame.image.load('Assets/idle.png')
char = pygame.image.load('Assets/idle1.png')
BulletLeft = pygame.image.load('Assets/Bullet1.png')
BulletRight = pygame.image.load('Assets/Bullet.png')
WizardBullet = pygame.image.load('Assets/EnemyBullet.png')
Pause = pygame.image.load('Assets/Hit.png')
Health = pygame.image.load('Assets/Health1.png')
Energy = [pygame.image.load(f'Assets/Energy{i}.png') for i in range(1, 8)]
GRAVITY = 0.8
JUMP_STRENGTH = -16
TERMINAL_VELOCITY = 20

BulletSound = pygame.mixer.Sound('Assets/BulletSound.wav')
BulletHitSound = pygame.mixer.Sound('Assets/LaserHit.wav')
pygame.mixer.music.load('Assets/BackgroundMusic.mp3')
pygame.mixer.music.play(-1)

with open('Assets/Score.txt', 'r') as file:
    score1 = int(file.read())
with open('Assets/Health.txt', 'r') as file:
    Life = int(file.read())

class Player:
    def __init__(self, x, y, width, height):
        self.falling = True
        self.y_velocity = 0
        self.gravity = 0.8
        self.jump_strength = -16
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 9
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.shoot = False
        self.idleshoot = False
        self.fall = True
        self.health = Life
        self.energy = 1
        self.visible = True
        self.powerUp = False
        self.pause = False
        self.update_hitbox()
    def handle_jumping(self):
        keys = pygame.key.get_pressed()
        
        self.y_velocity += self.gravity
        self.y += self.y_velocity
        
        if self.y > 505:  # Ground level
            self.y = 505
            self.y_velocity = 0
            self.falling = False
            self.isJump = False
        else:
            self.falling = True

        if (keys[K_UP] or keys[K_w]) and not self.falling:
            self.y_velocity = self.jump_strength
            self.isJump = True

    def handle_platform_collision(self, platform):
        player_bottom = self.y + self.height
        player_top = self.y
        player_right = self.x + self.width
        player_left = self.x
        
        plat_left = platform.hitbox[0]
        plat_right = platform.hitbox[0] + platform.hitbox[2]
        plat_top = platform.hitbox[1]
        plat_bottom = platform.hitbox[1] + platform.hitbox[3]
        
        if (player_right > plat_left and 
            player_left < plat_right and 
            player_bottom > plat_top and 
            player_top < plat_bottom):
            
            if self.y_velocity > 0 and player_bottom - self.y_velocity <= plat_top:
                self.y = plat_top - self.height
                self.y_velocity = 0
                self.falling = False
                self.isJump = False
                
                

    def update_hitbox(self):
        if self.left:
            self.hitbox = (self.x + 47, self.y + 12, 54, 105)
        else:
            self.hitbox = (self.x + 33, self.y + 12, 54, 105)

    def draw(self, screen):
        if self.walkCount >= 24:
            self.walkCount = 0

        if not self.standing:
            if not self.shoot:
                images = walkLeft if self.left else walkRight
            else:
                images = ShootLeft if self.left else ShootRight
            screen.blit(images[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            if not self.idleshoot:
                screen.blit(char if self.left else Char, (self.x, self.y))
            else:
                screen.blit(IdleShootLeft if self.left else IdleShoot, (self.x, self.y))
        
        self.update_hitbox()

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 505
        self.walkCount = 0
        
        screen.blit(Pause, (0, 0))
        font = pygame.font.SysFont('Berlin Sans FB', 100)
        text = font.render('You Got Hit!', 1, (255, 255, 255))
        screen.blit(text, (1366/2 - (text.get_width()/2), 768/2 - (text.get_height()/2)))
        pygame.display.update()
        
        pygame.time.delay(1000)
        
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('Assets/Picture2.png')
        self.hitbox = (self.x + 43, self.y + 80, 550, 45)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x + 43, self.y + 80, 550, 45)
class LaserTurret:
    def __init__(self, x, y, firing_direction):
        self.x = x
        self.y = y
        self.firing_direction = firing_direction  # 'up', 'down', 'left', 'right'
        self.charge_time = 60  # frames
        self.current_charge = 0
        self.is_firing = False
        self.laser_length = 800
        self.warning_color = (255, 0, 0, 128)
        self.laser_color = (255, 0, 0)
        
    def update(self):
        self.current_charge += 1
        if self.current_charge >= self.charge_time:
            self.is_firing = True
            self.current_charge = 0
        else:
            self.is_firing = False
            
    def draw(self, screen):
        # Draw turret base
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, 30, 30))
        
        # Draw warning or laser
        if self.is_firing:
            if self.firing_direction == 'right':
                pygame.draw.line(screen, self.laser_color, 
                               (self.x + 30, self.y + 15), 
                               (self.x + self.laser_length, self.y + 15), 4)
        else:
            # Draw warning indicator
            warning_surface = pygame.Surface((self.laser_length, 4), pygame.SRCALPHA)
            warning_surface.fill(self.warning_color)
            if self.firing_direction == 'right':
                screen.blit(warning_surface, (self.x + 30, self.y + 15))

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type  
        self.active = True
        self.hitbox = (self.x, self.y, 30, 30)
        
    def draw(self, screen):
        if self.active:
            color = {
                'speed': (0, 255, 0),
                'shield': (0, 0, 255),
                'double_jump': (255, 255, 0)
            }.get(self.type, (255, 255, 255))
            pygame.draw.rect(screen, color, self.hitbox)

class BreakablePlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 3
        self.breaking_state = 0
        self.visible = True 
        
    def hit(self):
        self.health -= 1
        self.breaking_state += 1
        if self.health <= 0:
            self.visible = False
            
    def draw(self, screen):
        if self.visible:
            super().draw(screen)
            if self.breaking_state > 0:
                crack_color = (0, 0, 0)
                for i in range(self.breaking_state):
                    start_x = self.x + (i + 1) * 100
                    pygame.draw.line(screen, crack_color, 
                                   (start_x, self.y + 80),
                                   (start_x + 30, self.y + 100), 3)
                    
class Player(Player):  # Inheriting from existing Player class
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.has_shield = False
        self.shield_time = 0
        self.double_jump_available = False
        self.can_double_jump = False
        
    def handle_power_up(self, power_up):
        if power_up.type == 'speed':
            self.vel = 15
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  
        elif power_up.type == 'shield':
            self.has_shield = True
            self.shield_time = 300  
        elif power_up.type == 'double_jump':
            self.double_jump_available = True
            
    def update(self):
        if self.has_shield:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.has_shield = False
                
        if not self.isJump:
            self.can_double_jump = self.double_jump_available
            
    def draw(self, screen):
        super().draw(screen)
        if self.has_shield:
            pygame.draw.circle(screen, (0, 0, 255, 128), 
                             (int(self.x + self.width/2), int(self.y + self.height/2)),
                             60, 2)

class DisappearingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.visible = True
        self.timer = 0
        self.cycle_time = 120
        
    def update(self):
        self.timer += 1
        if self.timer >= self.cycle_time:
            self.visible = not self.visible
            self.timer = 0
            
    def draw(self, screen):
        if self.visible:
            super().draw(screen)

class Projectile:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 14 * facing

    def draw(self, screen):
        image = BulletLeft if self.facing < 0 else BulletRight
        screen.blit(image, (self.x, self.y))

    def move(self):
        self.x += self.vel

class EliteProjectile(Projectile):
    def __init__(self, x, y, facing):
        super().__init__(x, y, facing)
        self.vel = 12
        self.homing = True
        self.homing_strength = 0.3
        
    def update(self, target):
        if self.homing:
            dx = target.x - self.x
            dy = target.y - self.y
            angle = math.atan2(dy, dx)
            
            self.vel_x = math.cos(angle) * 8
            self.vel_y = math.sin(angle) * 8
            
            self.x += self.vel_x
            self.y += self.vel_y
        else:
            self.x += self.vel

class EliteEnemy:
    enemyRight = [pygame.image.load('Assets/EW1.png'), pygame.image.load('Assets/EW2.png'),
                 pygame.image.load('Assets/EW3.png'), pygame.image.load('Assets/EW4.png'), pygame.image.load('Assets/EW5.png'),
                 pygame.image.load('Assets/EW6.png'), pygame.image.load('Assets/EW7.png'), pygame.image.load('Assets/EW8.png'),
                 pygame.image.load('Assets/EW9.png'),pygame.image.load('Assets/EW10.png'), pygame.image.load('Assets/EA1.png'), pygame.image.load('Assets/EA2.png'),
                 pygame.image.load('Assets/EA3.png'), pygame.image.load('Assets/EA4.png'), pygame.image.load('Assets/EA5.png'),
                 pygame.image.load('Assets/EA6.png'), pygame.image.load('Assets/EA7.png'), pygame.image.load('Assets/EA8.png')]
    enemyLeft = [pygame.image.load('Assets/EL1.png'), pygame.image.load('Assets/EL2.png'),
                pygame.image.load('Assets/EL3.png'), pygame.image.load('Assets/EL4.png'), pygame.image.load('Assets/EL5.png'),
                pygame.image.load('Assets/EL6.png'), pygame.image.load('Assets/EL7.png'), pygame.image.load('Assets/EL8.png'),
                pygame.image.load('Assets/EL9.png'),pygame.image.load('Assets/EL10.png') ,pygame.image.load('Assets/EAL1.png'), pygame.image.load('Assets/EAL2.png'),
                 pygame.image.load('Assets/EAL3.png'), pygame.image.load('Assets/EAL4.png'), pygame.image.load('Assets/EAL5.png'),
                 pygame.image.load('Assets/EAL6.png'), pygame.image.load('Assets/EAL7.png'), pygame.image.load('Assets/EAL8.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 5
        self.health = 40
        self.visible = True
        self.walkcount = 0
        self.path = [x, end]
        self.teleport_cooldown = 120
        self.teleport_timer = 0
        self.update_hitbox()
        
    def update_hitbox(self):
        self.hitbox = (self.x + 36, self.y + 3, 74, 93)
        
    def update(self):
        self.move()
        self.teleport_timer += 1
        if self.teleport_timer >= self.teleport_cooldown:
            self.teleport()
            
    def teleport(self):
        self.x = random.randint(100, 1200)
        self.teleport_timer = 0
        
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        self.update_hitbox()

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (255, 0, 0), 
                           (self.hitbox[0], self.hitbox[1] - 20, 70, 10))
            pygame.draw.rect(screen, (0, 128, 0), 
                           (self.hitbox[0], self.hitbox[1] - 20, 
                            70 - ((70/40) * (40 - self.health)), 10))
            
            if self.vel > 0:
                screen.blit(EliteEnemy.enemyRight[self.walkcount // 3], (self.x, self.y))
            else:
                screen.blit(EliteEnemy.enemyLeft[self.walkcount // 3], (self.x, self.y))
            
            self.walkcount = (self.walkcount + 1) % 54

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def main():
    clock = pygame.time.Clock()
    player = Player(50, 505, 177, 117)
    
    enemies = [
        EliteEnemy(500, 527, 181, 117, 1000),
        EliteEnemy(200, 200, 181, 117, 800),
        EliteEnemy(800, 100, 181, 117, 1200)
    ]
    
    turrets = [
        LaserTurret(300, 200, 'right'),
        LaserTurret(550, 300, 'right')
    ]
    
    power_ups = [
        PowerUp(150, 250, 'speed'),
        PowerUp(200, 400, 'shield')
    ]
    
    platforms = [
        BreakablePlatform(600, 300),
        DisappearingPlatform(300, 450),
        
    ]
    
    bullets = []
    enemy_bullets = []
    shoot_cooldown = 0
    score = score1
    
    running = True
    while running:
        clock.tick(40)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == USEREVENT + 1:  # Speed power-up timer
                player.vel = 9  # Reset speed to normal
        
        # Handle shooting cooldown
        if shoot_cooldown > 0:
            shoot_cooldown -= 1
            

        
        # Update turrets
        for turret in turrets:
            turret.update()
            if turret.is_firing:
                # Check collision with player
                if turret.firing_direction == 'right':
                    if (player.y + player.height > turret.y + 10 and 
                        player.y < turret.y + 20 and 
                        player.x > turret.x and 
                        player.x < turret.x + turret.laser_length):
                        if not player.has_shield:
                            player.hit()
                            score = max(0, score - 5)
        
        # Check power-up collisions
        for power_up in power_ups[:]:  # Use slice copy to safely remove while iterating
            if power_up.active:
                if (player.x + player.width > power_up.x and 
                    player.x < power_up.x + 30 and 
                    player.y + player.height > power_up.y and 
                    player.y < power_up.y + 30):
                    player.handle_power_up(power_up)
                    power_up.active = False
        
        # Update enemies and their projectiles
        for enemy in enemies:
            if enemy.visible:
                enemy.update()
                if random.random() < 0.03:
                    facing = 1 if enemy.vel > 0 else -1
                    enemy_bullets.append(EliteProjectile(
                        enemy.x + (98 if facing > 0 else 25),
                        enemy.y + 63,
                        facing
                    ))
        
        # Update projectiles and check platform collisions
        for bullet in bullets[:]:
            bullet.move()
            if not (0 < bullet.x < 1360):
                bullets.remove(bullet)
                continue
                
            # Check bullet collision with breakable platforms
            for platform in platforms:
                if isinstance(platform, BreakablePlatform) and platform.visible:
                    if (bullet.y + 12 > platform.hitbox[1] and
                        bullet.y - 12 < platform.hitbox[1] + platform.hitbox[3] and
                        bullet.x + 14 > platform.hitbox[0] and
                        bullet.x - 14 < platform.hitbox[0] + platform.hitbox[2]):
                        platform.hit()
                        bullets.remove(bullet)
                        break
            
            # Check bullet collision with enemies
            for enemy in enemies:
                if enemy.visible:
                    if (bullet.y - 12 < enemy.hitbox[1] + enemy.hitbox[3] and
                        bullet.y + 12 > enemy.hitbox[1] and
                        bullet.x + 14 > enemy.hitbox[0] and
                        bullet.x - 14 < enemy.hitbox[0] + enemy.hitbox[2]):
                        BulletHitSound.play()
                        enemy.hit()
                        score += 1
                        bullets.remove(bullet)
                        break
        
        # Update enemy projectiles
        for bullet in enemy_bullets[:]:
            if isinstance(bullet, EliteProjectile):
                bullet.update(player)
            
            if player.visible:
                if (bullet.y < player.hitbox[1] + player.hitbox[3] and
                    bullet.y > player.hitbox[1] and
                    bullet.x > player.hitbox[0] and
                    bullet.x < player.hitbox[0] + player.hitbox[2]):
                    BulletHitSound.play()
                    player.hit()
                    score = max(0, score - 5)
                    enemy_bullets.remove(bullet)
                elif not (0 < bullet.x < 1360):
                    enemy_bullets.remove(bullet)
        
        # Handle player input
        keys = pygame.key.get_pressed()
        
        # Shooting
        if keys[K_SPACE] and shoot_cooldown == 0:
            BulletSound.play()
            facing = -1 if player.left else 1
            if len(bullets) < 5:
                bullets.append(Projectile(
                    player.x + (10 if facing == -1 else 115),
                    player.y + 63,
                    facing
                ))
            shoot_cooldown = 20
        
        # Movement
        player.shoot = bool(keys[K_SPACE] and (keys[K_LEFT] or keys[K_RIGHT] or keys[K_a] or keys[K_d]))
        player.idleshoot = bool(player.standing and keys[K_SPACE])
        
        if (keys[K_LEFT] or keys[K_a]) and player.x > player.vel:
            player.x -= player.vel
            player.left = True
            player.right = False
            player.standing = False
        elif (keys[K_RIGHT] or keys[K_d]) and player.x < 1360 - player.width - player.vel:
            player.x += player.vel
            player.right = True
            player.left = False
            player.standing = False
        else:
            player.standing = True
            player.walkCount = 0
        
        # Jumping
        if not player.isJump:
            if keys[K_UP] or keys[K_w]:
                player.isJump = True
                player.walkCount = 0
        else:
            if player.jumpCount >= -10:
                neg = 1 if player.jumpCount >= 0 else -1
                player.y -= (player.jumpCount ** 2) * 0.7 * neg
                player.jumpCount -= 1
            else:
                player.isJump = False
                player.jumpCount = 10
        
        # Platform collision detection
        for platform in platforms:
            if isinstance(platform, DisappearingPlatform) and not platform.visible:
                continue
                
            player.handle_platform_collision(platform)
            if (player.y + player.height > platform.hitbox[1] and 
                player.y < platform.hitbox[1] + platform.hitbox[3] and
                player.x + player.width > platform.hitbox[0] and 
                player.x < platform.hitbox[0] + platform.hitbox[2]):
                
                # Top collision
                if player.y + player.height > platform.hitbox[1] and player.y < platform.hitbox[1]:
                    player.y = platform.hitbox[1] - player.height
                    player.isJump = False
                    player.jumpCount = 10
                    
                   
        player.handle_jumping()
        # Power-up logic
        if player.powerUp:
            if player.x < P1x and player.y > P1y:
                player.x = P2x
                player.y = P2y
            player.vel = 15
        
        # Draw everything
        draw_game(screen, player, enemies, platforms, bullets, enemy_bullets, score, turrets, power_ups)
        
        # Save game state periodically
        if score != score1:
            with open('Assets/Score.txt', 'w') as file:
                file.write(str(score))
            with open('Assets/Health.txt', 'w') as file:
                file.write(str(player.health))
    
    pygame.quit()
    sys.exit()

def draw_game(screen, player, enemies, platforms, bullets, enemy_bullets, score, turrets, power_ups):
    """Draw all game elements to the screen"""
    # Draw background
    screen.blit(bg, (0, 0))
    
    # Draw score
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(text, (1170, 10))
    
    # Draw health bar
    screen.blit(Health, (0, 0))
    pygame.draw.rect(screen, (230, 0, 0), 
                    (65, 27, 203 - ((203 / 29) * (29 - player.health)), 19))
    
    # Draw energy meter
    if player.energy >= 1:
        energy_index = min(int(player.energy // 3), 6)
        screen.blit(Energy[energy_index], (0, 60))
    
    # Draw portals if power-up is active
    if player.powerUp:
        screen.blit(portal1, (P1x, P1y))
        screen.blit(portal2, (P2x, P2y))
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen)
        # Draw warning for disappearing platforms
        if isinstance(platform, DisappearingPlatform):
            if platform.timer > platform.cycle_time - 40:
                pygame.draw.rect(screen, (255, 0, 0), 
                               (platform.x, platform.y - 10, 550, 5))
    
    # Draw turrets
    for turret in turrets:
        turret.draw(screen)
    
    # Draw power-ups
    for power_up in power_ups:
        power_up.draw(screen)
    
    # Draw enemies
    for enemy in enemies:
        if enemy.visible:
            enemy.draw(screen)
            if enemy.teleport_timer > enemy.teleport_cooldown - 30:
                pygame.draw.circle(screen, (255, 0, 0),
                                 (int(enemy.x + 50), int(enemy.y + 50)), 30, 2)
    
    # Draw player
    player.draw(screen)
    
    # Draw ground
    screen.blit(ground, (0, 622))
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    for bullet in enemy_bullets:
        bullet.draw(screen)
    
    pygame.display.update()

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = (248, 248, 255)
        
    def draw(self, screen):
        if self.text != '':
            font = pygame.font.SysFont('Berlin Sans FB', 70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)
            ))
    
    def is_over(self, pos):
        return (self.x < pos[0] < self.x + self.width and 
                self.y < pos[1] < self.y + self.height)

def fade():
    """Create a fade transition effect"""
    fade_surface = pygame.Surface((1366, 680))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 40):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

if __name__ == "__main__":
    # Set up game constants
    P1x, P1y = 25, 100
    P2x, P2y = 1300, 650
    
    try:
        main()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        pygame.quit()
        sys.exit(1)
