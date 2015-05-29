#!/usr/bin/python2.7

import pygame
from pygame.locals import *
from random import randint, uniform
import time
import sys

# Image paths
enemy_img = "img/enemy.png"
player_img = "img/car.png"
shot_img = "img/shot.png"
button_img = "img/button.png"

# Settings, enter whatever values you like
jump_power = 7 #How high can you jump?
shot_power = 7 #How hard can you shoot?
ammo_on_kill = 2 #Ammo awarded on kill
score_on_kill = 10 #Score awarded on kill
enemy_damage = 30 #Score lost on enemy collision
score = 0 #Starting score
ammo = 20 #Starting ammo
font_name = "Sans" #Font family for text
font_size = 25 #Font size for text

#Init lists
shots = []
enemies = []

#Init game
screen = pygame.display.set_mode((500, 500), DOUBLEBUF)
pygame.init()

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
font = pygame.font.SysFont(font_name, font_size)

#Classes
class Entity(object): #The main class for objects on screen
    def __init__(self, x, y, filename, movement=None, gravity=0.1):
        self.alive = True
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename)
        if movement is None:
            self.movement = [0, 0]
        else:
            self.movement = movement
        self.gravity = gravity
    def update(self):
        self.movement[1] += self.gravity
        self.x += self.movement[0]
        self.y += self.movement[1]

        if self.y > 500:
            self.alive = False
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.image.get_rect().width,
                                self.image.get_rect().height)

class Shot(Entity):
    def __init__(self, x, y, movement=None):
        global shot_power
        super(Shot, self).__init__(x, y, shot_img, movement)

class Player(Entity):
    def __init__(self):
        super(Player, self).__init__(200, 350, player_img)
    def update(self):
        super(Player, self).update()
        if self.y < 0:
            self.y = 0
        elif self.y > (500 - self.image.get_rect().height):
            self.y = 500 - self.image.get_rect().height
            self.movement[1] = 0

        if self.x < 0:
            self.x = 0
        elif self.x > (500 - self.image.get_rect().width):
            self.x = 500 - self.image.get_rect().width
    def jump(self):
        if self.y >= (500 - self.image.get_rect().height):
            global jump_power
            self.movement[1] = -jump_power
    def shoot(self):
        global ammo
        if ammo > 0:
            ammo -= 1
            shots.append(Shot(self.x + self.image.get_rect().width/2, p.y, [0, -shot_power]))

class Enemy(Entity):
    justCollided = False
    def __init__(self):
        self.image = pygame.image.load(enemy_img)
        super(Enemy, self).__init__(randint(0, 500 - self.image.get_rect().width), randint(0, 200), enemy_img, [uniform(1.0, 5.0), 0], 0)
    def update(self):
        super(Enemy, self).update()
        if self.x < 0 or self.x > 500 - self.image.get_rect().width:
        	self.movement[0] = -self.movement[0];
        if self.y >= 500:
            global score
            score += score_on_kill
            global ammo
            ammo += ammo_on_kill
            self.alive = False
        if (not self.rect().colliderect(p.rect())) and self.justCollided:
            self.justCollided = False
        if self.rect().colliderect(p.rect()) and not self.justCollided:
            self.justCollided = True
            global score
            if score - enemy_damage < 0:
                score = 0
            else:
                score -= enemy_damage

class Button(Entity):
    def __init__(self, x, y):
        super(Button, self).__init__(x, y, button_img, gravity=0)
    def update(self):
        if self.rect().colliderect(p.rect()):
            enemies.append(Enemy())
        else:
            self.y = 500 - 8

enemies = [Enemy(), Enemy(), Enemy()]
p = Player()
button = Button(0, 500-8)

while True:
    #Check input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print 'Exiting...'
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                p.movement[0] += 10
            elif event.key == K_LEFT:
                p.movement[0] += -10
            elif event.key == K_DOWN:
                p.gravity = 0.5
            elif event.key == K_SPACE:
                p.jump()
            elif event.key == K_z:
                p.shoot()
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                p.movement[0] -= 10
            elif event.key == K_LEFT:
                p.movement[0] -= -10
            elif event.key == K_DOWN:
                p.gravity = 0.1

    #Update stuff
    for entity in shots + enemies:
        entity.update()

    for shot in shots:
        for enemy in enemies:
            if shot.rect().colliderect(enemy.rect()):
                enemy.gravity = 0.1
                shot.alive = False

    enemies = [enemy for enemy in enemies if enemy.alive]
    shots = [shot for shot in shots if shot.alive]

    if len(enemies) == 0:
        enemies.append(Enemy())
        enemies.append(Enemy())
        enemies.append(Enemy())

    p.update()
    button.update()

    #Draw everything to screen
    screen.fill((255, 255, 255))

    for entity in enemies + shots:
        entity.draw()

    p.draw()
    button.draw()

    #Render text
    textlines = []
    linenumber = 0
    textlines.append(font.render("Score: " + str(score), 1, (0,0,0)))
    textlines.append(font.render("Ammo: " + str(ammo), 1, (0,0,0)))
    if p.gravity == 0.5:
        textlines.append(font.render("GRAVITY", 1, (0,0,0)))
    if score == 420:
        textlines.append(font.render("Blaze it!", 1, (0,0,0)))

    for line in textlines:
        screen.blit(line, (0, linenumber * (font_size + 5)))
        linenumber += 1


    pygame.display.flip()
    time.sleep(0.01)
