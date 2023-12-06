import math

import pygame

from weapon_image import WeaponImage
from upgrade import Upgrade
from src.weapons.magic_projectile import MagicProjectile
from src.weapons.magic_laser import MagicLaser


class Player(pygame.sprite.Sprite):
    def __init__(self, program, x=500, y=500):
        super().__init__()
        self.program = program
        self.tM = program.textureManager
        self.aM = program.audioManager
        self.x = x
        self.y = y
        self.image = self.tM.textures["player"]["idle"][0]
        self.rect = self.image.get_rect(center=(x, y))
        width = 32
        height = 16
        if self.program.settings.scaleX != 1 and \
                self.program.settings.scaleY != 1:
            width *= program.settings.scaleX
            height *= program.settings.scaleY
        self.feet = self.image.get_rect(center=self.rect.midbottom,
                                        width=width, height=height)
        self.stats = {"health": program.settings.player_health,
                      "health_regen": program.settings.player_health_regen,
                      "mana": program.settings.player_mana,
                      "mana_regen": program.settings.player_mana_regen,
                      "stamina": program.settings.player_stamina,
                      "stamina_regen": program.settings.player_stamina_regen,
                      "sprint": program.settings.player_sprint,
                      "attack_speed": program.settings.player_attack_speed,
                      "radius": program.settings.player_radius}
        self.level = 1
        self.experience = 0
        self.walk = program.settings.player_speed
        self.currentHealth = self.stats["health"]
        self.currentMana = self.stats["mana"]
        self.currentStamina = self.stats["stamina"]
        self.regenTime = 0
        self.speed = self.walk
        self.sprintTime = 0
        self.weaponImg = WeaponImage(self, self.program)
        self.defaultProjectile = MagicProjectile(self)
        self.defaultLaser = MagicLaser(self)
        self.reload = 0
        self.attack = 0
        self.primaryAttack = False
        self.secondAttack = False
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
            filesAmount = len(self.tM.textures["player"]["idle"])
            if self.animationIndex >= filesAmount:
                self.animationIndex = 0
            self.image = self.tM.textures["player"]["idle"][
                int(self.animationIndex)]
        else:
            self._stateIdle = 0
        self._check_animation_state(self._stateUp, self.tM.textures[
            "player"]["move_up"])
        self._check_animation_state(self._stateDown, self.tM.textures[
            "player"]["move_down"])
        self._check_animation_state(self._stateLeft, self.tM.textures[
            "player"]["move_left"])
        self._check_animation_state(self._stateRight, self.tM.textures[
            "player"]["move_right"])

    def _move(self):
        """Odpowiada za poruszanie się gracza oraz detekcję kolizji z
        przeszkodami, przez które gracz nie może przejść. """
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

    def _check_if_hited(self):
        if self.hited:
            if pygame.time.get_ticks() - self.hited < 500:
                mask = pygame.mask.from_surface(self.image)
                maksSrf = mask.to_surface(unsetcolor=(0, 0, 0, 0),
                                          setcolor=(150, 0, 0, 150))
                point = self.program.camera.update_point(self.rect.topleft)
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
        self.experience += amount
        if self.experience >= 10 * self.level:
            self.aM.play("lvlUp", 5)
            self.aM.stop(1)
            self.aM.stop(2)
            self.aM.stop(3)
            self.aM.stop(4)
            self.level += 1
            self.experience = 0
            upgrade = Upgrade(self.program)
            upgrade.pick()
            del upgrade
            self._stateUp = 0
            self._stateDown = 0
            self._stateLeft = 0
            self._stateRight = 0
            self._stateSprint = 0
            self.speed = self.walk

    def input(self, event):
        """Funkcja sprawdza input z klawiatury i myszy dla gracza."""
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.primaryAttack = True
            if event.button == 3:
                self.secondAttack = True
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
                self.speed = self.walk
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.primaryAttack = False
            if event.button == 3:
                self.secondAttack = False


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
            self.speed = self.walk

    def _regen_health(self):
        if self.currentHealth < self.stats["health"] and not self.hited:
            self.currentHealth += self.stats["health_regen"]

    def _regen_mana(self):
        if self.currentMana < self.stats["mana"]:
            self.currentMana += self.stats["mana_regen"]

    def _regen_stamina(self):
        if not self._stateSprint or self._stateIdle:
            if self.currentStamina + self.stats["stamina_regen"] \
                    > self.stats["stamina"]:
                self.currentStamina = self.stats["stamina"]
            else:
                self.currentStamina += self.stats["stamina_regen"]

    def _regen(self):
        if pygame.time.get_ticks() - self.regenTime > 100:
            self.regenTime = pygame.time.get_ticks()
            self._regen_health()
            self._regen_mana()
            self._regen_stamina()

    def _check_circle_range(self):
        # Podświetla przeciwnika w zasięgu podnoszenia gracza.
        for enemy in self.program.enemies:
            if self._rect_circle_collision(enemy.feet):
                self.circleColor = (255, 0, 0)
                enemy.selected = True
            else:
                self.circleColor = (0, 255, 0)

    def _check_xp_orb(self):
        for item in self.program.expOrbs:
            if self._rect_circle_collision(item.rect) and not item.sucked:
                item.suck()

    def _rect_circle_collision(self, rect):
        # Sprawdź, czy prostokąt i okrąg mają przecinające się prostokąty
        bounding_rect = pygame.Rect(self.feet.centerx - self.stats["radius"],
                                    self.feet.bottom - self.stats["radius"],
                                    2 * self.stats["radius"],
                                    2 * self.stats["radius"])
        if rect.colliderect(bounding_rect):
            # Sprawdź, czy którakolwiek krawędź prostokąta znajduje się w
            # odległości nie większej niż promień okręgu od jego centrum
            for corner in [(rect.left, rect.top), (rect.right, rect.top),
                           (rect.left, rect.bottom), (rect.right, rect.bottom)]:
                distance = math.sqrt(
                    (self.feet.centerx - corner[0]) ** 2 + (
                            self.feet.bottom - corner[1]) ** 2)
                if distance <= self.stats["radius"]:
                    return True
            # Sprawdź, czy środek okręgu znajduje się w prostokącie
            return rect.collidepoint(self.feet.centerx, self.feet.bottom)
        return False

    def update(self):
        self._move()
        self.feet.midbottom = self.rect.midbottom
        if self.primaryAttack:
            # self.weaponImg.primary_attack()
            self.defaultProjectile.use()
        if self.secondAttack:
            # if self.currentMana > self.weaponImg.laser.cost * 10:
            #     self.weaponImg.secondary_attack()
            self.defaultLaser.use()
        else:
            self.defaultLaser.casting = False
            self.aM.stop(2)
        # UPDATE BRONI
        self.defaultProjectile.update()
        self.defaultLaser.update()

        self._check_sprint()
        self._regen()
        self._animation_state()
        center = self.program.camera.update_rect(self.rect)
        self.weaponImg.update(center.center)
        # self._check_circle_range()
        self._check_if_hited()
        self._check_xp_orb()

    def display(self):
        if not self._stateUp:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
        elif self._stateLeft or self._stateRight:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
        elif self._stateUp:
            self.program.camera.camera_draw(self.image, self.rect.topleft)
        self.weaponImg.display()
        self.defaultProjectile.display()
        self.defaultLaser.display()


        DEV = 0
        if DEV:
            self._draw_rect()
            self._draw_feet()
            self._draw_feet_rect()

    def _draw_rect(self):
        rect = self.program.camera.update_rect(self.rect)
        pygame.draw.rect(self.program.screen, (0, 255, 0), rect, 2)

    def _draw_feet(self):
        feet = self.program.camera.update_point(self.feet.midbottom)
        pygame.draw.circle(self.program.screen, (0, 0, 255), feet, 3)
        pygame.draw.circle(self.program.screen, self.circleColor,
                           feet, self.stats["radius"], 2)

    def _draw_feet_rect(self):
        feet_rect = self.program.camera.update_rect(self.feet)
        pygame.draw.rect(self.program.screen, (0, 0, 255), feet_rect, 3)
