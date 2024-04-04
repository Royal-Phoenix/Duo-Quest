from pygame.locals import *
import pygame

from singlePlayer import Single_Player_UI
from multiPlayer import Multi_Player_UI
from components.game import Game
from components.controller import Controller
#Calisto MT 72

class Main:
    def __init__(self):
        pygame.init()
        self.game = Game()
        self.controller = Controller(None, None, None)
        self.logo = None
        self.load_game1()
        self.intro_screen()

    def load_game1(self):
        i, j = 0, 50
        run = True
        while run:
            self.game.display.blit(pygame.image.load('assets/sprites/screens/load_screen.png'), (0, 0))
            self.game.display.blit(pygame.font.SysFont('Comics', 20).render('Loading', True, 'purple'), (j, 300))
            i, j = i+1, j+12.9
            for k in range(i):
                pygame.draw.rect(self.game.display, 'purple', (80+k*12.9, 325, 10.9, 20))
            pygame.time.delay(100)
            events = pygame.event.get()
            if i > 30:
                self.intro_screen()
            for event in events:
                if event.type == QUIT:
                    run = False
            self.game.refresh_window()

    def load_game(self):
        i = 0
        run = True
        while run:
            self.game.display.blit(pygame.image.load('assets/sprites/screens/load_screen.png'), (0, 0))
            i += 1
            self.game.display.blit(pygame.font.SysFont('Comics', 20).render('Loading', True, 'purple'), (75+i, 300))
            pygame.draw.rect(self.game.display, 'purple', (80, 325, 10+i, 20))
            events = pygame.event.get()
            if i > 375:
                self.intro_screen()
            for event in events:
                if event.type == QUIT:
                    run = False
            self.game.refresh_window()

    def intro_screen(self):
        intro_screen = pygame.image.load('assets/sprites/screens/intro_screen.png')
        indicator = pygame.image.load('assets/sprites/screens/game_indicator.png')
        mode, ind = "Single Player", 264
        while True:
            self.game.display.blit(intro_screen, (0, 0))
            self.game.display.blit(indicator, (140, ind))
            events = pygame.event.get()
            if self.controller.press_key(events, K_DOWN) or self.controller.press_key(events, K_UP):
                mode = "Multi Player" if mode == "Single Player" else "Single Player"
                ind = 264 if mode == "Single Player" else 314
            if self.controller.press_key(events, K_RETURN):
                if mode == "Single Player":
                    Single_Player_UI(self.game, self.controller, self.intro_screen)
                elif mode == "Multi Player":
                    Multi_Player_UI(self.game, self.controller, self.intro_screen)
                elif mode == "Settings":
                    self.settings_screen()
            self.game.refresh_window()

    def settings_screen(self):
        pass


Main()
