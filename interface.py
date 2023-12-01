import pygame


class Interface:
    pygame.font.init()

    def __init__(self, program):
        self.program = program
        self.player = program.player
        self.image = pygame.image.load(
            "res/graphic/interface/player_interface3.png")
        x = program.screen.get_width() // 2
        y = program.screen.get_height()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.font = pygame.font.Font("res/font/Pixeltype.ttf", 35)
        self.color = program.settings.BLACK

    def update(self):
        pass

    def _draw_exp_bar(self, full=0):
        rect = pygame.Rect((0, 0), (self.program.settings.get_res()[0], 28))
        pygame.draw.rect(self.program.screen, (55, 71, 79), rect)
        perCent = self.player.experience / (self.player.level * 10)
        if full:
            rect.w = self.program.settings.get_res()[0]
        if not full:
            rect.w = self.program.settings.get_res()[0] * perCent
        pygame.draw.rect(self.program.screen, (0, 150, 200), rect)

        # text = self.font.render(
        #     f"LVL: {self.player.level}   EXP: {self.player.experience}/"
        #     f"{self.player.level * 10}", True, self.color)
        text = self.font.render(
            f"LVL : {self.player.level}", True, self.color)
        rect.w = self.program.settings.get_res()[0]
        textRect = text.get_rect(centerx=rect.centerx, centery=rect.centery)
        self.program.screen.blit(text, textRect)

    def _draw_bar(self, color, index, maxStat, currentStat):
        perCent = currentStat / maxStat
        rect = pygame.Rect((self.rect.x + 144, 0),
                           (240 * perCent, 28))
        rect.y = self.rect.y + 18 + index * (4 + rect.h)
        pygame.draw.rect(self.program.screen, color, rect)

        rect.w = 240
        text = self.font.render(f"{int(currentStat)} / {int(maxStat)}", True,
                                self.color)
        textRect = text.get_rect(centerx=rect.centerx, centery=rect.centery)
        self.program.screen.blit(text, textRect)

    def _draw_player_hp(self):
        self._draw_bar((150, 0, 0), 0, self.player.stats["health"],
                       self.player.currentHealth)

    def _draw_player_mana(self):
        self._draw_bar((0, 255, 255), 1, self.player.stats["mana"],
                       self.player.currentMana)

    def _draw_player_stamina(self):
        self._draw_bar((200, 150, 40), 2, self.player.stats["stamina"],
                       self.player.currentStamina)

    def display(self):
        self.program.screen.blit(self.image, self.rect)
        self._draw_player_hp()
        self._draw_player_mana()
        self._draw_player_stamina()

        self._draw_exp_bar()
