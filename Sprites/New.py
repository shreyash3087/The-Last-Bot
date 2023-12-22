import math, random, sys
import pygame
#set up the clock
clock = pygame.time.Clock()
#import pygame modules
from pygame.locals import *
pygame.init()
#Colors
BLACK = (0, 0, 0, 255)
#set the windows name
pygame.display.set_caption("The Knight")

#initiates the window
screen = pygame.display.set_mode((1366,768))

#load images
bg = pygame.image.load("mountains.png").convert()
ground = pygame.image.load("Ground.png")
walkRight = [pygame.image.load('run1.png'),pygame.image.load('run2.png'),pygame.image.load('run3.png'),pygame.image.load('run4.png'),pygame.image.load('run5.png'),pygame.image.load('run6.png'),pygame.image.load('run7.png'),pygame.image.load('run8.png'),]
walkLeft = [pygame.image.load('rleft1.png'),pygame.image.load('rleft2.png'),pygame.image.load('rleft3.png'),pygame.image.load('rleft4.png'),pygame.image.load('rleft5.png'),pygame.image.load('rleft6.png'),pygame.image.load('rleft7.png'),pygame.image.load('rleft8.png')]
Char = pygame.image.load('idle.png')
char = pygame.image.load('idle1.png')
BulletLeft = pygame.image.load('Bullet1.png')
BulletRight = pygame.image.load('Bullet.png')


score = 0

#Defined class for player
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
    def draw(self,screen):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if not (self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                # self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                # pygame.draw.rect(screen, (225, 0, 0), self.Armourhitbox, 2)
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                # self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
                # pygame.draw.rect(screen, (225, 0, 0), self.Armourhitbox, 2)

        else:
            if self.left:
                screen.blit(char, (self.x, self.y))
                # self.Armourhitbox = (self.x + 47, self.y + 12, 54, 105)
                # pygame.draw.rect(screen, (225, 0, 0), self.Armourhitbox, 2)
            else:
                screen.blit(Char, (self.x, self.y))
                # self.Armourhitbox = (self.x + 33, self.y + 12, 54, 105)
                # pygame.draw.rect(screen, (225, 0, 0), self.Armourhitbox, 2)



#Defined class for bullets
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

class enemy(object):
    enemyRight = [pygame.image.load('EW0.png'), pygame.image.load('EW1.png'), pygame.image.load('EW2.png'),
                 pygame.image.load('EW3.png'), pygame.image.load('EW4.png'), pygame.image.load('EW5.png'),
                 pygame.image.load('EW6.png'), pygame.image.load('EW7.png'), pygame.image.load('EW8.png'),
                 pygame.image.load('EW9.png'),pygame.image.load('EAR0.png'), pygame.image.load('EAR1.png'), pygame.image.load('EAR2.png'),
                 pygame.image.load('EAR3.png'), pygame.image.load('EAR4.png'), pygame.image.load('EAR5.png'),
                 pygame.image.load('EAR6.png'), pygame.image.load('EAR7.png'), pygame.image.load('EAR8.png'),
                 pygame.image.load('EAR9.png')]
    enemyLeft = [pygame.image.load('ES0.png'), pygame.image.load('ES1.png'), pygame.image.load('ES2.png'),
                pygame.image.load('ES3.png'), pygame.image.load('ES4.png'), pygame.image.load('ES5.png'),
                pygame.image.load('ES6.png'), pygame.image.load('ES7.png'), pygame.image.load('ES8.png'),
                pygame.image.load('ES9.png'), pygame.image.load('EAL0.png'), pygame.image.load('EAL1.png'), pygame.image.load('EAL2.png'),
                 pygame.image.load('EAL3.png'), pygame.image.load('EAL4.png'), pygame.image.load('EAL5.png'),
                 pygame.image.load('EAL6.png'), pygame.image.load('EAL7.png'), pygame.image.load('EAL8.png'),
                 pygame.image.load('EAL9.png')]

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

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 60:
                self.walkcount = 0

            if self.vel > 0:
                screen.blit(self.enemyRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 62, self.y + 32, 144, 140)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0], self.Armourhitbox[1] - 20, 100, 10))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0], self.Armourhitbox[1] - 20, 100 - ((100/29) * (29 - self.health)), 10))
                # pygame.draw.rect(screen, (225, 0, 0), self.Armourhitbox, 2)
            else:
                screen.blit(self.enemyLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
                self.Armourhitbox = (self.x + 35, self.y + 32, 144, 140)
                pygame.draw.rect(screen, (255, 0, 0), (self.Armourhitbox[0] + 60, self.Armourhitbox[1] - 20, 100, 10))
                pygame.draw.rect(screen, (0, 128, 0), (self.Armourhitbox[0] + 60, self.Armourhitbox[1] - 20, 100 - ((100/29) * (29 - self.health)), 10))
                # pygame.draw.rect(screen, (225,0,0), self.Armourhitbox, 2)


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
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")

#Background and some other stuffs
def redrawGameWindow():
    screen.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    screen.blit(text, (1170, 10))
    Player.draw(screen)
    Knight1.draw(screen)
    screen.blit(ground, (0, 622))
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()

font = pygame.font.SysFont('Berlin Sans FB', 50)
Player = player(50, 505, 177, 117)
Knight1 = enemy(400,450,181,117, 1000)
shootLoop = 0
bullets = []

#main loop
while True:
    # maintain 27 fps
    clock.tick(40)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 20:
        shootLoop = 0

    # event loop
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):#Check for buttons
            # stop pygame
            pygame.quit()
            # stop script
            sys.exit()
    #loop for bullets
    for bullet in bullets:
        if (bullet.y - 12 < Knight1.Armourhitbox[1] + Knight1.Armourhitbox[3] and bullet.y + 12 > Knight1.Armourhitbox[1]) :
            if (bullet.x + 14 > Knight1.Armourhitbox[0] and bullet.x - 14 < Knight1.Armourhitbox[0] + Knight1.Armourhitbox[2]) :
                Knight1.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        if bullet.x < 1360 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    #Tracking key pressed
    keys = pygame.key.get_pressed()
    #Space key for bullet
    if keys[K_SPACE] and shootLoop == 0:
        Player.shoot = True
        if Player.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(Player.x + Player.width //2), round(Player.y + Player.height //2), facing))
        shootLoop = 1
    #Left arrow key for moving left,Right arrow key for moving right

    if keys[pygame.K_LEFT] and Player.x > Player.vel:
        Player.x -= Player.vel
        Player.left = True
        Player.right = False
        Player.standing = False
    elif keys[pygame.K_RIGHT] and Player.x < 1360 - Player.width - Player.vel:
        Player.x += Player.vel
        Player.right = True
        Player.left = False
        Player.standing = False
    else:
        Player.standing = True
        Player.walkCount = 0

    if not(Player.isJump):
        #Up arrow key for jumping
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