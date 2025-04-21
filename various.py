import pygame
from pygame.math import Vector2
from logger import logger as log

class Timer:
    def __init__(
            self,
            duration: int,
            starting: float = 0,
            paused: bool = False
        ) -> None:
        '''
        duration: duration of the timer
        starting: starting point of the timer
        paused: create paused timer when set to True
        '''

        self.duration = duration
        self.paused = paused

        self.time = starting
    
    def tick(self, delta_time: float) -> bool:
        if self.paused:
            return False
        
        self.time += delta_time

        if self.time > self.duration:
            self.time %= self.duration
            return True
    
    def pause(self): self.paused = True
    def resume(self): self.paused = False


class key_map:
    def __init__(self,up,down,left,right):
        log.debug(f'Initializing keybindings: {up}, {down}, {left}, {right}')

        self.up =    pygame.key.key_code(up)
        self.down =  pygame.key.key_code(down)
        self.left =  pygame.key.key_code(left)
        self.right = pygame.key.key_code(right)

        self.keys = [self.up,self.down,self.left,self.right]

    def __contains__(self, key) -> bool:
        return key in self.keys


class Renderable:
    def render(self, surface: pygame.Surface) -> None:
        '''
        Render the object on the given surface.
        '''
        log.critical('This is a blueprint for a renderable object. DO NOT USE IT!')
        raise NotImplementedError('Renderable is an abstract class.')


class Image(Renderable):
    def __init__(
            self, path: str,
            position: tuple[int, int],
            scale: tuple[int, int] = None
        ) -> None:

        log.debug(f'Initializing image: {path}')

        self.image = pygame.image.load(path).convert_alpha()
        if scale:
            size = self.image.get_size()
            self.image = pygame.transform.scale(self.image, [size[0]*scale[0], size[1]*scale[1]])

        self.rect = self.image.get_rect(center=position)
    
    def render(self, surface: pygame.Surface) -> None:
        '''
        Render the image on the given surface.
        '''
        surface.blit(self.image, self.rect)


class Menu:
    def __init__(
            self,
            screen_size: tuple[int, int],
            font_path: str,
            font_size: int,
            title: str,
            bg_color: pygame.Color,
            fps: int = 60
        ) -> None:

        log.debug(f'Initializing menu: {title}')

        # Initialize pygame
        pygame.init()

        # Screen settings
        self.screen = pygame.display.set_mode(screen_size)
        
        self.title = title
        self.font = pygame.font.Font(font_path, font_size)
        self.bg_color = bg_color
        self.center = Vector2(screen_size[0] / 2, screen_size[1] / 2)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.options = {}
        self.custom_renderables: Renderable = []

        pygame.display.set_caption(title)
    
    def add_custom_renderable(self, renderable: Renderable) -> None:
        '''
        Add a renderable object to the menu.
        '''
        log.debug(f'Adding renderable: {renderable}')
        self.custom_renderables.append(renderable)
    
    def add_option(
            self,
            name: str,
            text: str,
            text_color: pygame.Color,
            action: callable,
            thikness: tuple[int, int],
            center_pos: tuple[int, int],
            button_color: pygame.Color = None,
            button_texture: str = None
        ) -> None:
        '''
        Add an option to the menu, a button with a text and an action.
        '''

        # Check if the option already exists
        if name in self.options:
            log.warning(f'Option {name} already exists. Skipping...')
            return
        
        log.debug(f'Adding option: {name}')

        # Render the texture
        if button_texture:
            try:
                button_texture = pygame.image.load(button_texture).convert_alpha()
            except pygame.error:
                log.error(f'Failed to load texture: {button_texture}')
                button_texture = None

        # Create the option
        self.options[name] = {
            'text': self.font.render(text,True,text_color),
            'rect': pygame.Rect(0,0,*thikness),
            'button_color': button_color,
            'button_texture': button_texture,
            'action': action,
        }

        # Set the center position of the option
        self.options[name]['rect'].center = center_pos

    def _run(self):
        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.debug('Quitting menu by pressing exit button')
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        log.debug('Quitting menu by pressing exit key')
                        return
                
                # Check for options clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for name, option in self.options.items():
                        if option['rect'].collidepoint(event.pos):
                            log.debug(f'Option {name} clicked')
                            option['action']()
                            return

            self.screen.fill(self.bg_color)

            # Draw buttons
            for name, option in self.options.items():
                # Draw the texture if it exists
                if option['button_texture']:
                    self.screen.blit(option['button_texture'], option['rect'])
                else:
                    pygame.draw.rect(
                        self.screen,
                        option['button_color'],
                        option['rect']
                    )
                
                # Draw the text
                self.screen.blit(
                    option['text'],
                    option['text'].get_rect(center=option['rect'].center)
                )
            
            # Render custom renderables
            for renderable in self.custom_renderables:
                renderable.render(self.screen)

            pygame.display.flip()

            self.clock.tick(self.fps)