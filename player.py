import pygame

import os
from weapon import Weapon


class Player(pygame.sprite.Sprite):
    def __init__(self, program):
        super().__init__()
        self.program = program
        self.image = pygame.surface.Surface((64, 128))
        self.rect = self.image.get_rect(center=program.screen.get_rect().center)
        self.feet = self.rect.midbottom
        self.speed = program.settings.player_speed
        self.sprint = program.settings.player_sprint
        self.weapon = Weapon(self, self.program)
        self.obstacles = program.map.obstacles
        # Animacje.
        self._state_up = 0
        self._state_down = 0
        self._state_left = 0
        self._state_right = 0
        self._state_sprint = 0
        self.animation_index = 0
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

    def _hit_list(self):
        hit_list = []
        for field in self.obstacles:
            if self.rect.colliderect(field.rect):
                hit_list.append(field)
        return hit_list

    def _check_obstacle_collision(self):
        hit_list = self._hit_list()
        for field in hit_list:
            # W dół.
            rect = (self.rect.x, self.rect.y + self.speed,
                    self.rect.w, self.rect.h)
            if field.rect.colliderect(rect):
                self.rect.y -= self.speed
            # W górę.
            rect = (self.rect.x, self.rect.y - self.speed,
                    self.rect.w, self.rect.h)
            if field.rect.colliderect(rect):
                self.rect.y += self.speed
            # W Prawo.
            rect = (self.rect.x + self.speed, self.rect.y,
                    self.rect.w, self.rect.h)
            if field.rect.colliderect(rect):
                self.rect.x -= self.speed
            # W lewo.
            rect = (self.rect.x - self.speed, self.rect.y,
                    self.rect.w, self.rect.h)
            if field.rect.colliderect(rect):
                self.rect.x += self.speed

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

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _draw_feet(self):
        pygame.draw.circle(self.program.screen, (0, 0, 255), self.feet, 3)

    def move(self, event):
        """Funkcja sprawdza, czy gracz ma iść, w którą stronę."""
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
                self.speed += self.sprint
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
                self.speed -= self.sprint

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

    def _check_animation_state(self, state, animation):
        if state:
            if self._state_sprint:
                self.animation_index += 0.1 * 3
            elif not self._state_sprint:
                self.animation_index += 0.1
            if self.animation_index >= len(animation):
                self.animation_index = 0
            self.image = animation[int(self.animation_index)]

    # def _move2(self):
    #     if self._state_up:
    #         if self._state_sprint:
    #             self.rect.y -= self.sprint
    #         if not self._state_sprint:
    #             self.rect.y -= self.speed
    #     if self._state_down:
    #         if self._state_sprint:
    #             self.rect.y += self.sprint
    #         if not self._state_sprint:
    #             self.rect.y += self.speed
    #     if self._state_left:
    #         if self._state_sprint:
    #             self.rect.x -= self.sprint
    #         if not self._state_sprint:
    #             self.rect.x -= self.speed
    #     if self._state_right:
    #         if self._state_sprint:
    #             self.rect.x += self.sprint
    #         if not self._state_sprint:
    #             self.rect.x += self.speed
    #     self._check_obstacle_collision()

    def _move2(self):
        if self._state_up:
            self.rect.y -= self.speed
        if self._state_down:
            self.rect.y += self.speed
        if self._state_left:
            self.rect.x -= self.speed
        if self._state_right:
            self.rect.x += self.speed
        self._check_obstacle_collision()

    def _move(self):
        map = self.program.map.width
        map = self.program.map.height
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom > 0:  # GÓRA
            self.rect.y -= self.speed
        if keys[
            pygame.K_s] and self.rect.bottom < self.program.map.height:  # DÓŁ
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:  # LEWO
            self.rect.x -= self.speed
        if keys[
            pygame.K_d] and self.rect.right < self.program.map.width:  # PRAWO
            self.rect.x += self.speed

    def update(self):
        # self._move()
        self._animation_state()
        self._move2()
        center = self.program.camera.update_rect(self.rect)
        self.weapon.update(center.center)

    def display(self):
        # self.program.screen.blit(self.image, self.rect)
        if not self._state_up:
            # Jeżeli gracz skierowany jest w dół, najpierw wyświetl gracza,
            # potem jego broń
            self.program.camera.camera_draw(self.image, self.rect.topleft)
            self.weapon.display()
        elif self._state_up:
            # Jeżeli gracz jest skierowany w górę...
            if self._state_left or self._state_right:
                # ...ORAZ jest skierowany w lewo albo w prawo to najpierw
                # wyświetl gracza, a potem jego broń.
                self.program.camera.camera_draw(self.image, self.rect.topleft)
                self.weapon.display()
            else:
                # ...najpierw wyświetl broń, a następnie gracza.
                self.weapon.display()
                self.program.camera.camera_draw(self.image, self.rect.topleft)
        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_feet()
        # print(self.rect.center)
