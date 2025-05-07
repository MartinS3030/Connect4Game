import pygame
from constants import (ROW_COUNT, COLUMN_COUNT, SQUARESIZE, RADIUS, SIZE, WIDTH, HEIGHT,
                      BLUE, BLACK, RED, YELLOW, WHITE, GREEN, PLAYER_PIECE, AI_PIECE)


class Connect4UI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Connect 4 - Neural Network AI")
        self.font = pygame.font.SysFont("monospace", 30)
        self.small_font = pygame.font.SysFont("monospace", 20)
        self.draw_board()
        pygame.display.update()

    def draw_board(self, game=None):
        self.screen.fill(WHITE)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE,
                                 (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        if game:
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):
                    if game.board[r][c] == PLAYER_PIECE:
                        pygame.draw.circle(self.screen, RED, (
                            int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                           RADIUS)
                    elif game.board[r][c] == AI_PIECE:
                        pygame.draw.circle(self.screen, YELLOW, (
                            int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                           RADIUS)

        pygame.display.update()

    def draw_piece(self, row, col, piece):
        color = RED if piece == PLAYER_PIECE else YELLOW
        pygame.draw.circle(self.screen, color,
                           (int(col * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(row * SQUARESIZE + SQUARESIZE / 2)),
                           RADIUS)
        pygame.display.update()

    def draw_player_turn_indicator(self, pos, piece):
        self.screen.fill(WHITE, (0, 0, WIDTH, SQUARESIZE))
        color = RED if piece == PLAYER_PIECE else YELLOW
        pygame.draw.circle(self.screen, color, (pos, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    def show_game_over_message(self, game):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        result_box = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 4)
        pygame.draw.rect(self.screen, BLUE, result_box, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, result_box, 4, border_radius=15)

        if game.winner == PLAYER_PIECE:
            label = self.font.render("YOU WIN!", 1, WHITE)
        elif game.winner == AI_PIECE:
            label = self.font.render("AI Wins!", 1, WHITE)
        else:
            label = self.font.render("It's a Draw!", 1, WHITE)

        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 3 + 20))

        play_again_label = self.small_font.render("Play Again? (Y/N)", 1, WHITE)
        self.screen.blit(play_again_label, (WIDTH // 2 - play_again_label.get_width() // 2, HEIGHT // 3 + 80))

        pygame.display.update()

    def show_training_progress(self, episode, total_episodes):
        self.screen.fill(WHITE)
        text = f"Training AI: {episode}/{total_episodes}"
        label = self.font.render(text, 1, BLUE)
        self.screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))

        bar_width = WIDTH * 0.8
        bar_height = 30
        progress = episode / total_episodes
        pygame.draw.rect(self.screen, BLACK, (WIDTH // 2 - bar_width // 2, HEIGHT // 2 + 20, bar_width, bar_height), 2)
        pygame.draw.rect(self.screen, GREEN,
                         (WIDTH // 2 - bar_width // 2, HEIGHT // 2 + 20, bar_width * progress, bar_height))

        pygame.display.update()