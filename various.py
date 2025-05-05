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
            bg_color: pygame.Color = None,
            bg_texture: str = None,
            fps: int = 60,
            inherit_screen: pygame.surface.Surface | None = None
        ) -> None:

        log.info(f'Initializing menu: {title}')

        # Initialize pygame
        pygame.init()

        # Screen settings
        if inherit_screen is not None:
            self.screen = inherit_screen
        else:
            self.screen = pygame.display.set_mode(screen_size)
        
        self.title = title
        self.font = pygame.font.Font(font_path, font_size)
        self.center = Vector2(screen_size[0] / 2, screen_size[1] / 2)
        self.running = True

        self.clock = pygame.time.Clock()
        self.fps = fps

        self.bg_color = bg_color
        if bg_texture:
            try:
                self.bg_texture = pygame.image.load(bg_texture).convert_alpha()
                self.bg_texture = pygame.transform.scale(self.bg_texture, screen_size)
            except pygame.error:
                log.error(f'Failed to load background texture: {bg_texture}')
                self.bg_texture = None
        else:
            self.bg_texture = None
        if not any([self.bg_color, self.bg_texture]):
            log.warning('No background color or texture set. Using default black.')
            self.bg_color = pygame.Color(0, 0, 0)

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

            action: callable,
            thikness: tuple[int, int],
            center_pos: tuple[int, int],

            text_color: pygame.Color = "BLACK",
            text_color_hover: pygame.Color = "WHITE",

            button_color: pygame.Color = "WHITE",
            button_color_hover: pygame.Color = "BLACK",

            button_texture: str = None,
            button_texture_hover: str = None
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
        if button_texture and button_texture_hover:
            try:
                button_texture = pygame.image.load(button_texture).convert_alpha()
                button_texture_hover = pygame.image.load(button_texture_hover).convert_alpha()
            except pygame.error:
                log.error(f'Failed to load texture: {button_texture}')
                log.error(f'Failed to load texture: {button_texture_hover}')
                button_texture = None
                button_texture_hover = None
        elif button_texture or button_texture_hover:
            log.warning(f'Failed to load button {name} textures because only one of the two is specified')

        # Create the option
        self.options[name] = {
            'text': text,
            'rect': pygame.Rect(0,0,*thikness),

            'text_color': text_color,
            'text_color_hover': text_color_hover,
            'button_color': button_color,
            'button_color_hover': button_color_hover,
            'button_texture': button_texture,
            'button_texture_hover': button_texture_hover,

            'action': action,
        }

        # Set the center position of the option
        self.options[name]['rect'].center = center_pos

    def quit(self) -> None:
        log.info(f'Quitting menu: {self.title}')
        self.running = False

    def _run(self):
        mouse_pressed_pos=Vector2(0,0)
        # Main loop
        while self.running:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.debug('Quitting menu by pressing exit button')
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        log.debug('Quitting menu by pressing exit key')
                        return
                    

            if not self.bg_texture:
                # Fill the screen with the background color
                self.screen.fill(self.bg_color)
            else:
                # Fill the screen with the background texture
                self.screen.blit(self.bg_texture, (0, 0))


            # Get mouse things
            mouse_pos = Vector2(pygame.mouse.get_pos())
            mouse_pressed_any = any(pygame.mouse.get_pressed())

            if mouse_pressed_any and (mouse_pressed_pos == Vector2(0,0)):
                mouse_pressed_pos = mouse_pos # Set the mouse position when the mouse is first pressed
            elif mouse_pressed_any:
                pass # The mouse is still beeing pressed
            else:
                mouse_pressed_pos = Vector2(0,0) # Reset the mouse position


            # Buttons logic and rendering
            for name, option in self.options.items():

                
                if option['rect'].collidepoint(mouse_pos):

                    # Draw the texture if it exists
                    if option['button_texture_hover']:
                        self.screen.blit(option['button_texture_hover'], option['rect'])

                    else:
                        pygame.draw.rect(
                            self.screen,
                            option['button_color_hover'],
                            option['rect']
                        )
                    
                    # Draw the text
                    text = self.font.render(option['text'],True,option['text_color_hover'])
                    self.screen.blit(
                        text,
                        text.get_rect(center=option['rect'].center)
                    )

                    # Check for pressed mouse buttons and for the mouse position when it pressed them
                    if mouse_pressed_any and option['rect'].collidepoint(mouse_pressed_pos):
                        log.debug(f'Option {name} clicked')
                        option['action']()
                

                # The button is not beeing hovered
                else:
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
                    text = self.font.render(option['text'],True,option['text_color'])
                    self.screen.blit(
                        text,
                        text.get_rect(center=option['rect'].center)
                    )


            # Render custom renderables
            for renderable in self.custom_renderables:
                renderable.render(self.screen)

            pygame.display.flip()

            self.clock.tick(self.fps)