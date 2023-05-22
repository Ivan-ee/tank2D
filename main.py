import pygame as pg
from settings import *
from map import *
from tank import *
from npc import *
from pathfind import *
from ui import *
import sys


class Game:
    def __init__(self):
        pg.mixer.init(12000, -8, 1, 32768)
        pg.mixer.music.load('Sounds/super-mario-saundtrek.mp3')
        pg.mixer.music.play(-1)
        pg.init()
        self.volume = 1
        self.tanks = []
        self.npcs = []
        self.blocks = []
        self.bangs = []
        self.bonuses = []
        self.sound_lose = pg.mixer.Sound('Sounds/09 Game Over.mp3')
        self.sound_win = pg.mixer.Sound('Sounds/level_finish.wav')
        self.timer = 60
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.screen = pg.display.set_mode(RES)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.tank = Tank(self)
        self.pathfind = PathFind(self)
        self.npc = NPC(self)
        self.ui = UI(self)

    def update(self):
        self.start_game()
        self.tank.update()
        self.npc_update()
        self.bangs_update()
        self.bonus_update()
        self.map.spawn_bonus()
        self.check_end_game()
        self.delta_time = self.clock.tick(FPS)
        pg.display.flip()
        pg.display.set_caption("Tank 2D")

    def npc_update(self):
        for npc in self.npcs:
            npc.update()

    def npc_draw(self):
        for npc in self.npcs:
            npc.draw()

    def bangs_update(self):
        for bang in self.bangs:
            bang.update()

    def bangs_draw(self):
        for bang in self.bangs:
            bang.draw()

    def bonus_update(self):
        for bonus in self.bonuses:
            bonus.update()

    def bonus_draw(self):
        for bonus in self.bonuses:
            bonus.draw()

    def start_game(self):

        image = pg.image.load('Images/start.png')
        rect = 200, 200

        if self.timer > 0:
            self.screen.blit(image, rect)
            self.timer -= 1
        else:
            pg.mixer.music.set_volume(0.05)

    def check_end_game(self):
        if len(self.tanks) == 0:
            image = pg.image.load('Images/lose.png')
            rect = 200, 200
            self.screen.blit(image, rect)

            self.play_lose_music()
            self.stop_tanks()

        if len(self.npcs) == 0:
            image = pg.image.load('Images/win.png')
            rect = 200, 200
            self.screen.blit(image, rect)

            self.play_win_music()
            self.stop_tanks()

    def play_lose_music(self):
        pg.mixer.music.stop()
        self.sound_lose.set_volume(0.02)
        self.sound_lose.play(1)

    def play_win_music(self):
        pg.mixer.music.stop()
        self.sound_win.set_volume(0.02)
        self.sound_win.play(1)

    def stop_tanks(self):
        self.tank.end_game()
        self.npc.end_game()

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.tank.draw()
        # self.pathfind.draw_path()
        self.npc_draw()
        self.bangs_draw()
        self.bonus_draw()
        self.ui.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            self.pathfind.create_path()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
