import pygame as pg

class Bang:
    def __init__(self, game, px, py):
        self.game = game
        self.game.bangs.append(self)

        self.image_bangs = [
            pg.image.load('Images/bang1.png'),
            pg.image.load('Images/bang2.png'),
            pg.image.load('Images/bang3.png'),
    ]

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3: self.game.bangs.remove(self)

    def draw(self):
        image = self.image_bangs[int(self.frame)]
        rect = image.get_rect(center = (self.px, self.py))
        self.game.screen.blit(image, rect)
