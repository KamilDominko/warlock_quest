import pygame


class Camera(pygame.sprite.Group):
    """Klasa odpowiadająca za to, co jest obecnie widocznie na ekranie."""

    def __init__(self, program):
        super().__init__()
        self.settings = program.settings
        self.screen = program.screen
        self.player = program.player
        self.x = 0
        self.y = 0
        self.offset = pygame.math.Vector2()

    def update(self):
        self.offset.x = self.player.rect.centerx - self.screen.get_width() // 2
        self.offset.y = self.player.rect.centery - self.screen.get_height() // 2

    def camera_draw(self, image, topleft):
        _offset = topleft - self.offset
        self.screen.blit(image, _offset)

    def update_rect(self, rect: pygame.Rect):
        topleft = rect.topleft - self.offset
        rect = pygame.Rect((topleft), (rect.w, rect.h))
        return rect

    def update_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        adjusted_mouse_x = mouse_x + self.offset[0]
        adjusted_mouse_y = mouse_y + self.offset[1]
        return adjusted_mouse_x, adjusted_mouse_y

    # def updated_mouse(self):
    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     mouse_x -= self.offset[0]
    #     mouse_y -= self.offset[1]
    #     return mouse_x, mouse_y
