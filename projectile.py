import pygame
import math


class Projectile(pygame.sprite.Sprite):
    image = pygame.image.load(
        "res/graphic/projectiles/projectile.png")

    def __init__(self, weapon):
        super().__init__()
        self.program = weapon.program
        self.image = Projectile.image.convert_alpha()
        self.image = pygame.transform.rotate(Projectile.image.convert_alpha(),
                                             weapon.angle - 90)
        self.rect = self.image.get_rect(center=(weapon.rect.centerx,
                                                weapon.rect.centery))
        self.speed = weapon.stats["speed"]
        self.damage = weapon.stats["damage"]
        self.hits = weapon.stats["piercing"]
        self.hited = []

        self.x, self.y = self._adjusted_x_y(
            self.program.camera.update_mouse()[0],
            self.program.camera.update_mouse()[1], weapon)

        self._rect = pygame.Rect((self.program.camera.update_mouse()), (1, 1))
        _angle = math.atan2(self._rect.y - weapon.rect.centery,
                            self._rect.x - weapon.rect.centerx)
        self.dx = math.cos(_angle) * self.speed
        self.dy = math.sin(_angle) * self.speed

    def _adjusted_x_y(self, adjusted_mouse_x, adjusted_mouse_y, weapon):
        direction_x = adjusted_mouse_x - weapon.rect.centerx
        direction_y = adjusted_mouse_y - weapon.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        x = weapon.rect.centerx + direction_x * 64  # 64 to offset spawnopintu
        y = weapon.rect.centery + direction_y * 64
        return x, y

    def _enemy_collision(self):
        for enemy in self.program.enemies:
            # Jeżeli rect pocisku dotyka hitbox wroga
            if self.rect.colliderect(enemy.hitbox) and \
                    enemy not in self.hited and not enemy.hited:
                self.hited.append(enemy)
                enemy.deal_damage(self.damage)
                # enemy.current_healt -= self.damage
                # enemy.hited = pygame.time.get_ticks()
                # if enemy.current_healt < 0:
                #     enemy.kill()
                if len(self.hited) == self.hits:
                    self.kill()
                break

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self._enemy_collision()
        self._check_borders()

    def _check_borders(self):
        """Jeżeli pocisk wyleci poza mapę, zniszcz go."""
        if self.rect.left > self.program.map.width:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > self.program.map.height:
            self.kill()
        # """Jeżeli pocisk wyleci poza ekran, zniszcz go."""
        # rect = self.program.camera.update_rect(self.rect)
        # if rect.left > self.program.screen.get_width():
        #     self.kill()
        # if rect.right < 0:
        #     self.kill()
        # if rect.bottom < 0:
        #     self.kill()
        # if rect.top > self.program.screen.get_height():
        #     self.kill()

    def display(self):
        # self.program.camera.camera_draw(self.image,self.rect.topleft)
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)

        # DEV
        DEV = 0
        if DEV:
            # left-top pocisku
            pygame.draw.rect(self.program.screen, (0, 200, 0),
                             (rect.x, rect.y, 11, 11))
            # rect pocisku
            pygame.draw.rect(self.program.screen, (255, 0, 0), rect, 2)
            # środek pocisku
            pygame.draw.circle(self.program.screen, (0, 255, 0), rect.center, 5)
            rect2 = self.program.camera.update_rect(self._rect)
            # punkt w kierunku, którym przemieszcza się pocisku
            pygame.draw.circle(self.program.screen, (0, 255, 0),
                               (rect2.x, rect2.y),
                               5)
