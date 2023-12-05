import pygame
import math
import random

from weapon_interface import WeaponInterface


class NewProjectile(WeaponInterface):
    WEAPON_ID = "PROJECTILE"

    def __init__(self, player):
        super().__init__(player)
        self.group = pygame.sprite.Group()
        self.stats = self._load_stats(self.WEAPON_ID)

    def _set_dx_dy(self):
        self._rect = pygame.Rect((self.program.camera.update_mouse()), (1, 1))
        _angle = math.atan2(
            self._rect.y - self.weapon.rect.centery,
            self._rect.x - self.weapon.rect.centerx)
        dx = math.cos(_angle) * self.stats["speed"]
        dy = math.sin(_angle) * self.stats["speed"]
        return dx, dy

    def _set_x_y(self):
        mouseX = self.program.camera.update_mouse()[0]
        mouseY = self.program.camera.update_mouse()[1]
        direction_x = mouseX - self.weapon.rect.centerx
        direction_y = mouseY - self.weapon.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        x = self.weapon.rect.centerx + direction_x * self.weaponOffset
        y = self.weapon.rect.centery + direction_y * self.weaponOffset
        return x, y

    def _create_bullet(self):
        x, y = self._set_x_y()
        dx, dy = self._set_dx_dy()
        image = self.tM["projectiles"]["projectile"]
        bullet = Bullet(self.stats, self.weaponAngle, image, x, y, dx, dy)
        self.group.add(bullet)

    def use(self):
        self._create_bullet()

    def update(self):
        if self.group:
            self.group.update(self.program.enemies,
                              self.program.map.width, self.program.map.height)

    def display(self):
        if self.group:
            for bullet in self.group:
                bullet.display(self.program.camera, self.program.screen)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, stats, weapon_angle, image, x, y, dx, dy):
        super().__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = pygame.transform.rotate(image, weapon_angle - 90)
        self.rect = self.image.get_rect(x=y, y=y)
        self.damage = stats["damage"]
        self.maxHits = stats["piercing"]
        self.hits = []

    def _check_borders(self, map_width, map_height):
        """Jeżeli pocisk wyleci poza mapę, zniszcz go."""
        if self.rect.left > map_width:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > map_height:
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

    def update(self, enemies, map_width, map_height):
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self._enemy_collision(enemies)
        self._check_borders(map_width, map_height)

    def display(self, camera, screen):
        rect = camera.update_rect(self.rect)
        screen.blit(self.image, rect)
