import pygame as pg
from tank import *
from bang import *
from settings import *


class Bullet:
    def __init__(self, game, tank, dx, dy):
        self.game = game
        self.tank = tank
        self.tank.bullets.append(self)
        self.damage = 1
        self.sound_destroy = pg.mixer.Sound('Sounds/destroy.wav')

        self.x, self.y = self.tank.rect.centerx, self.tank.rect.centery
        self.dx, self.dy = dx, dy
        self.old_x, self.old_y = self.x, self.y

        self.timer = 0

    def update(self):
        self.movement()
        self.remove()
        self.check_collision()
        self.check_move()
        self.draw()

    def movement(self):
        self.x += self.dx
        self.y += self.dy

    def remove(self):
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.tank.bullets.remove(self)

    def check_move(self):
        self.timer += 0.1
        if self.timer >= 2 and self.old_x == self.x and self.old_y == self.y:
            self.tank.bullets.remove(self)

    def check_collision(self):
        for block in self.game.blocks:
            if block.rect.collidepoint(self.x, self.y):
                self.tank.bullets.remove(self)
                self.sound_destroy.play()
                Bang(self.game, self.x, self.y)
                break

        for npc in self.game.npcs:
            if npc != self.tank and npc.rect.collidepoint(self.x, self.y):
                self.tank.bullets.remove(self)
                self.sound_destroy.play()
                Bang(self.game, self.x, self.y)
                npc.damage(self.damage)
                break

        for tank in self.game.tanks:
            if tank != self.tank and tank.rect.collidepoint(self.x, self.y):
                self.tank.bullets.remove(self)
                self.sound_destroy.play()
                Bang(self.game, self.x, self.y)
                tank.damage(self.damage)
                break

    def draw(self):
        pg.draw.circle(self.game.screen, 'yellow', (self.x, self.y), 5)
