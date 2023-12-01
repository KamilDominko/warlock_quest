import pygame
import math

from projectile import Projectile
from laser import Laser


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, program):
        super().__init__()
        self.program = program
        self.player = player
        self._image = program.textureMenager.textures["weapons"]["staff"]
        # self._image = pygame.image.load(
        #     "res/graphic/weapons/staff.png").convert_alpha()
        self.image = self._image
        self.rect = self.image.get_rect()
        self.height = self.rect.h
        self.projectiles = pygame.sprite.Group()
        self.angle = 0

        self.stats = {"damage": program.settings.projectile_damage,
                      "piercing": program.settings.projectile_hits,
                      "projectile_speed": program.settings.projectile_speed,
                      "attack_speed":program.settings.weapon_attack_speed}
        self.reload = 0
        self.laser = Laser(program, self)

    def _draw_line(self):
        rect = self.program.camera.update_rect(self.rect)
        end = pygame.mouse.get_pos()
        pygame.draw.line(self.program.screen, (255, 0, 0), rect.center, end)

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _rotate_image(self):
        rect = self.program.camera.update_rect(self.player.rect)
        self.angle = self._give_angle(rect.center)
        self.image = pygame.transform.rotate(self._image, self.angle - 90)

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
        if self.laser.casting:
            self.laser.update()
        self._rotate_image()
        x = player_center[0]
        y = player_center[1]
        x = self.player.rect.centerx
        y = self.player.rect.centery
        self.rect = self.image.get_rect(center=(x, y))

    def display(self):
        for projectile in self.projectiles:
            projectile.display()
        if self.laser.casting:
            self.laser.display()
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)
        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_line()

    # def primary_attack(self):
    #     projectile = Projectile(self.program, self)
    #     self.projectiles.add(projectile)

    def primary_attack(self):
        if self.reload == 0:
            self.reload = pygame.time.get_ticks()
            projectile = Projectile(self.program, self)
            self.projectiles.add(projectile)
        if pygame.time.get_ticks() - self.reload \
                > 1000 // self.stats["attack_speed"]:
            self.reload = pygame.time.get_ticks()
            projectile = Projectile(self.program, self)
            self.projectiles.add(projectile)

    def second_attack(self):
        self.laser.casting = True
