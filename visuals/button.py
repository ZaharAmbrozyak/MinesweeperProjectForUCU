import pygame
from pygame.sprite import Sprite
from settings import Settings


class Button(Sprite):
    """Button class"""

    def __init__(self, game_settings: Settings, screen: pygame.surface.Surface,
                 actual_image: str = '0', image_name: str = 'default',
                 hover_image_name: str = 'hover_default', x_pos: int = 0, y_pos: int = 0,
                 x: int = 0, y: int = 0):
        """Init button and set its pos"""
        super(Button, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Button events
        self.image_name = image_name
        self.hover_image_name = hover_image_name

        self.image = pygame.image.load(f'images/{self.image_name}.png').convert()
        self.actual_image = actual_image
        self.is_hover = False
        self.is_revealed = False
        self.rect = self.image.get_rect()

        # Button start pos
        self.rect.x = x
        self.rect.y = y
        self.coords = (x_pos, y_pos)

    def blit_me(self) -> None:
        """Малювання кнопки"""
        self.screen.blit(self.image, self.rect)

    def change_image(self, file_name: str) -> None:
        """
            Зміна зображення кнопки
        """
        self.image = pygame.image.load(f'images/{file_name}.png').convert()
        self.image_name = file_name
        self.hover_image_name = f'hover_{self.image_name}'
        self.is_hover = False

    def hover(self) -> None:
        """
            Метод, що починає анімовувати ефект наведення
        """
        if not self.is_hover:
            self.is_hover = True
            self.image = pygame.image.load(f'images/{self.hover_image_name}.png').convert()

    def stop_hover(self) -> None:
        """
            Метод, що дозволяє перестати анімовувати ефект наведення
        """
        if self.is_hover:
            self.is_hover = False
            self.image = pygame.image.load(f'images/{self.image_name}.png').convert()

    def on_click(self, image: str) -> None:
        """
            Метод, що змінює зображення кнопки після натиснення
        """
        self.change_image(image)
        self.is_revealed = True

    def get_coords(self) -> list:
        return self.coords
