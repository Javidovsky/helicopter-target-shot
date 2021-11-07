import math
import pygame
from pygame import mixer
import random

# initialise
pygame.init()

# sound

shootingnoise = mixer.Sound("./assets/shootingnoise.mp3")
hitnoise = mixer.Sound("./assets/hit.mp3")

# screen
screen = pygame.display.set_mode((800, 600))

# title background logo stuff
pygame.display.set_caption("Javid aim trainer")
icon = pygame.image.load("./assets/blueheli.png")
pygame.display.set_icon(icon)

ground = pygame.image.load("./assets/ground.png")


def floor():
    screen.blit(ground, (0, 551))


# player
playerImg = pygame.image.load("./assets/blueheli.png")
playerx = 100
playery = 360
newplayerx = 0
newplayery = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# target
targetImg = pygame.image.load("./assets/target.png")
targetx = 700
targety = 250
newtargetx = 0
newtargety = 0.5


def target(x, y):
    screen.blit(targetImg, (x, y))

# title screen
titleImg = pygame.image.load("./assets/title.png")
titlex = 0
titley = 0

def titlescreen(x, y):
    screen.blit(titleImg, (x, y))


# bullet
bulletImg = pygame.image.load("./assets/bullet.png")
bulletx = 100
bullety = 300
newbulletx = 0
newbullety = 0
bulletstate = "ready"


def firebullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletImg, (x, y + 5))


# collision
def iscollision(targetx, targety, bulletx, bullety):
    distance = math.sqrt((math.pow((targetx + 32) - (bulletx + 12), 2)) + (math.pow((targety + 32) - (bullety + 5), 2)))
    if distance < 33:
        return True
    else:
        return False

def checkcollision(object1xpos, object1ypos, object1xlength, object1ylength, object2xpos, object2ypos, object2xlength, object2ylength):
    rect1 = pygame.Rect(object1xpos, object1ypos, object1xlength, object1ylength)
    rect2 = pygame.Rect(object2xpos, object2ypos, object2xlength, object2ylength)
    if rect1.colliderect(rect2):
        return True


# score
scorevalue = 0
font = pygame.font.Font("./assets/freesansbold.ttf",32)
textx = 10
texty = 10

def showscore(x, y):
    score = font.render("Score: " + str(scorevalue), True, (255,255,255))
    screen.blit(score, (x,y))

def showlastscore(x, y):
    score = font.render("Last score: " + str(scorevalue), True, (255,255,255))
    screen.blit(score, (x,y))

#timer
timervalue = 0
timertextx = 700
timertexty = 10

lastsec = 0

def showtimer(x, y):
    timer = font.render("Timer: " + str(15 - timervalue), True, (255,255,255))
    screen.blit(timer, (x,y))

# misc
start_ticks = pygame.time.get_ticks()

# game loop
running = True
menu = True
game = True
while running:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scorevalue = 0
                    playery = 300
                    game = True
                    menu = False
        # rgb
        screen.fill((113, 196, 210))
        # floor
        floor()
        # title
        titlescreen(0, 0)
        # last score
        showlastscore(textx, texty)
        lastsec = 0
        timervalue = 0
        start_ticks = pygame.time.get_ticks()
        # update
        pygame.display.update()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu = False
                game = False
            # keystroke
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    newplayery = -0.8
                    playerImg = pygame.image.load("./assets/backwardtilt.png")
                if event.key == pygame.K_SPACE:
                    if bulletstate == "ready":
                        shootingnoise.play()
                        bullety = playery
                        firebullet(bulletx + 20, bullety + 40)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    newplayery = 0
                    playerImg = pygame.image.load("./assets/forwardtilt.png")

        # borders
        if playery > 500:
            menu = True
            game = False
        if playery < 0:
            playery = 0

        # rgb
        screen.fill((113, 196, 210))

        # player
        playery += 0.4
        playerx += newplayerx
        playery += newplayery
        player(playerx, playery)

        # target
        target(targetx, targety)

        # bullet
        if bulletx >= 800:
            bulletx = 100
            bulletstate = "ready"
        if bulletstate == "fire":
            firebullet(bulletx, bullety)
            bulletx += 2

        # collision
        if checkcollision(bulletx, bullety, 30, 11, targetx, targety, 64, 64):
            hitnoise.play()
            bulletx = 100
            bulletstate = "ready"
            targety = random.randint(50, 430)
            scorevalue += 1

        # floor
        floor()

        # timer
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 15:
            menu = True
            game = False
        if seconds - lastsec >= 1:
            lastsec += 1
            timervalue += 1
        showtimer(650, 10)


        # score
        showscore(textx, texty)

        # update
        pygame.display.update()
