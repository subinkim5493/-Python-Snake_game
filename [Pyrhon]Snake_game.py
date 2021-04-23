import pygame
import sys
import time
import random

from pygame.locals import *



win_width = 800
win_height = 600
grid_size = 20
grid_width = win_width / grid_size      # 40
grid_height = win_height / grid_size    # 30

white = (255, 255, 255)
green = (0, 100, 0)
red = (255, 0, 0)
gray = (100, 100, 100)

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FPS = 10

class Python(object):
    def __init__(self):
        self.creat()
        self.color = green
        
    def creat(self):
        self.length = 2
        self.positions = [((win_width /2),(win_height/2))] # in the middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def control(self, xy):
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy


    def move(self):
        cur = self.positions[0]
        x,y = self.direction
        new = (((cur[0] + (x * grid_size)) % win_width), (cur[1] + (y * grid_size)) % win_height)

        if new in self.positions[2:]:
            self.creat()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def eat(self):
        self.length += 1

    def draw(self,surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

class Feed(object):
    def __init__(self):
        self.position = (0,0)
        self.color = red
        self.creat()

    def creat(self):
        self.position = (random.randint(0,grid_width-1)*grid_size , random.randint(0, grid_height-1)*grid_size)
    
    def draw(self, surface):
        draw_object(surface, self.color, self.position)


    
def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0],pos[1]),(grid_size,grid_size))
    pygame.draw.rect(surface,color, r)



def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        feed.creat()

def show_info(length, speed, surface):
    font = pygame.font.Font(None,34)
    text = font.render("Length : " + str(length)+ " speed : " + str(round(speed,2)),1,gray)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos) 



if __name__ == "__main__":
    python = Python()
    feed = Feed()



    pygame.init()

    window = pygame.display.set_mode((win_width, win_height),0,32)
    pygame.display.set_caption("Subinkim")
    surface = pygame.Surface(window.get_size()) 
    surface = surface.convert()
    surface.fill(white)
    clock = pygame.time.Clock()
    
    pygame.key.set_repeat(1, 40)
    window.blit(surface,(0,0))


    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.control(UP)
                elif event.key == K_DOWN:
                    python.control(DOWN)
                elif event.key == K_LEFT:
                    python.control(LEFT)
                elif event.key == K_RIGHT:
                    python.control(RIGHT) 
        
        surface.fill(white)
        python.move()
        check_eat(python,feed)
        speed = (FPS + python.length) /2
        show_info(python.length, speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface,(0,0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)
