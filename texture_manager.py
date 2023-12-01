import os

import pygame


class TextureManager:
    """Klasa, która ładuje potrzebne do działania gry tekstury. """

    def __init__(self, program):
        self.program = program
        self.settings = program.settings
        self.textures = {}
        self._load_textures()

        # self._print_loaded_textures()

    def _print_loaded_textures(self):
        # print(self.textures)
        for entity in self.textures:
            print(entity)
            for anim in self.textures[entity]:
                print("\t", anim)
                # if entity == "lasers":
                #     for surface in self.textures[entity][anim]:
                #         print(surface)
                # for surface in self.textures[entity][anim]:
                #     print("\t", "\t", surface)

    def _load_textures(self):
        self._load_player()
        self._load_projectiles()
        self._load_lasers()
        self._load_enemy()
        self._load_map()
        self._load_weapon()

    def _load_animations(self, animations, file_name):
        """Funkcja ładuje obrazy do animacji i dodaje je do głównego słownika
        animacji. Pobiera dwa argumenty: listę nazw animacji oraz nazwę
        pliku, którą dodaje."""
        self.textures[file_name] = {}
        for animation in animations:
            path = f"res/graphic/{file_name}/{file_name}_{animation}"
            animationPack = self._load_images(path, file_name, animation)
            self.textures[file_name].update({animation: animationPack})

    def _load_images(self, path, img_name, animation, file_extension=".png"):
        """Funkcja ładująca obrazy do animacji sprite'a. Pobiera trzy
        argumenty: ścieżkę do folderu z animacją, nazwę animacji BEZ jej
        indeksu oraz listę z nazwami animacji."""
        animationPack = []
        files_count = len(os.listdir(path))
        for i in range(files_count):
            img = pygame.image.load(
                f"{path}/{img_name}_{animation}{i + 1}{file_extension}").convert_alpha()
            if self.program.settings.scaleX != 1 and \
                    self.program.settings.scaleY != 1:
                rect = img.get_rect()
                img = pygame.transform.scale(img,
                                             (rect.w * self.settings.scaleX,
                                              rect.h * self.settings.scaleY))
            animationPack.append(img)
        return animationPack

    def _load_image(self, path, file_name, file_extension=".png"):
        """Funkcja ładuje pojedynczy obrazek z podanego w argumencie path
        folderu znajdującego się w res/graphic/..."""
        p = f"res/graphic/{path}/{file_name}{file_extension}"
        image = pygame.image.load(p).convert_alpha()
        if self.program.settings.scaleX != 1 and \
                self.program.settings.scaleY != 1:
            rect = image.get_rect()
            image = pygame.transform.scale(image,
                                           (rect.w * self.settings.scaleX,
                                            rect.h * self.settings.scaleY))
        self.textures[path].update({file_name: image})

    def _load_projectiles(self):
        _projectile = "projectiles"
        self.textures[_projectile] = {}
        self._load_image(_projectile, "projectile")

    def _load_lasers(self):
        path = "res/graphic/lasers"
        self.textures["lasers"] = {}
        animationPack = self._load_images(path, "magic", "laser")
        self.textures["lasers"].update({"laser": animationPack})

    def _load_map(self):
        _map = "map"
        self.textures[_map] = {}
        self._load_image(_map, "stone_ground")
        self._load_image(_map, "stone_wall")
        self._load_image(_map, "stone_wall_n")
        self._load_image(_map, "stone_wall_s")
        self._load_image(_map, "stone_wall_w")
        self._load_image(_map, "stone_wall_e")
        self._load_image(_map, "stone_wall_inside")

    def _load_player(self):
        animations = ["idle", "move_up", "move_down", "move_left",
                      "move_right"]
        self._load_animations(animations, "player")

    def _load_enemy(self):
        animations = ["idle", "move_up", "move_down", "move_left",
                      "move_right"]
        self._load_animations(animations, "enemy")

    def _load_weapon(self):
        self.textures["weapons"] = {}
        self._load_image("weapons", "staff")
