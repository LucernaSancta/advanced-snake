try:
    from .menu_components import Menu
    from logger import logger as log
except ImportError:
    from menu_components import Menu
    import logging
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)


def main(surface=None):
    log.name = 'template_change_menu'
    log.debug('Initializing tempalte change menu')

    # Initialize menu
    menu = Menu(
        screen_size=(800,800),
        font_path='menu_assets/font.ttf',
        font_size=32,
        title='Advanced Snake - settings - tempalte change',
        bg_texture='menu_assets/background.png',
        inherit_screen=surface, # This is used to set the surface of the menu to the main menu surface
    )

    def dummy(): return

    # Define buttun costants
    b_th = (500, 60) # Button dimensions
    b_th2 = (700, 70)
    delta_height = 35

    # Define buttons
    options = [
        ['test1',  'TO CAHNGE THE CURRENT', dummy,     b_th2, [menu.center.x, menu.center.y - 7*delta_height], 'BLACK', 'BLACK', 'WHITE', 'WHITE'],
        ['test2',  'SETTING OPEN THE FILE', dummy,     b_th2, [menu.center.x, menu.center.y - 5*delta_height], 'BLACK', 'BLACK', 'WHITE', 'WHITE'],
        ['test3',  'config.json IN THE',    dummy,     b_th2, [menu.center.x, menu.center.y - 3*delta_height], 'BLACK', 'BLACK', 'WHITE', 'WHITE'],
        ['test4',  'PROJECT ROOT DIR',      dummy,     b_th2, [menu.center.x, menu.center.y - 1*delta_height], 'BLACK', 'BLACK', 'WHITE', 'WHITE'],
        ['back',   'BACK',                  menu.quit, b_th,  [menu.center.x, menu.center.y + 7*delta_height]]
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