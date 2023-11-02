class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.title = "Warlock Quest"
        self.fps = 60

        self.player_speed = 3
        self.player_sprint = 5

        self.projectile_speed = 11

        self.field_size = 64

    def get_res(self):
        return self.screen_width, self.screen_height
