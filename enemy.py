import math

import pygame

import os
import random

from xp_orb import XpOrb


class Enemy(pygame.sprite.Sprite):
    def __init__(self, program, centerx, centery):
        super().__init__()
        self.program = program
        self.image = pygame.image.load(
            "res/graphic/enemy/enemy.png").convert_alpha()
        self.rect = self.image.get_rect(center=(centerx, centery))
        self.feet = self.image.get_rect(center=self.rect.midbottom,
                                        width=32, height=32)
        self.hitbox = self.image.get_rect(center=self.rect.midbottom,
                                          width=32, height=128)
        self.hited = 0
        self.selected = False
        self.speed = program.settings.enemy_speed
        self.speed += random.randrange(2)
        self.max_healt = program.settings.enemy_health
        self.current_healt = self.max_healt
        self.moving_up = 0
        self.moving_down = 0
        self.moving_left = 0
        self.moving_right = 0
        self.animation_index = 0
        self._load_animations()
        self.obstacles = program.map.obstacles
        program.map.obstacles.add(self)

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

    # def _move(self):
    #     move_vectors = [pygame.math.Vector2(0, -self.speed),  # Góra
    #                     pygame.math.Vector2(0, self.speed),  # Dół
    #                     pygame.math.Vector2(-self.speed, 0),  # Lewo
    #                     pygame.math.Vector2(self.speed, 0)]  # Prawo
    #     for i in range(4):
    #         if (i == 0 and self.moving_up) or (i == 1 and self.moving_down) or (
    #                 i == 2 and self.moving_left) or (
    #                 i == 3 and self.moving_right):
    #             _speed = self.speed
    #             # Do obecnej pozycji punktu feet dodaje vektor ruchu...
    #             _feet = self.rect.midbottom + move_vectors[i]
    #             # ...po czym sprawdza, czy nie spowoduje to kolizji z przeszkodą
    #             for obstacle in self.obstacles:
    #                 if obstacle.rect.collidepoint(_feet):
    #                     _speed = 0
    #                     break
    #             if i == 0:  # Przesuń y o speed w górę
    #                 self.rect.y -= _speed
    #             elif i == 1:  # Przesuń y o speed w dół
    #                 self.rect.y += _speed
    #             elif i == 2:  # Przesuń x o speed w lewo
    #                 self.rect.x -= _speed
    #             elif i == 3:  # Przesuń x o speed w prawo
    #                 self.rect.x += _speed

    def deal_damage(self, damage):
        self.current_healt -= damage
        self.hited = pygame.time.get_ticks()
        if self.current_healt <= 0:
            self.die()

    def die(self):
        # Stwórz XP orb w miejscu stóp
        xpOrb = XpOrb(self.program, self.feet.centerx, self.feet.centery)
        self.program.items.add(xpOrb)
        self.program.camera.add(xpOrb)
        # KYS
        self.kill()

    def _move(self):
        """Odpowiada za poruszanie się gracza oraz detekcje kolizji z
        przeszkodami, przez które gracz nie może przejść."""
        # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
        speed_x = -self.speed if self.moving_left else self.speed if self.moving_right else 0
        speed_y = -self.speed if self.moving_up else self.speed if self.moving_down else 0
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
                        speed_x = 0
                    elif speed_x < 0:
                        speed_x = 0
                # Sprawdza kolizje z przeszkodami w pionie
                if new_rect_y.colliderect(obstacle.feet):
                    if speed_y > 0:
                        speed_y = 0
                    elif speed_y < 0:
                        speed_y = 0
            # Aktualizuje pozycję self.feet
        self.feet.x += speed_x
        self.feet.y += speed_y
        # Aktualizuje pozycję self.rect na podstawie self.feet
        self.rect.midbottom = self.feet.midbottom

    def _ai(self):
        """Sprawdza gdzie obecnie znajduje się gracz i przemieszcza wroga w
        jego stronę."""

        self_feet = self.rect.midbottom
        player_feet = self.program.player.feet.midbottom

        # Oblicz wektor kierunku od wroga do gracza
        vector = (player_feet[0] - self_feet[0], player_feet[1] - self_feet[1])

        # Oblicz długość wektora
        length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

        # Unikaj dzielenia przez zero
        if length != 0:
            # Normalizuj wektor
            normalized_vector = (vector[0] / length, vector[1] / length)

            # Sprawdź, czy wrogowi nie zostało już zbyt mało do przesunięcia
            if length > self.speed:
                # Ustaw odpowiednie prędkości w zależności od kierunku
                if not self.feet.left < self.program.player.feet.right:
                    self.moving_left = normalized_vector[0] < 0
                else:
                    self.moving_left = 0
                if not self.feet.right > self.program.player.feet.left:
                    self.moving_right = normalized_vector[0] > 0
                else:
                    self.moving_right = 0
                if not self.feet.top < self.program.player.feet.bottom:
                    self.moving_up = normalized_vector[1] < 0
                else:
                    self.moving_up = 0
                if not self.feet.bottom > self.program.player.feet.top:
                    self.moving_down = normalized_vector[1] > 0
                else:
                    self.moving_down = 0
            else:
                # Zatrzymaj wroga, gdy jest wystarczająco blisko gracza
                self.moving_left = False
                self.moving_right = False
                self.moving_up = False
                self.moving_down = False

    def update(self):
        self._ai()
        self._animation_state()
        self._move()
        self.feet = self.image.get_rect(width=48, height=16,
                                        midbottom=self.rect.midbottom)
        self.hitbox = self.image.get_rect(width=32, height=128,
                                          midbottom=self.rect.midbottom)

    def _check_if_hited(self):
        if self.hited:
            if pygame.time.get_ticks() - self.hited < 200:
                mask = pygame.mask.from_surface(self.image)
                maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                          setcolor=(150, 0, 0, 150))
                point = self.program.camera.update_point((self.rect.topleft))
                self.program.screen.blit(maksSrf, point)
            else:
                self.hited = 0

    def _check_if_selected(self):
        if self.selected:
            mask = pygame.mask.from_surface(self.image)
            maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                      setcolor=(255, 255, 255, 150))
            point = self.program.camera.update_point((self.rect.topleft))
            self.program.screen.blit(maksSrf, point)

            self.selected = False

    def display(self):
        self.program.camera.camera_draw(self.image, self.rect.topleft)

        self._check_if_hited()
        self._check_if_selected()

        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_feet_rect()
            self._draw_hit_box()
            self._draw_mask()

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _draw_feet_rect(self):
        feet_rect = self.program.camera.update_rect(self.feet)
        pygame.draw.rect(self.program.screen, (0, 0, 255), feet_rect, 3)

    def _draw_hit_box(self):
        hitBox = self.program.camera.update_rect(self.hitbox)
        pygame.draw.rect(self.program.screen, (255, 0, 0), hitBox, 2)

    def _draw_mask(self):
        mask = pygame.mask.from_surface(self.image)
        maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(150, 0,
                                                                     0, 150))
        # maksSrf.fill((0, 255, 0))
        point = self.program.camera.update_point((self.rect.topleft))
        self.program.screen.blit(maksSrf, point)
