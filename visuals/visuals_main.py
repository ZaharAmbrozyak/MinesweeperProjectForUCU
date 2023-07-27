from sys import exit
import os
import pygame
from pygame.sprite import Group
from settings import Settings
from button import Button
from icon import Icon
from display import Display
from pygame.locals import *


def _get_number_buttons_x(game_settings: Settings, button_width: int) -> int:
    """
        Функція, що рахує та повертає кількість можливих полей на осі Х
    """
    available_space_x = game_settings.screen_width - 22
    number_buttons_x = int(available_space_x / button_width)

    return number_buttons_x


def _get_number_rows(game_settings: Settings, button_height: int) -> int:
    """
        Функція, що рахує та повертає кількість можливих рядів
    """
    available_space_y = game_settings.screen_height - button_height - 60
    number_rows = int(available_space_y / button_height)

    return number_rows


def _create_field(game_settings: Settings, screen: pygame.surface.Surface,
                  buttons: Group, button_number: int, row_number: int) -> None:
    """
        Функція, що створює кнопку button.
        Змінює свої координати X Y по формулі.
        Додає Кнопку до класу Group (списку спрайтів)
    """

    # Екземпляр кнопки
    button = Button(game_settings, screen)

    # Обрахунок координат
    button_width = button.rect.width
    button.x = button_width * button_number + 11
    button.y = button.rect.height + 54 + button.rect.height * row_number

    # Присвоєння координат об'єкту
    button.rect.x = button.x
    button.rect.y = button.y

    # Додаємо кнопку до списку кнопок Group
    buttons.add(button)


def create_fields(game_settings: Settings, screen: pygame.surface.Surface, buttons: Group) -> None:
    """
        Створює ігрове поле завдяки двох for-циклів.
        Використовує допоміжну функцію _create_button
    """
    # Екземпляр кнопки
    button = Button(game_settings, screen)

    # Прораховуєм кількість кнопок в одному рядку і саму кількість рядків
    number_buttons_x = _get_number_buttons_x(game_settings, button.rect.width)
    number_rows = _get_number_rows(game_settings, button.rect.height)

    # Створюєм ришітку кнопок - ігрове поле
    for button_number in range(number_buttons_x):
        for row_number in range(number_rows):
            _create_field(game_settings, screen, buttons, button_number, row_number)


def _button_keydown(event, buttons: Group, game_settings: Settings, mines_display=None):
    """
        Обробник помилок для ігрового поля (кнопок)
    """
    for button in buttons.sprites():
        if button.rect.collidepoint(event.pos):
            if event.button == 1 and button.image_name != 'flag' and not button.is_revealed:
                if button.actual_image == 'mine':
                    pygame.mixer.Sound.play(game_settings.explosion_sound)
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.Sound.play(game_settings.click_sound)
                    pygame.mixer.music.stop()

                    button.on_click()
            elif event.button == 3:
                if not button.is_revealed:
                    if button.image_name == 'flag':
                        pygame.mixer.Sound.play(game_settings.flag_sound_backwards)
                        pygame.mixer.music.stop()

                        if button.actual_image == 'mine':
                            game_settings.mines += 1
                        mines_display.display_plus_one()
                        button.change_image('default')
                    elif mines_display.got_mines():
                        pygame.mixer.Sound.play(game_settings.flag_sound)
                        pygame.mixer.music.stop()

                        if button.actual_image == 'mine':
                            game_settings.mines -= 1
                        mines_display.display_minus_one()
                        button.change_image('flag')


def buttons_hover(buttons: Group):
    for button in buttons.sprites():
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.hover()
        else:
            button.stop_hover()


def event_handler(buttons: Group, game_settings: Settings, mines_display) -> None:
    """
        Головний обробник помилок у грі
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            _button_keydown(event, buttons, game_settings, mines_display)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


def run_game() -> None:
    """
        Головна функція гри.
    """
    # Оптимізовуєм звук гри
    pygame.mixer.pre_init(44100, 16, 2, 4096)

    # Ініціалізація pygame
    pygame.init()

    # Створення об'єкту налаштувань гри
    game_settings = Settings()

    # Налаштовування вікна гри
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Minesweeper')
    pygame.display.set_icon(pygame.image.load('images/mine.png'))
    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode((
        game_settings.screen_width,
        game_settings.screen_height),
        flags,
        16)
    clock = pygame.time.Clock()

    # Обмежуєм кількість можливих кнопок, які можна натиснути. ОПТИМІЗАЦІЯ
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    # Створення ігрових об'єктів
    buttons = Group()
    sound_button = Button(game_settings, screen, 'sound_button_muted', 'sound_button',
                          'hover_sound_button', game_settings.screen_width/1.25, 20)
    buttons.add(sound_button)

    # Створюєм два дисплея: час та кількість мін
    clock_display = Display(game_settings, screen, game_settings.screen_width / 1.5, 20, [0, 0, 0])
    mines_display = Display(game_settings, screen, game_settings.screen_width / 4, 20, [0, 3, 0])

    # Додаєм іконки
    clock_display.change_icon(
        Icon('images/clock.png', screen, game_settings, clock_display.rect1.x - 60, 0))
    mines_display.change_icon(
        Icon('images/mine_32px.png', screen, game_settings, mines_display.rect1.x - 40, mines_display.rect1.y))

    # Створення ігрового поля
    create_fields(game_settings, screen, buttons)

    # Заповнюєм екран суцільним кольором
    screen.fill(game_settings.bg_color)

    # Головний цикл
    while 1:
        # Обробник подій
        event_handler(buttons, game_settings, mines_display)

        # Збільшуєм час якщо frame_count кратне frame_rate
        if game_settings.frame_count % game_settings.frame_rate == 0:
            clock_display.display_plus_one()

        # Оновлюєм дисплеї
        clock_display.blit_display()
        mines_display.blit_display()

        # Малюєм ігрове поле
        buttons.draw(screen)
        buttons_hover(buttons)

        # Лічильник кадрів
        game_settings.frame_count += 1
        clock.tick(game_settings.frame_rate)

        # Оновлення екрану
        pygame.display.flip()


# Запуск гри
if __name__ == '__main__':
    run_game()
