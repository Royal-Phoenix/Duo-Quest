from pygame.locals import *
import pygame, json, sys

from components.screen import Screen
from components.character import Character
from components.controller import Controller
from components.doors import Doors
from components.gates import Gates
from components.levels import LevelSelect

class Single_Player_UI:
    def __init__(self, game, controller, home_screen):
        self.locations = json.load(open('assets/levels/properties.json'))
        self.controller = controller
        self.game = game
        self.home_screen = home_screen
        self.level_screen()

    def level_screen(self):
        level_select = LevelSelect()
        self.level = self.game.level_select_screen(level_select, self.controller)
        self.run_game()

    def run_game(self):
        self.screen = Screen('assets/levels/'+self.level+'.csv')
        properties = self.locations[self.level]
        if properties['gates'] is not None and properties['plates'] is not None:
            gates = [Gates(properties['gates'][gate], properties['plates'][gate], properties['gate_styles'][gate] if properties['gate_styles'] else 'black',
                           properties['gate_types'][gate], properties['gate_opens'][gate]) for gate in range(len(properties['gates']))]
        else:
            gates = []
        fire_door = Doors(properties['fire_door'], pygame.image.load("assets/sprites/doors/fire_door.png"))
        water_door = Doors(properties['water_door'], pygame.image.load("assets/sprites/doors/water_door.png"))
        doors = [fire_door, water_door]
        fire_boy = Character(properties['fire_boy'], pygame.image.load('assets/sprites/players/fire_boy.png'),
                             pygame.image.load('assets/sprites/players/fire_boy_left.png'),
                             pygame.image.load('assets/sprites/players/fire_boy_right.png'), "fire")
        water_girl = Character(properties['water_girl'], pygame.image.load('assets/sprites/players/water_girl.png'),
                               pygame.image.load('assets/sprites/players/water_girl_left.png'),
                               pygame.image.load('assets/sprites/players/water_girl_right.png'), "water")
        arrows_controller = Controller(K_LEFT, K_RIGHT, K_UP)
        wasd_controller = Controller(K_a, K_d, K_w)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            events = pygame.event.get()
            self.game.draw_screen(self.screen)
            if gates:
                self.game.draw_gates(gates)
            self.game.draw_doors(doors)
            self.game.draw_player([fire_boy, water_girl])
            arrows_controller.control_player(events, fire_boy)
            wasd_controller.control_player(events, water_girl)
            self.game.move_player(self.screen, gates, [fire_boy, water_girl])
            self.game.check_for_death(self.screen, [fire_boy, water_girl])
            self.game.check_gate_press(gates, [fire_boy, water_girl])
            self.game.check_gem_collect(self.screen, [fire_boy, water_girl])
            self.game.check_door_open(fire_door, fire_boy)
            self.game.check_door_open(water_door, water_girl)
            self.game.refresh_window()
            if not water_girl.alive or not fire_boy.alive:
                if not water_girl.alive:
                    pass
                if not fire_boy.alive:
                    pass
                self.death_screen()
            if self.game.level_complete(doors):
                self.win_screen()
            if self.controller.press_key(events, K_ESCAPE):
                self.level_screen()
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def win_screen(self):
        win_screen = pygame.image.load('assets/sprites/screens/win_screen.png')
        indicator = pygame.image.load('assets/sprites/screens/option_indicator.png')
        option, ind = "Play Again", 88
        while True:
            self.game.display.blit(win_screen, (0, 0))
            self.game.display.blit(indicator, (ind, 175))
            events = pygame.event.get()
            if self.controller.press_key(events, K_RIGHT) or self.controller.press_key(events, K_LEFT):
                option = "Exit Game" if option == "Play Again" else "Play Again"
                ind = 88 if option == "Play Again" else 290
            if self.controller.press_key(events, K_RETURN):
                if option == "Play Again":
                    self.level_screen()
                elif option == "Exit Game":
                    self.home_screen()
            self.game.refresh_window()

    def death_screen(self):
        death_screen = pygame.image.load('assets/sprites/screens/death_screen.png')
        indicator = pygame.image.load('assets/sprites/screens/option_indicator.png')
        option, ind = "Restart", 100
        while True:
            self.game.display.blit(death_screen, (0, 0))
            self.game.display.blit(indicator, (ind, 195))
            events = pygame.event.get()
            if self.controller.press_key(events, K_RIGHT) or self.controller.press_key(events, K_LEFT):
                option = "Exit Game" if option == "Restart" else "Restart"
                ind = 100 if option == "Restart" else 295
            if self.controller.press_key(events, K_RETURN):
                if option == "Restart":
                    self.run_game()
                elif option == "Exit Game":
                    self.home_screen()
            self.game.refresh_window()
