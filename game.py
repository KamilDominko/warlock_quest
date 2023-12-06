import pygame

from settings import Settings
from map import Map
from player import Player
from camera import Camera
from enemy import Enemy
from spawner import Spawner
from information import Information
from xp_orb import XpOrb
from interface import Interface
from texture_manager import TextureManager
from audio_manager import AudioManager
from src.enemies.skeleton import Skeleton
from src.enemies.zombie import Zombie

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.isRunning = True
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.get_res()))
        pygame.display.set_caption(self.settings.title)
        icon = pygame.image.load("res/graphic/icon/icon64.png")
        pygame.display.set_icon(icon)
        self.textureManager = TextureManager(self)
        self.audioManager = AudioManager(self)
        self.map = Map(self)
        self.camera = Camera(self)
        self.player = Player(self)
        self.camera.add(self.player)
        self.clock = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks()
        self.enemies = pygame.sprite.Group()
        self.spawner = Spawner(self)
        self.expOrbs = pygame.sprite.Group()
        self.information = Information(self)
        self.showInfo = False
        self.interface = Interface(self)

    def _dev(self, event):
        # Num1 spawnuje wroga w miejscach myszki
        if event.key == pygame.K_KP1:
            x, y = self.camera.give_mouse()
            for i in range(1):
                # enemy = Enemy(self, x, y)
                enemy = Skeleton(self, x, y)
                self.camera.add(enemy)
                self.enemies.add(enemy)
        # Num2 wywołuje spawner, tworzy wroga w losowym miejscu
        if event.key == pygame.K_KP2:
            x, y = self.spawner.create_enemy()
            for i in range(100):
                x, y = self.spawner.create_enemy()
                enemy = Enemy(self, x, y)
                self.camera.add(enemy)
                self.enemies.add(enemy)
        # Num3 zabija wszystkich wrogów
        if event.key == pygame.K_KP3:
            print(len(self.enemies))
            for enemy in self.enemies:
                enemy.kill()
        if event.key == pygame.K_KP4:
            for expOrb in self.expOrbs:
                expOrb.suck()
        if event.key == pygame.K_KP5:
            for enemy in self.enemies:
                enemy.die()
        if event.key == pygame.K_KP6:
            x, y = self.camera.give_mouse()
            for i in range(1):
                enemy = Zombie(self, x, y)
                self.camera.add(enemy)
                self.enemies.add(enemy)
        # Num+ zwiększa szybkostrzelność gracza
        if event.key == pygame.K_KP_PLUS:
            self.player.stats["attack_speed"] += 0.5
        # Num- zmniejsza szybkostrzelność gracza
        if event.key == pygame.K_KP_MINUS:
            self.player.stats["attack_speed"] -= 0.5
        # Num* otwiera statystyki gracza
        if event.key == pygame.K_KP_MULTIPLY:
            self.showInfo = not self.showInfo
        # Num/ pojawia XPorb w miejscu kursora
        if event.key == pygame.K_KP_DIVIDE:
            for i in range(10):
                x, y = self.camera.give_mouse()
                xpOrb = XpOrb(self, x, y)
                self.expOrbs.add(xpOrb)
                # self.camera.add(xpOrb)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isRunning = False
                self._dev(event)

            self.player.input(event)

    def _update_entities(self):
        # self.player.update()
        self.expOrbs.update()
        self.camera.update()
        self.camera.update_offset()

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        self.map.display()
        # self.player.display()
        # for enemy in self.enemies:
        #     enemy.display()
        for xpOrb in self.expOrbs:
            xpOrb.display()
        self.camera.draw_y_sorted()
        if self.showInfo:
            self.information.display_info()
        self.interface.display()
        pygame.display.update()

    def run(self):
        while self.isRunning:
            # pygame.display.set_caption(f"{self.clock.get_fps(): .1f}")
            # self.delta_time = self.clock.tick()
            self._check_events()
            self._update_entities()
            self._update_screen()
            self.spawner.update()
            self.clock.tick(self.settings.fps)
        pygame.quit()


Game().run()
