import pygame


class XpOrb(pygame.sprite.Sprite):
    def __init__(self, program, x, y):
        super().__init__()
        self.program = program
        self.image = pygame.image.load(
            "res/graphic/items/xp-orb.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (24,24))
        # TODO Wgrać XpOrb'a do TextureManager'a.
        self.rect = self.image.get_rect(center=(x, y))
        self.feet = self.rect
        self.sucked = False
        self.suckTime = 0
        self.speed = 10
        self.value = 1

    def suck(self):
        self.sucked = True
        self.suckTime = pygame.time.get_ticks()

    def update(self):
        if self.sucked:
            if pygame.time.get_ticks() - self.suckTime > 100:
                playerRect = self.program.player.feet
                self.move_towards(playerRect)
                self._pick_up()
            else:
                playerRect = self.program.player.feet
                speed = 15
                self.move_opposite(playerRect, speed)
        # self.display()

    def display(self):
        self.program.camera.camera_draw(self.image, self.rect.topleft)

    def _pick_up(self):
        player = self.program.player
        if self.rect.colliderect(player.feet):
            player.add_xp(self.value)
            self.kill()

    def move_towards(self, target):
        # Oblicz wektor kierunku od obecnego położenia do położenia celu
        direction = pygame.Vector2(target.center[0] - self.rect.center[0],
                                   target.center[1] - self.rect.center[1])
        # Jeśli długość wektora jest większa niż 0, znormalizuj go
        if direction.length() > 0:
            direction.normalize_ip()
        # Przesuń rect w kierunku gracza
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def move_opposite(self, target, speed):
        # Oblicz wektor kierunku od obecnego położenia do położenia celu
        direction = pygame.Vector2(target.center[0] - self.rect.center[0],
                                   target.center[1] - self.rect.center[1])
        # Jeśli długość wektora jest większa niż 0, znormalizuj go
        if direction.length() > 0:
            direction.normalize_ip()
        # Przesuń rect w kierunku przeciwnym do gracza
        self.rect.x -= direction.x * speed
        self.rect.y -= direction.y * speed
