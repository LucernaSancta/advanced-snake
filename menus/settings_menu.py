import easygui
import os
import shutil
import webbrowser
import time
try:
    from .menu_components import Menu
    from logger import logger as log
except ImportError:
    from menu_components import Menu
    import logging
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)


def main(surface=None):
    log.name = 'settings_menu'
    log.debug('Initializing settings menu')


    # Initialize menu
    menu = Menu(
        screen_size=(800,800),
        font_path='menu_assets/font.ttf',
        font_size=32,
        title='Advanced Snake - settings',
        bg_texture='menu_assets/background.png',
        inherit_screen=surface, # This is used to set the surface of the menu to the main menu surface
    )


    def open_docs():
        # Resolve root project directory
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        docs_path = os.path.join(root_dir, 'docs', 'templates.md')

        if not os.path.exists(docs_path):
            log.error(f"Documentation file not found at {docs_path}")
            return

        # Open in default app (usually a text editor or browser)
        webbrowser.open(f'file://{docs_path}')
        log.info('Doc file opened in the browser')
        time.sleep(1) # Prevent user from opening 5000 tabs


    def chose_template():
        path = easygui.fileopenbox(default='./templates/*.json')
        if not path:
            log.info("No file selected.")
            return

        # Resolve root project directory (2 levels up from this script)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(root_dir, 'config.json')

        log.debug(f'Opening JSON template file at: {path}')
        log.debug(f'Overwriting config.json at: {config_path}')

        shutil.copy(path, config_path)
        log.info(f'Successfully replaced config.json with {path}')


    # Define buttun costants
    b_th = (500, 60) # Button dimensions
    delta_height = 35

    # Define buttons
    options = [
        ['what',   'WHAT TEMPLATE?!', open_docs,                          b_th, [menu.center.x, menu.center.y - 7*delta_height]],
        ['chose',  'CHOSE TEMPLATE',  chose_template,                     b_th, [menu.center.x, menu.center.y - 3*delta_height]],
        ['cahnge', 'CHANGE CURRENT',  lambda: log.debug('BUTT - Change'), b_th, [menu.center.x, menu.center.y -   delta_height]],
        ['save',   'SAVE CURRENT',    lambda: log.debug('BUTT - Save'),   b_th, [menu.center.x, menu.center.y +   delta_height]],
        ['back',   'BACK',            menu.quit,                          b_th, [menu.center.x, menu.center.y + 7*delta_height]]
    ]

    # Add buttons to menu
    for option in options:
        menu.add_option(*option)

    log.debug('Running menu')
    menu._run()

# Run the menu
if __name__ == '__main__':
    # Run the menu
    main()