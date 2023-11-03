import pygame

from obstacle import Obstacle

stone_map10x10 = [
    ["swe", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", 11, "sdg", 11, "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", 11, "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["xxx", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "xxx"]]

map10x10 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map20x20 = [[11, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 5],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 11, 1, 1, 1, 1, 2, 2, 2, 5],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 11, 1, 11, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map40x40 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1,
     1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2,
     1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

map20x10 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]]


# map20x10 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
#             [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


class Map:
    """Klasa przechowująca i wyświetlająca mapę."""

    _map_10x10 = map10x10
    _map_20x20 = map20x20
    _map_20x10 = map20x10
    _map_40x40 = map40x40
    _stone_map_10x10 = stone_map10x10

    def __init__(self, program):
        map = Map._stone_map_10x10
        self.map = map
        self.width = program.settings.field_size * len(self.map[0])
        self.height = len(self.map) * program.settings.field_size
        self.program = program
        self.grass_img = pygame.image.load(
            "res/graphic/ground/grass.png").convert()
        self.grass_img = pygame.transform.scale(self.grass_img, (128, 128))
        self.stone_img = pygame.image.load(
            "res/graphic/ground/stone.png").convert()
        self.stone_img = pygame.transform.scale(self.stone_img, (128, 128))
        self.stone_wall_img = pygame.image.load(
            "res/graphic/ground/stone_wall.png").convert()
        self.wall = pygame.image.load("res/graphic/ground/wall.png")
        # STONE WALLS
        self.stone_wall_n_img = pygame.image.load(
            "res/graphic/ground/stone_wall_n.png").convert()
        self.stone_wall_s_img = pygame.image.load(
            "res/graphic/ground/stone_wall_s.png").convert()
        self.stone_wall_w_img = pygame.image.load(
            "res/graphic/ground/stone_wall_w.png").convert()
        self.stone_wall_e_img = pygame.image.load(
            "res/graphic/ground/stone_wall_e.png").convert()

        self.sheet_img = pygame.image.load("hatka.png").convert_alpha()
        self.sheet_img = pygame.transform.scale(self.sheet_img, (64, 64))
        self.obstacles = pygame.sprite.Group()
        self._load_obstacles()

        self.field_width = 128
        self.field_height = 128

    def _load_obstacles(self):
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                if field == 11:
                    obstacle = Obstacle(j, i)
                    self.obstacles.add(obstacle)

    def display_map(self):
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                if field == 1:
                    x = j * self.grass_img.get_width()
                    y = i * self.grass_img.get_height()
                    self.program.camera.camera_draw(self.grass_img, (x, y))
                    self._draw_grid(x, y, self.grass_img.get_width(),
                                    self.grass_img.get_height())
                if field == 2:
                    x = j * self.stone_img.get_width()
                    y = i * self.stone_img.get_height()
                    self.program.camera.camera_draw(self.stone_img, (x, y))
                    self._draw_grid(x, y, self.stone_img.get_width(),
                                    self.stone_img.get_height())

                if field == 3:
                    x = j * self.grass_img.get_width()
                    y = i * self.grass_img.get_height()
                    self.program.camera.camera_draw(self.grass_img, (x, y))
                    # x += self.grass_img.get_width() / 4
                    # y += self.grass_img.get_height() / 4
                    self.program.camera.camera_draw(self.sheet_img, (x, y))
                if field == 4:
                    x = j * self.stone_wall_img.get_width()
                    y = i * self.stone_wall_img.get_height()
                    self.program.camera.camera_draw(self.stone_wall_img, (x, y))
                    self._draw_grid(x, y, self.stone_wall_img.get_width(),
                                    self.stone_wall_img.get_height())
                if field == 5:
                    x = j * self.wall.get_width()
                    y = i * self.wall.get_height()
                    self.program.camera.camera_draw(self.wall, (x, y))
                    self._draw_grid(x, y, self.wall.get_width(),
                                    self.wall.get_height())
                if field == "sdg":
                    x = j * self.field_width
                    y = i * self.field_height
                    self.program.camera.camera_draw(self.stone_img, (x, y))
                    self._draw_grid(x, y, self.field_width,
                                    self.field_width)
                if field == "sws":
                    x = j * self.field_width
                    y = i * self.field_height
                    self.program.camera.camera_draw(self.stone_wall_img,
                                                    (x, y))
                    self._draw_grid(x, y, self.field_width,
                                    self.field_width)
                if field == "swn":
                    x = j * self.field_width
                    y = i * self.field_height
                    self.program.camera.camera_draw(self.stone_wall_n_img,
                                                    (x, y))
                    self._draw_grid(x, y, self.field_width,
                                    self.field_width)
                if field == "swe":
                    x = j * self.field_width
                    y = i * self.field_height
                    self.program.camera.camera_draw(self.stone_wall_e_img,
                                                    (x, y))
                    self._draw_grid(x, y, self.field_width,
                                    self.field_width)
                if field == "sww":
                    x = j * self.field_width
                    y = i * self.field_height
                    self.program.camera.camera_draw(self.stone_wall_w_img,
                                                    (x, y))
                    self._draw_grid(x, y, self.field_width,
                                    self.field_width)
                if field == 11:
                    for obstacle in self.obstacles:
                        if obstacle.y == i and obstacle.x == j:
                            obstacle.display(self.program.screen,
                                             self.program.camera)

    def _draw_grid(self, x, y, w, h):
        pass
        # _offset = (x, y) - self.program.camera.offset
        # rect = pygame.Rect(_offset, (w, h))
        # pygame.draw.rect(self.program.screen, (0, 0, 0), rect, 1)
        #
        # player_rect = self.program.camera.update_rect(self.program.player.rect)
        # if rect.collidepoint(player_rect.midbottom):
        #     pygame.draw.rect(self.program.screen, (255, 0, 0), rect, 2)
