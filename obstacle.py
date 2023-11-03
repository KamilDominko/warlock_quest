import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self._image = image
        self.image = self._image
        self.rect = self.image.get_rect(topleft=(x * 128, y * 128))


    def _draw_rect(self, screen, camera):
        rect = camera.update_rect(self.rect)
        pygame.draw.rect(screen, (255, 0, 0), rect, 3)

    def display(self, screen, camera):
        # screen.blit(self.image, self.rect)
        camera.camera_draw(self.image, self.rect.topleft)

        DEV = 1
        if DEV:
            self._draw_rect(screen, camera)
