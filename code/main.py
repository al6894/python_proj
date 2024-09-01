import pygame
from random import randint, uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
        
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 2000
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        # This implemention results in importing the surfaces each time.
        # self.image = pygame.image.load(join('images', 'star.png')).convert_alpha()
        self.image = surf
        self.rect = self.image.get_frect(center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

# General setup
pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


# Imports 
# Importing an image (by default means we are importing a surface)
# Notes: Using convert or convert_alpha on an image will improve performance.
# Moved into a class for cleanliness
# player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# No longer needed after player became a class.
# player_direction = pygame.math.Vector2(0, 0)
# player_speed = 300
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
# star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
# star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
# meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
# meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
player = Player(all_sprites)
# laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
# laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT-20))

# creating meteors using an interval timer
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)
            
    # input
    # Moved all this into player class
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_direction * player_speed * dt
    
    # recent_keys = pygame.key.get_just_pressed()
    # if recent_keys[pygame.K_SPACE]:
    #     print('fire laser')
    all_sprites.update(dt)
            
    # Draw the game (display order matters, last display is on top)
    display_surface.fill('black') 
    
    # Drawing 20 stars.
    # for pos in star_positions:
    #     display_surface.blit(star_surf, pos)
    
    # Player movement (Replaced with user input in the event loop)
    # if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
    #     player_direction.y *= -1
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction.x *= -1
    
    # player_rect.x += 20
    # player_rect.y -= 10
    
    # Adding a vector to the tuple position of the rect to avoid 2 lines of code.
    # player_rect.center += player_direction * player_speed * dt
        
    # Line 87 removed since we moved player into a class.
    #display_surface.blit(player_surf, player_rect) # Attaching the surface, surf, to the display_surface
    
    # display_surface.blit(meteor_surf, meteor_rect)
    # display_surface.blit(laser_surf, laser_rect)
    all_sprites.draw(display_surface)
    
    pygame.display.update()
    
pygame.quit()