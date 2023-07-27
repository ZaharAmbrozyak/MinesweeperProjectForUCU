import pygame


class Settings:
    """Settings class"""

    def __init__(self, x: int, y: int, button_w: int = 64, button_h: int = 64,
                 extra_x: int = 22, extra_y: int = 128) -> None:
        """Init the game settings"""
        # Screen settings
        self.game_active = True
        info = pygame.display.Info()
        self.screen_width = x * button_w + extra_x
        self.screen_height = y * button_h + extra_y
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
