class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.title = "Warlock Quest"
        self.fps = 60

        self.player_health = 150
        self.player_health_regen = 1
        self.player_mana = 300
        self.player_mana_regen = 5
        self.player_stamina = 200
        self.player_stamina_regen = 3
        self.player_speed = 5
        self.player_sprint = 7
        self.player_attack_speed = 20.0

        self.enemy_speed = 1
        self.enemy_health = 100

        self.projectile_speed = 17
        self.projectile_damage = 35
        self.projectile_hits = 3

        self.field_size = 128

        self.BLACK = (0, 0, 0)

    def get_res(self):
        return self.screen_width, self.screen_height
