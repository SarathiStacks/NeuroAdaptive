import random

class DQNQuizAgent:
    def __init__(self):
        self.q_table = {}
        self.current_level = 1
        self.last_reward = 0.0

    def get_state_key(self, action: str):
        return f"{self.current_level}:{action}"

    def choose_difficulty(self):
        difficulties = ["easy", "medium", "hard"]

        if random.random() < 0.4:
            return random.choice(difficulties)

        best_diff = "medium"
        best_q = -float("inf")

        for diff in difficulties:
            q = self.q_table.get(self.get_state_key(diff), 0)
            if q > best_q:
                best_q = q
                best_diff = diff

        return best_diff

    def update(self, reward: float, action: str):
        state = self.get_state_key(action)
        old_q = self.q_table.get(state, 0.0)
        self.q_table[state] = old_q + 0.2 * (reward - old_q)
        self.last_reward = reward

        if reward > 0:
            self.current_level += 1

    def get_level(self):
        return self.current_level

    def get_reward_feedback(self):
        if self.last_reward > 0.6:
            return "Great job! The difficulty matched you well. Keep going 🚀"
        elif self.last_reward > 0.3:
            return "You're doing well! Stay focused and push a bit more 💪"
        else:
            return "It's okay to struggle sometimes. Take a breath and try again 💛"
