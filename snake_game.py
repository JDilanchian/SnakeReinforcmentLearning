import pygame
import random
from enum import Enum
from collections import namedtuple 
from configuration import (SCREEN_WIDTH, SCREEN_HEIGHT, Direction, SNAKE_INITIAL, BOX_SIZE, Point, BLACK, WHITE, RED, BLUE, SPEED)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class SnakeGame:
    
    def __init__(self) -> None:
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.snake = SNAKE_INITIAL
        self.head = self.snake[0]

        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self._place_food()

    def _place_food(self):
        x = random.randrange(0, SCREEN_WIDTH - BOX_SIZE, BOX_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT - BOX_SIZE, BOX_SIZE)

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        print(self.direction)
        self._move(self.direction)

        self.snake.insert(0, self.head)

        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        box = pygame.Surface((BOX_SIZE, BOX_SIZE))

        box.fill(BLUE)
        self.display.blit(box, (self.head.x, self.head.y))

        box.fill(WHITE)
        for pt in self.snake[1:]:
            self.display.blit(box, (pt.x, pt.y))
        
        box.fill(RED)
        self.display.blit(box, (self.food.x, self.food.y))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, (0, 0))
        pygame.display.flip()

    def _is_collision(self):
        if self.head.x >= SCREEN_WIDTH or \
            self.head.x < 0 or \
            self.head.y >= SCREEN_HEIGHT or \
            self.head.y < 0 :
            return True 
        
        if self.head in self.snake[1:]:
            return True
        
        return False



    # in pygame.display.setmode increasing value of y moves the cursur toward bottom  
    def _move(self, direction):
        if direction == Direction.LEFT:
            self.head = Point(self.head.x - BOX_SIZE, self.head.y)
        elif direction == Direction.RIGHT:
            self.head = Point(self.head.x + BOX_SIZE, self.head.y)
        elif direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - BOX_SIZE)
        elif direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y  + BOX_SIZE)

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)    
    pygame.quit()