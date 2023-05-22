import pygame as pg


class Block:
    def __init__(self, game, map, px, py):
        self.game = game
        self.map = map
        self.game.blocks.append(self)
        self.rect = pg.Rect(px, py, self.map.cell_size, self.map.cell_size)
