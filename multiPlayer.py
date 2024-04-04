from pygame.locals import *
from tkinter import *
import pygame, socket, threading, json, sys

from components.screen import Screen
from components.character import Character
from components.controller import Controller
from components.doors import Doors
from components.gates import Gates
from components.levels import LevelSelect
from components.client import Client
from components.server import Server

# screen hangs due to pause on screen refresh
class Multi_Player_UI:
    def __init__(self, game, controller, home_screen):
        self.window = Tk()
        self.window.geometry('375x150+500+300')
        self.window.title('Login to Begin')
        self.game = game
        self.controller = controller
        self.home_screen = home_screen
        self.conn = None
        self.locations = json.load(open('assets/levels/properties.json'))
        self.font = ('arial', 12, 'bold')
        self.mainFrame = Frame(self.window)
        pygame.init()
        self.create_room()

    def create_room(self):
        server = socket.gethostbyname(socket.gethostname())
        create = Button(self.mainFrame, text='CREATE ROOM', command=lambda: self.login_screen('CREATE', server), font=self.font)
        create.pack()
        join = Button(self.mainFrame, text='JOIN ROOM', command=lambda: self.login_screen('JOIN'), font=self.font)
        join.pack()
        self.mainFrame.pack()
        self.window.mainloop()

    def login_screen(self, user, server=None):
        self.user = user
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.window)
        hostFrame = Frame(self.mainFrame)
        host = Label(hostFrame, text='HOST:', font=self.font)
        host.pack(side=LEFT)
        self.HOST = Entry(hostFrame)
        self.HOST.pack(side=LEFT)
        if server:
            self.HOST.insert(0, server)
        hostFrame.pack()
        portFrame = Frame(self.mainFrame)
        port = Label(portFrame, text='PORT:', font=self.font)
        port.pack(side=LEFT)
        self.PORT = Entry(portFrame)
        self.PORT.pack(side=LEFT)
        portFrame.pack()
        nameFrame = Frame(self.mainFrame)
        name = Label(nameFrame, text='NAME:', font=self.font)
        name.pack(side=LEFT)
        self.NAME = Entry(nameFrame)
        self.NAME.pack(side=LEFT)
        nameFrame.pack()
        submit = Button(self.mainFrame, text='SUBMIT', command=self.collect_data, font=('arial', 14, 'bold'))
        submit.pack()
        self.mainFrame.pack(pady=15)
        self.window.mainloop()

    def collect_data(self):
        self.data = [self.HOST.get(), int(self.PORT.get()), self.NAME.get()]
        if self.user == 'CREATE':
            self.server = Server(self.data)
            self.character_screen()
        elif self.user == 'JOIN':
            self.window.destroy()
            self.client = Client(self.data, self)
            self.conn = self.client.client
        self.run_game()

    def character_screen(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.window)
        fire = PhotoImage(file='assets/sprites/players/fire_boy.png')
        water = PhotoImage(file='assets/sprites/players/water_girl.png')
        fire_boy = Button(self.mainFrame, text='Fire Boy', command=lambda: self.get_character_type('fire'), image=fire, compound=BOTTOM, font=self.font)
        fire_boy.pack(side=LEFT)
        water_girl = Button(self.mainFrame, text='Water Girl', command=lambda: self.get_character_type('water'), image=water, compound=BOTTOM, font=self.font)
        water_girl.pack()
        self.mainFrame.pack()
        self.window.mainloop()

    def get_character_type(self, type):
        self.type = type
        self.server.type = type
        self.server.types = ['fire', 'water']
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.window)
        text = Label(self.mainFrame, text='Waiting for the Other Player')
        text.pack()
        self.mainFrame.pack()
        self.window.destroy()
        self.level_screen()

    def level_screen(self):
        level_select = LevelSelect()
        self.level = self.game.level_select_screen(level_select, self.controller)
        self.server.level = self.level
        if not self.conn:
            self.conn = self.server.conn
        print(self.server.level)
        self.conn.send(self.server.level.encode())
        self.run_game()
    
    def run_game(self):
        self.run = True
        self.initialize()
        self.thread = threading.Thread(target=self.receive_messages, daemon=False)
        self.thread.start()
        self.send_messages()

    def initialize(self):
        self.screen = Screen('assets/levels/'+self.level+'.csv')
        properties = self.locations[self.level]
        if properties['gates'] is not None and properties['plates'] is not None:
            self.gates = [Gates(properties['gates'][gate], properties['plates'][gate], properties['gate_styles'][gate] if properties['gate_styles'] else 'black',
                                properties['gate_types'][gate], properties['gate_opens'][gate]) for gate in range(len(properties['gates']))]
        else:
            self.gates = []
        self.fire_door = Doors(properties['fire_door'], pygame.image.load("assets/sprites/doors/fire_door.png"))
        self.water_door = Doors(properties['water_door'], pygame.image.load("assets/sprites/doors/water_door.png"))
        self.doors = [self.fire_door, self.water_door]
        self.fire_boy = Character(properties['fire_boy'], pygame.image.load('assets/sprites/players/fire_boy.png'),
                                  pygame.image.load('assets/sprites/players/fire_boy_left.png'),
                                  pygame.image.load('assets/sprites/players/fire_boy_right.png'), "fire")
        self.water_girl = Character(properties['water_girl'], pygame.image.load('assets/sprites/players/water_girl.png'),
                                    pygame.image.load('assets/sprites/players/water_girl_left.png'),
                                    pygame.image.load('assets/sprites/players/water_girl_right.png'), "water")

    def send_messages(self):
        self.player = Controller(K_LEFT, K_RIGHT, K_UP)
        self.sprite = self.fire_boy if self.type == 'fire' else self.water_girl
        clock = pygame.time.Clock()
        while self.run:
            clock.tick(60)
            self.events = pygame.event.get()
            self.game.draw_screen(self.screen)
            if self.gates:
                self.game.draw_gates(self.gates)
            self.game.draw_doors([self.fire_door, self.water_door])
            self.game.draw_player([self.fire_boy, self.water_girl])
            self.player.control_player(self.events, self.sprite)
            self.player.control_player(self.events, self.client_sprite)
            self.game.move_player(self.screen, self.gates, [self.sprite])
            self.conn.send((' '.join([str(i) for i in [self.sprite.rect.x, self.sprite.rect.y,
                                                       int(self.sprite.moving_left), int(self.sprite.moving_right)]])+'$').encode())
            self.game.check_for_death(self.screen, [self.fire_boy, self.water_girl])
            self.game.check_gate_press(self.gates, [self.fire_boy, self.water_girl])
            self.game.check_gem_collect(self.screen, [self.fire_boy, self.water_girl])
            self.game.check_door_open(self.fire_door, self.fire_boy)
            self.game.check_door_open(self.water_door, self.water_girl)
            self.game.refresh_window()
            if not self.water_girl.alive or not self.fire_boy.alive:
                pass
                '''
                self.run = False
                self.death_screen()
                '''
            if self.game.level_complete(self.doors):
                self.run = False
                self.win_screen()
            if self.controller.press_key(self.events, K_ESCAPE):
                # exit current level
                pass
            for event in self.events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def receive_messages(self):
        self.client_sprite = self.fire_boy if self.type == 'water' else self.water_girl
        while self.run:
            self.data = self.conn.recv(4096).decode()
            self.data = [int(i) for i in list(set(self.data.strip('$').split('$')))[0].split(' ') if i.isdigit()]
            if len(self.data) == 4:
                self.client_sprite.rect.x, self.client_sprite.rect.y, self.client_sprite.moving_left, self.client_sprite.moving_right = self.data
        print('thread destroyed')

    def win_screen(self):
        win_screen = pygame.image.load('assets/sprites/screens/win_screen.png')
        win_screen.set_colorkey('white')
        self.game.display.blit(win_screen, (0, 0))
        while True:
            self.game.refresh_window()
            if self.controller.press_key(pygame.event.get(), K_RETURN) and self.user == 'CREATE':
                self.level_screen()
            elif self.user == 'JOIN':
                print('waiting for data')
                self.level = self.conn.recv(4096).decode()
                print(self.level)
                self.run_game()

    def death_screen(self):
        death_screen = pygame.image.load('assets/sprites/screens/death_screen.png')
        death_screen.set_colorkey('white')
        self.game.display.blit(death_screen, (0, 0))
        while True:
            self.game.refresh_window()
            events = pygame.event.get()
            if self.controller.press_key(events, K_RETURN):
                self.run_game()
            if self.controller.press_key(events, K_ESCAPE):
                pass  # self.level_screen()
