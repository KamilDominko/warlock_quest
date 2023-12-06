import pygame
import math
import json


class WeaponInterface(pygame.sprite.Sprite):
    """Klasa-interfejs do wszystkich broni."""
    WEAPON_ID = "INTERFACE"

    def __init__(self, player):
        super().__init__()
        self.program = player.program
        self.player = player
        self.weaponImg = player.weaponImg
        self.tM = player.program.textureManager.textures
        self.aM = player.program.audioManager
        self.weaponImgOffset = player.weaponImg.height // 2

        self.stats = self._load_stats(self.WEAPON_ID)

    def _set_x_y(self, width=0):
        """Funkcja dodaje do punktu środka broni wektor w stronę myszki
        pomnożony przez podaną długość."""
        mouseX = self.program.camera.update_mouse()[0]
        mouseY = self.program.camera.update_mouse()[1]
        # Oblicz dystans x i y między środkiem obrazka broni a myszką
        direction_x = mouseX - self.weaponImg.rect.centerx
        direction_y = mouseY - self.weaponImg.rect.centery
        # Oblicz dystans linii prostej między środkiem obrazka broni a myszką
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        # Do środka obrazka broni dodaj wektor kierunku pomnożony o offset broni
        x = self.weaponImg.rect.centerx + direction_x * width
        y = self.weaponImg.rect.centery + direction_y * width
        return x, y

    def _json_load(self):
        f = open('src/data/weaponStatistics.json')
        return json.load(f)

    def _load_stats(self, name):
        statistics = self._json_load()
        stats = statistics[name]
        if stats["damage"]:
            minDmg = stats["damage"][0]
            maxDmg = stats["damage"][1]
            stats["damage"] = range(minDmg, maxDmg)
        return stats

    def _enemy_collision(self):
        pass

    def update(self):
        pass

    def display(self):
        pass

    def use(self):
        pass
