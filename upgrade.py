import pygame
import random
import json


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
            "res/graphic/interface/upgrade_options/option.png").convert()
        self.image = pygame.image.load(
            "res/graphic/interface/info.png").convert()
        self.rect = self.image.get_rect(center=self.screen.get_rect().center)
        self.font = pygame.font.Font("res/font/Pixeltype.ttf", 35)
        self.options = []
        self.click = False

        self.upgrades = self._json_upgrades_load()

    def _json_upgrades_load(self):
        f = open('src/data/upgrades.json')
        return json.load(f)

    def _create_options(self):
        """Tworzy trzy losowe opcje do wyboru."""
        picked = []
        while len(picked) != 3:
            i = len(picked)
            x = self.rect.x + i * self.optionImage.get_width() + 2 * 16 + i * 16
            y = self.rect.y + 5 * 16
            stat = random.choice(list(self.upgrades.keys()))

            # stat = "projectile_damage"
            # self.options.append(Option(self.upgrades, stat, (x, y)))
            # picked.append(stat)

            if stat not in picked:
                picked.append(stat)
                self.options.append(Option(self.upgrades, stat, (x, y)))

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
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         self.picked = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False

            self.update()
            self.display()

    def update(self):
        for option in self.options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.selected = True
                if self.click:
                    option.add_bonus(self.player, self.player.weaponImg)
                    self.picked = True
            else:
                option.selected = False

    def display(self):
        self.screen.blit(self.image, self.rect)
        for option in self.options:
            option.display(self.screen, self.font)
        pygame.display.update()


class Option:
    """Opcja, która daje graczowi ulepszenie."""
    f = open('src/data/upgrades.json')
    upgrades = json.load(f)
    _options = upgrades

    def __init__(self, options, stat, topleft):
        self.options = options
        self.stat = stat
        self.image = pygame.image.load(
            f"res/graphic/interface/upgrade_options"
            f"/option_{stat}.png").convert()
        self.rect = self.image.get_rect(topleft=topleft)
        self.selected = False
        self.bonus = 1

    def _draw_text(self, screen, font):
        """Wyświetla nazwę i opis ulepszenia."""
        text = font.render(f'{self.options[self.stat]["name"].upper()}',
                           True, (0, 0, 0))
        textRect = text.get_rect(centerx=self.rect.centerx,
                                 centery=self.rect.centery + self.rect.centery / 4)
        screen.blit(text, textRect)
        text2 = font.render(f"{self.options[self.stat]['description']} "
                            f"by {self.options[self.stat]['value']}",
                            True, (0, 0, 0))
        textRect2 = text2.get_rect(centerx=self.rect.centerx, y=textRect.bottom)
        screen.blit(text2, textRect2)

    # def add_bonus(self, player):
    #     """Dodaje bonus, sowjego typu, graczowi."""
    #     if self.subject == "player":
    #         player.stats[self.stat] += self.options[self.stat]["value"]
    #     elif self.subject == "weapon":
    #         player.weapon.stats[self.stat] += self.options[self.stat]["value"]

    def add_bonus(self, player, weapon):
        """Dodaje bonus graczowi."""
        upgradeType = self.options[self.stat]["type"]
        upgradeTarget = self.options[self.stat]["target"]
        if upgradeTarget == "player":
            if upgradeType == "stat":
                player.stats[self.stat] += self.options[self.stat]["value"]
            elif upgradeType == "dimension":
                player.stats[self.stat] += self.options[self.stat]["value"]
                # TODO Dodać skalowanie przez rozdzielczość
        elif upgradeTarget == "weapon":
            if upgradeType == "stat":
                weapon.stats[self.stat] += self.options[self.stat]["value"]
            elif upgradeType == "range":
                value = self.options[self.stat]["value"]
                current = weapon.stats[self.stat]
                start = int(current.start + value)
                end = int(current.stop + value)
                new = range(start, end)
                weapon.stats.update({self.stat: new})

    def display(self, screen, font):
        screen.blit(self.image, self.rect)
        self._draw_text(screen, font)
        if self.selected:
            pygame.draw.rect(screen, (0, 151, 167), self.rect, 7)
