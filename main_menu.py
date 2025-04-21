from various import Menu
from logger import logger as log


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Initialize menu
menu = Menu(
    (800,800),
    'menu_assets/font.ttf',
    32,
    'Advanced Snake - Main Menu',
    WHITE
)

# Define buttun costants
b_cl = BLACK # Button color
b_th = (400, 60) # Button dimensions
delta_height = 35

# Define buttons
options = [
    ['local',        'LOCAL',        BLACK, lambda: log.debug('BUTT - Local'),        b_th, [menu.center.x, menu.center.y -   delta_height], GRAY],
    ['online',       'ONLINE',       BLACK, lambda: log.debug('BUTT - Online'),       b_th, [menu.center.x, menu.center.y +   delta_height], GRAY],
    ['settings',     'SETTINGS',     BLACK, lambda: log.debug('BUTT - Setting'),      b_th, [menu.center.x, menu.center.y + 3*delta_height], GRAY],
    ['contributors', 'CONTRIBUTORS', BLACK, lambda: log.debug('BUTT - Contributors'), b_th, [menu.center.x, menu.center.y + 5*delta_height], GRAY],
    ['quit',         'QUIT',         BLACK, lambda: log.debug('BUTT - Quit'),         b_th, [menu.center.x, menu.center.y + 7*delta_height], GRAY]
]

# Add buttons to menu
for option in options:
    menu.add_option(*option)

# Run the menu
if __name__ == '__main__':
    # Run the menu
    log.debug('Running menu')
    menu._run()