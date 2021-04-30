import pygame, random
import sys
import numpy as np
from NeuralNetwork import neuralNetwork
from pygame.locals import *
import math


WIN_HEIGHT = 800
WIN_WIDTH = 500
POPULATION = 250
maxScore = 0
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT),pygame.SRCALPHA)

# bg image
bg_surface = pygame.image.load('Assets/bg.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# base image
floor_surface = pygame.image.load('Assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)


# bird image
bird_surface = pygame.image.load('Assets/bird2.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)

# pipe image
pipe_surface = pygame.image.load('Assets/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

#class HUD
class HUD:
    def __init__(self):
        self.font = pygame.font.Font('Assets/Raleway-Regular.ttf', 24)
        self.X = 300
        self.Y = 100
        self.string = 'Generation Number : 1'
        self.text = self.font.render(self.string, True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.X / 2, self.Y / 2)

        self.X1 = 300
        self.Y1 = 150
        self.string1 = 'No. of Birds: 500'
        self.text1 = self.font.render(self.string1, True, (255, 255, 255))
        self.textRect1 = self.text1.get_rect()
        self.textRect1.center = (self.X1 / 2, self.Y1 / 2)

        self.X2 = 300
        self.Y2 = 200
        self.string2 = 'Max Score: 0'
        self.text2 = self.font.render(self.string2, True, (255, 255, 255))
        self.textRect2 = self.text2.get_rect()
        self.textRect2.center = (self.X2 / 2, self.Y2 / 2)

    def updateGen(self,genNum):
        self.string = "Generation Number: "+str(genNum)
        self.text = self.font.render(self.string, True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.X / 2, self.Y / 2)

    def updateBirdNum(self,birdNum):
        self.string1 = "No. of Birds: "+str(birdNum)
        self.text1 = self.font.render(self.string1, True, (255, 255, 255))
        self.textRect1 = self.text1.get_rect()
        self.textRect1.center = (self.X1 / 2, self.Y1 / 2)

    def updateMaxScore(self,maxScore):
        self.string2 = 'Max Score: '+ str(maxScore)
        self.text2 = self.font.render(self.string2, True, (255, 255, 255))
        self.textRect2 = self.text2.get_rect()
        self.textRect2.center = (self.X2 / 2, self.Y2 / 2)

    def draw(self,screen):
        rect = Rect(15, 30, 275, 100)
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, (0,0,0,127), shape_surf.get_rect())
        screen.blit(shape_surf, rect)
        screen.blit(self.text,self.textRect)
        screen.blit(self.text1,self.textRect1)
        screen.blit(self.text2,self.textRect2)
        

# bird class
class Bird:
    def __init__(self,brain = None):
        self.x = 50
        self.y = 375
        self.bird_rect = bird_surface.get_rect(center=(self.x, self.y))
        self.vel = 0
        if brain !=None:
            self.brain = brain
        else:
            self.brain = neuralNetwork(4, 4, 2, 0.1)
        self.score = 0
        self.fitness = 0
        self.height = self.y

    def jump(self):
        self.vel = 0
        self.vel -= 6

    def move(self):
        # game variables
        gravity = 0.25
        self.score += 1
        self.vel += gravity
        self.bird_rect.centery += self.vel
        if self.bird_rect.centery >= WIN_HEIGHT:
            self.bird_rect.centery = WIN_HEIGHT
        if self.bird_rect.centery <= 0:
            self.bird_rect.centery = 0
        self.y = self.bird_rect.centery

    def draw(self, win):
        win.blit(bird_surface, self.bird_rect)

    def think(self,pipes):
        closest = None
        closestD = np.inf
        for pipe in pipes:
            d = pipe.top_pipe.left - self.x
            if d < closestD and d > 0 :
                closest = pipe
                closestD = d

        inputs = [0,0,0,0]
        output = []
        if closest != None:
            inputs[0] = self.y / WIN_HEIGHT
            inputs[1] = closest.top_pipe.midbottom[1] / WIN_HEIGHT
            inputs[2] = closest.bottom_pipe.midtop[1] / WIN_HEIGHT
            inputs[3] = closest.bottom_pipe.left / WIN_WIDTH
            output = self.brain.predict(inputs)

        if len(output):
            if output[0] > output[1]:
                 self.jump()

    def collision(self,pipes):
        for i in range(len(pipes)-1,-1,-1):
            if self.bird_rect.colliderect(pipes[i].top_pipe) or self.bird_rect.colliderect(pipes[i].bottom_pipe):
                return 1
        #if self.bird_rect.top <= -100 or self.bird_rect.bottom >= WIN_HEIGHT - 180:
            #print("collision")
         #   return 0
        return 0
# pipe class
class Pipe:
    def __init__(self):
        pipe_height = [500, 600, 700]
        self.height = random.choice(pipe_height)
        self.bottom_pipe = pipe_surface.get_rect(midtop=(400, self.height))
        self.top_pipe = pipe_surface.get_rect(midbottom=(400, self.height - 300))

    def move_pipes(self,pipes):
        self.bottom_pipe.left -= 4
        self.top_pipe.left -= 4
        if self.top_pipe.left <= - self.top_pipe.width:
            for i in range(len(pipes)-1,-1,-1):
                if pipes[i] == self:
                    pipes.pop(i)

    def draw_pipes(self,screen):
        screen.blit(pipe_surface, self.bottom_pipe)
        flip_pipe = pygame.transform.flip(pipe_surface, False, True)
        screen.blit(flip_pipe, self.top_pipe)

# ground class
"""class Ground:
    def __init__(self,y):
        self.y = y
        self.x = 0

    def move_floor(self):
        self.x -= 1
        if self.x <= -500:
            self.x = 0

    def draw_floor(self, screen):
        screen.blit(floor_surface, (self.x, self.y))
        screen.blit(floor_surface, (self.x + 500, self.y))
"""

def draw_surfaces(screen, pipes, hud, birdNum):
    
    screen.blit(bg_surface, (0, 0))
    for pipe in pipes:
          pipe.draw_pipes(screen)
    hud.updateBirdNum(birdNum)
    hud.draw(screen)

#crossover
def crossover(parent1,parent2):
    a = np.random.uniform(0,1)
    child1 = Bird()
    child2 = Bird()
    for i in range(len(parent1.brain.wih)):
            for j in range(len(parent1.brain.wih[i])):
                child1.brain.wih[i][j] = a*(parent1.brain.wih[i][j]+ (1-a)*parent2.brain.wih[i][j])
                child2.brain.wih[i][j] = a*(parent2.brain.wih[i][j]+ (1-a)*parent1.brain.wih[i][j])
    
    for i in range(len(parent1.brain.who)):
            for j in range(len(parent1.brain.who[i])):
                child1.brain.who[i][j] = a*(parent1.brain.who[i][j]+ (1-a)*parent2.brain.who[i][j])
                child2.brain.who[i][j] = a*(parent2.brain.who[i][j]+ (1-a)*parent1.brain.who[i][j])

    return child1,child2

# picks a child from the previous generation randomly
def pick_child(savedBirds):
    i = 0
    r = np.random.uniform(0,1)
    while r > 0:
        r = r - savedBirds[i].fitness
        i+=1
    i-=1
    bird = savedBirds[i]
    child = Bird(bird.brain)
    child.brain.map_mutate(0.1)
    return child

# returns fitness score
def calculate_fitness(birds):
    sum = 0
    for bird in birds:
        sum += bird.score
    for bird in birds:
        bird.fitness = bird.score / sum

# creates new population of birds randomly picked out of previous generation with its experience intact
def next_gen(birds,savedBirds):
    calculate_fitness(savedBirds)
    for i in range(0,int(POPULATION-POPULATION/10)):
        birds.append(pick_child(savedBirds))
    for i in range(0,int(0.1*POPULATION)):
        birds.append(Bird())
    savedBirds = []
    return savedBirds

def main(win):
    clock = pygame.time.Clock()
    pipe_list = []
    savedBirds = []
    birds = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)
    hud = HUD()
    genNum = 1

    for i in range(0,POPULATION):
        birds.append(Bird())

    while True:
        global maxScore

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_SPACE:
             #       bird.jump()
            if event.type == SPAWNPIPE:
                pipe_list.append(Pipe())

        draw_surfaces(win, pipe_list,hud,len(birds))

        for i in range(len(birds)-1,-1,-1):
            if(birds[i].score>maxScore):
                maxScore=birds[i].score
                hud.updateMaxScore(maxScore)    
            birds[i].think(pipe_list)
            birds[i].move()
            birds[i].draw(win)
            if birds[i].collision(pipe_list) == 1:
                savedBirds.append(birds.pop(i))

        if len(birds) == 0:
            genNum+=1
            hud.updateGen(genNum)
            savedBirds=next_gen(birds,savedBirds)
            pipe_list = []
        for pipe in pipe_list:
            pipe.move_pipes(pipe_list)

        pygame.display.update()
        clock.tick(120)

main(screen)