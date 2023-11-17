class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.title = "Warlock Quest"
        self.fps = 60

        self.player_health = 100
        self.player_health_regen = 0.1
        self.player_mana = 200
        self.player_mana_regen = 5
        self.player_stamina = 50
        self.player_stamina_regen = 0.5
        self.player_stamina_drain = 0.7
        self.player_speed = 4
        self.player_sprint = 7
        self.player_attack_speed = 3.0
        self.player_radius = 100

        self.enemy_speed = 1
        self.enemy_health = 100
        self.enemy_damage = 5
        self.enemy_attack_speed = 1

        self.projectile_speed = 17
        self.projectile_damage = 35
        self.projectile_hits = 2

        self.field_size = 128

        self.BLACK = (0, 0, 0)

    def get_res(self):
        return self.screen_width, self.screen_height
