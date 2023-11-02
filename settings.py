class Settings:
    """Klasa przechowująca kluczowe dane dla działania programu."""

    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.title = "Makaron"
        self.fps = 60

        self.player_speed = 4
        self.player_sprint = 8

        self.projectile_speed = 2

        self.field_size = 64

    def get_res(self):
        return (self.screen_width, self.screen_height)
