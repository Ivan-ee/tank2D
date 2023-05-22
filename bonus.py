import pygame as pg


class Bonus:
    def __init__(self, game, x, y):
        self.game = game
        self.game.bonuses.append(self)
        self.x, self.y = x, y

        self.image = pg.image.load('Images/bonus_star.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.sound = pg.mixer.Sound('Sounds/star.wav')
        self.sound.play()

        self.timer = 600

    def update(self):
        self.remove()
        self.check_collision()

    def check_collision(self):
        for tank in self.game.tanks:
            if self.rect.colliderect(tank.rect):
                self.game.bonuses.remove(self)
                tank.rank += 1
                tank.hp += 2
                break
        for npc in self.game.npcs:
            if self.rect.colliderect(npc.rect):
                npc.rank += 1
                npc.hp += 2
                self.game.bonuses.remove(self)
                break

    def remove(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.game.bonuses.remove(self)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
