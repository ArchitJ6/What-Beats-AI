from collections import deque
import time

class GameSession:
    def __init__(self):
        self.history = deque()
        self.score = 0
        self.last_active_time = time.time()
        self.timeout_duration = 300  # 5 minutes

    def add_guess(self, guess: str):
        if guess in self.history:
            return False
        if len(self.history) == 0:
            self.history.append('rock')
        self.history.append(guess)
        self.score += 1
        self.last_active_time = time.time()
        return True

    def get_history(self):
        self.last_active_time = time.time()
        return list(self.history)

    def reset(self):
        self.last_active_time = time.time()
        self.history.clear()
        self.score = 0

    def is_expired(self):
        return (time.time() - self.last_active_time) > self.timeout_duration