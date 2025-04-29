from various import Menu
from logger import logger as log
import webbrowser

def main(surface=None):
    log.name = 'contributors_menu'
    log.debug('Initializing contributors menu')

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)


    # Initialize menu
    menu = Menu(
        screen_size=(800,800),
        font_path='menu_assets/font.ttf',
        font_size=32,
        title='Advanced Snake - Contributors',
        bg_texture='menu_assets/background.png',
        eredited_screen=surface, # This is used to set the surface of the menu to the main menu surface
    )

    def open_webpage(link: str):
        webbrowser.open(link)
        log.info(f'Opening {link}')

    # Define buttons
    contributors = [
        ['@LucernaSancta',      'https://github.com/LucernaSancta'],
        ['@Dominik',            'https://github.com/Dospalko'],
        ['@ericfan20211215',    'https://github.com/ericfan20211215'],
        ['@GiacomoArgento',     'https://github.com/GiacomoArgento'],
        ['@kotlalokeshwari098', 'https://github.com/kotlalokeshwari098']
    ]
    # Define buttun costants
    b_th = (700, 60) # Button dimensions
    delta_height = 35

    # Add buttons to with the name of the contributors
    for i, contributor in enumerate(contributors):
        
        menu.add_option(
            contributor[0], 
            contributor[0], 
            BLACK, 
            lambda link=contributor[1]: open_webpage(link), 
            b_th, 
            [menu.center.x, 2*i*delta_height + (delta_height*5)], 
            WHITE
        )
    
    # Add back button
    menu.add_option(
        'back', 
        'BACK', 
        BLACK, 
        menu.quit, 
        b_th, 
        [menu.center.x, 2*delta_height], 
        WHITE
    )

    log.debug('Running menu')
    menu._run()

# Run the menu
if __name__ == '__main__':
    # Run the menu
    main()