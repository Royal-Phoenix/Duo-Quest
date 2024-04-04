from pygame.locals import *
import pygame
import sys


class Controller:
    def __init__(self, left, right, up):
        self.controls = {"LEFT": left, "RIGHT": right, "UP": up}

    def control_player(self, events, player):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == self.controls["RIGHT"]:
                    player.moving_right = True
                elif event.key == self.controls["LEFT"]:
                    player.moving_left = True
                elif event.key == self.controls["UP"]:
                    if player.air_timer < 6:
                        player.jumping = True
            elif event.type == KEYUP:
                if event.key == self.controls["RIGHT"]:
                    player.moving_right = False
                elif event.key == self.controls["LEFT"]:
                    player.moving_left = False
                elif event.key == self.controls["UP"]:
                    player.jumping = False

    @staticmethod
    def press_key(events, key):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == key:
                    return True
        return False
