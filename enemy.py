import pygame

import os
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, program, centerx, centery):
        super().__init__()
        self.program = program
        self.image = pygame.image.load(
            "res/graphic/enemy/enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(centerx, centery))
        self.speed = program.settings.enemy_speed
        self.moving_up = 0
        self.moving_down = 0
        self.moving_left = 0
        self.moving_right = 0
        self.animation_index = 0
        self._load_animations()
        self.obstacles = program.map.obstacles

    def _load_animations(self):
        self.animation_idle = self._load_images(
            "res/graphic/enemy/enemy_idle", "enemy_idle", ".png")
        self.animation_up = self._load_images(
            "res/graphic/enemy/enemy_move_up", "enemy_move_up", ".png")
        self.animation_down = self._load_images(
            "res/graphic/enemy/enemy_move_down", "enemy_move_down", ".png")
        self.animation_left = self._load_images(
            "res/graphic/enemy/enemy_move_left", "enemy_move_left", ".png")
        self.animation_right = self._load_images(
            "res/graphic/enemy/enemy_move_right", "enemy_move_right", ".png")

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
            self.animation_index += 0.1
            if self.animation_index >= len(animation):
                self.animation_index = 0
            self.image = animation[int(self.animation_index)]

    def _animation_state(self):
        if not self.moving_up and not self.moving_down and not \
                self.moving_left and not self.moving_right:
            self.animation_index += 0.05
            if self.animation_index >= len(self.animation_idle):
                self.animation_index = 0
            self.image = self.animation_idle[int(self.animation_index)]
        self._check_animation_state(self.moving_up, self.animation_up)
        self._check_animation_state(self.moving_down, self.animation_down)
        self._check_animation_state(self.moving_left, self.animation_left)
        self._check_animation_state(self.moving_right, self.animation_right)

    # def _move2(self):
    #     _speed = self.speed
    #     if self._state_up:
    #         for obstacle in self.obstacles:
    #             rect = pygame.Rect(self.rect.x, self.rect.y - self.speed,
    #                                self.rect.w, self.rect.h)
    #             if rect.colliderect(obstacle.rect):
    #                 _speed = 0
    #                 break
    #         self.rect.y -= _speed
    #     _speed = self.speed
    #     if self._state_down:
    #         for obstacle in self.obstacles:
    #             rect = pygame.Rect(self.rect.x, self.rect.y + self.speed,
    #                                self.rect.w, self.rect.h)
    #             if rect.colliderect(obstacle.rect):
    #                 _speed = 0
    #                 break
    #         self.rect.y += _speed
    #     _speed = self.speed
    #     if self._state_left:
    #         for obstacle in self.obstacles:
    #             rect = pygame.Rect(self.rect.x - self.speed, self.rect.y,
    #                                self.rect.w, self.rect.h)
    #             if rect.colliderect(obstacle.rect):
    #                 _speed = 0
    #                 break
    #         self.rect.x -= _speed
    #     _speed = self.speed
    #     if self._state_right:
    #         for obstacle in self.obstacles:
    #             rect = pygame.Rect(self.rect.x + self.speed, self.rect.y,
    #                                self.rect.w, self.rect.h)
    #             if rect.colliderect(obstacle.rect):
    #                 _speed = 0
    #                 break
    #         self.rect.x += _speed

    def _move(self):
        move_vectors = [pygame.math.Vector2(0, -self.speed),  # Góra
                        pygame.math.Vector2(0, self.speed),  # Dół
                        pygame.math.Vector2(-self.speed, 0),  # Lewo
                        pygame.math.Vector2(self.speed, 0)]  # Prawo
        for i in range(4):
            if (i == 0 and self.moving_up) or (i == 1 and self.moving_down) or (
                    i == 2 and self.moving_left) or (
                    i == 3 and self.moving_right):
                _speed = self.speed
                # Do obecnej pozycji punktu feet dodaje vektor ruchu...
                _feet = self.rect.midbottom + move_vectors[i]
                # ...po czym sprawdza, czy nie spowoduje to kolizji z przeszkodą
                for obstacle in self.obstacles:
                    if obstacle.rect.collidepoint(_feet):
                        _speed = 0
                        break
                if i == 0:  # Przesuń y o speed w górę
                    self.rect.y -= _speed
                elif i == 1:  # Przesuń y o speed w dół
                    self.rect.y += _speed
                elif i == 2:  # Przesuń x o speed w lewo
                    self.rect.x -= _speed
                elif i == 3:  # Przesuń x o speed w prawo
                    self.rect.x += _speed

    def _ai(self):
        """Sprawdza gdzie obecnie znajduje się gracz i przemieszcza wroga w
        jego stronę."""

        self_feet = self.rect.midbottom
        player_feet = self.program.player.feet

        # Sprawdź, czy jesteś w zasięgu zainteresowania gracza.
        range_x = 200
        range_y = 200
        dist_x = self_feet[0] - player_feet[0]
        dist_y = self_feet[1] - player_feet[1]

        if player_feet[0] - range_x < self_feet[0] < player_feet[0] + range_x:
            if player_feet[0] > self_feet[0] and self_feet != player_feet:
                self.moving_left = 0
                self.moving_right = 1
            if player_feet[0] < self_feet[0] and self_feet != player_feet:
                self.moving_right = 0
                self.moving_left = 1
        if player_feet[1] - range_y < self_feet[1] < player_feet[1] + range_y:
            if player_feet[1] > self_feet[1] and self_feet != player_feet:
                self.moving_up = 0
                self.moving_down = 1
            if player_feet[1] < self_feet[1] and self_feet != player_feet:
                self.moving_down = 0
                self.moving_up = 1



        # Jeżeli wróg jest poza zasięgiem zainteresowania x
        # if self_feet[0] < player_feet[0] - range_x:
        #     self.moving_left = 0
        #     self.moving_right = 1
        # elif self_feet[0] > player_feet[0] + range_x:
        #     self.moving_right = 0
        #     self.moving_left = 1

        # # Jeżeli wróg jest poza zasięgiem zmierzania do gracza.
        # if self_feet[1] < player_feet[1] - range_y:
        #     self.moving_up = 0
        #     self.moving_down = 1
        # elif self_feet[1] > player_feet[1] + range_y:
        #     self.moving_down = 0
        #     self.moving_up = 1
        # else:
        #     self.moving_up = 0
        #     self.moving_down = 0
        # if self_feet[0] < player_feet[0] - range_x:
        #     self.moving_left = 0
        #     self.moving_right = 1
        # elif self_feet[0] > player_feet[0] + range_x:
        #     self.moving_right = 0
        #     self.moving_left = 1
        # else:
        #     self.moving_left = 0
        #     self.moving_right = 0
        # # Jeżeli wróg jest w zasięgu zmierzania do gracza.
        # if self_feet[1] >= player_feet[1] - range_y and \
        #         self_feet[1] <= player_feet[1] + range_y:
        #     if dist_x < 0:
        #         self.moving_left = 0
        #         self.moving_right = 1
        #     elif dist_x > 0:
        #         self.moving_right = 0
        #         self.moving_left = 1
        # if self_feet[0] >= player_feet[0] - range_x and \
        #         self_feet[0] <= player_feet[1] + range_x:
        #     if dist_y < 0:
        #         print("asd")
        #         self.moving_up = 0
        #         self.moving_down = 1
        #     elif dist_y < 0:
        #         self.moving_down = 0
        #         self.moving_up = 1

    # if player_feet[0] > self_feet[0] and self_feet != player_feet:
    #     self.moving_left = 0
    #     self.moving_right = 1
    # if player_feet[0] < self_feet[0] and self_feet != player_feet:
    #     self.moving_right = 0
    #     self.moving_left = 1
    # if player_feet[1] > self_feet[1] and self_feet != player_feet:
    #     self.moving_up = 0
    #     self.moving_down = 1
    # if player_feet[1] < self_feet[1] and self_feet != player_feet:
    #     self.moving_down = 0
    #     self.moving_up = 1

    def update(self):
        self._ai()
        self._animation_state()
        self._move()

    def display(self):
        self.program.camera.camera_draw(self.image, self.rect.topleft)

        DEV = 1
        if DEV:
            self._draw_rect()

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (255, 0, 0), rect, 2)
