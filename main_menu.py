from main import Game
from various import Menu, Image
from logger import logger as log


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)


# Initialize menu
menu = Menu(
    screen_size=(800,800),
    font_path='menu_assets/font.ttf',
    font_size=32,
    title='Advanced Snake - Main Menu',
    bg_texture='menu_assets/background.png',
)

# Define buttun costants
b_th = (400, 60) # Button dimensions
delta_height = 35

def load_local_game():
    log.info('Loading local game')
    # Run the game
    Game()._run()

# Define buttons
options = [
    ['local',        'LOCAL',        BLACK, load_local_game,                          b_th, [menu.center.x, menu.center.y -   delta_height], WHITE],
    ['online',       'ONLINE',       BLACK, lambda: log.debug('BUTT - Online'),       b_th, [menu.center.x, menu.center.y +   delta_height], WHITE],
    ['settings',     'SETTINGS',     BLACK, lambda: log.debug('BUTT - Setting'),      b_th, [menu.center.x, menu.center.y + 3*delta_height], WHITE],
    ['contributors', 'CONTRIBUTORS', BLACK, lambda: log.debug('BUTT - Contributors'), b_th, [menu.center.x, menu.center.y + 5*delta_height], WHITE],
    ['quit',         'QUIT',         BLACK, menu.quit,                                b_th, [menu.center.x, menu.center.y + 7*delta_height], WHITE]
]

# Add buttons to menu
for option in options:
    menu.add_option(*option)

menu.add_custom_renderable(Image(
    'menu_assets/white_title.png',
    (menu.center.x, menu.center.y - 6*delta_height),
    (2,2)
))

# Run the menu
if __name__ == '__main__':
    # Run the menu
    log.debug('Running menu')
    menu._run()