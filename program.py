import pygame

from settings import Settings
from map import Map
from player import Player
from camera import Camera
from enemy import Enemy


class Program:
    def __init__(self):
        self.isRunning = True
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.get_res()))
        pygame.display.set_caption(self.settings.title)
        icon = pygame.image.load("res/graphic/icon/icon64.png")
        pygame.display.set_icon(icon)
        self.map = Map(self)
        self.player = Player(self)
        self.camera = Camera(self)
        self.camera.add(self.player)
        self.clock = pygame.time.Clock()
        self.enemies = pygame.sprite.Group()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                # DEV spawnuje wroga w miejscach myszki
                if event.key == pygame.K_KP1:
                    x, y = self.camera.give_mouse()
                    for i in range(1):
                        self.camera.add(Enemy(self, x, y))

            self.player.input(event)

    def _update_entities(self):
        # self.player.update()
        self.camera.update()
        self.camera.update_offset()

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.map.display()
        # self.player.display()
        # for enemy in self.enemies:
        #     enemy.display()
        self.camera.draw_y_sorted()
        pygame.display.update()

    def run(self):
        while self.isRunning:
            self._check_events()
            self._update_entities()
            self._update_screen()
            self.clock.tick(self.settings.fps)
        pygame.quit()


Program().run()
