import sys
import pygame
import time
# Set up the clock
clock = pygame.time.Clock()
# Import pygame modules
from pygame.locals import *
# Initialize pygame
pygame.init()
pygame.mixer.init()
# Set the window's name
pygame.display.set_caption("The Last Bot")
# Set a window icon
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
# Window's Size
screen = pygame.display.set_mode((1366,768))
# Load images
bg = pygame.image.load("Assets/Background1.jpg").convert()
ground = pygame.image.load("Assets/Ground.png")
walkRight = [pygame.image.load('Assets/run1.png'), pygame.image.load('Assets/run2.png'),
             pygame.image.load('Assets/run3.png'), pygame.image.load('Assets/run4.png'),
             pygame.image.load('Assets/run5.png'), pygame.image.load('Assets/run6.png'),
             pygame.image.load('Assets/run7.png'), pygame.image.load('Assets/run8.png')]
walkLeft = [pygame.image.load('Assets/rleft1.png'), pygame.image.load('Assets/rleft2.png'),
            pygame.image.load('Assets/rleft3.png'), pygame.image.load('Assets/rleft4.png'),
            pygame.image.load('Assets/rleft5.png'), pygame.image.load('Assets/rleft6.png'),
            pygame.image.load('Assets/rleft7.png'), pygame.image.load('Assets/rleft8.png')]
ShootRight = [pygame.image.load('Assets/runshoot1.png'), pygame.image.load('Assets/runshoot2.png'),
              pygame.image.load('Assets/runshoot3.png'), pygame.image.load('Assets/runshoot4.png'),
              pygame.image.load('Assets/runshoot5.png'), pygame.image.load('Assets/runshoot6.png'),
              pygame.image.load('Assets/runshoot7.png'), pygame.image.load('Assets/runshoot8.png')]
ShootLeft = [pygame.image.load('Assets/rsleft1.png'), pygame.image.load('Assets/rsleft2.png'),
             pygame.image.load('Assets/rsleft3.png'), pygame.image.load('Assets/rsleft4.png'),
             pygame.image.load('Assets/rsleft5.png'), pygame.image.load('Assets/rsleft6.png'),
             pygame.image.load('Assets/rsleft7.png'), pygame.image.load('Assets/rsleft8.png')]
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
Energy = [pygame.image.load('Assets/Energy1.png'), pygame.image.load('Assets/Energy2.png'),
          pygame.image.load('Assets/Energy3.png'), pygame.image.load('Assets/Energy4.png'),
          pygame.image.load('Assets/Energy5.png'), pygame.image.load('Assets/Energy6.png'),
          pygame.image.load('Assets/Energy7.png')]
BulletSound = pygame.mixer.Sound('Assets/BulletSound.wav')
BulletHitSound = pygame.mixer.Sound('Assets/LaserHit.wav')
BackgroundMusic = pygame.mixer.music.load('Assets/BackgroundMusic.mp3')
pygame.mixer.music.play(-1)

# Declaring Some Variables
Life = 0
score = 0
P1x = 25
P2x = 1200
P1y = 462
P2y = 462

# New variable for charged shot threshold
CHARGE_THRESHOLD = 30

# Defined class for player
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 11
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.shoot = False
        self.idleshoot = False
        self.health = 29
        self.energy = 1
        self.visible = True
        self.powerUp = False
        self.pause = False
        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
        # New attributes for charged shot
        self.charge = 0
        self.isCharging = False

    def draw(self, screen):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if self.visible:
            if not self.standing:
                if not self.shoot:
                    if self.left:
                        screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                    elif self.right:
                        screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                        self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
                else:
                    if self.left:
                        screen.blit(ShootLeft[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                    elif self.right:
                        screen.blit(ShootRight[self.walkCount // 3], (self.x, self.y))
                        self.walkCount += 1
                        self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
            else:
                if not self.idleshoot:
                    if self.left:
                        screen.blit(char, (self.x, self.y))
                        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                    else:
                        screen.blit(Char, (self.x, self.y))
                        self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
                else:
                    if self.left:
                        screen.blit(IdleShootLeft, (self.x, self.y))
                        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                    else:
                        screen.blit(IdleShoot, (self.x, self.y))
                        self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
        # Draw the charging bar if the player is charging a shot
        if self.isCharging:
            bar_width = 50
            charge_ratio = self.charge / 60  # assuming a max charge of 60
            fill_width = int(bar_width * charge_ratio)
            pygame.draw.rect(screen, (255,215,0), (self.x, self.y - 20, fill_width, 10))
            pygame.draw.rect(screen, (255,255,255), (self.x, self.y - 20, bar_width, 10), 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 505
        self.walkCount = 0
        if Player.visible:
            screen.blit(Pause, (0, 0))
            font1 = pygame.font.SysFont('Berlin Sans FB', 100)
            text = font1.render('You Got Hit!', 1, (255,255,255,0))
            screen.blit(text, (1366/2 - (text.get_width()/2), 768/2 - (text.get_height()/2)))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(2)
                i += 1
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        i = 301
                        pygame.quit()
                        sys.exit()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# Defined class for Player's bullets
class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 14 * facing

    def draw(self, screen):
        if self.facing < 0:
            screen.blit(BulletLeft, (self.x, self.y))
        else:
            screen.blit(BulletRight, (self.x, self.y))

# New class for the charged projectile (complex feature)
class chargedProjectile(object):
    def __init__(self, x, y, facing, charge):
        self.x = x
        self.y = y
        self.facing = facing
        self.charge = charge
        self.vel = 14 * facing
        self.damage = 1 + (charge // 10)  # Damage scales with charge level

    def draw(self, screen):
        radius = int(10 + (self.charge / 6))  # Visual size scales with charge
        pygame.draw.circle(screen, (255,215,0), (self.x, self.y), radius)

# Defined class for Enemy's bullets
class enemyprojectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, screen):
        if Enemy1.visible:
            screen.blit(WizardBullet, (self.x, self.y))

# Defined class for Enemy
class enemy1(object):
    enemyRight = [pygame.image.load('Assets/EW1.png'), pygame.image.load('Assets/EW2.png'),
                  pygame.image.load('Assets/EW3.png'), pygame.image.load('Assets/EW4.png'),
                  pygame.image.load('Assets/EW5.png'), pygame.image.load('Assets/EW6.png'),
                  pygame.image.load('Assets/EW7.png'), pygame.image.load('Assets/EW8.png'),
                  pygame.image.load('Assets/EW9.png'), pygame.image.load('Assets/EW10.png'),
                  pygame.image.load('Assets/EA1.png'), pygame.image.load('Assets/EA2.png'),
                  pygame.image.load('Assets/EA3.png'), pygame.image.load('Assets/EA4.png'),
                  pygame.image.load('Assets/EA5.png'), pygame.image.load('Assets/EA6.png'),
                  pygame.image.load('Assets/EA7.png'), pygame.image.load('Assets/EA8.png')]
    enemyLeft = [pygame.image.load('Assets/EL1.png'), pygame.image.load('Assets/EL2.png'),
                 pygame.image.load('Assets/EL3.png'), pygame.image.load('Assets/EL4.png'),
                 pygame.image.load('Assets/EL5.png'), pygame.image.load('Assets/EL6.png'),
                 pygame.image.load('Assets/EL7.png'), pygame.image.load('Assets/EL8.png'),
                 pygame.image.load('Assets/EL9.png'), pygame.image.load('Assets/EL10.png'),
                 pygame.image.load('Assets/EAL1.png'), pygame.image.load('Assets/EAL2.png'),
                 pygame.image.load('Assets/EAL3.png'), pygame.image.load('Assets/EAL4.png'),
                 pygame.image.load('Assets/EAL5.png'), pygame.image.load('Assets/EAL6.png'),
                 pygame.image.load('Assets/EAL7.png'), pygame.image.load('Assets/EAL8.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.Armourhitbox = (self.x + 35, self.y + 32, 144, 140)
        self.health = 29
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 54:
                self.walkcount = 0
            if self.vel > 0:
                screen.blit(self.enemyRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 36, self.y + 3, 74, 93)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0], self.Armourhitbox[1] - 20, 70, 10))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0], self.Armourhitbox[1] - 20, 70 - ((70/29) * (29 - self.health)), 10))
            else:
                screen.blit(self.enemyLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 30, self.y + 3, 74, 93)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0] + 10, self.Armourhitbox[1] - 20, 70, 10))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0] + 10, self.Armourhitbox[1] - 20, 70 - ((70/29) * (29 - self.health)), 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkcount = 0

    def hit(self):
        Player.energy += 1
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# Fade between scenes
def fade():
    fade = pygame.Surface((1366,680))
    fade.fill((0,0,0))
    for alpha in range(0,40):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)

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
            font = pygame.font.SysFont('Berlin Sans FB', 70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# Background and drawing routine
def redrawGameWindow():
    screen.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (255,255,255,0))
    screen.blit(text, (1170, 10))
    screen.blit(Health, (0, 0))
    pygame.draw.rect(screen, (230, 0, 0), (65, 27, 203 - ((203 / 29) * (29 - Player.health)), 19))
    if 3 > Player.energy >= 1:
        screen.blit(Energy[0], (0,60))
    elif 6 > Player.energy >= 3:
        screen.blit(Energy[1], (0,60))
    elif 9 > Player.energy >= 6:
        screen.blit(Energy[2], (0,60))
    elif 12 > Player.energy >= 9:
        screen.blit(Energy[3], (0,60))
    elif 15 > Player.energy >= 12:
        screen.blit(Energy[4], (0,60))
    elif 18 > Player.energy >= 15:
        screen.blit(Energy[4], (0,60))
    elif Player.energy >= 18:
        screen.blit(Energy[6], (0,60))
        Player.powerUp = True
        screen.blit(portal1, (P1x, P1y))
        screen.blit(portal2, (P2x, P2y))
    Player.draw(screen)
    Enemy1.draw(screen)
    if Player.pause:
        screen.blit(Pause, (0, 0))
        Button.draw(screen, (0, 0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('Pause', 1, (255, 255, 255, 0))
        text1 = font2.render('Score -' + str(score), 1, (255, 255, 255, 0))
        pygame.draw.line(screen, (255, 255, 255), (650 - (text.get_width()) / 2, 320), (980, 320), 5)
        screen.blit(text, (683 - (text.get_width()) / 2, 200))
        screen.blit(text1, (683 - (text1.get_width()) / 2, 400))
        if pygame.key.get_pressed()[K_SPACE]:
            Player.pause = False
    Life = Player.health
    file2 = open('Assets/Health.txt', 'w')
    file2.write(str(Life))
    file2.close()
    screen.blit(ground, (0, 622))
    for bullet in bullets:
        bullet.draw(screen)
    for c_bullet in chargedBullets:
        c_bullet.draw(screen)
    for enemybullet in EnemyBullets:
        enemybullet.draw(screen)
    if not Player.visible:
        screen.blit(Pause, (0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('GameOver', 1, (255, 255, 255, 0))
        text1 = font2.render('Score -' + str(score), 1, (255, 255, 255, 0))
        pygame.draw.line(screen, (255, 255, 255), (650 - (text.get_width()) / 2, 320), (1110, 320), 5)
        screen.blit(text, (683 - (text.get_width()) / 2, 200))
        screen.blit(text1, (683 - (text1.get_width()) / 2, 400))
        List2.append(Endtime)
        Length = len(List2)
        Timer2 = List2[Length - 1] - List2[0]
        if Timer2 >= 3:
            fade()
            import Menu
    if not Enemy1.visible:
        screen.blit(Pause, (0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('Victory!', 1, (255, 255, 255, 0))
        text1 = font2.render('Level Complete', 1, (255, 255, 255, 0))
        screen.blit(text, (683 - (text.get_width())/2, 200))
        screen.blit(text1, (683 - (text1.get_width())/2, 400))
        List2.append(Endtime)
        Length = len(List2)
        Timer2 = List2[Length - 1] - List2[0]
        file1 = open('Assets/Score.txt', 'w')
        file1.write(str(score))
        file1.close()
        if Timer2 >= 3:
            fade()
            import Stage2
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(2)
            i += 1
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    i = 301
                    pygame.quit()
                    sys.exit()
    pygame.display.update()

# Font declaration
font = pygame.font.SysFont('Berlin Sans FB', 50)
# Player's position and dimensions
Player = player(50, 505, 177, 117)
# Enemy's position, dimensions, and path end point
Enemy1 = enemy1(500, 527, 181, 117, 1000)

Button = button((0,255,0), 610, 500, 150, 100, 'Retry')
shootLoop = 0
bullets = []
chargedBullets = []  # List for charged projectiles
EnemyBullets = []
List = []
List2 = []
startTime = time.time()

# Main loop
while True:
    clock.tick(40)
    Endtime = int(time.time() - startTime)

    # Player's PowerUp logic (unchanged)
    if Player.powerUp:
        List.append(Endtime)
        Length = len(List)
        Timer = List[Length - 1] - List[0]
        if Timer >= 15:
            Player.vel = 11
            Player.energy = 1
            Player.powerUp = False
            List = []
        else:
            if Player.x < 35:
                if Player.Armourhitbox[1] + Player.Armourhitbox[3] > P1y:
                    Player.x = 1130
            elif Player.x > 1140:
                if Player.Armourhitbox[1] + Player.Armourhitbox[3] > P2y:
                    Player.x = 40
            Player.vel = 30

    # Collision detection between player and enemy
    if Enemy1.visible:
        if (Player.Armourhitbox[1] < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and 
            Player.Armourhitbox[1] + Player.Armourhitbox[3] > Enemy1.Armourhitbox[1]):
            if (Player.Armourhitbox[0] + Player.Armourhitbox[2] > Enemy1.Armourhitbox[0] and 
                Player.Armourhitbox[0] < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]):
                Player.hit()
                if score >= 3:
                    score -= 3
                else:
                    score = 0

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 20:
        shootLoop = 0

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if Button.isOver(pos):
                import Stage1
        if event.type == MOUSEMOTION:
            Button.textColor = (255, 34, 34) if Button.isOver(pos) else (248, 248, 255)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Handle charging for the new charged shot
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                Player.isCharging = True
                Player.charge = 0
        if event.type == KEYUP:
            if event.key == K_SPACE and Player.isCharging:
                if Player.charge >= CHARGE_THRESHOLD:
                    BulletSound.play()
                    facing = -1 if Player.left else 1
                    if facing == 1 and not Player.standing:
                        x = round(Player.x + 115)
                        y = round(Player.y + 63)
                    elif facing == -1 and not Player.standing:
                        x = round(Player.x + 10)
                        y = round(Player.y + 63)
                    elif facing == 1 and Player.standing:
                        x = round(Player.x + 98)
                        y = round(Player.y + 50)
                    elif facing == -1 and Player.standing:
                        x = round(Player.x + 19)
                        y = round(Player.y + 50)
                    chargedBullets.append(chargedProjectile(x, y, facing, Player.charge))
                else:
                    BulletSound.play()
                    facing = -1 if Player.left else 1
                    if facing == 1 and not Player.standing:
                        x = round(Player.x + 115)
                        y = round(Player.y + 63)
                    elif facing == -1 and not Player.standing:
                        x = round(Player.x + 10)
                        y = round(Player.y + 63)
                    elif facing == 1 and Player.standing:
                        x = round(Player.x + 98)
                        y = round(Player.y + 50)
                    elif facing == -1 and Player.standing:
                        x = round(Player.x + 19)
                        y = round(Player.y + 50)
                    bullets.append(projectile(x, y, facing))
                Player.isCharging = False
                Player.charge = 0
                shootLoop = 1

    # Increment the charge if the player is holding the shot button
    if Player.isCharging:
        Player.charge += 1
        if Player.charge > 60:
            Player.charge = 60
        Player.shoot = True
    else:
        Player.shoot = False

    # Update and move normal projectiles
    for bullet in bullets:
        if (bullet.y - 12 < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and 
            bullet.y + 12 > Enemy1.Armourhitbox[1]):
            if (bullet.x + 14 > Enemy1.Armourhitbox[0] and 
                bullet.x - 14 < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]):
                if Enemy1.visible:
                    BulletHitSound.play()
                    Enemy1.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if 0 < bullet.x < 1360:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Update and move charged projectiles
    for c_bullet in chargedBullets:
        if (c_bullet.y - 12 < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and 
            c_bullet.y + 12 > Enemy1.Armourhitbox[1]):
            if (c_bullet.x + 14 > Enemy1.Armourhitbox[0] and 
                c_bullet.x - 14 < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]):
                if Enemy1.visible:
                    BulletHitSound.play()
                    for i in range(c_bullet.damage):
                        Enemy1.hit()
                    score += 1
                    chargedBullets.pop(chargedBullets.index(c_bullet))
        if 0 < c_bullet.x < 1360:
            c_bullet.x += c_bullet.vel
        else:
            chargedBullets.pop(chargedBullets.index(c_bullet))

    # Update enemy projectiles
    if Enemy1.visible and Player.visible:
        for enemybullet in EnemyBullets:
            if (enemybullet.y < Player.Armourhitbox[1] + Player.Armourhitbox[3] and 
                enemybullet.y > Player.Armourhitbox[1]):
                if (enemybullet.x > Player.Armourhitbox[0] and 
                    enemybullet.x < Player.Armourhitbox[0] + Player.Armourhitbox[2]):
                    BulletHitSound.play()
                    Player.hit()
                    score = score - 5 if score >= 5 else 0
                    EnemyBullets.pop(EnemyBullets.index(enemybullet))
            if 0 < enemybullet.x < 1360:
                enemybullet.x += enemybullet.vel
            else:
                EnemyBullets.pop(EnemyBullets.index(enemybullet))
    if Enemy1.vel != 0 and shootLoop == 0:
        facing = -1 if Enemy1.vel < 0 else 1
        if len(EnemyBullets) < 1:
            if facing == 1:
                EnemyBullets.append(enemyprojectile(round(Enemy1.x + 98), round(Enemy1.y + 63), facing))
            else:
                EnemyBullets.append(enemyprojectile(round(Enemy1.x + 25), round(Enemy1.y + 63), facing))

    # Left/Right movement for the player
    keys = pygame.key.get_pressed()
    if (keys[K_LEFT] or keys[K_a]) and Player.x > Player.vel:
        Player.x -= Player.vel
        Player.left = True
        Player.right = False
        Player.standing = False
    elif (keys[K_RIGHT] or keys[K_d]) and Player.x < 1360 - Player.width - Player.vel:
        Player.x += Player.vel
        Player.right = True
        Player.left = False
        Player.standing = False
    else:
        Player.standing = True
        Player.walkCount = 0

    if not Player.isJump:
        if keys[K_UP] or keys[K_w]:
            Player.isJump = True
            Player.left = False
            Player.right = False
            Player.walkCount = 0  # Fixed attribute name
    else:
        if Player.jumpCount >= -10:
            neg = 1 if Player.jumpCount >= 0 else -1
            Player.y -= (Player.jumpCount ** 2) * 0.7 * neg
            Player.jumpCount -= 1
        else:
            Player.isJump = False
            Player.jumpCount = 10

    redrawGameWindow()
