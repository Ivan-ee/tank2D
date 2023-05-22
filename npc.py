import pygame as pg
from bullet import *
from settings import *
from level import *


class NPC:
    def __init__(self, game):
        self.game = game
        self.game.npcs.append(self)
        self.hp = NPC_HP
        self.bullets = []
        self.color = "blue"
        self.images = [pg.image.load('Images/npc_tank_up.png'),
                       pg.image.load('Images/npc_tank_right.png'),
                       pg.image.load('Images/npc_tank_bottom.png'),
                       pg.image.load('Images/npc_tank_left.png')]
        self.image = self.images[0]

        self.sound_shoot = pg.mixer.Sound('Sounds/shot.wav')
        self.sound_dead = pg.mixer.Sound('Sounds/dead.wav')
        self.sound_destroy = pg.mixer.Sound('Sounds/destroy.wav')

        self.rect = self.image.get_rect(center = NPC_POS)
        self.direct = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.pos = self.rect.center

        self.direction = pg.math.Vector2(0, 0)
        self.dir_x, self.dir_y = 0, 0
        self.dir = [self.dir_x, self.dir_y]

        self.shoot_distance = 250
        self.move_distance = 40

        self.path = []
        self.collision_rects = []
        self.empty_path = self.game.pathfind.empty_path

        self.shot_timer = 0

        self.rank = 0
        self.speed = MOVE_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]

    def update(self):
        self.stat_update()
        self.movement_logic()
        self.image_rotation()
        self.bullets_update()

    def end_game(self):
        self.rank = 6

    def stat_update(self):
        self.speed = MOVE_SPEED[self.rank]
        self.shot_delay = SHOT_DELAY[self.rank]
        self.bullet_speed = BULLET_SPEED[self.rank]

    def movement_logic(self):
        distance = self.get_distance(self.game.tank.position, self.game.npc.position)

        if distance > self.move_distance:
            self.movement()
        if distance < self.shoot_distance:
            self.shoot()

    def get_distance(self, pos_1, pos_2):
        return ((pos_2[0] - pos_1[0]) ** 2 + (pos_2[1] - pos_1[1]) ** 2) ** 0.5

    def movement(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos

    def shoot(self):
        self.dir = [self.dir_x, self.dir_y]

        if self.shot_timer == 0:
            self.sound_shoot.play()
            Bullet(self.game, self, self.dir[0] * self.bullet_speed, self.dir[1] * self.bullet_speed)
            self.shot_timer = self.shot_delay

        if self.shot_timer > 0: self.shot_timer -= 1

    def bullets_update(self):
        for bullet in self.bullets:
            bullet.update()

    def damage(self, value):
        self.hp -= value
        self.sound_destroy.play()
        if self.hp <= 0:
            self.game.npcs.remove(self)
            self.sound_dead.play()

    def image_rotation(self):
        self.dir_x = int(self.direction[0] + (0.5 if self.direction[0] > 0 else -0.5))
        self.dir_y = int(self.direction[1] + (0.5 if self.direction[0] > 0 else -0.5))

        if self.dir_x == 1:
            self.image = self.images[1]
        elif self.dir_x == -1:
            self.image = self.images[3]
        if self.dir_y == 1:
            self.image = self.images[2]
        elif self.dir_y == -1:
            self.image = self.images[0]

    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] * 50) + 25
                y = (point[1] * 50) + 25
                rect = pg.Rect((x - 12.5, y - 12.5), (25, 25))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pg.math.Vector2(self.pos)
            end = pg.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pg.math.Vector2(0, 0)
            self.path = []

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    @property
    def position(self):
        return self.rect.centerx, self.rect.centery

    @property
    def map_pos(self):
        return self.rect.centerx // self.game.map.cell_size, self.rect.centery // self.game.map.cell_size
