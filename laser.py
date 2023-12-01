import pygame
import math


class Laser:
    def __init__(self, program, weapon):
        self.program = program
        self.weapon = weapon
        self.offset = weapon.height // 2
        self.weaponOffset = weapon.height // 2
        self.tM = program.textureMenager.textures
        self._image = self.tM["lasers"]["laser"][0]
        self.imgH = self._image.get_rect().h
        self.imgW = self._image.get_rect().w
        self.width = 600
        self.image = pygame.transform.rotate(self._image, weapon.angle)
        self.rect = self.image.get_rect(center=(weapon.rect.centerx,
                                                weapon.rect.centery))
        self.damage = weapon.stats["damage"]
        self.hits = weapon.stats["piercing"]
        self.hited = []
        self.animationIndex = 0
        self.casting = 0
        self.reload = 0

    def _check_animation_state(self, state, animation):
        if state:
            self.animationIndex += 0.35
            if self.animationIndex >= len(animation):
                self.animationIndex = 0
            self._image = animation[int(self.animationIndex)]

    def _weapon_tip(self):
        direction_x = self.program.camera.update_mouse()[
                          0] - self.weapon.rect.centerx
        direction_y = self.program.camera.update_mouse()[
                          1] - self.weapon.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        width = self.width * self.program.settings.scaleX
        x = self.weapon.rect.centerx + direction_x * (
                width / 2 + self.weaponOffset)
        y = self.weapon.rect.centery + direction_y * (
                width / 2 + self.weaponOffset)
        return x, y

    def _draw_line(self):
        p1, p2 = self._create_line()
        p1 = self.program.camera.update_point(p1)
        p2 = self.program.camera.update_point(p2)
        pygame.draw.line(self.program.screen, (0, 255, 0), p1, p2, 10)

    def _create_line(self):
        """Tworzy linię od centrum broni linię ma określoną długoś w kierunku
        kursora. Linie są na rzeczywistych współrzędnych, nierysowanych! """
        direction_x = self.program.camera.update_mouse()[
                          0] - self.weapon.rect.centerx
        direction_y = self.program.camera.update_mouse()[
                          1] - self.weapon.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        width = (self.width + self.weaponOffset) * self.program.settings.scaleX
        x = self.weapon.rect.centerx + direction_x * width
        y = self.weapon.rect.centery + direction_y * width

        start = self.weapon.rect.center
        end = (x, y)

        return start, end

    def _enemy_collision(self):
        for enemy in self.program.enemies:
            # Jeżeli linia przechodzi przez hitbox wroga
            p1, p2 = self._create_line()
            if enemy.hitbox.clipline(p1, p2) and not enemy.hited:
                enemy.deal_damage(20)

    def display(self):
        self._prepare_laser()
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)

        DEV = 0
        if DEV:
            self._draw_line()

    def _prepare_laser(self):
        # Zmień rozmiar wartość width lasera na wartość statystyki
        self._image = pygame.transform.scale(self._image, (
            self.width * self.program.settings.scaleX, self.imgH))
        # Obróć laser w stronę kursora
        self.image = pygame.transform.rotate(self._image, self.weapon.angle)
        # Weź nowy rect
        self.rect = self.image.get_rect()
        # Weź pozycję szubka broni gracza + offset + 1/2 długość lasera
        self.x, self.y = self._weapon_tip()
        # Dodaj je do siebie
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def update(self):
        # self._image = pygame.transform.scale(self._image, (self.width,
        #                                                    self.imgH))
        # self.image = pygame.transform.rotate(self._image, self.weapon.angle)
        # self.rect = self.image.get_rect()
        # self.x, self.y = self._weapon_tip()
        # self.rect.centerx = int(self.x)
        # self.rect.centery = int(self.y)
        self._check_animation_state(self.casting, self.tM["lasers"]["laser"])
        # self._prepare_laser()

        # if self.animationIndex >= len(self.tM["lasers"]["laser"]) - 1:
        #     self._enemy_collision()
        #     self.animationIndex = 0

        if self.reload == 0:
            self.reload = pygame.time.get_ticks()
            self._enemy_collision()
        if pygame.time.get_ticks() - self.reload \
                > 1000 // 4.0:
            self.reload = pygame.time.get_ticks()
            self._enemy_collision()
