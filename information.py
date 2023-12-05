import pygame


class Information:
    pygame.font.init()

    def __init__(self, program):
        self.program = program
        self.screen = program.screen
        self.player = program.player
        self.weapon = program.player.weapon
        self.font = pygame.font.Font("res/font/Pixeltype.ttf", 50)
        self.color = program.settings.BLACK
        self.window = pygame.Surface((350, 700))
        self.window.fill((90, 10, 20))
        x = program.screen.get_width() - self.window.get_width()
        self.windowRect = self.window.get_rect(topleft=(x, 111))

    def display_window(self):
        self.screen.blit(self.window, self.windowRect)
        self.display_info()
        self.window.fill((90, 10, 20))

    def render_stat(self, label, value, x, y):
        text = self.font.render(f"{label}: {value}", True, self.color)
        textRect = text.get_rect(x=x, y=y)
        self.window.blit(text, textRect)
        return textRect.bottom

    def render_section(self, header, stats, x, y):
        text = self.font.render(header, True, self.color)
        textRect = text.get_rect(centerx=self.window.get_rect().centerx, y=y)
        self.window.blit(text, textRect)
        y = textRect.bottom

        for label, value in stats:
            y = self.render_stat(label, value, x, y)

        return y + 20  # Add some space between sections

    def display_info(self):
        current_y = 20

        current_y = self.render_section("Player Statistics", [
            ("Health", f"{self.player.currentHealth}/"
                       f"{self.player.stats['health']}"),
            ("Regen", f"{self.player.stats['health_regen']}/sec"),
            (
                "Mana",
                f"{self.player.currentMana}/{self.player.stats['mana']}"),
            ("Regen", f"{self.player.stats['mana_regen']}/sec"),
            ("Stamina", f"{int(self.player.currentStamina)}"
                        f"/{self.player.stats['stamina']}"),
            ("Regen", f"{self.player.stats['stamina_regen']}/sec"),
        ], 20, current_y)

        current_y = self.render_section("Weapon Statistics", [
            ("Attack Speed", self.weapon.stats["attack_speed"]),
            ("PD", self.weapon.stats["projectile_damage"]),
            ("LD", self.weapon.stats["laser_damage"]),
            ("Piercing", self.weapon.stats["piercing"]),
        ], 20, current_y)

        self.render_section("DEV", [
            ("FPS", self.program.clock.get_fps()),
            ("ENEMIES", len(self.program.enemies))
        ], 20, current_y)

        self.screen.blit(self.window, self.windowRect)
        self.window.fill((90, 10, 20))

        # import pygame
        #
        #
        # class Information:
        #     pygame.font.init()
        #
        #     def __init__(self, program):
        #         self.program = program
        #         self.screen = program.screen
        #         self.player = program.player
        #         self.weapon = program.player.weapon
        #         self.font = pygame.font.Font("res/font/Pixeltype.ttf", 50)
        #         self.color = program.settings.BLACK
        #         self.window = pygame.Surface((350, 700))
        #         self.window.fill((90, 10, 20))
        #         self.windowRect = self.window.get_rect(topleft=(111, 111))
        #
        #     def display_window(self):
        #         self.screen.blit(self.window, self.windowRect)
        #         # infoText = self.font.render("Player Statistics", True, self.color)
        #         # infoTextRect = infoText.get_rect()
        #         # self.window.blit(infoText, infoTextRect)
        #         plrAtcSpd = self.font.render(f"Attack Speed: {self.player.attackSpeed}",
        #                                      True, self.color)
        #         plrAtcSpdRect = self.window.get_rect()
        #         self.window.blit(plrAtcSpd, plrAtcSpdRect)
        #
        #     def display_info(self):
        #         # PLAYER HEADER
        #         text = self.font.render("Player Statistics", True, self.color)
        #         textRect = text.get_rect(
        #             centerx=self.window.get_rect().centerx,
        #             y=20)
        #         self.window.blit(text, textRect)
        #         # Health HEADER
        #         text = self.font.render("Health", True, self.color)
        #         textRect = text.get_rect(
        #             centerx=self.window.get_rect().centerx, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Health Amount
        #         text = self.font.render(f"Amount: {self.player.currentHealth}/"
        #                                 f"{self.player.maxHealth}",
        #                                 True, self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Health Regen
        #         text = self.font.render(f"Regen: {self.player.regenHealth}/sec", True,
        #                                 self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Mana HEADER
        #         text = self.font.render("Mana", True, self.color)
        #         textRect = text.get_rect(
        #             centerx=self.window.get_rect().centerx, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Mana Amount
        #         text = self.font.render(f"Amount: {self.player.currentMana}/"
        #                                 f"{self.player.maxMana}",
        #                                 True, self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Mana Regen
        #         text = self.font.render(f"Regen: {self.player.regenMana}/sec", True,
        #                                 self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Stamina HEADER
        #         text = self.font.render("Stamina", True, self.color)
        #         textRect = text.get_rect(
        #             centerx=self.window.get_rect().centerx, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Stamina Amount
        #         text = self.font.render(f"Amount: {self.player.currentStamina}/"
        #                                 f"{self.player.maxStamina}",
        #                                 True, self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Stamina Regen
        #         text = self.font.render(f"Regen: {self.player.regenStamina}/sec", True,
        #                                 self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # WEAPON HEADER
        #         text = self.font.render("Weapon Statistics", True, self.color)
        #         textRect = text.get_rect(
        #             centerx=self.window.get_rect().centerx, y=textRect.bottom + 20)
        #         self.window.blit(text, textRect)
        #         # Attack Speed
        #         text = self.font.render(
        #             f"Attack Speed: {self.player.attackSpeed}", True, self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Weapon Damage
        #         text = self.font.render(f"Damage: {self.weapon.damage}", True,
        #                                 self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #         # Weapon Piercing
        #         text = self.font.render(f"Piercing: {self.weapon.hits}", True,
        #                                 self.color)
        #         textRect = text.get_rect(x=20, y=textRect.bottom)
        #         self.window.blit(text, textRect)
        #
        #         # # PLAYER HEADER
        #         # playerText = self.font.render("Player Statistics", True, self.color)
        #         # playerTextRect = playerText.get_rect(
        #         #     centerx=self.window.get_rect().centerx,
        #         #     y=20)
        #         # self.window.blit(playerText, playerTextRect)
        #         # # Health HEADER
        #         # healthText = self.font.render("Health", True, self.color)
        #         # healthTextRect = healthText.get_rect(
        #         #     centerx=self.window.get_rect().centerx, y=playerTextRect.bottom)
        #         # self.window.blit(healthText, healthTextRect)
        #         # # Health Amount
        #         # healthAmount = self.font.render(f"Amount: 1500/1500", True, self.color)
        #         # healthAmountRect = healthAmount.get_rect(x=20, y=healthTextRect.bottom)
        #         # self.window.blit(healthAmount, healthAmountRect)
        #         # # Health Regen
        #         # healthRegen = self.font.render(f"Regen: 5/sec", True, self.color)
        #         # healthRegenRect = healthRegen.get_rect(x=20, y=healthAmountRect.bottom)
        #         # self.window.blit(healthRegen, healthRegenRect)
        #         # # Mana HEADER
        #         # manaText = self.font.render("Mana", True, self.color)
        #         # manaTextRect = manaText.get_rect(
        #         #     centerx=self.window.get_rect().centerx, y=healthRegenRect.bottom)
        #         # self.window.blit(manaText, manaTextRect)
        #         # # Mana Amount
        #         # manaAmount = self.font.render(f"Amount: 5000/5000", True, self.color)
        #         # manaAmountRect = manaAmount.get_rect(x=20, y=manaTextRect.bottom)
        #         # self.window.blit(manaAmount, manaAmountRect)
        #         # # Mana Regen
        #         # manaRegen = self.font.render(f"Regen: 15/sec", True, self.color)
        #         # manaRegenRect = manaRegen.get_rect(x=20, y=manaAmountRect.bottom)
        #         # self.window.blit(manaRegen, manaRegenRect)
        #         # # Stamina HEADER
        #         # staminaText = self.font.render("Stamina", True, self.color)
        #         # staminaTextRect = staminaText.get_rect(
        #         #     centerx=self.window.get_rect().centerx, y=manaRegenRect.bottom)
        #         # self.window.blit(staminaText, staminaTextRect)
        #         # # Stamina Amount
        #         # staminaAmount = self.font.render(f"Amount: 500/500", True, self.color)
        #         # staminaAmountRect = staminaAmount.get_rect(x=20,
        #         #                                            y=staminaTextRect.bottom)
        #         # self.window.blit(staminaAmount, staminaAmountRect)
        #         # # Stamina Regen
        #         # staminaRegen = self.font.render(f"Regen: 8/sec", True, self.color)
        #         # staminaRegenRect = staminaRegen.get_rect(x=20,
        #         #                                          y=staminaAmountRect.bottom)
        #         # self.window.blit(staminaRegen, staminaRegenRect)
        #         # # WEAPON HEADER
        #         # weaponText = self.font.render("Weapon Statistics", True, self.color)
        #         # weaponTextRect = weaponText.get_rect(
        #         #     centerx=self.window.get_rect().centerx,
        #         #     y=staminaRegenRect.bottom + 20)
        #         # self.window.blit(weaponText, weaponTextRect)
        #         # # Attack Speed
        #         # attackSpeed = self.font.render(
        #         #     f"Attack Speed: {self.player.attackSpeed}", True, self.color)
        #         # attackSpeedRect = attackSpeed.get_rect(x=20, y=weaponTextRect.bottom)
        #         # self.window.blit(attackSpeed, attackSpeedRect)
        #         # # Weapon Damage
        #         # damage = self.font.render(f"Damage: {self.weapon.damage}", True,
        #         #                           self.color)
        #         # damageRect = damage.get_rect(x=20, y=attackSpeedRect.bottom)
        #         # self.window.blit(damage, damageRect)
        #         # # Weapon Piercing
        #         # piercing = self.font.render(f"Piercing: {self.weapon.hits}", True,
        #         #                             self.color)
        #         # piercingRect = piercing.get_rect(x=20, y=damageRect.bottom)
        #         # self.window.blit(piercing, piercingRect)
        #
        #         # plrHp = self.font.render(f"Health: 100/100", True, self.color)
        #         # plrHpRect = plrHp.get_rect(topleft=playerTextRect.bottomleft)
        #         # self.window.blit(plrHp, plrHpRect)
        #         # # Player Health Regen
        #         # plrHpReg = self.font.render(f"Health regen: 1/sec", True, self.color)
        #         # plrHpRegRect = plrHpReg.get_rect(topleft=plrHpRect.bottomleft)
        #         # self.window.blit(plrHpReg, plrHpRegRect)
        #         # # Player Mana
        #         # plrMana = self.font.render(f"Mana: 500/500", True, self.color)
        #         # plrManaRect = plrMana.get_rect(topleft=plrHpRegRect.bottomleft)
        #         # self.window.blit(plrMana, plrManaRect)
        #         # # Player Mana Regen
        #         # plrManaReg = self.font.render(f"Mana regen: 10/sec", True, self.color)
        #         # plrManaRegRect = plrManaReg.get_rect(topleft=plrManaRect.bottomleft)
        #         # self.window.blit(plrManaReg, plrManaRegRect)
        #         # # Player Stamina
        #         # plrStamina = self.font.render(f"Stamina: 200/200", True, self.color)
        #         # plrStaminaRect = plrStamina.get_rect(topleft=plrManaRegRect.bottomleft)
        #         # self.window.blit(plrStamina, plrStaminaRect)
        #         # # Player Stamina Regen
        #         # plrStaminaReg = self.font.render(f"Stamina regen: 5/sec", True, self.color)
        #         # plrStaminaRegRect = plrStaminaReg.get_rect(topleft=plrStaminaRect.bottomleft)
        #         # self.window.blit(plrStaminaReg, plrStaminaRegRect)
        #         # # Player Attack Speed
        #         # plrAtcSpd = self.font.render(f"Attack Speed: {self.player.attackSpeed}",
        #         #                              True, self.program.settings.BLACK)
        #         # plrAtcSpdRect = plrAtcSpd.get_rect(topleft=plrStaminaRegRect.bottomleft)
        #         # self.window.blit(plrAtcSpd, plrAtcSpdRect)
        #         # # SPACJA
        #         # spacja = self.font.render("", True, self.color)
        #         # spacjaRect = spacja.get_rect(topleft=plrAtcSpdRect.bottomleft)
        #         # self.window.blit(spacja, spacjaRect)
        #         # # WEAPON HEADER
        #         # weaponText = self.font.render("Weapon Statistics", True, self.color)
        #         # weaponTextRect = weaponText.get_rect(topleft=spacjaRect.bottomleft)
        #         # self.window.blit(weaponText, weaponTextRect)
        #
        #         self.screen.blit(self.window, self.windowRect)
        #         self.window.fill((90, 10, 20))
