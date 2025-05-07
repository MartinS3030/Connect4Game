import pygame
import sys
import time
from game import Connect4Game
from neural_network import NeuralNetwork
from ui import Connect4UI
from trainer import self_play_training
from constants import COLUMN_COUNT, SQUARESIZE, PLAYER_PIECE, AI_PIECE


def play_against_ai():
    game = Connect4Game()
    agent = NeuralNetwork()
    ui = Connect4UI()

    if not agent.load_model():
        print("No trained model found. Training a new one...")
        agent = self_play_training(episodes=1000)

    agent.epsilon = 0.05

    ui.draw_board(game)
    pygame.display.update()

    playing = True

    while playing:
        game.reset()
        ui.draw_board(game)

        while not game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION and game.turn == 0:
                    pygame.draw.rect(ui.screen, (0, 0, 0), (0, 0, COLUMN_COUNT * SQUARESIZE, SQUARESIZE))
                    posx = event.pos[0]
                    ui.draw_player_turn_indicator(posx, PLAYER_PIECE)

                elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == 0:
                    pygame.draw.rect(ui.screen, (0, 0, 0), (0, 0, COLUMN_COUNT * SQUARESIZE, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if 0 <= col < COLUMN_COUNT and game.is_valid_location(col):
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, PLAYER_PIECE)
                        ui.draw_board(game)

                        if game.winning_move(PLAYER_PIECE):
                            game.game_over = True
                            game.winner = PLAYER_PIECE
                            ui.show_game_over_message(game)
                        elif game.is_draw():
                            game.game_over = True
                            game.winner = None
                            ui.show_game_over_message(game)
                        else:
                            game.turn = 1

            if not game.game_over and game.turn == 1:
                valid_locations = game.get_valid_locations()
                if not valid_locations:
                    game.game_over = True
                    game.winner = None
                    ui.show_game_over_message(game)
                    continue

                state = game.get_board_state()
                col = agent.act(state, valid_locations, game)
                time.sleep(0.5)

                if game.is_valid_location(col):
                    row = game.get_next_open_row(col)
                    game.drop_piece(row, col, AI_PIECE)
                    ui.draw_board(game)

                    if game.winning_move(AI_PIECE):
                        game.game_over = True
                        game.winner = AI_PIECE
                        ui.show_game_over_message(game)
                    elif game.is_draw():
                        game.game_over = True
                        game.winner = None
                        ui.show_game_over_message(game)
                    else:
                        game.turn = 0

            pygame.time.wait(50)

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        waiting_for_input = False
                    elif event.key == pygame.K_n:
                        waiting_for_input = False
                        playing = False
            pygame.time.wait(100)

    pygame.quit()
    print("Thanks for playing!")