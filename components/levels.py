import pygame


class LevelSelect:
    def __init__(self):
        self.screen = pygame.image.load('assets/sprites/screens/level_select_screen.png')
        self.levels = {}
        for i in range(5):
            self.levels[i+1] = pygame.image.load('assets/sprites/screens/level'+str(i+1)+'.png')
            self.levels[i+1].set_colorkey('white')
        self.indicator = pygame.image.load('assets/sprites/screens/level_indicator.png')
        self.watergirl_logo = pygame.transform.scale(pygame.image.load('assets/sprites/players/water_girl.png'), (64, 128))
        self.watergirl_logo.set_colorkey('white')
        self.fireboy_logo = pygame.transform.scale(pygame.image.load('assets/sprites/players/fire_boy.png'), (64, 128))
        self.fireboy_logo.set_colorkey('white')
