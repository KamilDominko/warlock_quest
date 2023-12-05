import pygame


# CHANNELS:
# 0. [MUSIC]
# 1. shoot
# 2. laser
# 3. hit
# 4. xp_orb
# 5. lvlUp
# 6. [EMPTY]
# 7. [EMPTY]

class AudioManager:
    def __init__(self, program):
        self.program = program
        self.settings = program.settings
        self.sounds = {}
        self._load_audios()

    def _load_audios(self):
        sV = self.settings.soundVolume
        self._load_audio("sounds", "hit", sV)
        self._load_audio("sounds", "lvlUp", sV)
        self._load_audio("sounds", "xpOrb", sV * 0.33)
        self._load_audio("sounds", "shoot", sV * 0.4)
        self._load_audio("sounds", "laser", sV * 0.5)

    def _load_file(self, folder, file_name, volume, file_extension=".wav"):
        _name = file_name
        self.sounds[_name] = {}
        path = f"res/audio/{folder}/{_name}{file_extension}"
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound

    def _load_audio(self, folder, name, volume):
        sound = self._load_file(folder, name, volume)
        self.sounds[name] = sound

    def play(self, name, channel):
        sound = self.sounds[name]
        pygame.mixer.Channel(channel).play(sound)

    def stop(self, channel):
        pygame.mixer.Channel(channel).stop()
