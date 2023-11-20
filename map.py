import pygame

from obstacle import Obstacle

stone_map10x10 = [
    ["swe", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["xxx", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "xxx"]]

stone_map40x20 = [
    ["swe", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws",
     "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws",
     "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws",
     "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sws", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "swi", "swi", "swi", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sws", "sws", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["swe", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg",
     "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sdg", "sww"],
    ["xxx", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn",
     "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn",
     "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn",
     "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "swn", "xxx"]]


class Map:
    """Klasa przechowująca i wyświetlająca mapę."""

    _stone_map_10x10 = stone_map10x10
    _stone_map_40x20 = stone_map40x20

    def __init__(self, program):
        self.tM = program.textureMenager.textures
        self.map = Map._stone_map_40x20
        self.width = program.settings.field_size * len(self.map[0])
        self.height = len(self.map) * program.settings.field_size
        self.program = program

        # self._load_images()

        self.obstacles = pygame.sprite.Group()  # Dla całej gry
        self._obstacles = []  # Tylko dla tej klasy
        self._load_obstacles(program)

        self.field_size = program.settings.field_size

    # def _load_images(self):
    #     self.stone_ground_img = pygame.image.load(
    #         "res/graphic/ground/stone_ground.png").convert()
    #     self.stone_wall_n_img = pygame.image.load(
    #         "res/graphic/ground/stone_wall_n.png").convert()
    #     self.stone_wall_s_img = pygame.image.load(
    #         "res/graphic/ground/stone_wall_s.png").convert()
    #     self.stone_wall_w_img = pygame.image.load(
    #         "res/graphic/ground/stone_wall_w.png").convert()
    #     self.stone_wall_e_img = pygame.image.load(
    #         "res/graphic/ground/stone_wall_e.png").convert()
    #     self.stone_wall_inside_img = pygame.image.load(
    #         "res/graphic/ground/stone_wall_inside.png")

    def _load_obstacles(self, program):
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                if field == "sws":
                    obstacle = Obstacle(program, j, i,
                                        self.tM["map"]["stone_wall_s"])
                    self.obstacles.add(obstacle)
                    self._obstacles.append(obstacle)
                if field == "swn":
                    obstacle = Obstacle(program, j, i,
                                        self.tM["map"]["stone_wall_n"])
                    self.obstacles.add(obstacle)
                    self._obstacles.append(obstacle)
                if field == "swe":
                    obstacle = Obstacle(program, j, i,
                                        self.tM["map"]["stone_wall_e"])
                    self.obstacles.add(obstacle)
                    self._obstacles.append(obstacle)
                if field == "sww":
                    obstacle = Obstacle(program, j, i,
                                        self.tM["map"]["stone_wall_w"])
                    self.obstacles.add(obstacle)
                    self._obstacles.append(obstacle)
                if field == "swi":
                    obstacle = Obstacle(program, j, i,
                                        self.tM["map"]["stone_wall_inside"])
                    self.obstacles.add(obstacle)
                    self._obstacles.append(obstacle)

    def display(self):
        for i, row in enumerate(self.map):
            for j, field in enumerate(row):
                x = j * self.field_size
                y = i * self.field_size
                if field == "sdg":
                    self.program.camera.camera_draw(
                        self.tM["map"]["stone_ground"], (x, y))
                DEV = 0
                if DEV:
                    self._draw_grid(x, y)
        # for obstacle in self.obstacles:
        #     obstacle.display()
        for obstacle in self._obstacles:
            obstacle.display()

    def _draw_grid(self, x, y):
        _offset = (x, y) - self.program.camera.offset
        rect = pygame.Rect(_offset, (self.field_size, self.field_size))
        pygame.draw.rect(self.program.screen, (0, 0, 0), rect, 1)

        player_rect = self.program.camera.update_rect(self.program.player.rect)
        if rect.collidepoint(player_rect.midbottom):
            pygame.draw.rect(self.program.screen, (255, 0, 0), rect, 2)
