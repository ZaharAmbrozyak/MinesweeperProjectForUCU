import pygame


class Settings:
    """Settings class"""

    def __init__(self, x: int, y: int, mines: int, button_w: int = 64, button_h: int = 64,
                 extra_x: int = 22, extra_y: int = 128) -> None:
        """Init the game settings"""
        # Screen settings
        self.game_active = False
        self.first_time_play = True
        self.extra_x = extra_x
        self.extra_y = extra_y
        self.x = x
        self.y = y
        self.button_w = button_w
        self.button_h = button_h
        self.screen_width = x * 32 + extra_x
        self.screen_height = y * 32 + extra_y
        self.bg_color = '#139917'

        # Sounds
        self.explosion_sound = pygame.mixer.Sound('visuals/sounds/boom.wav')
        self.click_sound = pygame.mixer.Sound("visuals/sounds/click.wav")
        self.flag_sound = pygame.mixer.Sound("visuals/sounds/flag.wav")
        self.flag_sound_backwards = pygame.mixer.Sound("visuals/sounds/flag_backwards.wav")

        # Font
        self.font = pygame.font.Font(None, 52)

        # Frames
        self.frame_rate = 60
        self.frame_count = 0

        # Mines count
        self.mines = mines
