import pygame


class Settings:
    """Settings class"""

    def __init__(self) -> None:
        """Init the game settings"""
        # Screen settings
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.bg_color = '#139917'

        # Sounds
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.click_sound = pygame.mixer.Sound("sounds/click.wav")
        self.flag_sound = pygame.mixer.Sound("sounds/flag.wav")
        self.flag_sound_backwards = pygame.mixer.Sound("sounds/flag_backwards.wav")

        # Font
        self.font = pygame.font.Font(None, 52)

        # Frames
        self.frame_rate = 60
        self.frame_count = 0

        # Mines count
        self.mines = 30
