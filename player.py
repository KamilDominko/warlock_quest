import math

import pygame

import os
from weapon import Weapon
from upgrade import Upgrade


class Player(pygame.sprite.Sprite):
    def __init__(self, program, x=2000, y=2000):
        super().__init__()
        self.program = program
        self.x = x
        self.y = y
        self.image = pygame.surface.Surface((64, 128))
        self.rect = self.image.get_rect(center=(x, y))
        self.feet = self.image.get_rect(center=self.rect.midbottom,
                                        width=32, height=32)
        # self.feet = self.rect.midbottom
        # self.foot = self.image.get_rect(center=self.rect.midbottom,
        #                                 width=32, height=32)

        self.stats = {"level": 1,
                      "experience": 9,
                      "health": program.settings.player_health,
                      "health regen": program.settings.player_health_regen,
                      "mana": program.settings.player_mana,
                      "mana regen": program.settings.player_mana_regen,
                      "stamina": program.settings.player_stamina,
                      "stamina regen": program.settings.player_stamina_regen,
                      "walk": program.settings.player_speed,
                      "sprint": program.settings.player_sprint,
                      "attack speed": program.settings.player_attack_speed}

        self.currentHealth = self.stats["health"]
        self.currentMana = self.stats["mana"]
        self.currentStamina = self.stats["stamina"]
        self.regenTime = 0
        self.speed = self.stats["walk"]
        self.sprintTime = 0
        self.weapon = Weapon(self, self.program)
        self.reload = 0
        self.attack = 0
        self.isShooting = False
        self.radius = 200
        self.hited = 0
        self.circleColor = (0, 255, 0)
        self.obstacles = program.map.obstacles
        program.map.obstacles.add(self)
        self._stateIdle = 0
        self._stateUp = 0
        self._stateDown = 0
        self._stateLeft = 0
        self._stateRight = 0
        self._stateSprint = 0
        self.animationIndex = 0
        self._load_animations()

    def _load_animations(self):
        self.animation_idle = self._load_images(
            "res/graphic/player/player_idle", "player_idle", ".png")
        self.animation_up = self._load_images(
            "res/graphic/player/player_move_up", "player_move_up", ".png")
        self.animation_down = self._load_images(
            "res/graphic/player/player_move_down", "player_move_down", ".png")
        self.animation_left = self._load_images(
            "res/graphic/player/player_move_left", "player_move_left", ".png")
        self.animation_right = self._load_images(
            "res/graphic/player/player_move_right", "player_move_right", ".png")

    def _load_images(self, folder_path, img_name, file_extension):
        """Funkcja ładująca pbrazy do animacji sprite'a. Pobiera dwa
        argumenty: ścierzkę do folderu z animcja oraz nazwę animacji BEZ jej
        indesu."""
        animation = []
        files_count = len(os.listdir(folder_path))
        for i in range(files_count):
            img = pygame.image.load(
                f"{folder_path}/{img_name}{i + 1}{file_extension}").convert_alpha()
            img = pygame.transform.scale(img, (64, 128))  # SKALUJE
            animation.append(img)
        return animation

    def _check_animation_state(self, state, animation):
        if state:
            if self._stateSprint:
                self.animationIndex += 0.1 * 3
            elif not self._stateSprint:
                self.animationIndex += 0.1
            if self.animationIndex >= len(animation):
                self.animationIndex = 0
            self.image = animation[int(self.animationIndex)]

    def _animation_state(self):
        if not self._stateUp and not self._stateDown and not \
                self._stateLeft and not self._stateRight:
            self._stateIdle = 1
            self.animationIndex += 0.05
            if self.animationIndex >= len(self.animation_idle):
                self.animationIndex = 0
            self.image = self.animation_idle[int(self.animationIndex)]
        else:
            self._stateIdle = 0
        self._check_animation_state(self._stateUp, self.animation_up)
        self._check_animation_state(self._stateDown, self.animation_down)
        self._check_animation_state(self._stateLeft, self.animation_left)
        self._check_animation_state(self._stateRight, self.animation_right)

    # def _move(self):
    #     # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
    #     speed_x = 0
    #     speed_y = 0
    #     if self._state_left:
    #         speed_x = -self.speed
    #     elif self._state_right:
    #         speed_x = self.speed
    #     if self._state_up:
    #         speed_y = -self.speed
    #     elif self._state_down:
    #         speed_y = self.speed
    #
    #     # Ustal nową pozycję gracza w pionie
    #     new_y = self.feet.y + speed_y
    #
    #     # Tworzy nowy rect na podstawie nowych współrzędnych w pionie
    #     new_rect_y = self.feet.copy()
    #     new_rect_y.y = new_y
    #
    #     # Sprawdza kolizje z przeszkodami w pionie
    #     for obstacle in self.obstacles:
    #         if new_rect_y.colliderect(obstacle.rect):
    #             if speed_y > 0:
    #                 new_y = obstacle.rect.top - self.feet.height
    #             elif speed_y < 0:
    #                 new_y = obstacle.rect.bottom
    #
    #     # Ustal nową pozycję gracza w poziomie
    #     new_x = self.feet.x + speed_x
    #
    #     # Tworzy nowy rect na podstawie nowych współrzędnych w poziomie
    #     new_rect_x = self.feet.copy()
    #     new_rect_x.x = new_x
    #
    #     # Sprawdza kolizje z przeszkodami w poziomie
    #     for obstacle in self.obstacles:
    #         if new_rect_x.colliderect(obstacle.rect):
    #             if speed_x > 0:
    #                 new_x = obstacle.rect.left - self.feet.width
    #             elif speed_x < 0:
    #                 new_x = obstacle.rect.right
    #
    #     # Aktualizuje pozycję gracza
    #     self.feet.x = new_x
    #     self.feet.y = new_y
    #     # Aktualizuje pozycję rect'a gracza na podstawie rect'a self.feet
    #     self.rect.midbottom = self.feet.midbottom

    # def _move(self):
    #     """Odpowiada za poruszanie się gracza oraz detekcje kolizji z
    #     przeszkodami, przez które gracz nie może przejść."""
    #     # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
    #     speed_x = -self.speed if self._state_left else self.speed if self._state_right else 0
    #     speed_y = -self.speed if self._state_up else self.speed if self._state_down else 0
    #     # Ustal nową pozycję gracza w poziomie i pionie
    #     new_x = self.feet.x + speed_x
    #     new_y = self.feet.y + speed_y
    #     # Utwórz hipotetyczne rect'y dla ruchu w poziomie i pionie
    #     new_rect_x = self.feet.copy()
    #     new_rect_x.x = new_x
    #     new_rect_y = self.feet.copy()
    #     new_rect_y.y = new_y
    #     # Spraawdź kolizję hipotetycznych rect'ów
    #     for obstacle in self.obstacles:
    #         if obstacle != self:
    #             # Sprawdza kolizje z przeszkodami w poziomie
    #             if new_rect_x.colliderect(obstacle.feet):
    #                 if speed_x > 0:
    #                     speed_x = 0
    #                 elif speed_x < 0:
    #                     speed_x = 0
    #             # Sprawdza kolizje z przeszkodami w pionie
    #             if new_rect_y.colliderect(obstacle.feet):
    #                 if speed_y > 0:
    #                     speed_y = 0
    #                 elif speed_y < 0:
    #                     speed_y = 0
    #     # Aktualizuje pozycję self.feet
    #     self.feet.x += speed_x
    #     self.feet.y += speed_y
    #     # Aktualizuje pozycję self.rect na podstawie self.feet
    #     self.rect.midbottom = self.feet.midbottom

    def _move(self):
        """Odpowiada za poruszanie się gracza oraz detekcję kolizji z przeszkodami, przez które gracz nie może przejść."""
        # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
        speed = pygame.math.Vector2(0, 0)
        if self._stateLeft:
            speed.x = -self.speed
        elif self._stateRight:
            speed.x = self.speed
        if self._stateUp:
            speed.y = -self.speed
        elif self._stateDown:
            speed.y = self.speed
        # Znormalizuj wektor prędkości, aby utrzymać stałą prędkość niezależnie od kierunku
        if speed.length() > 0:
            speed = speed.normalize() * self.speed
        # Ustal nową pozycję gracza w poziomie i pionie
        new_x = self.feet.x + speed.x
        new_y = self.feet.y + speed.y
        # Utwórz hipotetyczne rect'y dla ruchu w poziomie i pionie
        new_rect_x = self.feet.copy()
        new_rect_x.x = new_x
        new_rect_y = self.feet.copy()
        new_rect_y.y = new_y
        # Sprawdź kolizję hipotetycznych rect'ów
        for obstacle in self.obstacles:
            if obstacle != self:
                # Sprawdza kolizje z przeszkodami w poziomie
                if new_rect_x.colliderect(obstacle.feet):
                    speed.x = 0
                # Sprawdza kolizje z przeszkodami w pionie
                if new_rect_y.colliderect(obstacle.feet):
                    speed.y = 0
        # Aktualizuje pozycję self.feet
        self.feet.x += speed.x
        self.feet.y += speed.y
        # Aktualizuje pozycję self.rect na podstawie self.feet
        self.rect.midbottom = self.feet.midbottom

    def _shoot(self):
        if self.reload == 0:
            self.reload = pygame.time.get_ticks()
            self.weapon.shoot()
        if pygame.time.get_ticks() - self.reload > 1000 // self.stats[
            "attack speed"]:
            self.reload = pygame.time.get_ticks()
            self.weapon.shoot()
        # self.weapon.shoot()

    def _check_if_hited(self):
        if self.hited:
            if pygame.time.get_ticks() - self.hited < 500:
                mask = pygame.mask.from_surface(self.image)
                maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                          setcolor=(150, 0, 0, 150))
                point = self.program.camera.update_point((self.rect.topleft))
                self.program.screen.blit(maksSrf, point)
            else:
                self.hited = 0

    def deal_damage(self, damage):
        self.currentHealth -= damage
        self.hited = pygame.time.get_ticks()
        if self.currentHealth <= 0:
            pass
            # GAME OVER

    def add_xp(self, amount):
        self.stats["experience"] += amount
        if self.stats["experience"] >= 10 * self.stats["level"]:
            self.stats["level"] += 1
            self.stats["experience"] = 0
            Upgrade(self.program).pick()
            self._stateUp = 0
            self._stateDown = 0
            self._stateLeft = 0
            self._stateRight = 0
            self._stateSprint = 0
            self.speed = self.stats["walk"]

    def input(self, event):
        """Funkcja sprawdza input z klawiatury dla gracza."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._stateUp = 1
            if event.key == pygame.K_s:
                self._stateDown = 1
            if event.key == pygame.K_a:
                self._stateLeft = 1
            if event.key == pygame.K_d:
                self._stateRight = 1
            if event.key == pygame.K_LSHIFT:
                self._stateSprint = 1

                # self.sprintTime = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # self._shoot()
                self.isShooting = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self._stateUp:
                self._stateUp = 0
            if event.key == pygame.K_s and self._stateDown:
                self._stateDown = 0
            if event.key == pygame.K_a and self._stateLeft:
                self._stateLeft = 0
            if event.key == pygame.K_d and self._stateRight:
                self._stateRight = 0
            if event.key == pygame.K_LSHIFT:
                self._stateSprint = 0
                self.speed = self.stats["walk"]
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.isShooting = False

    def _check_sprint(self):
        if self._stateSprint and not self._stateIdle and self.currentStamina > 0:
            self.speed = self.stats["sprint"]
            if pygame.time.get_ticks() - self.sprintTime > 50:
                self.currentStamina -= self.program.settings.player_stamina_drain
                self.sprintTime = pygame.time.get_ticks()
        elif self.currentStamina <= 0:
            if self.currentStamina < 0:
                self.currentStamina = 0
            self._stateSprint = 0
            self.speed = self.stats["walk"]

    def _regen_health(self):
        if self.currentHealth < self.stats["health"] and not self.hited:
            self.currentHealth += self.stats["health regen"]

    def _regen_stamina(self):
        if not self._stateSprint or self._stateIdle:
            if self.currentStamina + self.stats["stamina regen"] > self.stats[
                "stamina"]:
                self.currentStamina = self.stats["stamina"]
            else:
                self.currentStamina += self.stats["stamina regen"]

    def _regen(self):
        if pygame.time.get_ticks() - self.regenTime > 100:
            self.regenTime = pygame.time.get_ticks()
            self._regen_health()
            self._regen_stamina()

    def update(self):
        self._move()
        self.feet = self.image.get_rect(width=32, height=16,
                                        midbottom=self.rect.midbottom)
        if self.isShooting:
            self._shoot()

        self._check_sprint()
        self._regen()

        # self.feet = self.rect.midbottom
        # self.foot = self.image.get_rect(width=32, height = 32,
        #                                 midbottom=self.feet)
        self._animation_state()
        center = self.program.camera.update_rect(self.rect)
        self.weapon.update(center.center)
        # self._check_circle_range()
        self._check_items()

    def _check_circle_range(self):
        # koło?
        for enemy in self.program.enemies:
            if self._rect_circle_collision(enemy.feet):
                self.circleColor = (255, 0, 0)
                enemy.selected = True
            else:
                self.circleColor = (0, 255, 0)

    def _check_items(self):
        for item in self.program.items:
            if self._rect_circle_collision(item.rect) and not item.sucked:
                item.suck()

    def _rect_circle_collision(self, rect):
        # Sprawdź, czy prostokąt i okrąg mają przecinające się prostokąty ograniczające
        bounding_rect = pygame.Rect(self.feet.centerx - self.radius,
                                    self.feet.bottom - self.radius,
                                    2 * self.radius, 2 * self.radius)
        if rect.colliderect(bounding_rect):
            # Sprawdź, czy którakolwiek krawędź prostokąta znajduje się w odległości nie większej niż promień okręgu od jego centrum
            for corner in [(rect.left, rect.top), (rect.right, rect.top),
                           (rect.left, rect.bottom), (rect.right, rect.bottom)]:
                distance = math.sqrt(
                    (self.feet.centerx - corner[0]) ** 2 + (
                            self.feet.bottom - corner[1]) ** 2)
                if distance <= self.radius:
                    return True
            # Sprawdź, czy środek okręgu znajduje się w prostokącie
            return rect.collidepoint(self.feet.centerx, self.feet.bottom)
        return False

    def display(self):
        if not self._stateUp:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
            self.weapon.display()
        elif self._stateLeft or self._stateRight:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
            self.weapon.display()
        elif self._stateUp:
            self.weapon.display()
            self.program.camera.camera_draw(self.image, self.rect.topleft)
        self._check_if_hited()

        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_feet()
            # self._draw_foot()
            self._draw_feet_rect()

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _draw_feet(self):
        feet = self.program.camera.update_point(self.feet.midbottom)
        pygame.draw.circle(self.program.screen, (0, 0, 255), feet, 3)
        pygame.draw.circle(self.program.screen, self.circleColor,
                           feet, self.radius, 2)

    def _draw_feet_rect(self):
        feet_rect = self.program.camera.update_rect(self.feet)
        pygame.draw.rect(self.program.screen, (0, 0, 255), feet_rect, 3)

    def _draw_foot(self):
        foot = self.program.camera.update_rect(self.foot)
        pygame.draw.rect(self.program.screen, (0, 0, 255), foot, 3)
