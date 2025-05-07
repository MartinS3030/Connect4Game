import os
import random
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError

from constants import ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE, MODEL_FILE


class NeuralNetwork:
    def __init__(self):
        self.learning_rate = 0.001
        self.model = self.create_model()
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model_file = MODEL_FILE

        if os.path.exists(self.model_file):
            try:
                self.model = load_model(self.model_file)
                print("Loaded model from file")
            except Exception as e:
                print(f"Could not load model: {e}")
                print("Using new model")

    def create_model(self):
        model = Sequential()
        model.add(Dense(256, input_dim=ROW_COUNT * COLUMN_COUNT, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(COLUMN_COUNT, activation='linear'))
        model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, valid_locations, game=None):
        if game:
            block_col = game.check_potential_win(PLAYER_PIECE)
            if block_col >= 0 and block_col in valid_locations:
                return block_col

            win_col = game.check_potential_win(AI_PIECE)
            if win_col >= 0 and win_col in valid_locations:
                return win_col

        if np.random.rand() <= self.epsilon:
            return random.choice(valid_locations)

        state_input = np.reshape(state, [1, ROW_COUNT * COLUMN_COUNT])
        act_values = self.model.predict(state_input, verbose=0)[0]

        valid_act_values = [(col, act_values[col]) for col in valid_locations]
        return max(valid_act_values, key=lambda x: x[1])[0]

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            state = np.reshape(state, [1, ROW_COUNT * COLUMN_COUNT])
            next_state = np.reshape(next_state, [1, ROW_COUNT * COLUMN_COUNT])

            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state, verbose=0)[0]))

            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self):
        self.model.save(self.model_file)
        print(f"Model saved to {self.model_file}")

    def load_model(self):
        if os.path.exists(self.model_file):
            try:
                self.model = load_model(self.model_file)
                print("Loaded model from file")
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False