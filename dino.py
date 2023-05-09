import pygame
from pygame.locals import *
import os
import random

pygame.init()

width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
dino_img = [pygame.image.load(os.path.join('imgs', 'dino_run1.png')), pygame.image.load(os.path.join('imgs', 'dino_run2.png')), pygame.image.load(os.path.join('imgs', 'dino_duck1.png')), pygame.image.load(os.path.join('imgs', 'dino_duck2.png'))]
base_img = pygame.image.load(os.path.join('imgs', 'ground.png'))
obstacle_img = [pygame.image.load(os.path.join('imgs', 'cactus_1.png')),pygame.image.load(os.path.join('imgs', 'cactus_2.png')),pygame.image.load(os.path.join('imgs', 'cactus_3.png'))]
bird_img = [pygame.image.load(os.path.join('imgs', 'bird_1.png')), pygame.image.load(os.path.join('imgs', 'bird_2.png'))]
#print(350 + dino_img[0].get_height())
#print(444 - dino_img[2].get_height())
class Dino:
     
    def __init__(self):
        self.x = 70
        self.y = 350
        self.dino = dino_img
        self.img_count = 0
        self.img_index = 0
        self.is_in_air = False
        self.vel = 0
        self.in_air_cnt = 0
        self.is_ducking = False;
    
    def toggle_ducking(self): 
        self.is_ducking = not self.is_ducking
 
        

    def draw(self, screen):
        if(self.is_in_air):
            self.jump()
        self.img_count += 1
        if(self.img_count >= 20 and not self.is_in_air):
            self.img_count = 0
            self.img_index = 0
            if(self.is_ducking):
                self.img_index = 2
        if(self.img_count >= 10 and not self.is_in_air):
            self.img_index = 1
            if(self.is_ducking):
                self.img_index = 3
                
        if(self.img_index >= 2):
            self.y = 384
            screen.blit(self.dino[self.img_index], (self.x, self.y))
            
        else:
            if not self.is_in_air:
                self.y = 350
            screen.blit(self.dino[self.img_index], (self.x, self.y ))
    
    def set_jump(self):
        self.is_in_air = True
        self.vel = 64
        self.in_air_cnt = 0

    def jump(self): 
        self.y -= self.vel

        if self.vel > 0:
            self.vel = self.vel // 2
        elif self.vel == 0:
            if self.in_air_cnt > 15:
                self.vel = -1
            else:
                self.in_air_cnt += 1
        else:
            self.vel *= 2

        if self.y == 350:
            self.is_in_air = False

class Base:
    def __init__(self, x):
        self.x = x
        self.y = 350 + dino_img[0].get_height() - 7
        self.base = base_img
        self.vel = 10

    def draw(self, screen):
        self.move()
        screen.blit(self.base, (self.x, self.y))

    def move(self):
        self.x -= self.vel

class Bird:
    def __init__(self, x):
        self.y = 284
        self.vel = 10
        self.x = x
        self.img_count = 0
        self.img = bird_img
        self.img_index = 0
    
    def move(self):
        self.x -= self.vel
    
    def draw(self, screen):
        self.move()
        self.img_count += 1
        if self.img_count >=20:
            self.img_index = 0
            self.img_count = 0
        elif self.img_count >= 10:
            self.img_index = 1
        
        
        screen.blit(self.img[self.img_index], (self.x, self.y))

class Obstacle:
    def __init__(self, img, x):
        self.x = x;
        self.img = img
        self.vel = 10
        self.y = dino_img[0].get_height() + 353 - img.get_height() 
    
    def move(self):
        self.x -= self.vel
    
    def draw(self, screen):
        self.move()
        screen.blit(self.img, (self.x, self.y))

def draw_window(screen, dino, bases, obstacles):
    screen.fill((0,0,0))
    dino.draw(screen)
    for base in bases:
        base.draw(screen)
    if(bases[0].x + base_img.get_width() <= 0):
        del bases[0]
        bases.append(Base(base_img.get_width()))
    for obs in obstacles:
        #print(obs.x)
        #screen.blit(obstacle_img[0], (300, 450))
        obs.draw(screen)
    if obstacles[0].x < 0:
        del obstacles[0]
    pygame.display.update()

def create_obstacle() -> list[Obstacle]:
    first_rand_img = random.randint(0, 2)
    second_rand_img = random.randint(0, 2)
    first_x = random.randint(1000, 1500)
    is_bird = random.randint(0, 100)
    if(is_bird > 70):
        obstacles = [Obstacle(obstacle_img[first_rand_img], first_x), Bird(first_x + random.randint(400, 1000))]
    else:
        obstacles = [Obstacle(obstacle_img[first_rand_img], first_x), Obstacle(obstacle_img[second_rand_img], first_x + random.randint(300, 800))]
    return obstacles

running = True
game_over = False
dino = Dino()
bases = [Base(0), Base(base_img.get_width())]
clock = pygame.time.Clock()
obstacles = create_obstacle()
while running:
    clock.tick(60)
    
    # keys = pygame.key.get_pressed()
    # if keys[K_DOWN] and not dino.is_in_air:
    #     dino.toggle_ducking()
    # else:
    #     dino.toggle_not_ducking()
    if not game_over:
        draw_window(screen, dino, bases, obstacles)
        if len(obstacles) == 0:
            obstacles = create_obstacle()
        dino_mask = pygame.mask.from_surface(dino.dino[dino.img_index])
        obstacle_mask = ''
        if (isinstance(obstacles[0].img, list)):
            obstacle_mask = pygame.mask.from_surface(obstacles[0].img[obstacles[0].img_index])
            
        else:
            obstacle_mask = pygame.mask.from_surface(obstacles[0].img)
        off_set = (obstacles[0].x - dino.x, obstacles[0].y - dino.y)
        collide = dino_mask.overlap(obstacle_mask, off_set)
        if collide:
            game_over = True
    else:
        screen.fill((0,0,0))
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (440, 100))
        screen.blit(dino.dino[dino.img_index], (dino.x, dino.y))
        for base in bases:
            screen.blit(base.base, (base.x, base.y))
        for obs in obstacles:
            if (isinstance(obs.img, list)):
                screen.blit(obs.img[obs.img_index], (obs.x, obs.y))
            else:
                screen.blit(obs.img, (obs.x, obs.y))
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if (event.key == K_SPACE or event.key == K_UP) and not dino.is_in_air and not dino.is_ducking:
                dino.set_jump()
            elif event.key == K_DOWN and not dino.is_in_air:
                dino.toggle_ducking()
    


pygame.quit()
