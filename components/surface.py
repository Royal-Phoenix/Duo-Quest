'''
from pygame.locals import *
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480), RESIZABLE)
bg = pygame.image.load('assets/sprites/bg.jpg')
bg_rect = bg.get_rect()
frame = pygame.Rect(0, 0, 640, 480)
display = pygame.Surface(bg_rect.size)
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and bg_rect.left < frame.left < bg_rect.right:
        frame.x -= 5
    if keys[K_RIGHT] and bg_rect.left < frame.right < bg_rect.right:
        frame.x += 5
    if keys[K_UP] and bg_rect.top < frame.top < bg_rect.bottom:
        frame.y -= 5
    if keys[K_DOWN] and bg_rect.top < frame.bottom < bg_rect.bottom:
        frame.y += 5
    display.blit(bg, (0, 0))
    screen.blit(display, (0, 0), area=frame)
    pygame.display.update()
    clock.tick(60)  # keep speed 60 FPS (Frames Per Second)

pygame.quit()
'''

'''
from pygame.locals import *
import pygame

pygame.init()
window = pygame.display.set_mode((640, 480), RESIZABLE)
window_rect = window.get_rect()
world_image = pygame.image.load('assets/sprites/bg.jpg')
bg_rect = world_image.get_rect()
fire = pygame.image.load('assets/sprites/players/fire_boy.png')
fire.set_colorkey('white')
fire_rect = pygame.Rect(100, 100, fire.get_width(), fire.get_height())
water = pygame.image.load('assets/sprites/players/water_girl.png')
water.set_colorkey('white')
water_rect = pygame.Rect(120, 100, water.get_width(), water.get_height())
frame = pygame.Rect(0, 0, 640, 480)
display = pygame.Surface(bg_rect.size)
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    # if keys[K_LEFT] and bg_rect.left < frame.left < bg_rect.right:
    if keys[K_LEFT]:
        if fire_rect.left < frame.left:
            frame.x -= 5
        if fire_rect.left > bg_rect.left:
            fire_rect.x -= 5
    if keys[K_a]:
        if water_rect.left < frame.left:
            frame.x -= 5
        if water_rect.left > bg_rect.left:
            water_rect.x -= 5
    
    # if keys[K_RIGHT] and  bg_rect.left < frame.right < bg_rect.right:
    if keys[K_RIGHT]:
        if fire_rect.right > frame.right:
            frame.x += 5
        if fire_rect.right < bg_rect.right:
            fire_rect.x += 5
    if keys[K_d]:
        if water_rect.right > frame.right:
            frame.x += 5
        if water_rect.right < bg_rect.right:
            water_rect.x += 5
    
    # if keys[K_UP] and bg_rect.top < frame.top < bg_rect.bottom:
    if keys[K_UP]:
        if fire_rect.top < frame.top:
            frame.y -= 5
        if fire_rect.top > bg_rect.top:
            fire_rect.y -= 5
    if keys[K_w]:
        if water_rect.top < frame.top:
            frame.y -= 5
        if water_rect.top > bg_rect.top:
            water_rect.y -= 5
    
    # if keys[K_DOWN] and bg_rect.top < frame.bottom < bg_rect.bottom:
    if keys[K_DOWN]:
        if fire_rect.bottom > frame.bottom:
            frame.y += 5
        if fire_rect.bottom < bg_rect.bottom:
            fire_rect.y += 5
    if keys[K_s]:
        if water_rect.bottom > frame.bottom:
            frame.y += 5
        if water_rect.bottom < bg_rect.bottom:
            water_rect.y += 5
    
    display.blit(world_image, (0, 0))
    display.blit(fire, fire_rect)
    display.blit(water, water_rect)
    window.blit(display, (0, 0), area=frame)
    pygame.display.update()
    clock.tick(60)  # keep speed 60 FPS (Frames Per Second)

pygame.quit()
'''

'''
from pygame.locals import *
import pygame

pygame.init()
window = pygame.display.set_mode((640, 480), RESIZABLE)
window_rect = window.get_rect()
world_image = pygame.image.load('assets/sprites/bg.jpg')  # .convert()
# world_image = pygame.transform.smoothscale(world_image, (2000, 2000))
bg_rect = world_image.get_rect()
player_image = pygame.Surface((40, 40))
player_image.fill((255, 0, 0))
player_rect = player_image.get_rect(centerx=window_rect.centerx, centery=window_rect.centery)
frame = pygame.Rect(0, 0, 640, 480)
direction = 'right'
display = pygame.Surface(bg_rect.size)
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if direction == 'right':
        # move right
        frame.x += 5
        player_rect.x += 5
        # change direction
        if frame.right > bg_rect.right:
            frame.x -= 5
            player_rect.x -= 5
            direction = 'left'
    else:
        # move left
        frame.x -= 5
        player_rect.x -= 5
        # change direction
        if frame.left < bg_rect.left:
            frame.x += 5
            player_rect.x += 5
            direction = 'right'
    display.blit(world_image, (0, 0))
    display.blit(player_image, player_rect)
    window.blit(display, (0, 0), area=frame)
    pygame.display.update()
    clock.tick(60)  # keep speed 60 FPS (Frames Per Second)

pygame.quit()
'''
