import pygame


class Interface:
    pygame.font.init()

    def __init__(self, program):
        self.program = program
        self.image = pygame.image.load(
            "res/graphic/interface/player_interface3.png")
        x = program.screen.get_width() // 2
        y = program.screen.get_height()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.font = pygame.font.Font("res/font/Pixeltype.ttf", 35)
        self.color = program.settings.BLACK

    def update(self):
        pass

    def _draw_player_hp(self):
        player = self.program.player
        playerMaxHp = player.maxHealth
        playerCurrentHp = player.currentHealth
        perCent = playerCurrentHp / playerMaxHp
        rect = pygame.Rect((0, 0), (240 * perCent, 28))
        rect.x = self.rect.x + 144
        rect.y = self.rect.y + 18
        pygame.draw.rect(self.program.screen, (150, 0, 0), rect)

        text = self.font.render(f"{playerCurrentHp} / {playerMaxHp}", True,
                                self.color)
        textRect = text.get_rect(centerx=rect.centerx, centery=rect.centery)
        self.program.screen.blit(text, textRect)

    def _draw_player_mana(self):
        player = self.program.player
        playerMaxMana = player.maxMana
        playerCurrentMana = player.currentMana
        perCent = playerCurrentMana / playerMaxMana
        rect = pygame.Rect((0, 0), (240 * perCent, 28))
        rect.x = self.rect.x + 144
        rect.y = self.rect.y + 18 + 1 * 4 + rect.h
        pygame.draw.rect(self.program.screen, (0, 255, 255), rect)

        text = self.font.render(f"{playerCurrentMana} / {playerMaxMana}", True,
                                self.color)
        textRect = text.get_rect(centerx=rect.centerx, centery=rect.centery)
        self.program.screen.blit(text, textRect)

    def _draw_player_stamina(self):
        player = self.program.player
        playerMaxStamina = player.maxStamina
        playerCurrentStamina = player.currentStamina
        perCent = playerCurrentStamina / playerMaxStamina
        rect = pygame.Rect((0, 0), (240 * perCent, 28))
        rect.x = self.rect.x + 144
        rect.y = self.rect.y + 18 + 2 * (4 + rect.h)
        pygame.draw.rect(self.program.screen, (200, 150, 40), rect)

        text = self.font.render(f"{playerCurrentStamina} / {playerMaxStamina}", True,
                                self.color)
        textRect = text.get_rect(centerx=rect.centerx, centery=rect.centery)
        self.program.screen.blit(text, textRect)

    def display(self):
        self.program.screen.blit(self.image, self.rect)
        self._draw_player_hp()
        self._draw_player_mana()
        self._draw_player_stamina()
