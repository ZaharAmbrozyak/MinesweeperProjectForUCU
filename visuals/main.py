from sys import exit
from os import environ
import pygame
from pygame.sprite import Group
from settings import Settings
from button import Button, NewGameButton
from icon import Icon
from display import Display
from pygame.locals import *
from PIL import Image, ImageFilter
import numpy as np
import game_logic as gl


def _get_number_buttons_x(game_settings: Settings, button_width: int) -> int:
    """
        Функція, що рахує та повертає кількість можливих полей на осі Х
    """
    available_space_x = game_settings.screen_width - game_settings.extra_x
    number_buttons_x = int(available_space_x / button_width)

    return number_buttons_x


def _get_number_rows(game_settings: Settings, button_height: int) -> int:
    """
        Функція, що рахує та повертає кількість можливих рядів
    """
    available_space_y = game_settings.screen_height - game_settings.extra_y
    number_rows = int(available_space_y / button_height)

    return number_rows


def _create_field(game_settings: Settings, screen: pygame.surface.Surface,
                  buttons: Group, button_number: int, row_number: int,
                  actual_image: str) -> None:
    """
        Функція, що створює кнопку button.
        Змінює свої координати X Y по формулі.
        Додає Кнопку до класу Group (списку спрайтів)
    """

    # Екземпляр кнопки
    button = Button(game_settings, screen, actual_image,
                    'default', 'hover_default', row_number, button_number)

    # Обрахунок координат
    button_width = button.rect.width
    button.x = button_width * button_number + game_settings.extra_x/2
    button.y = button.rect.height + 86 + button.rect.height * row_number

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
            _create_field(game_settings, screen, buttons, button_number,
                          row_number, '0')


def change_fields(buttons: Group, array_2d: np.ndarray) -> None:
    """
        Створює ігрове поле завдяки двох for-циклів.
        Використовує допоміжну функцію _create_button
    """

    # Екземпляр кнопки
    for x in range(0, array_2d.shape[0]):
        for y in range(0, array_2d.shape[1]):
            buttons.sprites()[y + x * array_2d.shape[1]].change_image(array_2d[x, y])
            if array_2d[x, y] != 'default' and array_2d[x, y] != 'flag':
                buttons.sprites()[y + x * array_2d.shape[1]].is_revealed = True


def _button_keydown(event, buttons: Group, game_settings: Settings, game: gl.Game, mines_display,
                    begin_game_button: NewGameButton) -> tuple:
    """
        Обробник помилок для ігрового поля (кнопок)
    """
    if not game_settings.game_active:
        if begin_game_button.rect.collidepoint(event.pos) or begin_game_button.rect.collidepoint(event.pos):
            game_settings.game_active = True
            game.end_game = False
    else:
        for button in buttons.sprites():
            if button.rect.collidepoint(event.pos):
                if event.button == 1 and button.image_name != 'flag' and not button.is_revealed:
                    print(button.actual_image)
                    if button.actual_image == 'mine':
                        pygame.mixer.Sound.play(game_settings.explosion_sound)
                        pygame.mixer.music.stop()
                        game_settings.game_active = False
                    else:
                        button.on_click()
                        pygame.mixer.Sound.play(game_settings.click_sound)
                        pygame.mixer.music.stop()
                    coords = button.get_coords()
                    return (coords[1], coords[0]), 'o'

                elif event.button == 3:
                    if not button.is_revealed:
                        if button.image_name == 'flag':
                            pygame.mixer.Sound.play(game_settings.flag_sound_backwards)
                            pygame.mixer.music.stop()
                            mines_display.display_plus_one()
                            button.change_image('default')
                            coords = button.get_coords()
                            return (coords[1], coords[0]), 'r'

                        elif mines_display.got_mines():
                            pygame.mixer.Sound.play(game_settings.flag_sound)
                            pygame.mixer.music.stop()
                            mines_display.display_minus_one()
                            button.change_image('flag')
                            coords = button.get_coords()
                            return (coords[1], coords[0]), 'f'


def buttons_hover(buttons: Group, start_game_buttons: Group):
    for button in start_game_buttons.sprites():
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.hover()
        else:
            button.stop_hover()
    for button in buttons.sprites():
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.hover()
        else:
            button.stop_hover()


def event_handler(buttons: Group, game_settings: Settings,
                  mines_display: Display, begin_game_button: NewGameButton,
                  game) -> tuple:
    """
        Головний обробник помилок у грі
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            return _button_keydown(event, buttons, game_settings, game, mines_display, begin_game_button)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


def load_image():
    # Ініціалізація pygame
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    pygame.display.set_icon(pygame.image.load('visuals/images/mine.png'))

    screen = pygame.display.set_mode((500, 500))

    # Обмежуєм кількість можливих кнопок, які можна натиснути. ОПТИМІЗАЦІЯ
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
    font = pygame.font.SysFont('arial', 12)
    text = 'Перетягніть зображення до екрану, щоб почати розмінування'
    text_image = font.render(text, True, (0, 0, 0))
    text_rect = text_image.get_rect()
    text_rect.x = 250
    text_rect.y = 250
    while 1:
        screen.fill('#FFFFFF')
        for event in pygame.event.get():
            if event.type == DROPFILE:
                image = pygame.image.load(event.file)
                return image
        screen.blit(text_image, text_rect)


def run_game(game: gl.Game, blur_image: pygame.Surface=None) -> None:
    """
        Головна функція гри.
    """

    # Створення об'єкту налаштувань гри
    game_settings = Settings(game.size[0], game.size[1], game.num_of_mines, 32, 32, 20, 192)
    print(game_settings.screen_width)
    # Налаштовування вікна гри
    environ['SDL_VIDEO_CENTERED'] = '1'
    flags = DOUBLEBUF
    screen = pygame.display.set_mode((
        game_settings.screen_width,
        game_settings.screen_height-game_settings.extra_y/3),
        flags,
        16)
    print(screen.get_width(), game_settings.screen_width)
    clock = pygame.time.Clock()

    # Створення ігрових об'єктів
    buttons = Group()
    start_game = NewGameButton(game_settings, screen, 'start',
                               game_settings.screen_width//2, int(game_settings.screen_height//2), 8)
    end_game = NewGameButton(game_settings, screen, 'lose',
                             game_settings.screen_width//2, int(game_settings.screen_height//2), 4)
    buttons_game_begin = Group()
    buttons_game_begin.add(start_game)
    buttons_game_begin.add(end_game)
    # Створюєм два дисплея: час та кількість мін
    clock_display = Display(game_settings, screen, game_settings.screen_width / 1.5, 20,
                            [0, 0, 0])
    mines_display = Display(game_settings, screen, game_settings.screen_width - 44*3 - game_settings.screen_width / 1.5, 20,
                            [game_settings.mines//100, (game_settings.mines//10) % 10, game_settings.mines % 10])

    # Додаєм іконки
    clock_display.change_icon(
        Icon('visuals/images/clock.png', screen, game_settings, clock_display.rect1.x - 60, 0))
    mines_display.change_icon(
        Icon('visuals/images/mine_32px.png', screen, game_settings, mines_display.rect1.x - 40, mines_display.rect1.y))

    # Створення ігрового поля
    create_fields(game_settings, screen, buttons)
    screen.fill(game_settings.bg_color)
    # Головний цикл
    while 1:

        # Обробник подій
        if game.end_game:
            game_settings.game_active = False
            game_settings.first_time_play = False
        event_result = event_handler(buttons, game_settings, mines_display, start_game, game)
        if event_result:
            game.do_action(event_result[0], event_result[1])
            change_fields(buttons, game.player_board)

        # Оновлюєм дисплеї
        clock_display.blit_display()
        mines_display.blit_display()

        # Малюєм ігрове поле
        buttons.draw(screen)
        buttons_hover(buttons, buttons_game_begin)
        if not game_settings.game_active:
            if game_settings.first_time_play:
                start_game.draw_me()
            else:
                end_game.draw_me()
        else:
            if game_settings.frame_count % game_settings.frame_rate == 0:
                clock_display.display_plus_one()

        # Лічильник кадрів
        game_settings.frame_count += 1
        clock.tick(game_settings.frame_rate)

        # Оновлення екрану
        pygame.display.flip()


# Запуск гри
if __name__ == '__main__':
    game_instance = gl.Game((18, 16), 30)
    run_game(game_instance, load_image())
