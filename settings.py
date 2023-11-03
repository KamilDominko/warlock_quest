class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.title = "Warlock Quest"
        self.fps = 60

        self.player_speed = 5
        self.player_sprint = 7

        self.projectile_speed = 17

        self.field_size = 128

    def get_res(self):
        return self.screen_width, self.screen_height
