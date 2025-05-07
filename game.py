import numpy as np
from constants import ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH, EMPTY, PLAYER_PIECE, AI_PIECE


class Connect4Game:
    def __init__(self):
        self.board = self.create_board()
        self.game_over = False
        self.winner = None
        self.turn = 0

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT):
            if self.board[r][col] == 0:
                return r
        return -1

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if (self.board[r][c] == piece and self.board[r][c + 1] == piece and
                        self.board[r][c + 2] == piece and self.board[r][c + 3] == piece):
                    return True

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == piece and self.board[r + 1][c] == piece and
                        self.board[r + 2][c] == piece and self.board[r + 3][c] == piece):
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and
                        self.board[r + 2][c + 2] == piece and self.board[r + 3][c + 3] == piece):
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and
                        self.board[r - 2][c + 2] == piece and self.board[r - 3][c + 3] == piece):
                    return True

        return False

    def check_potential_win(self, piece):
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                temp_board = self.board.copy()
                temp_board[row][col] = piece

                temp_game = Connect4Game()
                temp_game.board = temp_board

                if temp_game.winning_move(piece):
                    return col
        return -1

    def is_draw(self):
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                return False
        return True

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def reset(self):
        self.board = self.create_board()
        self.game_over = False
        self.winner = None
        self.turn = 0

    def get_board_state(self):
        return self.board.flatten()

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

        piece_count = np.count_nonzero(window == piece)
        opp_count = np.count_nonzero(window == opp_piece)
        empty_count = np.count_nonzero(window == 0)

        if piece_count == 4:
            score += 100
        elif piece_count == 3 and empty_count == 1:
            score += 5
        elif piece_count == 2 and empty_count == 2:
            score += 2

        if opp_count == 3 and empty_count == 1:
            score -= 15
        elif opp_count == 2 and empty_count == 2:
            score -= 3

        return score

    def evaluate_position(self, piece):
        score = 0

        center_array = [int(i) for i in list(self.board[:, COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(ROW_COUNT - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                window = [self.board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                window = [self.board[r - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score