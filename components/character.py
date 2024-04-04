import pygame


class Character:
    def __init__(self, location, image, left_image, right_image, element):
        self.image = image
        self.left_image = left_image
        self.right_image = right_image
        self.element = element
        self.rect = pygame.Rect(location[0], location[1], self.image.get_width(), self.image.get_height())
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.y_velocity = 0
        self.air_timer = 0
        self.alive = True

    def move(self):
        SPEED, THRUST, GRAVITY, DRAG = 3, -5, 0.2, 3
        self.movement = [0, 0]
        if self.moving_right:
            self.movement[0] += SPEED
        if self.moving_left:
            self.movement[0] -= SPEED
        if self.jumping:
            self.y_velocity = THRUST
            self.jumping = False
        self.movement[1] += self.y_velocity
        self.y_velocity += GRAVITY
        if self.y_velocity > DRAG:
            self.y_velocity = DRAG
