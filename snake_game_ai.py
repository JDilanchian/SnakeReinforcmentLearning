import pygame
import random
import copy
from enum import Enum
from collections import namedtuple 
from common import (SCREEN_WIDTH, SCREEN_HEIGHT, Direction, SNAKE_INITIAL, BOX_SIZE, Point, BLACK, WHITE, RED, BLUE, SPEED)

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision

class SnakeGameAI:
    
    def __init__(self) -> None:
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.snake = copy.deepcopy(SNAKE_INITIAL)
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

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     if event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     if event.key == pygame.K_UP:
            #         self.direction = Direction.UP
            #     if event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN
        self._move(action)

        self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

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

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > SCREEN_WIDTH - BOX_SIZE or pt.x < 0 or pt.y > SCREEN_HEIGHT - BOX_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False



    # in pygame.display.setmode increasing value of y moves the cursur toward bottom  
    # the direction changes from snakes point of view. Going down and turn right means going to left of screen
    def _move(self, action):
        # [straight, right, left]
        # No changes in case of [1, 0, 0]
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        if action[1]:
            self.direction = clockwise[(clockwise.index(self.direction) + 1) % 4]
        elif action[2]:
            self.direction = clockwise[(clockwise.index(self.direction) - 1) % 4]
        
        if self.direction == Direction.LEFT:
            self.head = Point(self.head.x - BOX_SIZE, self.head.y)
        elif self.direction == Direction.RIGHT:
            self.head = Point(self.head.x + BOX_SIZE, self.head.y)
        elif self.direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - BOX_SIZE)
        elif self.direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y  + BOX_SIZE)

# if __name__ == '__main__':
#     game = SnakeGameAI()

#     while True:
#         game_over, score = game.play_step()

#         if game_over == True:
#             break

#     print('Final Score', score)    
#     pygame.quit()