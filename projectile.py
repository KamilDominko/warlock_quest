import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, program, centerx, centery, anglee, speed):
        super().__init__()
        self.program = program
        self._image = pygame.image.load(
            "res/graphic/projectiles/projectile.png")
        self._image = pygame.transform.scale(self._image, (32,32))
        self.image = self._image
        self.x = centerx
        self.y = centery

        self.speed = speed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = mouse_x + program.camera.offset[0]
        y = mouse_y + program.camera.offset[1]
        self._rect = pygame.Rect((x, y), (1, 1))
        angle = math.atan2(self._rect.y - self.y, self._rect.x - self.x)
        self.image = pygame.transform.rotate(self._image, anglee - 90)
        # self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.direction_x = mouse_x - self.x
        self.direction_y = mouse_y - self.y
        distance = math.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        if distance != 0:
            self.direction_x /= distance
            self.direction_y /= distance

    def update(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        self._check_borders()

    def _check_borders(self):
        rect = self.program.camera.update_rect(self.rect)
        if rect.left > self.program.screen.get_width():
            self.kill()
        if rect.right < 0:
            self.kill()
        if rect.bottom < 0:
            self.kill()
        if rect.top > self.program.screen.get_height():
            self.kill()

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