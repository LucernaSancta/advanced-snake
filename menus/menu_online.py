import easygui
from online.server import GameServer
from online.client import GameClient
try:
    from .menu_components import Menu
    from logger import logger as log
except ImportError:
    from menu_components import Menu
    import logging
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)


def main(surface=None):
    log.name = 'online_menu'
    log.debug('Initializing online menu')

    # Initialize menu
    menu = Menu(
        screen_size=(800,800),
        font_path='menu_assets/font.ttf',
        font_size=32,
        title='Advanced Snake - online',
        bg_texture='menu_assets/background.png',
        inherit_screen=surface, # This is used to set the surface of the menu to the main menu surface
    )

    def connct_to_server():
        user_input = easygui.enterbox('Server IP address', '')
        GameClient(host=user_input).run()


    # Define buttun costants
    b_th = (500, 60) # Button dimensions
    delta_height = 35

    # Define buttons
    options = [
        ['start',   'START SERVER', lambda: GameServer().run(), b_th, [menu.center.x, menu.center.y - 3*delta_height]],
        ['enter',  'JOIN SERVER',  connct_to_server,            b_th, [menu.center.x, menu.center.y -  delta_height]],
        ['back',   'BACK',          menu.quit,                  b_th, [menu.center.x, menu.center.y + 7*delta_height]]
    ]

    # Add buttons to menu
    for option in options:
        menu.add_option(*option)

    log.debug('Running menu')
    menu.run()

# Run the menu
if __name__ == '__main__':
    # Run the menu
    main()