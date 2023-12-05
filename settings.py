class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080

        # self.screen_width = 2560
        # self.screen_height = 1440

        self.title = "Warlock Quest"
        self.fps = 60
        self.scaleX = 1
        self.scaleY = 1
        self.field_width = 128
        self.field_height = 128
        self.set_scale(self.screen_width, self.screen_height)

        self.player_health = 100
        self.player_health_regen = 0.1
        self.player_mana = 150
        self.player_mana_regen = 0.7
        self.player_stamina = 50
        self.player_stamina_regen = 0.5
        self.player_stamina_drain = 0.7
        self.player_speed = 4
        self.player_sprint = 7
        self.player_attack_speed = 1.0
        self.player_radius = 100

        self.enemy_speed = 1
        self.enemy_health = 100
        self.enemy_damage = 5
        self.enemy_attack_speed = 1

        self.weapon_attack_speed = 2.0
        self.projectile_speed = 33
        self.projectile_damage = range(20, 35)
        self.projectile_hits = 2
        self.laser_damage = range(15, 25)
        self.laser_range = 400

        self.soundVolume = 0.15
        self.musicVolume = 0.3

        self.BLACK = (0, 0, 0)

    def get_res(self):
        return self.screen_width, self.screen_height

    def set_scale(self, width, height):
        self.scaleX = width / 1920
        self.scaleY = height / 1080

        self.field_width = int(128 * self.scaleX)
        self.field_height = int(128 * self.scaleY)
