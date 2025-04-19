import pygame
import sys
from main import Game

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font('menu_assets/font.ttf', 30)

# Menu options
start_text = font.render('LOCAL',        True, BLACK)
multi_text = font.render('ONLINE',       True, BLACK)
sett_text =  font.render('SETTINGS',    True, BLACK)
contr_text = font.render('CONTRINUTORS', True, BLACK)
quit_text =  font.render('QUIT',         True, BLACK)

# Rects for buttons
screen_width_center = WIDTH // 2
delta_height = 35
rects_dimensions = [400, 60]
start_rect = pygame.Rect(0,0,*rects_dimensions)
multi_rect = pygame.Rect(0,0,*rects_dimensions)
sett_rect =  pygame.Rect(0,0,*rects_dimensions)
contr_rect = pygame.Rect(0,0,*rects_dimensions)
quit_rect =  pygame.Rect(0,0,*rects_dimensions)

start_rect.center = [screen_width_center, HEIGHT // 2 -   delta_height]
multi_rect.center = [screen_width_center, HEIGHT // 2 +   delta_height]
sett_rect.center =  [screen_width_center, HEIGHT // 2 + 3*delta_height]
contr_rect.center = [screen_width_center, HEIGHT // 2 + 5*delta_height]
quit_rect.center =  [screen_width_center, HEIGHT // 2 + 7*delta_height]

def main_menu():
    while True:
        screen.fill(WHITE)

        # Draw buttons
        pygame.draw.rect(screen, GRAY, start_rect)
        pygame.draw.rect(screen, GRAY, multi_rect)
        pygame.draw.rect(screen, GRAY, sett_rect)
        pygame.draw.rect(screen, GRAY, contr_rect)
        pygame.draw.rect(screen, GRAY, quit_rect)
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))
        screen.blit(multi_text, multi_text.get_rect(center=multi_rect.center))
        screen.blit(sett_text, sett_text.get_rect(center=sett_rect.center))
        screen.blit(contr_text, contr_text.get_rect(center=contr_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    Game().run()
                    return
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
