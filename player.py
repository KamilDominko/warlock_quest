import pygame

import os
from weapon import Weapon


class Player(pygame.sprite.Sprite):
    def __init__(self, program, x=300, y=300):
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
        self.speed = program.settings.player_speed
        self.walk = program.settings.player_speed
        self.sprint = program.settings.player_sprint
        self.weapon = Weapon(self, self.program)
        self.obstacles = program.map.obstacles
        program.map.obstacles.add(self)
        self._state_up = 0
        self._state_down = 0
        self._state_left = 0
        self._state_right = 0
        self._state_sprint = 0
        self.animation_index = 0
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
            if self._state_sprint:
                self.animation_index += 0.1 * 3
            elif not self._state_sprint:
                self.animation_index += 0.1
            if self.animation_index >= len(animation):
                self.animation_index = 0
            self.image = animation[int(self.animation_index)]

    def _animation_state(self):
        if not self._state_up and not self._state_down and not \
                self._state_left and not self._state_right:
            self.animation_index += 0.05
            if self.animation_index >= len(self.animation_idle):
                self.animation_index = 0
            self.image = self.animation_idle[int(self.animation_index)]
        self._check_animation_state(self._state_up, self.animation_up)
        self._check_animation_state(self._state_down, self.animation_down)
        self._check_animation_state(self._state_left, self.animation_left)
        self._check_animation_state(self._state_right, self.animation_right)

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

    def _move(self):
        """Odpowiada za poruszanie się gracza oraz detekcje kolizji z
        przeszkodami, przez które gracz nie może przejść."""
        # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
        speed_x = -self.speed if self._state_left else self.speed if self._state_right else 0
        speed_y = -self.speed if self._state_up else self.speed if self._state_down else 0
        # Ustal nową pozycję gracza w poziomie i pionie
        new_x = self.feet.x + speed_x
        new_y = self.feet.y + speed_y
        # Utwórz hipotetyczne rect'y dla ruchu w poziomie i pionie
        new_rect_x = self.feet.copy()
        new_rect_x.x = new_x
        new_rect_y = self.feet.copy()
        new_rect_y.y = new_y
        # Spraawdź kolizję hipotetycznych rect'ów
        for obstacle in self.obstacles:
            if obstacle != self:
                # Sprawdza kolizje z przeszkodami w poziomie
                if new_rect_x.colliderect(obstacle.feet):
                    if speed_x > 0:
                        new_x = obstacle.feet.left - self.feet.width
                    elif speed_x < 0:
                        new_x = obstacle.feet.right
                # Sprawdza kolizje z przeszkodami w pionie
                if new_rect_y.colliderect(obstacle.feet):
                    if speed_y > 0:
                        new_y = obstacle.feet.top - self.feet.height
                    elif speed_y < 0:
                        new_y = obstacle.feet.bottom
        # Aktualizuje pozycję self.feet
        self.feet.x = new_x
        self.feet.y = new_y
        # Aktualizuje pozycję self.rect na podstawie self.feet
        self.rect.midbottom = self.feet.midbottom

    def input(self, event):
        """Funkcja sprawdza input z klawiatury dla gracza."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self._state_up = 1
            if event.key == pygame.K_s:
                self._state_down = 1
            if event.key == pygame.K_a:
                self._state_left = 1
            if event.key == pygame.K_d:
                self._state_right = 1
            if event.key == pygame.K_LSHIFT:
                self._state_sprint = 1
                self.speed = self.sprint
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.weapon.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self._state_up:
                self._state_up = 0
            if event.key == pygame.K_s and self._state_down:
                self._state_down = 0
            if event.key == pygame.K_a and self._state_left:
                self._state_left = 0
            if event.key == pygame.K_d and self._state_right:
                self._state_right = 0
            if event.key == pygame.K_LSHIFT:
                self._state_sprint = 0
                self.speed = self.walk

    def update(self):
        self._move()
        self.feet = self.image.get_rect(width=32, height=16,
                                        midbottom=self.rect.midbottom)
        # self.feet = self.rect.midbottom
        # self.foot = self.image.get_rect(width=32, height = 32,
        #                                 midbottom=self.feet)
        self._animation_state()
        center = self.program.camera.update_rect(self.rect)
        self.weapon.update(center.center)

    def display(self):
        if not self._state_up:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
            self.weapon.display()
        elif self._state_left or self._state_right:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
            self.weapon.display()
        elif self._state_up:
            self.weapon.display()
            self.program.camera.camera_draw(self.image, self.rect.topleft)

        DEV = 1
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

    def _draw_feet_rect(self):
        feet_rect = self.program.camera.update_rect(self.feet)
        pygame.draw.rect(self.program.screen, (0, 0, 255), feet_rect, 3)

    def _draw_foot(self):
        foot = self.program.camera.update_rect(self.foot)
        pygame.draw.rect(self.program.screen, (0, 0, 255), foot, 3)
