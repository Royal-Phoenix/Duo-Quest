from pygame.locals import *
import pygame


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480), RESIZABLE)
        pygame.display.set_caption("Duo Quest")
        self.display = pygame.Surface((34*16, 25*16))

    def draw_level_screen(self, level_select):
        self.display.blit(level_select.screen, (0, 0))
        for level in range(5):
            image = level_select.levels[level + 1]
            title_x = (self.display.get_width() - image.get_width()) / 2
            title_y = 50 * level + 100
            self.display.blit(image, (title_x, title_y))
        self.display.blit(level_select.watergirl_logo, (50, 150))
        self.display.blit(level_select.fireboy_logo, (430, 150))

    def level_select_screen(self, level_select, controller):
        ind = 1
        while True:
            self.draw_level_screen(level_select)
            events = pygame.event.get()
            if controller.press_key(events, K_DOWN):
                ind = 1 if ind > 4 else ind+1
            if controller.press_key(events, K_UP):
                ind = 5 if ind < 2 else ind-1
            self.draw_level_select_indicator(level_select, ind)
            if controller.press_key(events, K_RETURN):
                return 'level'+str(ind)

    def draw_level_select_indicator(self, level_select, level_index):
        indicator = level_select.indicator
        location_x = (self.display.get_width() - indicator.get_width()) / 2
        location_y = (level_index-1) * 50 + 96
        self.display.blit(indicator, (location_x, location_y))
        self.refresh_window()

    def refresh_window(self):
        new_window_size, center_cords = self.adjust_scale()
        new_disp = pygame.transform.scale(self.display, new_window_size)
        self.screen.blit(new_disp, center_cords)
        pygame.display.update()

    def adjust_scale(self):
        window_size = self.screen.get_size()
        if window_size[0] / window_size[1] >= 1.5:
            display_size = (int(1.5 * window_size[1]), window_size[1])
        else:
            display_size = (window_size[0], int(0.75 * window_size[0]))
        # display_size = self.screen.get_size()
        coords = ((window_size[0] - display_size[0]) / 2, (window_size[1] - display_size[1]) / 2)
        return display_size, coords

    def draw_screen(self, screen):
        self.display.blit(screen.background, (0, 0))  # Try self.screen for funny shit
        screen_textures = screen.screen_textures
        for y, row in enumerate(screen.screen):
            for x, tile in enumerate(row):
                if tile != "0":
                    self.display.blit(screen_textures[f"{tile}"], (x * 16, y * 16))

    @staticmethod
    def color_fill(surface, color):
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                if surface.get_at((x, y)) == Color(0, 0, 0):
                    surface.set_at((x, y), color)

    def draw_gates(self, gates):
        for gate in gates:
            gate_image = gate.gate_image
            self.color_fill(gate_image, gate.color)
            self.display.blit(gate_image, gate.gate_location)
            for location in gate.plate_locations:
                plate_image = gate.plate_image
                self.color_fill(plate_image, gate.color)
                self.display.blit(plate_image, location)

    def draw_doors(self, doors):
        for door in doors:
            self.display.blit(door.door_background, door.background_location)
            self.display.blit(door.door_image, door.door_location)
            self.display.blit(door.frame_image, door.frame_location)

    def draw_player(self, players):
        for player in players:
            player_image = player.left_image if player.moving_left else player.right_image if player.moving_right else player.image
            player_image.set_colorkey('white')
            self.display.blit(player_image, (player.rect.x, player.rect.y))

    def move_player(self, screen, gates, players):
        for player in players:
            player.move()
            movement = player.movement
            collide_blocks = screen.walls
            for gate in gates:
                collide_blocks += [gate.gate]
            collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
            player.rect.x += movement[0]
            hit_list = self.check_collision(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[0] > 0:
                    player.rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    player.rect.left = tile.right
                    collision_types['left'] = True
            player.rect.y += movement[1]
            hit_list = self.check_collision(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[1] > 0:
                    player.rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    player.rect.top = tile.bottom
                    collision_types['top'] = True
            if collision_types['bottom']:
                player.y_velocity = 0
                player.air_timer = 0
            else:
                player.air_timer += 1
            if collision_types['top']:
                player.y_velocity = 0

    def check_for_death(self, screen, players):
        for player in players:
            if player.element == "water":
                is_killed = self.check_collision(player.rect, screen.lava)
            if player.element == "fire":
                is_killed = self.check_collision(player.rect, screen.water)
            is_killed += self.check_collision(player.rect, screen.toxic)
            if is_killed:
                player.alive = False

    def check_door_open(self, door, player):
        door_collision = self.check_collision(player.rect, [door.rect])
        door.player_at_door = True if door_collision else False
        door.control_door()

    def check_gate_press(self, gates, players):
        for gate in gates:
            plate_collisions = []
            for player in players:
                plate_collisions += self.check_collision(player.rect, gate.plates)
            gate.plate_pressed = True if plate_collisions else False
            gate.control_gate()

    def check_gem_collision(self, screen, gems, player):
        for gem in gems:
            if self.check_collision(player.rect, [gem]):
                screen[gem.y//16][gem.x//16] = '0'
                break

    def check_gem_collect(self, screen, players):
        for player in players:
            if player.element == "fire":
                self.check_gem_collision(screen.screen, screen.fire_gems, player)
            if player.element == "water":
                self.check_gem_collision(screen.screen, screen.water_gems, player)
            self.check_gem_collision(screen.screen, screen.life_gems, player)

    @staticmethod
    def level_complete(doors):
        return True if [door.door_open for door in doors] == [True] * 2 else False

    @staticmethod
    def check_collision(rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile)]
