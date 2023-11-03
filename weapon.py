import pygame
import math

from projectile import Projectile


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, program):
        super().__init__()
        self.program = program
        self.player = player
        self._image = pygame.image.load(
            "res/graphic/weapons/wand.png").convert_alpha()
        self.image = self._image
        # self.image = pygame.transform.scale(self._image, (16, 64))
        self.rect = self.image.get_rect()
        self.speed = self.program.settings.projectile_speed
        self.projectiles = pygame.sprite.Group()
        self._projectiles = []
        self.angle = 0

    def _draw_line(self):
        rect = self.program.camera.update_rect(self.rect)
        end = pygame.mouse.get_pos()
        pygame.draw.line(self.program.screen, (255, 0, 0), rect.center, end)

    def _draw_rect(self):
        # rect = self.program.camera.update_rect(self.rect)
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _rotate_image(self):
        rect = self.program.camera.update_rect(self.player.rect)
        self.angle = self._give_angle(rect.center)
        img = pygame.transform.scale(self._image, (32, 128))  # SKALUJE
        self.image = pygame.transform.rotate(img, self.angle - 90)

    def _give_angle(self, point):
        """Funkcja zwraca wartość kątu w stopniach mierzonego od punktu do
        pozycji myszki w chwili wywołania."""
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - point[0]
        y_dist = pos[1] - point[1]
        angle = math.atan2(y_dist, x_dist)
        angle = math.degrees(angle)
        return -angle

    def update(self, player_center):
        if self.projectiles:
            self.projectiles.update()
        self._rotate_image()
        x = player_center[0]
        y = player_center[1]
        x = self.player.rect.centerx
        y = self.player.rect.centery
        self.rect = self.image.get_rect(center=(x, y))

    def display(self):
        for projectile in self.projectiles:
            projectile.display()
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)
        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_line()

    def shoot(self):
        projectile = Projectile(self)
        self.projectiles.add(projectile)
