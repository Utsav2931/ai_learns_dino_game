import pygame
from pygame.locals import *
import os
import random
import neat

pygame.init()


width, height = 800, 600
dino_img = [pygame.image.load(os.path.join('imgs', 'dino_run1.png')), pygame.image.load(os.path.join('imgs', 'dino_run2.png')), pygame.image.load(os.path.join('imgs', 'dino_duck1.png')), pygame.image.load(os.path.join('imgs', 'dino_duck2.png'))]
base_img = pygame.image.load(os.path.join('imgs', 'ground.png'))
obstacle_img = [pygame.image.load(os.path.join('imgs', 'cactus_1.png')),pygame.image.load(os.path.join('imgs', 'cactus_2.png')),pygame.image.load(os.path.join('imgs', 'cactus_3.png'))]
bird_img = [pygame.image.load(os.path.join('imgs', 'bird_1.png')), pygame.image.load(os.path.join('imgs', 'bird_2.png'))]

original_width = obstacle_img[1].get_width()
original_height = obstacle_img[1].get_height() 
original_width *= 1.3
obstacle_img[1] = pygame.transform.scale(obstacle_img[1], (original_width, original_height)) 
original_width = obstacle_img[0].get_width()
original_height = obstacle_img[0].get_height() * 1.3
original_width *= 2
obstacle_img[0] = pygame.transform.scale(obstacle_img[0], (original_width, original_height)) 
original_width = obstacle_img[2].get_width() * 1.3
original_height = obstacle_img[2].get_height() * 1.2 
obstacle_img[2] = pygame.transform.scale(obstacle_img[2], (original_width, original_height)) 


gen = 0
class Dino:
     
    def __init__(self, x):
        self.x = x
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
        elif(self.img_count >= 10 and not self.is_in_air):
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
        self.vel = 15

    def draw(self, screen):
        self.move()
        screen.blit(self.base, (self.x, self.y))

    def move(self):
        self.x -= self.vel

class Bird:
    def __init__(self, x):
        self.y = 300
        self.vel = 15
        self.x = x
        self.img_count = 0
        self.img = bird_img
        self.img_index = 0
    
    def move(self):
        self.x -= self.vel
    
    def draw(self, screen):
        self.move()
        self.img_count += 1
        if self.img_count >=16:
            self.img_index = 0
            self.img_count = 0
        elif self.img_count >= 8:
            self.img_index = 1
        
        
        screen.blit(self.img[self.img_index], (self.x, self.y))

class Obstacle:
    def __init__(self, img, x):
        self.x = x;
        self.img = img
        self.vel = 15
        self.y = dino_img[0].get_height() + 353 - img.get_height() 
    
    def move(self):
        self.x -= self.vel
    
    def draw(self, screen):
        self.move()
        screen.blit(self.img, (self.x, self.y))

def draw_window(screen, dinos, bases, obstacles, instance):
    global gen
    pygame.font.init()
    screen.fill((0,0,0))
    font = pygame.font.Font(None, 36)
    text = font.render("Gen: " + str(gen), True, (255, 255, 255))
    screen.blit(text, (100, 100))
    font = pygame.font.Font(None, 36)
    text = font.render("Alive: " + str(len(dinos)), True, (255, 255, 255))
    screen.blit(text, (100, 150))
    font = pygame.font.Font(None, 36)
    #text = font.render("Is Bird: " + str((instance)), True, (255, 255, 255))
    #screen.blit(text, (500, 200))
    for dino in dinos:
        dino.draw(screen)
    for base in bases:
        base.draw(screen)
    if(bases[0].x + base_img.get_width() <= 0):
        del bases[0]
        bases.append(Base(base_img.get_width()))
    for obs in obstacles:
        
        obs.draw(screen)
    if obstacles[0].x < 0:
        del obstacles[0]
    pygame.display.update()

def create_obstacle(dist) -> list[Obstacle]:
    first_x = random.randint(900, 1200)
    is_bird = random.randint(0, 100)
    
    obstacles = []
    rand_obst = random.randint(0, 2)
    if(is_bird > 80 and dist > 20):
        obstacles.append(Bird(first_x))
    else:
        obstacles.append(Obstacle(obstacle_img[rand_obst], first_x))
    rand_obst = random.randint(0, 2)
    is_bird = random.randint(0, 100)
    
    if(is_bird > 80 and dist > 20):
        obstacles.append(Bird(first_x + random.randint(600, 1200)))
    else:
        obstacles.append(Obstacle(obstacle_img[rand_obst], first_x + random.randint(600,1200)))
    
    return obstacles

def main(genomes, config):
    running = True
    game_over = False
    global gen 
    gen += 1
    
    bases = [Base(0), Base(base_img.get_width())]
    clock = pygame.time.Clock()
    obstacles = create_obstacle(0)
    screen = pygame.display.set_mode((width, height))
    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        
        dinos.append(Dino(100))
        g.fitness = 0 
        ge.append(g)
    score = 0
    dist = 0
    while running:
        clock.tick(60)
        dist += 0.01
        
        if not game_over:
            if len(obstacles) == 0:
                obstacles = create_obstacle(dist)


            if len(dinos) == 0:
                running = False
            
            for x, dino in enumerate(dinos):
                output = nets[x].activate((dino.x - obstacles[0].x, dino.is_in_air, dino.is_ducking, isinstance(obstacles[0].img, list)))
                if output[0] > 0.5 and not dino.is_in_air and not dino.is_ducking:
                    dino.set_jump()
                if output[1] > 0.5 and not dino.is_in_air:
                    dino.toggle_ducking()
                    #dino.set_jump()
            
            for i in range(len(dinos)-1, -1, -1):
                dino = dinos[i]
                dino_mask = pygame.mask.from_surface(dino.dino[dino.img_index])
                obstacle_mask = ''
                if (isinstance(obstacles[0].img, list)):
                    obstacle_mask = pygame.mask.from_surface(obstacles[0].img[obstacles[0].img_index])
                    
                else:
                    obstacle_mask = pygame.mask.from_surface(obstacles[0].img)
                off_set = (obstacles[0].x - dino.x, obstacles[0].y - dino.y)
                collide = dino_mask.overlap(obstacle_mask, off_set)
                if collide:
                    ge[i].fitness -= 100
                    dinos.pop(i)
                    nets.pop(i)
                    ge.pop(i)
            
            for x, dino in enumerate(dinos):
                ge[x].fitness += dist

            draw_window(screen, dinos, bases, obstacles, isinstance(obstacles[0].img, list))
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
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        main()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if (event.key == K_SPACE or event.key == K_UP) and not dino.is_in_air and not dino.is_ducking:
                    dino.set_jump()
                elif event.key == K_DOWN and not dino.is_in_air:
                    dino.toggle_ducking()
        


    pygame.quit()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,100000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)