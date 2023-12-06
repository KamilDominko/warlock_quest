import pygame

import random

from enemy import Enemy


class Spawner:
    def __init__(self, program):
        self.program = program
        self.enemies = program.enemies
        self.offspace = 150
        self.offset = 100
        self.scrW = program.screen.get_width()
        self.scrH = program.screen.get_height()
        self.spawnStart = pygame.time.get_ticks()
        self.spawnTime = 1000
        self.fsw = program.settings.field_width
        self.fsh = program.settings.field_height

    def _pick_position(self):
        playerFeet = self.program.player.feet.midbottom
        mapW = self.program.map.width
        mapH = self.program.map.height

        mapXrange = range(128, mapW - 128)
        mapYrange = range(128, mapH - 128)
        spawnXrange = range((playerFeet[0] - (self.scrW // 2 + self.offset)),
                            (playerFeet[0] + (self.scrW // 2 + self.offset)))
        spawnYrange = range((playerFeet[1] - (self.scrH // 2 + self.offset)),
                            (playerFeet[1] + (self.scrH // 2 + self.offset)))
        while True:
            spawnX = random.randrange(
                (playerFeet[0] - (self.scrW // 2 + self.offset)),
                (playerFeet[0] + (self.scrW // 2 + self.offset)))
            if spawnX in mapXrange:
                if spawnX in spawnXrange:
                    break
        while True:
            spawnY = random.randrange(
                (playerFeet[1] - (self.scrH // 2 + self.offset)),
                (playerFeet[1] + (self.scrH // 2 + self.offset)))
            if spawnY in mapYrange:
                if spawnY in spawnYrange:
                    break
        return spawnX, spawnY

    def _better_pick_position(self):
        # enemy size
        es = (64, 128)
        # map width
        mw = self.program.map.width
        # map height
        mh = self.program.map.height

        # nswe  N  S  W  E
        nswe = [0, 0, 0, 0]

        # weź współrzędne gracza
        playerXY = self.program.player.rect.center
        # print(playerXY)

        # Sprawdź w każdym kierunku, czy jest miejsce

        # czy jest miejsce u góry, czyli y > 0 + długość pola + obszar
        if playerXY[1] - (self.scrH / 2 + self.fsh + 2 * es[1]) > 0:
            nswe[0] = 1

        # czy jest miejsce na dole, czyli y < wysokość mapy + pola + obszar
        if playerXY[1] + (self.scrH / 2 + self.fsh + 2 * es[1]) < mh:
            nswe[1] = 1

        # czy jest miejsce na lewo, czyli czy x > 0 + długość pola + obszar
        if playerXY[0] - (self.scrW / 2 + self.fsw + 2 * es[0]) > 0:
            nswe[2] = 1

        # czy jest miejsce na prawo, czyli x < długość mapy + pola + obszar
        if playerXY[0] + (self.scrW / 2 + self.fsw + 2 * es[0]) < mw:
            nswe[3] = 1

        # Określ przedział, z którego można wybrać współrzędne

        przedzialX = list()
        przedzialY = list()

        # X

        # jeżeli jest wolne z lewej
        if nswe[2]:
            przedzialX += list(range(int(0 + self.fsw + es[0] / 2),
                                     int(playerXY[0] - self.scrW / 2)))

        # jeżeli jest wolne z prawej
        if nswe[3]:
            przedzialX += list(range(int(playerXY[0] + self.scrW / 2),
                                     int(mw - self.fsw - es[0] / 2)))

        # Y

        # jeżeli jest wolne u góry
        if nswe[0]:
            przedzialY += list(range(int(0 + self.fsh + es[1] / 2),
                                     int(playerXY[1] - self.scrH / 2)))

        # jeżeli jest wolne na dole
        if nswe[1]:
            przedzialY += list(range(int(playerXY[1] + self.scrH / 2),
                                     int(mh - self.fsh - es[1] / 2)))

        # wybierz losowo X Y z przedziałów

        x = random.choice(przedzialX)
        y = random.choice(przedzialY)

        return x, y

    def _even_better_pick_position(self):
        # enemy size
        es = (64, 128)
        # map width
        mw = self.program.map.width
        # map height
        mh = self.program.map.height

        playerXY = self.program.player.rect.center

        # obszar mapy z wyłączeniem ścian
        mf = pygame.Rect(0 + self.fsw + es[0] / 2,
                         0 + self.fsh + es[1] / 2,
                         mw - 2 * (self.fsw + es[0] / 2),
                         mh - 2 * (self.fsh + es[1] / 2))

        # obszar widzenia gracza
        pfx = int(playerXY[0] - self.scrW / 2)
        pfy = int(playerXY[1] - self.scrH / 2)
        pf = pygame.Rect(pfx, pfy, self.scrW, self.scrH)

        # obszar spawnu
        spawnWidth = es[0] * 3
        spawnHeight = es[1] * 3

        sfx = int(playerXY[0] - (self.scrW / 2 + spawnWidth))
        sfy = int(playerXY[1] - (self.scrH / 2 + spawnHeight))

        sf = pygame.Rect(0, 0, self.scrW + 2 * spawnWidth,
                         self.scrH + 2 * spawnHeight)
        sf.center = playerXY

        # print("PF", pf)
        # print("SF", sf)

        # wybierz punkt z obszaru spawnu
        while True:
            x = random.randrange(sf.x, sf.x + sf.w)
            y = random.randrange(sf.y, sf.y + sf.h)
            point = (x, y)
            # sprawdź, czy punk jest w obszarze mapy
            if mf.collidepoint(point):
                # sprawdź, czy punkt nie jest w obszarze widzenia gracza
                if not pf.collidepoint(point):
                    # sprawdź, czy w tym miejscu nie ma już wroga
                    if self.enemies:
                        tempRect = pygame.Rect(0, 0, 32, 16)
                        tempRect.center = point
                        for enemy in self.enemies:
                            if not enemy.feet.colliderect(tempRect):
                                # if not enemy.feet.collidepoint(point):
                                return x, y
                                # break
                    else:
                        return x, y
            # else:
            #     print("XD")

    def _update(self):
        if pygame.time.get_ticks() - self.spawnStart >= self.spawnTime and \
                len(self.program.enemies) < 300:
            self.spawnStart = pygame.time.get_ticks()
            self.spawnTime = random.randrange(100, 500)
            # x, y = self._pick_position()

            x, y = self._even_better_pick_position()
            # self._even_better_pick_position()

            enemy = Enemy(self.program, x, y)
            self.program.camera.add(enemy)
            self.program.enemies.add(enemy)

    def create_enemy(self):
        pos = self._even_better_pick_position()
        return pos

    def update(self):
        # self._update()
        pass
