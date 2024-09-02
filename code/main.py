import pygame
import random
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# General setup
pygame.init() 
# width and height of game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

# basic surface
# surf = pygame.Surface((100,200))
# surf.fill('orange')

player = Player()

# Imports 
# Importing an image (by default means we are importing a surface)
# Notes: Using convert or convert_alpha on an image will improve performance.
# Moved into a class for cleanliness
# player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2(0, 0)
player_speed = 300

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT-20))

while running:
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # input
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_direction * player_speed * dt
    
    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print('fire laser')
            
    # Draw the game (display order matters, last display is on top)
    display_surface.fill('black') 
    
    # Drawing 20 stars.
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    
    # Player movement (Replaced with user input in the event loop)
    # if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
    #     player_direction.y *= -1
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction.x *= -1
    
    # player_rect.x += 20
    # player_rect.y -= 10
    
    # Adding a vector to the tuple position of the rect to avoid 2 lines of code.
    # player_rect.center += player_direction * player_speed * dt
        
    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    #display_surface.blit(player_surf, player_rect) # Attaching the surface, surf, to the display_surface
    display_surface.blit(player.image, player.rect) 
    pygame.display.update()
    
pygame.quit()