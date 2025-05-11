from main import Game
from map_creator import Map_creator
from logger import logger as log

from menus.menu_components import Menu, Image
from menus.menu_contributors import main as contributors_menu
from menus.menu_settings import main as settings_menu
from various import print_new_game

def run_main_menu():
    result = [None]  # Using a list to hold mutable return value from menu callback

    def start_local_game():
        result[0] = 'local'
        menu.quit()

    def start_map_creator():
        result[0] = 'map_creator'
        menu.quit()

    # Initialize menu
    menu = Menu(
        screen_size=(800, 800),
        font_path='menu_assets/font.ttf',
        font_size=32,
        title='Advanced Snake - Main Menu',
        bg_texture='menu_assets/background.png',
    )

    b_th = (400, 60)
    delta_height = 35
    offset = -5

    options = [
        ['local',        'LOCAL',        start_local_game,                      b_th, [menu.center.x, menu.center.y -   delta_height + offset]],
        ['online',       'ONLINE',       lambda: log.debug('BUTT - Online'),    b_th, [menu.center.x, menu.center.y +   delta_height + offset]],
        ['map_creator',  'MAP CREATOR',  start_map_creator,                     b_th, [menu.center.x, menu.center.y + 3*delta_height + offset]],
        ['settings',     'SETTINGS',     lambda: settings_menu(menu.screen),    b_th, [menu.center.x, menu.center.y + 5*delta_height + offset]],
        ['contributors', 'CONTRIBUTORS', lambda: contributors_menu(menu.screen),b_th, [menu.center.x, menu.center.y + 7*delta_height + offset]],
        ['quit',         'QUIT',         menu.quit,                             b_th, [menu.center.x, menu.center.y + 9*delta_height + offset]]
    ]

    for option in options:
        menu.add_option(*option)

    menu.add_custom_renderable(Image(
        'menu_assets/white_title.png',
        (menu.center.x, menu.center.y - 6*delta_height),
        (2, 2)
    ))

    log.debug('Running menu')
    menu._run()
    return result[0]


def main():
    while True:
        choice = run_main_menu()
        if choice == 'local':
            log.info('Starting local game')
            Game()._run()
        elif choice == 'map_creator':
            log.info('Starting map creator')
            Map_creator()._run()
        else:
            break  # User quit or selected a non-restarting action


if __name__ == '__main__':
    log.name = 'main_menu' # Set the logger name
    print_new_game('MAIN MENU') # Log the start message
    main()
