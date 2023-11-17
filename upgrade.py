import pygame
import random


class Upgrade:
    """Wyświetla okno wyboru ulepszeń, z trzech losowo wybranych gracz ma
    wybrać jedno."""
    pygame.font.init()

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
            subject = random.choice(("player", "weapon"))
            if subject == "player":
                type = random.choice(("attack_speed", "health"))
            elif subject == "weapon":
                type = random.choice(("damage", "piercing"))
            self.options.append(Option(subject, type, (x, y)))

    def display(self):
        self.screen.blit(self.image, self.rect)
        for option in self.options:
            option.display(self.screen, self.font)
        pygame.display.update()

    def pick(self):
        """Wywołuje ulepszenie, gra zostaje 'zatrzymana' do czasu aż gracz
        wybierze ulepszenie."""
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
    """Opcja, która daje graczowi ulepszenie."""
    _options = {"attack_speed": {"name": "attack speed",
                                 "description": "Increases attacks per second",
                                 "value": 0.2},
                "damage": {"name": "damage",
                           "description": "Increases attack damage",
                           "value": 7.5},
                "health": {"name": "health",
                           "description": "Increases health",
                           "value": 10},
                "mana": {"name": "mana",
                         "description": "Increases mana",
                         "value": 10},
                "stamina": {"name": "stamina",
                            "description": "Increases stamina",
                            "value": 10},
                "piercing": {"name": "piercing",
                             "description": "Increases number of pierced "
                                            "enemies",
                             "value": 1},
                "projectile_speed": {"name": "projectile speed",
                                     "description": "Increases projectile "
                                                    "speed",
                                     "value": 1}}

    def __init__(self, subject, option, topleft):
        self.subject = subject
        self.type = option
        self.image = pygame.image.load(
            f"res/graphic/interface/option_{option}.png").convert()
        self.rect = self.image.get_rect(topleft=topleft)
        self.selected = False
        self.bonus = 1

    def _draw_text(self, screen, font):
        """Wyświetla nazwę i opis ulepszenia."""
        text = font.render(f'{Option._options[self.type]["name"].upper()}',
                           True, (0, 0, 0))
        textRect = text.get_rect(centerx=self.rect.centerx,
                                 centery=self.rect.centery + self.rect.centery / 4)
        screen.blit(text, textRect)
        text2 = font.render(f"{Option._options[self.type]['description']} "
                            f"by {Option._options[self.type]['value']}",
                            True, (0, 0, 0))
        textRect2 = text2.get_rect(centerx=self.rect.centerx, y=textRect.bottom)
        screen.blit(text2, textRect2)

    def display(self, screen, font):
        screen.blit(self.image, self.rect)
        self._draw_text(screen, font)
        if self.selected:
            pygame.draw.rect(screen, (0, 151, 167), self.rect, 7)

    def add_bonus(self, player):
        """Dodaje bonus, sowjego typu, graczowi."""
        if self.subject == "player":
            player.stats[Option._options[self.type]["name"]] += \
                Option._options[self.type]["value"]
        elif self.subject == "weapon":
            player.weapon.stats[Option._options[self.type]["name"]] += \
                Option._options[self.type]["value"]
