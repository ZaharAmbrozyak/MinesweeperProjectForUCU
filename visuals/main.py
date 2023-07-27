from sys import exit
from os import environ
import pygame
from pygame.sprite import Group
from settings import Settings
from button import Button
from icon import Icon
from display import Display
from pygame.locals import *
import numpy as np
import game_logic as gl


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
            _create_field(game_settings, screen, buttons, button_number,
                          row_number, '0')


def change_fields(game_settings: Settings, screen: pygame.surface.Surface, buttons: Group, array_2d: np.ndarray) -> None:
    """
        Створює ігрове поле завдяки двох for-циклів.
        Використовує допоміжну функцію _create_button
    """
    # Екземпляр кнопки
    button = Button(game_settings, screen)

    # Прораховуєм кількість кнопок в одному рядку і саму кількість рядків
    number_buttons_x = _get_number_buttons_x(game_settings, button.rect.width)
    number_rows = _get_number_rows(game_settings, button.rect.height)

    # Екземпляр кнопки
    for x in range(0, array_2d.shape[0]):
        for y in range(0, array_2d.shape[1]):
            buttons.sprites()[y + x * array_2d.shape[1]].change_image(array_2d[x, y])


def _button_keydown(event, buttons: Group, game_settings: Settings, mines_display=None) -> tuple:
    """
        Обробник помилок для ігрового поля (кнопок)
    """
    for button in buttons.sprites():
        if button.rect.collidepoint(event.pos):
            if event.button == 1 and button.image_name != 'flag' and not button.is_revealed:
                button.on_click(button.actual_image)
                if button.actual_image == 'mine':
                    pygame.mixer.Sound.play(game_settings.explosion_sound)
                    pygame.mixer.music.stop()
                    game_settings.game_active = False

                else:
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


def buttons_hover(buttons: Group):
    for button in buttons.sprites():
        if button.rect.collidepoint(pygame.mouse.get_pos()):
            button.hover()
        else:
            button.stop_hover()


def event_handler(buttons: Group, game_settings: Settings, mines_display: Display) -> tuple:
    """
        Головний обробник помилок у грі
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            return _button_keydown(event, buttons, game_settings, mines_display)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()


def run_game(game: gl.Game) -> None:
    """
        Головна функція гри.
    """
    # Оптимізовуєм звук гри
    pygame.mixer.pre_init(44100, 16, 2, 4096)



    # Ініціалізація pygame
    pygame.init()

    # Створення об'єкту налаштувань гри
    game_settings = Settings(game.size[0], game.size[1])

    # Налаштовування вікна гри
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Minesweeper')
    pygame.display.set_icon(pygame.image.load('images/mine.png'))
    flags = DOUBLEBUF
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
        if game.end_game:
            print("Game ended!")
            break
        event_result = event_handler(buttons, game_settings, mines_display)
        if event_result:
            game.do_action(event_result[0], event_result[1])
            # print(game.player_board)
            # if event_result[1] == 'o' and first_click:
            #     game.setup(event_result[0])
            change_fields(game_settings, screen, buttons, game.player_board)
                # print(game.nums_board)
                # first_click = False

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
    game_instance = gl.Game((10, 8), 10)

    # while not game.end_game:
        # print(game.num_of_left_mines())
        # game.print_board(game.player_board)
        # game.do_action()
        # game.print_board(game.game_board)
        # game.print_board(game.nums_board)

    # game.reveal_player_board()

    run_game(game_instance)

