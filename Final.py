import math, sys
import pygame
import time
# Set up the clock
clock = pygame.time.Clock()

# Import pygame modules
from pygame.locals import *
# Initialize pygame
pygame.init()
# Set the windows name
pygame.display.set_caption("The Last Bot")
# Set a icon
pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
# Window's Size
screen = pygame.display.set_mode((1366,768))
# Load images
bg = pygame.image.load("Assets/Background3.jpg").convert()
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
WizardBullet = pygame.image.load('Assets/BossBullet.png')
Pause = pygame.image.load('Assets/Hit.png')
Health = pygame.image.load('Assets/Health1.png')
Energy = [pygame.image.load('Assets/Energy1.png'),pygame.image.load('Assets/Energy2.png'),pygame.image.load('Assets/Energy3.png'),pygame.image.load('Assets/Energy4.png'),pygame.image.load('Assets/Energy5.png'),pygame.image.load('Assets/Energy6.png'),pygame.image.load('Assets/Energy7.png')]
# BulletSound = pygame.mixer.Sound('Assets/BulletSound.wav')
# BulletHitSound = pygame.mixer.Sound('Assets/LaserHit.wav')
# BackgroundMusic = pygame.mixer.music.load('Assets/BossMusic.mp3')
# pygame.mixer.music.play(-1)

# Declaring Some Variables
file1 = open('Assets/Score.txt', 'r')
value = file1.read()
file2 = open('Assets/Health.txt', 'r')
H = file2.read()
Life = int(H)
score = int(value)
P1x = 25
P2x = 1200
P1y = 462
P2y = 462

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
        self.health = Life
        self.energy = 1
        self.visible = True
        self.powerUp = False
        self.pause = False
        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)

    def draw(self,screen):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if self.visible:
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
        if self.visible:
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
                self.health -= 2
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

# Defined class for Enemy's bullets
class enemyprojectile(object):
    def __init__(self,x,y,facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 14 * facing

    def draw(self,screen):
        if Enemy1.visible == True:
            screen.blit(WizardBullet,(self.x,self.y))

# Defined class for Enemy
class enemy1(object):
    enemyRight = [pygame.image.load('Assets/BW1.png'), pygame.image.load('Assets/BW2.png'),
                  pygame.image.load('Assets/BW3.png'), pygame.image.load('Assets/BW4.png'), pygame.image.load('Assets/BW5.png'),
                  pygame.image.load('Assets/BW6.png'), pygame.image.load('Assets/BW7.png'), pygame.image.load('Assets/BW8.png'),
                  pygame.image.load('Assets/BW9.png'), pygame.image.load('Assets/BW10.png'), pygame.image.load('Assets/BWA1.png'),
                  pygame.image.load('Assets/BWA2.png'),
                  pygame.image.load('Assets/BWA3.png'), pygame.image.load('Assets/BWA4.png'), pygame.image.load('Assets/BWA5.png'),
                  pygame.image.load('Assets/BWA6.png'), pygame.image.load('Assets/BWA7.png'), pygame.image.load('Assets/BWA8.png')]
    enemyLeft = [pygame.image.load('Assets/BS1.png'), pygame.image.load('Assets/BS2.png'),
                 pygame.image.load('Assets/BS3.png'), pygame.image.load('Assets/BS4.png'), pygame.image.load('Assets/BS5.png'),
                 pygame.image.load('Assets/BS6.png'), pygame.image.load('Assets/BS7.png'), pygame.image.load('Assets/BS8.png'),
                 pygame.image.load('Assets/BS9.png'), pygame.image.load('Assets/BS10.png'), pygame.image.load('Assets/BSA1.png'),
                 pygame.image.load('Assets/BSA2.png'),
                 pygame.image.load('Assets/BSA3.png'), pygame.image.load('Assets/BSA4.png'), pygame.image.load('Assets/BSA5.png'),
                 pygame.image.load('Assets/BSA6.png'), pygame.image.load('Assets/BSA7.png'), pygame.image.load('Assets/BSA8.png')]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.Armourhitbox = (self.x + 200, self.y + 15, 190, 330)
        self.health = 150
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 54:
                self.walkcount = 0
            if self.vel > 0:
                screen.blit(self.enemyRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 200, self.y + 15, 190, 330)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0] - 30, self.Armourhitbox[1] - 30, 250, 15))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0] - 30, self.Armourhitbox[1] - 30, 250 - ((250/150) * (150 - self.health)), 15))
            else:
                screen.blit(self.enemyLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 155, self.y + 15, 190, 330)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0] - 30, self.Armourhitbox[1] - 30, 250, 15))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0] - 30, self.Armourhitbox[1] - 30, 250 - ((250/150) * (150 - self.health)), 15))
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
        screen.blit(portal1,(P1x,P1y))
        screen.blit(portal2,(P2x,P2y))
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
        if pygame.key.get_pressed()[K_SPACE] :
            Player.pause = False
    Life = Player.health
    file2 = open('Assets/Health.txt', 'w')
    file2.write(str(Life))
    file2.close()
    screen.blit(ground, (0, 622))
    for bullet in bullets:
        bullet.draw(screen)
    for enemybullet in EnemyBullets:
        enemybullet.draw(screen)
    if Player.visible == False:
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
        if Timer2 >= 10:
            fade()
            import Menu
    if Enemy1.visible == False:
        screen.blit(Pause, (0, 0))
        font1 = pygame.font.SysFont('Space Ranger', 150)
        font2 = pygame.font.SysFont('Space Ranger', 100)
        text = font1.render('Victory!!', 1, (255, 255, 255, 0))
        text1 = font2.render('YOU KILLED THE BOSS!', 1, (255, 255, 255, 0))
        screen.blit(text, (683 - (text.get_width())/2 , 200 ))
        screen.blit(text1, (683 - (text1.get_width())/2, 400))
        List2.append(Endtime)
        Length = len(List2)
        Timer2 = List2[Length - 1] - List2[0]
        file1 = open('Assets/Score.txt', 'w')
        file1.write(str(score))
        file1.close()
        if Timer2 >= 3:
            fade()
            import Menu
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
# Enemy's path,width and height declaration
Enemy1 = enemy1(300,280,181,117, 800)

Button = button((0,255,0), 610,500,150,100,'Retry')
shootLoop = 0
bullets = []
EnemyBullets = []
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
            if Player.x < 35:
                if Player.Armourhitbox[1] + Player.Armourhitbox[3] > P1y:
                    Player.x = 1130
            elif Player.x > 1140:
                if Player.Armourhitbox[1] + Player.Armourhitbox[3] > P2y:
                    Player.x = 40
            Player.vel = 30

    # Decreases score if enemy's bullet collids with player
    if Enemy1.visible == True:
        if (Player.Armourhitbox[1] < Enemy1.Armourhitbox[1] + Enemy1.Armourhitbox[3] and Player.Armourhitbox[1] + Player.Armourhitbox[3] > Enemy1.Armourhitbox[1]):
            if (Player.Armourhitbox[0] + Player.Armourhitbox[2] > Enemy1.Armourhitbox[0] and Player.Armourhitbox[0] < Enemy1.Armourhitbox[0] + Enemy1.Armourhitbox[2]):
                Player.hit()
                if score >= 3:
                    score -= 3
                else:
                    score = 0

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
                import Final

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
                    # BulletHitSound.play()
                    Enemy1.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < 1360 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Loop for enemy's bullet
    if Enemy1.visible and Player.visible:
        for enemybullet in EnemyBullets:
            if (enemybullet.y < Player.Armourhitbox[1] + Player.Armourhitbox[3] and enemybullet.y  > Player.Armourhitbox[1]) :
                if (enemybullet.x > Player.Armourhitbox[0] and enemybullet.x < Player.Armourhitbox[0] + Player.Armourhitbox[2]) :
                        # BulletHitSound.play()
                        Player.hit()
                        if score >= 5:
                            score -= 5
                        else:
                            score = 0
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
            EnemyBullets.append(enemyprojectile(round(Enemy1.x + 320), round(Enemy1.y + 250), facing))
        if len(EnemyBullets) < 1 and facing == -1:
            EnemyBullets.append(enemyprojectile(round(Enemy1.x + 25), round(Enemy1.y + 250), facing))

    # Tracking key pressed
    keys = pygame.key.get_pressed()

    # Space key for bullet
    if keys[K_SPACE] and shootLoop == 0:
        # BulletSound.play()
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



