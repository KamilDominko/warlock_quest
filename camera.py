import pygame


class Camera(pygame.sprite.Group):
    """Klasa odpowiadająca za to, co jest obecnie widocznie na ekranie."""

    def __init__(self, program):
        super().__init__()
        self.program = program
        self.screen = program.screen
        # self.player = program.player
        self.screenHalfWidth = program.screen.get_width() // 2
        self.screenHalfHeight = program.screen.get_height() // 2
        self.x = 0
        self.y = 0
        self.offset = pygame.math.Vector2()

    def draw_y_sorted(self):
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.feet.centery):
            sprite.display()

    def update_offset(self):
        """Funkcja aktualizuje wartość przesunięcia kamery, która mówi jak
        bardzo wszystko ma być przesunięte podczas wyświetlania na ekranie,
        aby gracz był ciągle na środku ekranu."""
        self.offset.x = self.program.player.rect.centerx - \
                        self.screenHalfWidth
        self.offset.y = self.program.player.rect.centery - \
                        self.screenHalfHeight

    def camera_draw(self, image, topleft):
        _offset = topleft - self.offset
        self.screen.blit(image, _offset)

    def update_rect(self, rect: pygame.Rect):
        topleft = rect.topleft - self.offset
        rect = pygame.Rect((topleft), (rect.w, rect.h))
        return rect

    def update_point(self, point):
        return point - self.offset

    def give_mouse(self):
        x, y = pygame.mouse.get_pos()
        x += self.offset[0]
        y += self.offset[1]
        return x, y

    def update_mouse(self):
        """Funkcja pobiera aktualną pozycję myszki, dodaje do niej offset i
        zwraca dwie wartości x i y. Dzięki temu pozycja myszki jest względem
        gracza a nue względem okna."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        adjusted_mouse_x = mouse_x + self.offset[0]
        adjusted_mouse_y = mouse_y + self.offset[1]
        return adjusted_mouse_x, adjusted_mouse_y
