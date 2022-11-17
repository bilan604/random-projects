import pygame
from math import sqrt

# base params
pygame.init()
winX, winY = 1280, 780
win = pygame.display.set_mode((winX, winY))
pygame.display.set_caption("TheGame")
running = True

# players and NPC
vel = 12
x, y = 100, 100

enemyVel1 = 7
enemyX1, enemyY1 = 200, 500

enemyVel2 = 9
enemyX2, enemyY2 = 800, 300

shotX, shotY = -1, -1

def draw_game():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (0, 0, 255), (x, y, 20, 20))

    # draw if enemy not been shot:
    #  or maybe a better implementation
    pygame.draw.rect(win, (255, 0, 0), (enemyX1, enemyY1, 35, 35))
    pygame.draw.rect(win, (0, 255, 0), (enemyX2, enemyY2, 35, 35))
    if shotX > 0:
        pygame.draw.rect(win, (0, 0, 255), (shotX, shotY, 10, 10))
    pygame.display.update()

def updateEnemy(eX, eY, eVel):
    isRun = True
    if eX < x - 10:
        eX = eX + eVel
        draw_game()
    elif eX > x + 10:
        eX = eX - eVel
        draw_game()
    elif eY < y - 10:
        eY = eY + eVel
    elif eY > y + 10:
        eY = eY - eVel
    else:
        isRun = False
    return eX, eY, isRun

while running:
    pygame.time.delay(50)
    enemyX1, enemyY1, running1 = updateEnemy(enemyX1, enemyY1, enemyVel1)
    enemyX2, enemyY2, running2 = updateEnemy(enemyX2, enemyY2, enemyVel2)
    if 0 < shotX < winX and 0 < shotY < winY:
        shotX += shotDirX
        shotY += shotDirY
    else:
        shotX = -1
        shotY = -1
    running = any([running1, running2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    # mouse click makes you shoot a projectile
    mpos = pygame.mouse.get_pos()
    mpress = pygame.mouse.get_pressed(3)
    if mpress[0] and shotX == -1 and shotY == -1:
        factor = 1 / sqrt((mpos[0]-x)**2 + (mpos[1]-y)**2)
        shotDirX = (mpos[0]-x)*factor
        shotDirY = (mpos[1]-y)*factor
        # bullet speed
        shotDirX, shotDirY = int(shotDirX*40), int(shotDirY*40)
        shotX, shotY = x + (shotDirY), y + (shotDirY)

    draw_game()

pygame.quit()