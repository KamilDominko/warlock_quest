import pygame
import math
import random

from weapon_interface import WeaponInterface


class MagicLaser(WeaponInterface):
    WEAPON_ID = "LASER"

    def __init__(self, player):
        super().__init__(player)
        self.group = pygame.sprite.Group()
        self.casting = False
        self.drainTime = 0
        self.reload = 0
        self.hits = []

        self.animationIndex = 0

        self._image = self.tM["lasers"]["laser"][0]
        self.imgH = self._image.get_rect().h

    def _animation_state(self, state, animation):
        if state:
            self.animationIndex += 0.45
            if self.animationIndex >= len(animation):
                self.animationIndex = 0
            self._image = animation[int(self.animationIndex)]

    def _weapon_tip(self):
        # TODO da się zrefaktoryzować z metodą _set_x_y() default_projectile'a
        mouseX = self.program.camera.update_mouse()[0]
        mouseY = self.program.camera.update_mouse()[1]
        direction_x = mouseX - self.weaponImg.rect.centerx
        direction_y = mouseY - self.weaponImg.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        width = self.weaponImg.stats["laser_range"] * \
                self.program.settings.scaleX
        x = self.weaponImg.rect.centerx + direction_x * (
                width / 2 + self.weaponImgOffset)
        y = self.weaponImg.rect.centery + direction_y * (
                width / 2 + self.weaponImgOffset)
        return x, y

    def _drain_mana(self):
        if pygame.time.get_ticks() - self.drainTime > 100:
            self.player.currentMana -= self.stats["cost"]
            self.drainTime = pygame.time.get_ticks()

    def _enemy_collision(self):
        for enemy in self.program.enemies:
            # p1, p2 - punkty linii
            p1 = self.weaponImg.rect.center
            p2 = self._set_x_y(self.stats["range"]+self.weaponImgOffset)
            pygame.draw.line(self.program.screen, (255, 0, 0), p1, p2)
            if enemy.hitbox.clipline(p1, p2) and not enemy.hited \
                    and enemy not in self.hits:
                self.hits.append(enemy)
                damage = random.choice(self.stats["damage"])
                enemy.deal_damage(damage)

    def _prepare_laser(self):
        """Funkcja przygotowuje obrazek lasera do wyświetlenia."""
        # Zmień rozmiar wartość width lasera na wartość statystyki
        self._image = pygame.transform.scale(self._image, (
            self.stats["range"] * self.program.settings.scaleX,
            self.imgH))
        # Obróć laser w stronę kursora
        self.image = pygame.transform.rotate(self._image, self.weaponImg.angle)
        # Weź nowy rect
        self.rect = self.image.get_rect()
        # Weź pozycję szubka broni gracza + offset + 1/2 długość lasera
        width = self.weaponImgOffset + (self.stats["range"] // 2)
        self.x, self.y = self._set_x_y(width)
        # Ustal ten punkt jako środek lasera
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        if self.casting:
            if self.player.currentMana > self.stats["cost"]:
                self.aM.play("laser", 2)
                self._animation_state(self.casting, self.tM["lasers"]["laser"])
                self._drain_mana()
                self._enemy_collision()
                if self.reload == 0:
                    self.reload = pygame.time.get_ticks()
                    self.hits.clear()
                if pygame.time.get_ticks() - self.reload \
                        > 1000 // self.stats["attack_speed"]:
                    self.reload = pygame.time.get_ticks()
                    self.hits.clear()
            else:
                self.aM.stop(2)
                self.casting = False

    def _draw_line(self):
        p1 = self.weaponImg.rect.center
        p2 = self._set_x_y(self.stats["range"]+self.weaponImgOffset)
        p1 = self.program.camera.update_point(p1)
        p2 = self.program.camera.update_point(p2)
        pygame.draw.line(self.program.screen, (255, 255, 0), p1, p2, 10)

    def display(self):
        if self.casting:
            self._prepare_laser()
            rect = self.program.camera.update_rect(self.rect)
            self.program.screen.blit(self.image, rect)

        # self._draw_line()

    def use(self):
        self.casting = True
