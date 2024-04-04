import pygame
import csv
import os


class Screen:
    def __init__(self, path):
        self.CHUNK_SIZE = 16
        self.background = pygame.image.load('assets/sprites/screens/wall.png')
        self.screen_textures = {}
        self.load_screen(path)
        self.load_images()
        self.load_blocks()
    
    def load_screen(self, path):
        with open(path, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            self.screen = [row for row in reader]
        self.width = len(self.screen[0])
        self.height = len(self.screen)

    def load_images(self):
        images = [image for image in os.listdir('assets/sprites/screen_textures')]
        for image in images:
            ind = image[:image.index('.')]
            self.screen_textures[ind] = pygame.image.load('assets/sprites/screen_textures/'+image)
            self.screen_textures[ind].set_colorkey('white')

    def make_blocks(self, block):
        return [pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE, self.CHUNK_SIZE/2, self.CHUNK_SIZE/2)
                for y, row in enumerate(self.screen) for x, tile in enumerate(row) if tile == block]

    def load_blocks(self):
        self.walls = [pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE, self.CHUNK_SIZE, self.CHUNK_SIZE)
                      for y, row in enumerate(self.screen) for x, tile in enumerate(row) if len(tile) == 3]
        self.lava = self.make_blocks('2')
        self.water = self.make_blocks('3')
        self.toxic = self.make_blocks('4')
        self.fire_gems = self.make_blocks('21')
        self.water_gems = self.make_blocks('31')
        self.life_gems = self.make_blocks('41')
