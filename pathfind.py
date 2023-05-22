from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pygame as pg


class PathFind:
    def __init__(self, game):
        self.game = game
        self.matrix = game.map.mini_map
        self.grid = Grid(matrix = self.matrix)

        self.path = []
        self.collision_rects = []

    def empty_path(self):
        self.path = []

    def create_path(self):
        start_x, start_y = self.game.npc.map_pos
        start = self.grid.node(start_x, start_y)

        end_x, end_y = self.game.tank.map_pos
        end = self.grid.node(end_x, end_y)
        finder = AStarFinder()
        self.path,_ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.game.npc.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point[0] * 50) + 25
                y = (point[1] * 50) + 25
                points.append((x, y))

            pg.draw.lines(self.game.screen, '#4a4a4a', False, points, 5)

