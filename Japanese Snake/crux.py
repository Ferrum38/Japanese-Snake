import pygame
import random
from enum import Enum
from collections import namedtuple
from pygame import mixer

pygame.init()
mixer.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
Xcoord = 640
Ycoord = 480

Point = namedtuple('Point', "x, y")

#colours
WHITE = (255, 255, 255)
GREEN = (0, 51, 0)
BLUE1 = (255, 255, 255)
BLUE2 = (200, 0 , 0)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        #initialise display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Japanese_Snake")
        self.clock = pygame.time.Clock()
        #initialise game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                        Point(self.head.x-BLOCK_SIZE, self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
            x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
            y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
            self.food = Point(x, y)
            if self.food in self.snake:
                self._place_food()
        
        
    def play_step(self):
        #1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_s:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_w:
                    self.direction = Direction.UP

        #2. move
        self._move(self.direction) #update the heads
        self.snake.insert(0, self.head)

        #3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score


        #4 place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else: 
            self.snake.pop()

            
        #5 update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        #6 return if game over and score
        return game_over, self.score

        
    def _is_collision(self):
                #checking if it his the boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0 :
            return True
        #hits self
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):   
        display_surface = pygame.display.set_mode((Xcoord, Ycoord ))
        image = pygame.image.load('john_xina.png')
        display_surface.blit(image, (0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Sushi: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
            x = self.head.x
            y = self.head.y
            if direction == Direction.RIGHT:
                x += BLOCK_SIZE
            elif direction == Direction.LEFT:
                x -= BLOCK_SIZE
            elif direction == Direction.UP:
                y -= BLOCK_SIZE
            elif direction == Direction.DOWN:
                y += BLOCK_SIZE

            self.head = Point(x, y)

            

if __name__ == '__main__':
    game = SnakeGame()
    pygame.mixer.music.load('Japan_gog.mp3')
    pygame.mixer.music.play(-1)


    # game while loop
    while True:
        game_over, score = game.play_step()

        #break if game over
        if game_over == True:
            break
    print("Sushi Collected", score)


    pygame.quit()
