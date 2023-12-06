import pygame
import math
import json


class EnemyInterface(pygame.sprite.Sprite):
    ENEMY_ID = "interface"

    FEET_WIDTH = 0
    FEET_HEIGHT = 0
    HITBOX_WIDTH = 0
    HITBOX_HEIGHT = 0

    def __init__(self, program):
        super().__init__()
        self.program = program
        self.tM = program.textureManager.textures
        self.aM = program.audioManager
        self.stats = self._load_stats(self.ENEMY_ID)
        self._stateUp = 0
        self._stateDown = 0
        self._stateLeft = 0
        self._stateRight = 0
        self.animationIndex = 0
        self.selected = False
        self.hited = False
        self.reload = 0
        self.currentHealth = self.stats["health"]
        self.obstacles = program.map.obstacles
        program.map.obstacles.add(self)

    def _json_load(self):
        f = open('enemiesStatistics.json')
        return json.load(f)

    def _load_stats(self, name):
        statistics = self._json_load()
        stats = statistics[name]
        if stats["damage"]:
            minDmg = stats["damage"][0]
            maxDmg = stats["damage"][1]
            stats["damage"] = range(minDmg, maxDmg)
        return stats

    def _attack(self, target):
        pass

    def _move(self):
        pass

    def deal_damage(self, damage):
        pass

    def die(self):
        pass

    def update(self):
        pass

    def display(self):
        pass
