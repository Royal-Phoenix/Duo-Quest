import pygame


class Gates:
    def __init__(self, gate_location, plate_locations, color, type, open_type, movement=32, plate_attach=False):
        self.gate_location = gate_location
        self.plate_locations = plate_locations
        self.plate_pressed = False
        self.color = color
        self.type = type
        self.open_type = open_type
        self.gate_movement = movement
        self.plate_attach = plate_attach
        self.gate_open = False
        self.initial_pos = 0
        self.gate_image = pygame.image.load('assets/sprites/objects/'+self.type+'gate.png')
        self.plate_image = pygame.image.load('assets/sprites/objects/plate.png')
        self.gate = pygame.Rect(self.gate_location[0], self.gate_location[1], self.gate_image.get_width(),
                                self.gate_image.get_height())
        self.plates = [pygame.Rect(location[0], location[1], self.plate_image.get_width(),
                                   self.plate_image.get_height()) for location in self.plate_locations]

    def move_gate(self):
        SPEED = 1
        i = 1 if self.open_type in ['N', 'W'] else -1
        j = 1 if self.gate_open else -1
        dx, dy = (0, i*j*SPEED) if self.open_type in ['N', 'S'] else (i*j*SPEED, 0)
        self.gate_location = (self.gate_location[0] + dx, self.gate_location[1] + dy)
        if self.open_type in ['N', 'S']:
            self.gate.y += dy
        else:
            self.gate.x += dx
        if self.plate_attach:
            self.plate_locations = [[plate_x+dx, plate_y+dy] for plate_x, plate_y in self.plate_locations]
            self.plates = [pygame.Rect(x+dx, y+dy, w, h) for x, y, w, h in self.plates]
        self.initial_pos += -j*SPEED
        

    def control_gate(self):
        if self.plate_pressed and not self.gate_open:
            self.move_gate()
            if self.initial_pos >= self.gate_movement:
                self.gate_open = True
        if not self.plate_pressed and self.gate_open:
            self.move_gate()
            if self.initial_pos <= 0:
                self.gate_open = False
