import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, program, x, y, image):
        super().__init__()
        self.program = program
        self.x = x
        self.y = y
        self._image = image
        self.image = self._image
        _x = self.image.get_width()
        _y = self.image.get_height()
        self.rect = self.image.get_rect(topleft=(x * _x, y * _y))
        self.feet = self.rect

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (255, 0, 0), rect, 3)

    def update(self):
        self.display()

    def display(self):
        self.program.camera.camera_draw(self.image, self.rect.topleft)

        DEV = 0
        if DEV:
            self._draw_rect()
