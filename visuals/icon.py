import pygame
from settings import Settings


class Icon:
    def __init__(self, image_path: str, screen: pygame.surface.Surface,
                 game_settings: Settings, x: int, y: int) -> None:
        self.image = pygame.image.load(image_path)
        self.screen = screen
        self.game_settings = game_settings
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit_me(self) -> None:
        self.screen.blit(self.image, self.rect)
