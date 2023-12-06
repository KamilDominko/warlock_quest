import random

import pygame
import math

from xp_orb import XpOrb
from enemy_interface import EnemyInterface


class Skeleton(EnemyInterface):
    ENEMY_ID = "skeleton"

    def __init__(self, program, centerx, centery):
        super().__init__(program)
        self.image = self.tM[self.ENEMY_ID.lower()]["idle"][0]
        self.rect = self.image.get_rect(center=(centerx, centery))
        width = 32
        height = 16
        if self.program.settings.scaleX != 1:
            width *= program.settings.scaleX
            height *= program.settings.scaleY
        self.feet = self.image.get_rect(center=self.rect.midbottom,
                                        width=width, height=height)
        self.hitbox = self.image.get_rect(center=self.rect.midbottom,
                                          width=width)
        self.radius = math.sqrt((self.feet.w / 2) ** 2 + self.feet.h ** 2) + 1
        self.boundingRect = pygame.Rect(0, 0, 2 * self.radius, 2 * self.radius)
        self.currentHealth = self.stats["health"]

    def _check_animation_state(self, state, animation):
        if state:
            self.animationIndex += 0.1
            if self.animationIndex >= len(animation):
                self.animationIndex = 0
            self.image = animation[int(self.animationIndex)]

    def _animation_state(self):
        if not self._stateUp and not self._stateDown and not \
                self._stateLeft and not self._stateRight:
            self.animationIndex += 0.05
            filesAmount = len(self.tM["skeleton"]["idle"])
            if self.animationIndex >= filesAmount:
                self.animationIndex = 0
            self.image = self.tM["skeleton"]["idle"][int(
                self.animationIndex)]
        self._check_animation_state(self._stateUp,
                                    self.tM["skeleton"]["move_up"])
        self._check_animation_state(self._stateDown,
                                    self.tM["skeleton"]["move_down"])
        self._check_animation_state(self._stateLeft,
                                    self.tM["skeleton"]["move_left"])
        self._check_animation_state(self._stateRight,
                                    self.tM["skeleton"]["move_right"])

    def _attack(self, target):
        damage = random.choice(self.stats["damage"])
        target.deal_damage(damage)

    def die(self):
        # Stwórz XP orb w miejscu stóp
        xpOrb = XpOrb(self.program, self.feet.centerx, self.feet.centery)
        self.program.expOrbs.add(xpOrb)
        # self.program.camera.add(xpOrb)
        # KYS
        self.kill()

    def _move(self):
        """Odpowiada za poruszanie się gracza oraz detekcję kolizji z
        przeszkodami, przez które gracz nie może przejść. """
        # Inicjalizacja prędkości w pionie i poziomie na podstawie stanów klawiszy
        speed = pygame.math.Vector2(0, 0)
        if self._stateLeft:
            speed.x = -self.stats["speed"]
        elif self._stateRight:
            speed.x = self.stats["speed"]
        if self._stateUp:
            speed.y = -self.stats["speed"]
        elif self._stateDown:
            speed.y = self.stats["speed"]
        # Znormalizuj wektor prędkości, aby utrzymać stałą prędkość niezależnie od kierunku
        if speed.length() > 0:
            speed = speed.normalize() * self.stats["speed"]
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
            if length > self.stats["speed"]:
                # Ustaw odpowiednie prędkości w zależności od kierunku
                if not self.feet.left < self.program.player.feet.right:
                    self._stateLeft = normalized_vector[0] < 0
                else:
                    self._stateLeft = 0
                if not self.feet.right > self.program.player.feet.left:
                    self._stateRight = normalized_vector[0] > 0
                else:
                    self._stateRight = 0
                if not self.feet.top < self.program.player.feet.bottom:
                    self._stateUp = normalized_vector[1] < 0
                else:
                    self._stateUp = 0
                if not self.feet.bottom > self.program.player.feet.top:
                    self._stateDown = normalized_vector[1] > 0
                else:
                    self._stateDown = 0
            else:
                # Zatrzymaj wroga, gdy jest wystarczająco blisko gracza
                self._stateLeft = False
                self._stateRight = False
                self._stateUp = False
                self._stateDown = False

    def deal_damage(self, damage):
        self.aM.play("hit", 3)
        self.program.interface.add_hits(self.rect.midtop, damage)
        self.currentHealth -= damage
        self.hited = pygame.time.get_ticks()
        if self.currentHealth <= 0:
            self.die()

    def _check_if_hited(self):
        if self.hited:
            if pygame.time.get_ticks() - self.hited < 200:
                mask = pygame.mask.from_surface(self.image)
                maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                          setcolor=(150, 0, 0, 150))
                point = self.program.camera.update_point(self.rect.topleft)
                self.program.screen.blit(maksSrf, point)
            else:
                self.hited = 0

    def _check_if_selected(self):
        if self.selected:
            mask = pygame.mask.from_surface(self.image)
            maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                      setcolor=(255, 255, 255, 150))
            point = self.program.camera.update_point(self.rect.topleft)
            self.program.screen.blit(maksSrf, point)

            self.selected = False

    def rect_circle_collision(self, rect):
        # Sprawdź, czy prostokąt i okrąg mają przecinające się prostokąty
        self.boundingRect.center = self.feet.center
        if rect.colliderect(self.boundingRect):
            # Sprawdź, czy którakolwiek krawędź prostokąta znajduje się w
            # odległości nie większej niż promień okręgu od jego centrum
            for corner in [(rect.left, rect.top),
                           (rect.right, rect.top),
                           (rect.left, rect.bottom),
                           (rect.right, rect.bottom)]:
                distance = math.sqrt(
                    (self.feet.centerx - corner[0]) ** 2 + (
                            self.feet.bottom - corner[1]) ** 2)
                if distance <= self.radius:
                    return True
            # # Sprawdź, czy środek okręgu znajduje się w prostokącie
            # return rect.collidepoint(self.feet.centerx,
            #                          self.feet.bottom)
        return False

    def _check_range(self):
        player = self.program.player
        if self.rect_circle_collision(player.feet) and not player.hited:
            if self.reload == 0:
                self.reload = pygame.time.get_ticks()
                self._attack(player)
            if pygame.time.get_ticks() - self.reload \
                    > 1000 // self.stats["attack_speed"]:
                self.reload = pygame.time.get_ticks()
                self._attack(player)

    def update(self):
        self._ai()
        self._check_range()
        self._animation_state()
        self._move()
        self.feet.midbottom = self.rect.midbottom
        self.hitbox.midbottom = self.rect.midbottom

    def display(self):
        self.program.camera.camera_draw(self.image, self.rect.topleft)

        self._check_if_hited()
        self._check_if_selected()
