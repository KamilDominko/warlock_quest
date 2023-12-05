import pygame
import math


class WeaponImage(pygame.sprite.Sprite):
    """Klasa reprezentująca broń gracza. Odpowiada za obracanie obrazka oraz
    umieszczanie go w odpowiednim miejscu."""

    def __init__(self, player, program):
        super().__init__()
        self.program = program
        self.player = player
        self._image = program.textureManager.textures["weapons"]["staff"]
        self.aM = program.audioManager
        self.image = self._image
        self.rect = self.image.get_rect()
        self.height = self.rect.h
        self.angle = 0

    def _give_angle(self, point):
        """Funkcja zwraca wartość kąta w stopniach mierzonego od punktu do
        pozycji myszki w chwili wywołania."""
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - point[0]
        y_dist = pos[1] - point[1]
        angle = math.atan2(y_dist, x_dist)
        angle = math.degrees(angle)
        return -angle

    def _rotate_image(self):
        rect = self.program.camera.update_rect(self.player.rect)
        self.angle = self._give_angle(rect.center)
        self.image = pygame.transform.rotate(self._image, self.angle - 90)

    def update(self, player_center):
        self._rotate_image()
        self.rect = self.image.get_rect(center=self.player.rect.center)

    def display(self):
        rect = self.program.camera.update_rect(self.rect)
        self.program.screen.blit(self.image, rect)
        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_line()

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _draw_line(self):
        rect = self.program.camera.update_rect(self.rect)
        end = pygame.mouse.get_pos()
        pygame.draw.line(self.program.screen, (255, 0, 0), rect.center, end)
