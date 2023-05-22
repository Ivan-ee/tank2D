from settings import *
from level import *
import pygame as pg
from bullet import *
from bonus import *

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Tank:
    def __init__(self, game):
        self.game = game
        self.game.tanks.append(self)
        self.x, self.y = TANK_POS
        self.hp = TANK_HP
        self.bullets = []
        self.color = "red"
        self.line_image = pg.image.load('Images/line.png')
        self.rect = pg.Rect(self.x, self.y, TANK_SIZE_SCALE, TANK_SIZE_SCALE)
        self.images = [pg.image.load('Images/player_tank_up.png'),
                       pg.image.load('Images/player_tank_right.png'),
                       pg.image.load('Images/player_tank_bottom.png'),
                       pg.image.load('Images/player_tank_left.png')]
        self.image = self.images[0]

        self.sound_shoot = pg.mixer.Sound('Sounds/shot.wav')
        self.sound_dead = pg.mixer.Sound('Sounds/dead.wav')
        self.sound_destroy = pg.mixer.Sound('Sounds/destroy.wav')

        self.direct = 0
        self.shot_timer = 0

        self.rank = 0
        self.speed = MOVE_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]

    def update(self):
        self.stat_update()
        self.check_win()
        self.movement()
        self.shoot()
        self.bullets_update()

    def check_win(self):
        if self.rank == 5:
            self.game.check_end_game()

    def end_game(self):
        self.rank = 6

    def stat_update(self):
        self.speed = MOVE_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]

    def bullets_update(self):
        for bullet in self.bullets:
            bullet.update()

    def movement(self):
        keys = pg.key.get_pressed()
        old_x, old_y = self.rect.topleft
        if keys[pg.K_a]:
            self.rect.x -= self.speed
            self.direct = 3
        elif keys[pg.K_d]:
            self.rect.x += self.speed
            self.direct = 1
        elif keys[pg.K_w]:
            self.rect.y -= self.speed
            self.direct = 0
        elif keys[pg.K_s]:
            self.rect.y += self.speed
            self.direct = 2

        self.image = self.images[self.direct]

        self.change_collision(old_x, old_y)

    def change_collision(self, x, y):
        for block in self.game.blocks:
            if self.rect.colliderect(block.rect):
                self.rect.topleft = x, y

    def shoot(self):
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and self.shot_timer == 0:
            dx = DIRECTS[self.direct][0] * self.bullet_speed
            dy = DIRECTS[self.direct][1] * self.bullet_speed
            Bullet(self.game, self, dx, dy)
            self.sound_shoot.play()
            self.shot_timer = self.shot_delay
        if self.shot_timer > 0: self.shot_timer -= 1

    def damage(self, value):
        self.hp -= value
        self.sound_destroy.play()
        if self.hp <= 0:
            self.game.tanks.remove(self)
            self.sound_dead.play()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    @property
    def position(self):
        return self.rect.centerx, self.rect.centery

    @property
    def map_pos(self):
        return self.rect.x // self.game.map.cell_size, self.rect.y // self.game.map.cell_size
