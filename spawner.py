import pygame

import random

from enemy import Enemy


class Spawner:
    def __init__(self, program):
        self.program = program
        self.offspace = 150
        self.offset = 100
        self.scrW = program.screen.get_width()
        self.scrH = program.screen.get_height()
        self.spawnStart = pygame.time.get_ticks()
        self.spawnTime = 1000

    def _pick_position(self):
        playerFeet = self.program.player.feet.midbottom
        mapW = self.program.map.width
        mapH = self.program.map.height

        mapXrange = range(128, mapW - 128)
        mapYrange = range(128, mapH - 128)
        spawnXrange = range((playerFeet[0] - (self.scrW // 2 + self.offset)),
                            (playerFeet[0] + (self.scrW // 2 + self.offset)))
        spawnYrange = range((playerFeet[1] - (self.scrH // 2 + self.offset)),
                            (playerFeet[1] + (self.scrH // 2 + self.offset)))
        while True:
            spawnX = random.randrange(
                (playerFeet[0] - (self.scrW // 2 + self.offset)),
                (playerFeet[0] + (self.scrW // 2 + self.offset)))
            if spawnX in mapXrange:
                if spawnX in spawnXrange:
                    break
        while True:
            spawnY = random.randrange(
                (playerFeet[1] - (self.scrH // 2 + self.offset)),
                (playerFeet[1] + (self.scrH // 2 + self.offset)))
            if spawnY in mapYrange:
                if spawnY in spawnYrange:
                    break
        return spawnX, spawnY

    def create_enemy(self):
        pos = self._pick_position()
        return pos

    def _update(self):
        if pygame.time.get_ticks() - self.spawnStart >= self.spawnTime and \
                len(self.program.enemies) < 300:
            self.spawnStart = pygame.time.get_ticks()
            self.spawnTime = random.randrange(500, 2001)
            x, y = self._pick_position()
            enemy = Enemy(self.program, x, y)
            self.program.camera.add(enemy)
            self.program.enemies.add(enemy)

    def update(self):
        # self._update()
        pass