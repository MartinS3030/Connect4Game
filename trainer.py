import pygame
import numpy as np
from game import Connect4Game
from neural_network import NeuralNetwork
from ui import Connect4UI
from constants import PLAYER_PIECE, AI_PIECE


def self_play_training(episodes=1000, batch_size=64):
    game = Connect4Game()
    agent = NeuralNetwork()
    ui = Connect4UI()

    for episode in range(episodes):
        game.reset()
        state = game.get_board_state()
        done = False
        turn = 0

        if episode % 10 == 0 or episode == episodes - 1:
            ui.show_training_progress(episode, episodes)
            pygame.event.pump()

        while not done:
            valid_locations = game.get_valid_locations()
            if not valid_locations:
                done = True
                game.game_over = True
                continue

            if turn == 0:
                piece = PLAYER_PIECE
                action = agent.act(state, valid_locations, game)
            else:
                piece = AI_PIECE
                inverted_state = state.copy()
                inverted_state = np.where(inverted_state == PLAYER_PIECE, 3,
                                          inverted_state)
                inverted_state = np.where(inverted_state == AI_PIECE, PLAYER_PIECE, inverted_state)
                inverted_state = np.where(inverted_state == 3, AI_PIECE, inverted_state)
                action = agent.act(inverted_state, valid_locations, game)

            row = game.get_next_open_row(action)
            game.drop_piece(row, action, piece)

            reward = 0
            if game.winning_move(piece):
                if turn == 0:
                    reward = 1
                else:
                    reward = -1
                done = True
                game.game_over = True
                game.winner = piece
            elif game.is_draw():
                reward = 0.1
                done = True
                game.game_over = True
            else:
                if turn == 0:
                    position_reward = game.evaluate_position(PLAYER_PIECE) / 100
                    reward = position_reward
                else:
                    position_reward = -game.evaluate_position(AI_PIECE) / 100
                    reward = position_reward

            next_state = game.get_board_state()

            if turn == 0:
                agent.remember(state, action, reward, next_state, done)
            else:
                inverted_next_state = next_state.copy()
                inverted_next_state = np.where(inverted_next_state == PLAYER_PIECE, 3, inverted_next_state)
                inverted_next_state = np.where(inverted_next_state == AI_PIECE, PLAYER_PIECE, inverted_next_state)
                inverted_next_state = np.where(inverted_next_state == 3, AI_PIECE, inverted_next_state)

                agent.remember(inverted_state, action, -reward, inverted_next_state, done)

            state = next_state

            turn = 1 - turn

        agent.replay(min(batch_size, len(agent.memory)))

        if episode % 10 == 0 and agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

    agent.save_model()
    print("Training complete!")
    return agent