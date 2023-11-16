import pygame


class Upgrade:
    pygame.font.init()
    _options = {"attackSpeed": 0.2,
                "damage": 0.5,
                "health": 10,
                "mana": 10,
                "stamina": 10,
                "piercing": 1,
                "projectileSpeed": 1}

    def __init__(self, program):
        self.program = program
        self.screen = program.screen
        self.settings = program.settings
        self.player = program.player
        self.picked = False
        self.optionImage = pygame.image.load(
            "res/graphic/interface/option.png").convert()
        self.image = pygame.image.load(
            "res/graphic/interface/info.png").convert()
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.font = pygame.font.Font("res/font/Pixeltype.ttf", 35)
        self.options = []
        self.click = False

    def update(self):
        for option in self.options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.selected = True
                if self.click:
                    option.add_bonus(self.player)
                    self.picked = True
            else:
                option.selected = False

    def _create_options(self):
        for i in range(3):
            x = self.rect.x + i * self.optionImage.get_width() + 2 * 16 + i * 16
            y = self.rect.y + 5 * 16
            self.options.append(Option("attackSpeed", (x, y)))

    def display(self):
        self.screen.blit(self.image, self.rect)
        for option in self.options:
            option.display(self.screen, self.font)
        pygame.display.update()

    def pick(self):
        self._create_options()
        self.program.interface._draw_exp_bar(full=1)
        while not self.picked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.program.isRunning = False
                    self.picked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.picked = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False

            self.update()
            self.display()


class Option:
    _options = {"attackSpeed": {"name": "Attack Speed",
                                "description": "Increases attack speed.",
                                "value": 0.2},
                "damage": {"name": "Damage",
                           "description": "Increases attack damage..",
                           "value": 1},
                "health": {"name": "Health",
                           "description": "Increases health.",
                           "value": 10},
                "mana": {"name": "Mana",
                         "description": "Increases mana.",
                         "value": 10},
                "stamina": {"name": "Stamina",
                            "description": "Increases stamina.",
                            "value": 10},
                "piercing": {"name": "Piercing",
                             "description": "Piercing through enemies.",
                             "value": 1},
                "projectileSpeed": {"name": "Projectile Speed",
                                    "description": "Increases projectile "
                                                   "speed.",
                                    "value": 1}}

    def __init__(self, option, topleft):
        self.type = option
        self.image = pygame.image.load(
            f"res/graphic/interface/option_{option}.png").convert()
        self.rect = self.image.get_rect(topleft=topleft)
        self.selected = False
        self.bonus = 1

    def _draw_title(self, screen, font):
        text = font.render(f'{Option._options[self.type]["name"]}',
                           True, (0, 0, 0))
        textRect = text.get_rect(centerx=self.rect.centerx, y=self.rect.centery)
        screen.blit(text, textRect)
        text2 = font.render(f"{Option._options[self.type]['description']}",
                            True, (0, 0, 0))
        textRect2 = text2.get_rect(x=self.rect.x+32, y=textRect.bottom)
        screen.blit(text2, textRect2)

    def display(self, screen, font):
        screen.blit(self.image, self.rect)
        self._draw_title(screen, font)
        if self.selected:
            pygame.draw.rect(screen, (0, 151, 167), self.rect, 7)

    def add_bonus(self, player):
        pass
        # player += 10
        # player.stats[self.type] += Option._options[self.type]
