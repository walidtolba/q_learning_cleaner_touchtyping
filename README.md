# Playing Touch Typing with Reinforcement Learning

A Touch Typing game controlled by an AI agent. 

## Introduction

The game is developed using pygame. The goal for the player is to type as much as words as possible before it The cleaner clean all the dirts. The player can add more dirts by completing sentances .The agent is able to score over 50 after 500 episodes of training (which takes less than 15 seconds).

The agent is trained using the Q-learning algorithm. The agent receives a reward of +50 when the a dirt is eaten, and a penalty of -30 when hits a wall. To discourage any redundant step, the agent receives a penalty of -1 for each step it has taken.

A navie state space would use the exact positions of the cleaner and dirts. In an n^2 board, each square has three possible conditions: empty, occupied by the dirt, occupied by the cleaner. In this approach, the number of possible states is (n^2)^3, which makes training difficult. The state space used in this algorithm only considers 

1. whether the cleaner is going to hit an object (dirt or a wall) if it goes straight, left and right, and 
2.  whether the dirt is in front of/behind the cleaner and to the left/right of the cleaner. 

The size of the state space is, therefore, reduced to 3^3 x 2^2. However, since the agent can only read one step ahead, it does have a tendency to trap itself into a location where it doesn't have sufficient space to get itself out.

## Installation

```bash
$ git clone https://github.com/walidtolba/q_learning_cleaner_touchtyping
```

## Run

To run the game, type the following command in the terminal:

```bash
$ python play.py --display  --num_episodes=500
```

Argument description:

--display: (Optional) display the game view or not    
--retrain: (Optional) retrain the agent from scratch or continue training the policy stored in ``q.pickle``    
--num_episodes: (Optional) number of episodes to run in this training session (default=500)

Turning off the game display will speed up the training. The action-value function after 500 episodes of training is stored in ``q.pickle``. The file will automatically be loaded when the script is run, and the training will continue. If you want to re-train the agent, simply add the ``--retrain`` argument.

## This project

This project is a Daiai's TP for Master 1 students filter SDAI at NTIC (Constantine 2).