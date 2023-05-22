import pygame as pg


class UI:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 30)
        self.size = 50
        self.pos_x = 110
        self.pos_y = 25

    def draw(self):
        self.player_text()
        self.npc_text()
        self.player()
        self.npc()

    def player(self):
        for obj in self.game.tanks:
            pg.draw.rect(self.game.screen, obj.color, (self.pos_x, self.pos_y, self.size, self.size))

            text_hp = self.font.render(str(obj.hp), True, obj.color)
            rect = text_hp.get_rect(center=(self.pos_x + 70, self.pos_y + 25))
            self.game.screen.blit(text_hp, rect)

            text_rank = self.font.render(str(obj.rank), True, obj.color)
            rect = text_rank.get_rect(center=(self.pos_x + 100, self.pos_y + 25))
            self.game.screen.blit(text_rank, rect)

    def npc(self):
        for obj in self.game.npcs:
            pg.draw.rect(self.game.screen, obj.color, (self.pos_x + 1000, self.pos_y, self.size, self.size))

            text_hp = self.font.render(str(obj.hp), True, obj.color)
            rect = text_hp.get_rect(center=(self.pos_x + 1070, self.pos_y + 25))
            self.game.screen.blit(text_hp, rect)

            text_rank = self.font.render(str(obj.rank), True, obj.color)
            rect = text_rank.get_rect(center=(self.pos_x + 1100, self.pos_y + 25))
            self.game.screen.blit(text_rank, rect)

    def player_text(self):
        text = self.font.render("My Tank", True, (255, 250, 250))
        rect = text.get_rect(center=(self.pos_x - 50, self.pos_y + 25))
        self.game.screen.blit(text, rect)

    def npc_text(self):
        text = self.font.render("NPC", True, (255, 250, 250))
        rect = text.get_rect(center=(self.pos_x - 50 + 1000, self.pos_y + 25))
        self.game.screen.blit(text, rect)

