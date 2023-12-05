import pygame
import math
import random

from weapon_interface import WeaponInterface


class DefaultProjectile(WeaponInterface):
    WEAPON_ID = "PROJECTILE"

    def __init__(self, player):
        super().__init__(player)
        self.group = pygame.sprite.Group()
        self.stats = self._load_stats(self.WEAPON_ID)
        self.reload = 0

        self.image = self.tM["projectiles"]["projectile"]
        self.mapDimensions = self._get_map_dimensions()

    def _set_dx_dy(self):
        """Funkcja zwraca wartość prędkości????"""
        _weaponCenter = self.weaponImg.rect.center
        mosX, mosY = self.program.camera.update_mouse()
        _angle = math.atan2(mosY - _weaponCenter[1],
                            mosX - _weaponCenter[0])
        dx = math.cos(_angle) * self.stats["speed"]
        dy = math.sin(_angle) * self.stats["speed"]
        return dx, dy

    # def _set_x_y(self):
    #     """Funkcja zwraca punkt czubka obrazka broni gracza."""
    #     mouseX = self.program.camera.update_mouse()[0]
    #     mouseY = self.program.camera.update_mouse()[1]
    #     # Oblicz dystans x i y między środkiem obrazka broni a myszką
    #     direction_x = mouseX - self.weaponImg.rect.centerx
    #     direction_y = mouseY - self.weaponImg.rect.centery
    #     # Oblicz dystans linii prostej między środkiem obrazka broni a myszką
    #     distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
    #     if distance != 0:
    #         direction_x /= distance
    #         direction_y /= distance
    #     # Do środka obrazka broni dodaj wektor kierunku pomnożony o offset broni
    #     x = self.weaponImg.rect.centerx + direction_x * self.weaponImgOffset
    #     y = self.weaponImg.rect.centery + direction_y * self.weaponImgOffset
    #     return x, y

    def _get_map_dimensions(self):
        mapW = self.program.map.width
        mapH = self.program.map.height
        return mapW, mapH

    def _create_projectile(self):
        image = pygame.transform.rotate(self.image, self.weaponImg.angle - 90)
        x, y = self._set_x_y(width=self.weaponImgOffset)
        dx, dy = self._set_dx_dy()
        projectile = Projectile(self.stats, image, x, y, dx, dy)
        self.group.add(projectile)

    def use(self):
        if self.reload == 0:
            self.reload = pygame.time.get_ticks()
            self._create_projectile()
            self.aM.play("shoot", 1)
        if pygame.time.get_ticks() - self.reload \
                > 1000 // self.stats["attack_speed"]:
            self.reload = pygame.time.get_ticks()
            self._create_projectile()
            self.aM.play("shoot", 1)

    def update(self):
        if self.group:
            self.group.update(self.program.enemies, self.mapDimensions)

    def display(self):
        if self.group:
            for bullet in self.group:
                bullet.display(self.program.camera, self.program.screen)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, stats, image, x, y, dx, dy):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = image
        self.rect = self.image.get_rect(x=y, y=y)
        self.damage = random.choice(stats["damage"])
        self.maxHits = stats["piercing"]
        self.hits = []
        # print(f"NOWY DX:{self.dx} DY:{self.dy}")

    def _check_borders(self, map_width_height):
        """Jeżeli pocisk wyleci poza mapę, zniszcz go."""
        if self.rect.left > map_width_height[0]:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > map_width_height[1]:
            self.kill()

    def _enemy_collision(self, enemies):
        for enemy in enemies:
            # Jeżeli rect pocisku dotyka hitbox wroga
            if self.rect.colliderect(enemy.hitbox) and \
                    enemy not in self.hits and not enemy.hited:
                self.hits.append(enemy)
                enemy.deal_damage(self.damage)
                if len(self.hits) == self.maxHits:
                    self.kill()
                break

    def update(self, enemies, map_width_height):
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self._enemy_collision(enemies)
        self._check_borders(map_width_height)

    def display(self, camera, screen):
        rect = camera.update_rect(self.rect)
        screen.blit(self.image, rect)
