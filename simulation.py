import random
from collections import deque
import numpy as np
import pygame
import math

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

# find the new moving direction given the original direction and the chosen action 
# 3 possible actions - 0: go straight, 1: go left, 2: go right
action_to_direction = {
    "UP":    {0: "UP",    1: "LEFT",  2: "RIGHT"},
    "DOWN":  {0: "DOWN",  1: "RIGHT", 2: "LEFT"},
    "LEFT":  {0: "LEFT",  1: "DOWN",  2: "UP"},
    "RIGHT": {0: "RIGHT", 1: "UP",    2: "DOWN"}
}

class SimulationEnv():
    texts = [
    "The dog barked to protect its home",
    "Children played happily in the park",
    "The old tree swayed whispering low",
    "Moonlight bathed the city in glow",
    "A gentle breeze rustled the leaves",
    "The river flowed reflecting light",
    "Footsteps echoed softly at night",
    "The fire warmed weary travelers",
    "Birds chirped in the morning sun",
    "The wind whispered through the tree",
    "Stars twinkled in the midnight sky",
    "The waves crashed rhythmically",
    "A lone wolf howled in the moonlit",
    "Clouds drifted across the blue sky"
]

    def __init__(self):
        pygame.display.set_caption("NiggaHigga")
        self.window_width = 440
        self.window_height = 440
        self.screen = None
        self.square_size = 20
        self.margin = 20
        self.speed = 8
        self.cleaner = tuple()
        self.dirts = set()
        self.action_space = list(range(3))
        self.state_size = 5
        self.color_index = 0 ####
        self.reset()
        self.reset_text()
        self.game_end == False

    def step(self, action):
        """ Take an action as an input, return the resulting game state, reward receivedand whether the game is over """
        self.direction = action_to_direction[self.direction][action]
        new_coord = self._get_new_coord(self.cleaner, self.direction)
        self.cleaner = new_coord

        result = self._is_collided(self.cleaner)
        done = False

        if result == 1:
            # increment score and generate new dirt if dirt is eaten
            self.score += 1
            self.dirts.remove(self.cleaner)
        elif result == 2:
            # game over if cleaner eats itself or hits a wall
            done = True

        state = self._get_game_state()
        reward = self._get_reward(result)
        return state, reward, done

    def reset(self):
        """ Reset the game environment, use to start a new game """
        self.score = 0
        self.cleaner = (self.window_width // 2, self.window_height // 2) # starts at the center of the screen
        self.direction = "UP"
        self.dirts = set()
        self._generate_dirt(10)
        return self._get_game_state()

    def render(self):
        """ Display the graphics (background, cleaner, dirt and score) """
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.window_width, self.window_height + 10))
        clock = pygame.time.Clock()

        # draw the black background
        self.screen.fill(BLACK)

        # draw four borders
        top_left = (self.square_size, self.square_size)
        top_right = (self.window_width - self.square_size, self.square_size)
        bottom_left = (self.square_size, self.window_height - self.square_size)
        bottom_right = (self.window_width - self.square_size, self.window_height - self.square_size)
        pygame.draw.line(self.screen, WHITE, top_left, top_right) # top horizontal line
        pygame.draw.line(self.screen, WHITE, top_left, bottom_left) # left vertical line
        pygame.draw.line(self.screen, WHITE, bottom_left, bottom_right) # bottom horizontal
        pygame.draw.line(self.screen, WHITE, top_right, bottom_right) # right vertical

        # display score
        font = pygame.font.SysFont("Courier New", 18)
        score_text = font.render("SCORE: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, [self.window_width // 2 - 40, 0])
        score_text = font.render("TEXT: ", True, WHITE)
        self.screen.blit(score_text, [20, self.window_height - 15])
        for i, letter in enumerate(self.text):
            score_text = font.render(letter, True, GREEN if self.mask[i] == 1 else RED if self.mask[i] == -1 else WHITE)
            self.screen.blit(score_text, [80 + i * 10, self.window_height - 15])

        # draw cleaner
        pygame.draw.rect(self.screen, GREEN, (self.cleaner[0], self.cleaner[1], self.square_size, self.square_size), 2)
            
        # draw dirt
        for dirt in self.dirts:
            pygame.draw.rect(self.screen, RED, (dirt[0], dirt[1], self.square_size, self.square_size))
            
        clock.tick(self.speed)
        pygame.display.update()

    def _generate_dirt(self, number_of_dirts):
        """ Generate coordinates for the dirt"""
        for _ in range(number_of_dirts):
            in_cleaner_body = True
            while in_cleaner_body: 
                rand_x = random.randint(self.margin, self.window_width - self.square_size - self.margin) // self.square_size * self.square_size
                rand_y = random.randint(self.margin, self.window_height - self.square_size - self.margin) // self.square_size * self.square_size
                in_cleaner_body = self.cleaner == (rand_x, rand_y) or (rand_x, rand_y) in self.dirts # check if the generated position is in the cleaner body
            self.dirts.add((rand_x, rand_y))

    def _is_collided(self, coord):
        """ 
        Check if any object is located in a given set of coordinates
        Returns 0 if nothing
                1 if it is occupied by the dirt
                2 if it is occupied by the cleaner body (excluding the head)
        """
        x, y = coord
        if (x, y) in self.dirts: 
            return 1 # collide with dirt
        if  x < self.margin or x > self.window_width - self.square_size - self.margin or \
            y < self.margin or y > self.window_height - self.square_size - self.margin:
            return 2 # collide with the  wall
        return 0 # nothing

    def _get_reward(self, result):
        """ Return the reward for a given result  """
        rewards = {
            0:  -1, # nothing happens
            1:  50, # dirt is eaten
            2: -30, # eat itself or hit a wall
        }
        return rewards[result]

    def _get_new_coord(self, coord, direction):
        """ Return the coordinates of the cleaner head had the cleaner moved in the given direction """
        x, y = coord
        if direction == "UP":
            return (x, y - self.square_size)
        elif direction == "DOWN":
            return (x, y + self.square_size)
        elif direction == "LEFT":
            return (x - self.square_size, y)
        elif direction == "RIGHT":
            return (x + self.square_size, y)

    def _transform_coord(self, coord, direction):
        """ Transform coordinates relative to cleaner head based on moving direction """
        # if cleaner is moving up, no transformation is needed
        x, y = coord
        if direction == "LEFT": 
            return (-y, x)
        elif direction == "RIGHT": 
            return (y, -x)
        elif direction == "DOWN": 
            return (-x, -y)
        return (x, y)

    def _get_quadrant(self, coord):
        """ 
        Compute where (x, y) is, relative to the origin 
        Returns a tuple where
        qx: 1 if (x, y) is on the left of the origin, 2 if right, 0 otherwise
        qy: 1 if (x, y) is above the origin, 2 if below, 0 otherwise
        """
        def sign(n):
            if n < 0:
                return 1
            if n > 0:
                return 2
            return 0
        x, y = coord
        qx, qy = sign(x), sign(y)
        return (qx, qy)
    
    def get_closest_dirt(self, coord):
        closest_dirt = None
        closest_distance = None

        for dirt in self.dirts:
            distance = math.sqrt((coord[0] - dirt[0])**2 + (coord[1] - dirt[1])**2)
            if closest_distance is None or distance < closest_distance:
                closest_distance = distance
                closest_dirt = dirt

        return closest_dirt

    def _get_game_state(self):
        """list
        Return a 5-dimensional tuple that represents the state space
        1. the kind of object the cleaner will encounter if it goes straight
        2. the kind of object the cleaner will encounter if it goes left
        3. the kind of object the cleaner will encounter if it goes right
        4. the x-position of dirt relative to cleaner head
        5. the y-position of dirt relative to cleaner head
        """
        state = []

        # check if there is any object adjacent to cleaner head in straight, 
        # left and right directions (relative to the moving direction)
        for new_direction in action_to_direction[self.direction].values():
            new_x, new_y = self._get_new_coord(self.cleaner, new_direction)
            state.append(self._is_collided((new_x, new_y)))

        

        # compute which quadrant the dirt is in, relative to the cleaner head and moving direction
        dirt = self.get_closest_dirt(self.cleaner)
        trans_coord = self._transform_coord((dirt[0] - self.cleaner[0], dirt[1] - self.cleaner[1]), self.direction)
        qx, qy = self._get_quadrant(trans_coord)
        state.append(qx)
        state.append(qy)
        return tuple(state) # have to use convert to tuple as list is not hashable
    
    def complete_text(self):
        dirts_number = max(0, 10 - sum(1 for x in self.mask if x == -1))
        self.reset_text()
        self._generate_dirt(dirts_number)

    def reset_text(self):
        self.color_index = 0
        self.text = self.text = random.choice(self.texts)
        self.mask = [0] * len(self.text)
    
    def reset_color_index(self):
        self.color_index = 0
        self.mask = [0] * len(self.text)




