import torch
import random
import numpy as np

from snake_game_ai import SnakeGameAI
from common import (Point, Direction, BOX_SIZE)
from collections import deque

MAX_MEMORY = 100_000
BATH_SIZE = 1000

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate 
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = None 
        self.trainer = None
        # TODO: model, trainer 

    def get_state(self, game):
        head = game.snake[0]
        box_right = Point(head.x + BOX_SIZE, head.y)
        box_left = Point(head.x - BOX_SIZE, head.y)
        box_up = Point(head.x, head.y - BOX_SIZE)
        box_down = Point(head.x, head.y + BOX_SIZE)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN   
        state = [
            # Danger straight
            (dir_r and game.is_collision(box_right)) or 
            (dir_l and game.is_collision(box_left)) or 
            (dir_u and game.is_collision(box_up)) or 
            (dir_d and game.is_collision(box_down)),

            # Danger right
            (dir_u and game.is_collision(box_right)) or 
            (dir_d and game.is_collision(box_left)) or 
            (dir_l and game.is_collision(box_up)) or 
            (dir_r and game.is_collision(box_down)),

            # Danger left
            (dir_d and game.is_collision(box_right)) or 
            (dir_u and game.is_collision(box_left)) or 
            (dir_r and game.is_collision(box_up)) or 
            (dir_l and game.is_collision(box_down)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATH_SIZE:
            mini_sample = random.sample(self.memory, BATH_SIZE) # list of tuples
        else :
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    # for one step
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        #get old state
        state_old = agent.get_state(game)

        #get move based on current state
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory 
            game.reset()
            agent.n_games
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save() 

            print('Game', agent.n_games, 'Score', score, 'Record', record)

            # TODO: PLOT
if __name__ == '__main__':
    train()