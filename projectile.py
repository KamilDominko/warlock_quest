import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, camera, centerx, centery, anglee, speed):
        super().__init__()
        self._image = pygame.image.load(
            "res/graphic/projectiles/projectile.png")
        self._image = pygame.transform.scale(self._image, (64, 64))
        self.image = self._image
        self.x = centerx
        self.y = centery

        self.speed = 5
        mouse_x, mouse_y = pygame.mouse.get_pos()

        x = mouse_x + camera.offset[0]
        y = mouse_y + camera.offset[1]
        self._rect = pygame.Rect((x, y), (1, 1))
        # self._rect = camera.update_rect(self._rect)
        angle = math.atan2(self._rect.y - self.y, self._rect.x - self.x)
        angle2 = math.atan2(-(mouse_y - self.y), mouse_x - self.x)
        degre = math.degrees(angle2)
        print(mouse_x, mouse_y)
        self.image = pygame.transform.rotate(self._image, anglee - 90)
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

        print(self._rect)

        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def display(self, screen, camera):
        # screen.blit(self.image, self.rect)
        rect = camera.update_rect(self.rect)
        screen.blit(self.image, rect)
        # camera.camera_draw(self.image,self.rect.topleft)

        # DEV
        pygame.draw.rect(screen, (0, 200, 0),
                         (rect.x, rect.y, 11, 11))
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
        pygame.draw.circle(screen, (0, 255, 0), rect.center, 5)
        rect2 = camera.update_rect(self._rect)
        pygame.draw.circle(screen, (0, 255, 0), (rect2.x, rect2.y), 5)
