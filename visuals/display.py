import pygame
from settings import Settings
from icon import Icon


class Display:
    """Клас Дисплей, що має вбудовані три циферблати"""
    def __init__(self, game_settings: Settings, screen: pygame.surface.Surface,
                 x1: int, y1: int, counter: list, icon: Icon = None) -> None:
        self.game_settings = game_settings
        self.screen = screen

        self.icon = icon

        self.example_image = pygame.image.load('images/0.1.png').convert()

        self.rect1 = self.example_image.get_rect()
        self.rect2 = self.example_image.get_rect()
        self.rect3 = self.example_image.get_rect()

        self.rect1.x = x1
        self.rect2.x = self.rect1.x+self.rect1.width+3
        self.rect3.x = self.rect2.x+self.rect2.width+3

        self.rect1.y, self.rect2.y, self.rect3.y, = y1, y1, y1

        self.counter = counter

    def blit_display(self) -> None:
        if self.icon:
            self.icon.blit_me()
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(self.rect1.x-5, self.rect1.y-5, self.rect1.width*3+16, self.rect1.height+10))
        self.screen.blit(pygame.image.load(f'images/{self.counter[0]}.1.png').convert(), self.rect1)
        self.screen.blit(pygame.image.load(f'images/{self.counter[1]}.1.png').convert(), self.rect2)
        self.screen.blit(pygame.image.load(f'images/{self.counter[2]}.1.png').convert(), self.rect3)

    def display_plus_one(self) -> None:
        self.counter = [int(i) for i in str(int(''.join([str(i) for i in self.counter])) + 1)]
        while len(self.counter) != 3:
            self.counter.insert(0, 0)
        if self.counter[0] == 9 and self.counter[1] == 9 and self.counter[2] == 9:
            self.counter = [0, 0, 0]

    def display_minus_one(self) -> None:
        self.counter = [int(i) for i in str(int(''.join([str(i) for i in self.counter])) - 1)]
        while len(self.counter) != 3:
            self.counter.insert(0, 0)

    def got_mines(self) -> bool:
        for i in self.counter:
            if i:
                return True
        return False

    def change_icon(self, icon: Icon) -> None:
        self.icon = icon
