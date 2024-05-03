import argparse
import pickle
import sys
import pygame
from tqdm import tqdm
from simulation import SimulationEnv
from q_learning import QlearningAgent

def load_policy(agent):
    params = pickle.load(open("q.pickle", "rb"))
    agent.q = params["q"]
    agent.epsilon = params["epsilon"]
    
def save_policy(agent):
    outfile = open("q.pickle", "wb")
    params = {
        "q": agent.q,
        "epsilon": agent.epsilon
    }
    pickle.dump(params, outfile)

def run(display, retrain, num_episodes):
    pygame.init()
    env = SimulationEnv()
    agent = QlearningAgent(env)
    if not retrain:
        try:
            load_policy(agent)
        except:
            pass

    for _ in tqdm(range(num_episodes)):
        state = env.reset()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_policy(agent)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_a <= event.key <= pygame.K_z or event.key == pygame.K_SPACE:
                        if env.color_index >= len(env.text):
                            if event.key == pygame.K_SPACE:
                                env.complete_text()
  
                        else:
                            pressed_key = pygame.key.name(event.key)
                            pressed_key = ' ' if pressed_key == 'space' else pressed_key
                            mods = pygame.key.get_mods()
                            if mods & pygame.KMOD_SHIFT:
                                pressed_key = pressed_key.upper()
                            env.mask[env.color_index] = 1 if pressed_key == env.text[env.color_index] else -1
                            env.color_index += 1
                    elif event.key == pygame.K_BACKSPACE:
                            if env.color_index > 0:
                                env.color_index -= 1
                                env.mask[env.color_index] = 0
                    elif event.key == pygame.K_TAB:
                            env.reset_color_index()
                    elif event.key == pygame.K_TAB:
                            env.reset_color_index()
                    elif event.key == pygame.K_INSERT:
                            env._generate_dirt(1)

    
                        
            if display:
                env.render()
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.update_q_value(state, reward, action, next_state, done)
            state = next_state
        agent.epsilon = max(agent.epsilon * agent.epsilon_decay_rate, agent.min_epsilon)
    save_policy(agent)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--display", action='store_true', help="display the game view or not")
    parser.add_argument("--retrain", action='store_true', help="retrain the agent from scratch or not")
    parser.add_argument("--num_episodes", type=int, default=500, help="number of episodes to run in this training session")
    args = parser.parse_args()
    run(args.display, args.retrain, args.num_episodes)
