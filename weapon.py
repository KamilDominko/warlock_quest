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
        self.image = pygame.transform.scale(self._image, (16, 64))
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
        # if self._projectiles:
        #     for projectile in self._projectiles:
        #         projectile.update()
        self._rotate_image()
        x = player_center[0]
        y = player_center[1]
        x = self.player.rect.centerx
        y = self.player.rect.centery
        self.rect = self.image.get_rect(center=(x, y))
        # print(self.rect)

    def display(self):
        for projectile in self.projectiles:
            projectile.display()
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)
        # self.projectiles.draw(self.program.screen)
        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_line()

    # def shoot(self):
    #     cx = self.rect.center[0]
    #     cy = self.rect.center[1]
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     xdyst = mouse_x - cx
    #     ydyst = mouse_y - cy
    #     cdyst = math.sqrt(xdyst ** 2 + ydyst ** 2)
    #     projectile = Projectile(self.program, self.rect.center[0],
    #                             self.rect.center[1],
    #                             self.angle, self.speed)
    #     self.projectiles.add(projectile)
    #     self._projectiles.append(projectile)

    def shoot(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Przelicz pozycję myszy na przestrzeń gry
        adjusted_mouse_x = mouse_x + self.program.camera.offset[0]
        adjusted_mouse_y = mouse_y + self.program.camera.offset[1]
        # Oblicz kierunek od broni do pozycji myszy
        direction_x = adjusted_mouse_x - self.rect.centerx
        direction_y = adjusted_mouse_y - self.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)
        if distance != 0:
            direction_x /= distance
            direction_y /= distance
        # Utwórz pocisk na czubku broni, przesuwając go w kierunku kursora
        projectile = Projectile(self.program,
                                self.rect.centerx + direction_x * 64,
                                self.rect.centery + direction_y * 64,
                                self.angle, self.speed, self)
        self.projectiles.add(projectile)
