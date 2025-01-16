import math, sys
import pygame
import time
# Set up the clock
clock = pygame.time.Clock()
# Import pygame modules
from pygame.locals import *
# Initialize pygame
pygame.init()
pygame.mixer.init()
# Set the windows name
pygame.display.set_caption("The Last Bot")
# Set a icon
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
# Window's Size
screen = pygame.display.set_mode((1366,768))
# Load images
bg = pygame.image.load("Assets/Background2.jpg").convert()
ground = pygame.image.load("Assets/Ground.png")
walkRight = [pygame.image.load('Assets/run1.png'),pygame.image.load('Assets/run2.png'),pygame.image.load('Assets/run3.png'),pygame.image.load('Assets/run4.png'),pygame.image.load('Assets/run5.png'),pygame.image.load('Assets/run6.png'),pygame.image.load('Assets/run7.png'),pygame.image.load('Assets/run8.png'),]
walkLeft = [pygame.image.load('Assets/rleft1.png'),pygame.image.load('Assets/rleft2.png'),pygame.image.load('Assets/rleft3.png'),pygame.image.load('Assets/rleft4.png'),pygame.image.load('Assets/rleft5.png'),pygame.image.load('Assets/rleft6.png'),pygame.image.load('Assets/rleft7.png'),pygame.image.load('Assets/rleft8.png')]
ShootRight = [pygame.image.load('Assets/runshoot1.png'),pygame.image.load('Assets/runshoot2.png'),pygame.image.load('Assets/runshoot3.png'),pygame.image.load('Assets/runshoot4.png'),pygame.image.load('Assets/runshoot5.png'),pygame.image.load('Assets/runshoot6.png'),pygame.image.load('Assets/runshoot7.png'),pygame.image.load('Assets/runshoot8.png'),]
ShootLeft = [pygame.image.load('Assets/rsleft1.png'),pygame.image.load('Assets/rsleft2.png'),pygame.image.load('Assets/rsleft3.png'),pygame.image.load('Assets/rsleft4.png'),pygame.image.load('Assets/rsleft5.png'),pygame.image.load('Assets/rsleft6.png'),pygame.image.load('Assets/rsleft7.png'),pygame.image.load('Assets/rsleft8.png')]
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
Energy = [pygame.image.load('Assets/Energy1.png'),pygame.image.load('Assets/Energy2.png'),pygame.image.load('Assets/Energy3.png'),pygame.image.load('Assets/Energy4.png'),pygame.image.load('Assets/Energy5.png'),pygame.image.load('Assets/Energy6.png'),pygame.image.load('Assets/Energy7.png')]
BulletSound = pygame.mixer.Sound('Assets/BulletSound.wav')
BulletHitSound = pygame.mixer.Sound('Assets/LaserHit.wav')
BackgroundMusic = pygame.mixer.music.load('Assets/BackgroundMusic.mp3')
pygame.mixer.music.play(-1)

# Declaring Some Variables
file1 = open('Assets/Score.txt', 'r')
value = file1.read()
file2 = open('Assets/Health.txt', 'r')
H = file2.read()
Life = int(H)
score1 = int(value)
P1x = 25
P2x = 755
P1y = 462
P2y = 70

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
        self.fall = True
        self.PlatformTrigger  = True
        self.health = Life
        self.energy = 1
        self.visible = True
        self.powerUp = False
        self.pause = False
        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)

    def draw(self,screen):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if not (self.standing):
            if self.shoot == False:
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
            if self.idleshoot == False:
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

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 505
        self.walkCount = 0
        screen.blit(Pause,(0,0))
        font1 = pygame.font.SysFont('Berlin Sans FB', 100)
        text = font1.render('You Got Hit!',1, (255,255,255,0))
        screen.blit(text, (1366/2 - (text.get_width()/2),768/2 - (text.get_height()/2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(2)
            i += 1
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Check for buttons
                    i = 301
                    # stop pygame
                    pygame.quit()
                    # stop script
                    sys.exit()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# Defined class for Player's bullets
class projectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 14 * facing

    def draw(self,screen):
        if facing < 0:
            screen.blit(BulletLeft,(self.x,self.y))
        else:
            screen.blit(BulletRight, (self.x, self.y))

# Defined class for Enemy1's bullets
class enemyprojectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,screen):
        if Enemy1.visible == True:
            screen.blit(WizardBullet,(self.x,self.y))

# Defined class for Enemy2's bullets
class enemy2projectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,screen):
        if Enemy2.visible == True:
            screen.blit(WizardBullet,(self.x,self.y))
# Defined class for Enemy1
class enemy1(object):
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
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.Armourhitbox = (self.x + 35, self.y + 32, 144, 140)
        self.health = 29
        self.visible = True

    def draw(self,screen):
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
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        Player.energy += 1
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# Defined class for Enemy2
class enemy2(object):
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
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.Armourhitbox = (self.x + 35, self.y + 32, 144, 140)
        self.health = 29
        self.visible = True

    def draw(self,screen):
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
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        Player.energy += 1
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

# Defined class for Platform
class platforms(object):
    platform = pygame.image.load('Assets/Picture2.png')
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x + 35, self.y + 32, 144, 140)
    def draw(self, win):
        screen.blit(self.platform, (self.x, self.y))
        self.hitbox = (self.x + 43, self.y + 80, 550,45)
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
            font = pygame.font.SysFont('Berlin Sans FB',70)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
# Background and calling some other stuff
def redrawGameWindow():
    screen.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score1), 1, (255,255,255,0))
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
        screen.blit(portal1,(P1x,P1y))
        screen.blit(portal2,(P2x,P2y))
    Player.draw(screen)
    Enemy1.draw(screen)
    Enemy2.draw(screen)
    if Player.pause:
        screen.blit(Pause, (0, 0))
        Button.draw(screen, (0, 0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('Pause', 1, (255, 255, 255, 0))
        text1 = font2.render('Score -' + str(score1), 1, (255, 255, 255, 0))
        pygame.draw.line(screen, (255, 255, 255), (650 - (text.get_width()) / 2, 320), (980, 320), 5)
        screen.blit(text, (683 - (text.get_width()) / 2, 200))
        screen.blit(text1, (683 - (text1.get_width()) / 2, 400))
        if pygame.key.get_pressed()[K_SPACE] :
            Player.pause = False
    Life = Player.health
    file2 = open('Assets/Health.txt', 'w')
    file2.write(str(Life))
    file2.close()
    Platform.draw(screen)
    screen.blit(ground, (0, 622))
    for bullet in bullets:
        bullet.draw(screen)
    for enemybullet in EnemyBullets:
        enemybullet.draw(screen)
    for enemy2bullet in Enemy2Bullets:
        enemy2bullet.draw(screen)
    if Enemy1.visible == False and Enemy2.visible == False:
        screen.blit(Pause, (0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('Victory!', 1, (255, 255, 255, 0))
        text1 = font2.render('Level Complete', 1, (255, 255, 255, 0))
        screen.blit(text, (683 - (text.get_width()) / 2, 200))
        screen.blit(text1, (683 - (text1.get_width()) / 2, 400))
        List2.append(Endtime)
        Length = len(List2)
        Timer2 = List2[Length - 1] - List2[0]
        file1 = open('Assets/Score.txt', 'w')
        file1.write(str(score1))
        file1.close()
        if Timer2 >= 3:
            fade()
            import Final
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(2)
            i += 1
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # Check for buttons
                    i = 301
                    pygame.quit()
                    sys.exit()
    pygame.display.update()
# Font declaration
font = pygame.font.SysFont('Berlin Sans FB', 50)
# Player's position and width,height declaration
Player = player(50, 505, 177, 117)
# Enemy1's path,width and height declaration
Enemy1 = enemy1(500,527,181,117, 1000)
# Enemy2's path,width and height declaration
Enemy2 = enemy2(200,527,181,117, 1000)
# Platform's x and y values
Platform = platforms(300,150)

Button = button((0,255,0), 610,500,150,100,'Retry')
shootLoop = 0
bullets = []
EnemyBullets = []
Enemy2Bullets = []
List = []
List2 = []
# Stores the time at which application starts
startTime = time.time()

#main loop
while True:
    # Maintains 40 FPS
    clock.tick(40)

    # Stores the difference of current time - start time
    Endtime = int(time.time() - startTime)
    
    # Player's PowerUp
    if Player.powerUp:
        List.append(Endtime)
        Length = len(List)
        Timer = List[Length - 1]-List[0]
        if Timer >= 15:
            Player.vel = 11
            Player.energy = 1
            Player.powerUp = False
            List = []
        else:
            if Player.x < P1x:
                if Player.y > P1y:
                    Player.x = P2x
                    Player.y = Platform.y
            Player.vel = 30

    # Checks Player's collision with Platform
    if (Player.Armourhitbox[1] + Player.Armourhitbox[3] < Platform.hitbox[1] + Platform.hitbox[3] and Player.Armourhitbox[1] + Player.Armourhitbox[3] > Platform.hitbox[1]):
        if (Player.Armourhitbox[0] + Player.Armourhitbox[2] > Platform.hitbox[0] and Player.Armourhitbox[0] < Platform.hitbox[0] + Platform.hitbox[2]):
            Player.y = Platform.y - 35
            Player.PlatformTrigger = True
        else:
            Player.fall = True
    if (Player.fall == True) and (Player.PlatformTrigger == True):
        if Player.y >= 505:
            Player.y = 505
            Player.fall = False
            Player.PlatformTrigger = False
        else:
            Player.y += 20

    # Decreases score if enemy1's bullet collids with player
    if Enemy1.visible == True:
        if (Player.Armourhitbox[1] < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and Player.Armourhitbox[1] + Player.Armourhitbox[3] > Enemy1.Armourhitbox[1]):
            if (Player.Armourhitbox[0] + Player.Armourhitbox[2] > Enemy1.Armourhitbox[0] and Player.Armourhitbox[0] < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]):
                Player.hit()
                score1 -= 3
    # Decreases score if enemy2's bullet collids with player
    if Enemy2.visible == True:
        if (Player.Armourhitbox[1] < Enemy2.Armourhitbox[1] + Enemy2.Armourhitbox[3] and Player.Armourhitbox[1] + Player.Armourhitbox[3] > Enemy2.Armourhitbox[1]):
            if (Player.Armourhitbox[0] + Player.Armourhitbox[2] > Enemy2.Armourhitbox[0] and Player.Armourhitbox[0] < Enemy2.Armourhitbox[0] + Enemy2.Armourhitbox[2]):
                Player.hit()
                if score1 >= 3:
                    score1 -= 3
                else:
                    score1 = 0

    # Prevents more than one bullet to come out at the same time
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 20:
        shootLoop = 0

    # Event loop
    for event in pygame.event.get():
        # Mouse Position
        pos = pygame.mouse.get_pos()
        # Restarting Game
        if event.type == MOUSEBUTTONDOWN:
            if Button.isOver(pos):
                import Stage2

        # Changing Button's Color
        if event.type == MOUSEMOTION:
            if Button.isOver(pos):
                Button.textColor = (255, 34, 34)
            else:
                Button.textColor = (248, 248, 255)
        # Check for buttons
        if event.type == QUIT:
            # stop pygame
            pygame.quit()
            # stop script
            sys.exit()

    # Loop for player's bullet
    for bullet in bullets:
        if (bullet.y - 12 < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and bullet.y + 12 > Enemy1.Armourhitbox[1]) :
            if (bullet.x + 14 > Enemy1.Armourhitbox[0] and bullet.x - 14 < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]) :
                if Enemy1.visible == True:
                    BulletHitSound.play()
                    Enemy1.hit()
                    score1 += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 1360 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    for bullet in bullets:
        if (bullet.y - 12 < Enemy2.Armourhitbox[1] + Enemy2.Armourhitbox[3] and bullet.y + 12 > Enemy2.Armourhitbox[1]) :
            if (bullet.x + 14 > Enemy2.Armourhitbox[0] and bullet.x - 14 < Enemy2.Armourhitbox[0] + Enemy1.Armourhitbox[2]) :
                if Enemy2.visible == True:
                    BulletHitSound.play()
                    Enemy2.hit()
                    score1 += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 1360 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Loop for enemy1's bullet
    if Enemy1.visible and Player.visible:
        for enemybullet in EnemyBullets:
            if (enemybullet.y < Player.Armourhitbox[1] + Player.Armourhitbox[3] and enemybullet.y  > Player.Armourhitbox[1]) :
                if (enemybullet.x > Player.Armourhitbox[0] and enemybullet.x < Player.Armourhitbox[0] + Player.Armourhitbox[2]) :
                        BulletHitSound.play()
                        Player.hit()
                        if score1 >= 5:
                            score1 -= 5
                        else:
                            score1 = 0
                        EnemyBullets.pop(EnemyBullets.index(enemybullet))
            if enemybullet.x < 1360 and enemybullet.x > 0:
                enemybullet.x += enemybullet.vel
            else:
                EnemyBullets.pop(EnemyBullets.index(enemybullet))
    if Enemy1.vel > 0 and shootLoop == 0 or Enemy1.vel < 0 and shootLoop == 0:
        if Enemy1.vel < 0:
            facing = -1
        else:
            facing = 1
        if len(EnemyBullets) < 1 and facing == 1:
            EnemyBullets.append(enemyprojectile(round(Enemy1.x + 98), round(Enemy1.y + 63), facing))
        if len(EnemyBullets) < 1 and facing == -1:
            EnemyBullets.append(enemyprojectile(round(Enemy1.x + 25), round(Enemy1.y + 63), facing))
    # Loop for enemy2's bullet
    if Enemy2.visible and Player.visible:
        for enemy2bullet in Enemy2Bullets:
            if (enemy2bullet.y < Player.Armourhitbox[1] + Player.Armourhitbox[3] and enemy2bullet.y >Player.Armourhitbox[1]):
                if (enemy2bullet.x > Player.Armourhitbox[0] and enemy2bullet.x < Player.Armourhitbox[0] + Player.Armourhitbox[2]):
                    BulletHitSound.play()
                    Player.hit()
                    score1 -= 5
                    Enemy2Bullets.pop(Enemy2Bullets.index(enemy2bullet))
            if enemy2bullet.x < 1360 and enemy2bullet.x > 0:
                enemy2bullet.x += enemy2bullet.vel
            else:
                Enemy2Bullets.pop(Enemy2Bullets.index(enemy2bullet))
    if Enemy2.vel > 0 and shootLoop == 0 or Enemy2.vel < 0 and shootLoop == 0:
        if Enemy2.vel < 0:
            facing = -1
        else:
            facing = 1
        if len(Enemy2Bullets) < 1 and facing == 1:
            Enemy2Bullets.append(enemy2projectile(round(Enemy2.x + 98), round(Enemy2.y + 63), facing))
        if len(Enemy2Bullets) < 1 and facing == -1:
            Enemy2Bullets.append(enemyprojectile(round(Enemy2.x + 25), round(Enemy2.y + 63), facing))

    # Tracking key pressed
    keys = pygame.key.get_pressed()

    # Space key for bullet
    if keys[K_SPACE] and shootLoop == 0:
        BulletSound.play()
        if Player.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5 and facing == 1 and Player.standing == False:
            bullets.append(projectile(round(Player.x + 115), round(Player.y + 63), facing))
        if len(bullets) < 5 and facing == -1 and Player.standing == False:
            bullets.append(projectile(round(Player.x + 10), round(Player.y + 63), facing))
        if len(bullets) < 5 and facing == 1 and Player.standing == True:
            bullets.append(projectile(round(Player.x + 98), round(Player.y + 50), facing))
        if len(bullets) < 5 and facing == -1 and Player.standing == True:
            bullets.append(projectile(round(Player.x + 19), round(Player.y + 50), facing))

        shootLoop = 1
    if (keys[pygame.K_LEFT] and keys[pygame.K_SPACE]) or (keys[pygame.K_RIGHT] and keys[pygame.K_SPACE]) :
        Player.shoot = True
    else:
        Player.shoot = False
    if Player.standing == True and keys[pygame.K_SPACE]:
        Player.idleshoot = True
    else:
        Player.idleshoot = False

    # Left arrow key for moving left
    if keys[pygame.K_LEFT] and Player.x > Player.vel:
        Player.x -= Player.vel
        Player.left = True
        Player.right = False
        Player.standing = False

    # Right arrow key for moving right
    elif keys[pygame.K_RIGHT] and Player.x < 1360 - Player.width - Player.vel:
        Player.x += Player.vel
        Player.right = True
        Player.left = False
        Player.standing = False
    else:
        Player.standing = True
        Player.walkCount = 0

    if not(Player.isJump):

        # Up arrow key for jumping
        if keys[K_UP]:
            Player.isJump = True
            Player.left = False
            Player.right = False
            Player.walkcount = 0
    else:
        if Player.jumpCount >= -10:
            neg = 1
            if Player.jumpCount < 0:
                neg = -1
            Player.y -= (Player.jumpCount ** 2) * 0.7 * neg
            Player.jumpCount -= 1
        else:
            Player.isJump = False
            Player.jumpCount = 10

    redrawGameWindow()

