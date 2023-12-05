import pygame
import json


class WeaponInterface(pygame.sprite.Sprite):
    """Klasa-interfejs do wszystkich broni."""

    def __init__(self, player):
        super().__init__()
        self.program = player.program
        self.player = player
        self.weapon = player.weapon
        self.tM = player.program.textureManager.textures
        self.weaponOffset = player.weapon.height // 2
        self.weaponAngle = player.weapon.angle

        self.stats = {}

    def _json_load(self):
        f = open('weaponStatistics.json')
        return json.load(f)

    def _load_stats(self, name):
        statistics = self._json_load()
        stats = statistics[name]
        return stats

    def _enemy_collision(self):
        pass

    def update(self):
        pass

    def display(self):
        pass

    def use(self):
        pass
