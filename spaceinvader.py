import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.jpg")

# title and icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load("ship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(6):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"  # ready -cannot see bullet , fire - moving

#score
score = 0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10
exit_font=pygame.font.Font('freesansbold.ttf',32)

def gameovertext():
    overtext = exit_font.render("Game Over" + str(" "), True, (255, 255, 255))
    screen.blit(overtext, (350,300))

def show_score(x,y):
    global score
    score_value=font.render("score: "+str(score),True,(255,255,255))
    screen.blit(score_value, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def collision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if dist < 27:
        return True
    else:
        return False


running = True
while running:
    # screen.fill((20, 10, 30))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # print("key is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change -= 3
            #    print("left key pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            #   print("right key pressed")
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("key releadsed")
                playerX_change = 0

    playerX += playerX_change
    if playerX > 740:
        playerX = 730
    if playerX < 0:
        playerX = 10


    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=1000
            gameovertext()
            break
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i],i)
        
        # collision bw bullet and enemy
        collission = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collission:
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)


    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textx,texty)
    pygame.display.update()
