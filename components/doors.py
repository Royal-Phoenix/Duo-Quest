import pygame


class Doors:
    def __init__(self, location, image):
        self.door_location = location
        self.background_location = location
        self.frame_location = (location[0] - 8, location[1] - 8)
        self.door_image = image
        self.player_at_door = False
        self.height = 0
        self.door_open = False
        self.frame_image = pygame.image.load("assets/sprites/doors/door_frame.png")
        self.frame_image.set_colorkey('white')
        self.door_background = pygame.image.load("assets/sprites/doors/door_background.png")
        self.rect = pygame.Rect(self.door_location[0], self.door_location[1], self.door_image.get_width(), self.door_image.get_height())

    def control_door(self):
        SPEED = 1.5
        door_x, door_y = self.door_location
        if self.player_at_door and not self.door_open:
            self.door_location = (door_x, door_y - SPEED)
            self.height += SPEED
            if self.height >= 31:
                self.door_open = True
        elif not self.player_at_door and self.height > 0:
            self.door_location = (door_x, door_y + SPEED)
            self.height -= SPEED
            self.door_open = False
