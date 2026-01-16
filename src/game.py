import random
import copy
from typing import List, Tuple, Optional


class Game1024:
    def __init__(self, level=1, difficulty=1.0):
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.level = level
        self.difficulty = difficulty
        self.moves = 0
        self.merges = 0
        self.max_tile = 0
        self.target_score = 1024
        self.game_over = False
        self.won = False
        self.start_time = None
        self.end_time = None
        self.reset()

    def reset(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.moves = 0
        self.merges = 0
        self.max_tile = 0
        self.game_over = False
        self.won = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self) -> bool:
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False

        value = 2 if random.random() < 0.9 else 4
        row, col = random.choice(empty_cells)
        self.grid[row][col] = value
        return True

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        empty_cells = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def move(self, direction: str) -> bool:
        if self.game_over or self.won:
            return False

        if direction not in ['up', 'down', 'left', 'right']:
            return False

        original_grid = copy.deepcopy(self.grid)
        moved = False

        if direction == 'left':
            moved = self._move_left()
        elif direction == 'right':
            moved = self._move_right()
        elif direction == 'up':
            moved = self._move_up()
        elif direction == 'down':
            moved = self._move_down()

        if moved:
            self.moves += 1
            self.add_random_tile()
            self._update_max_tile()
            self._check_game_state()

        return moved

    def _move_left(self) -> bool:
        moved = False
        for i in range(self.grid_size):
            row = self.grid[i][:]
            new_row, row_score, row_merges = self._merge_row(row)
            self.score += row_score
            self.merges += row_merges

            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row
        return moved

    def _move_right(self) -> bool:
        moved = False
        for i in range(self.grid_size):
            row = self.grid[i][::-1]
            new_row, row_score, row_merges = self._merge_row(row)
            self.score += row_score
            self.merges += row_merges

            new_row = new_row[::-1]
            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row
        return moved

    def _move_up(self) -> bool:
        moved = False
        for j in range(self.grid_size):
            col = [self.grid[i][j] for i in range(self.grid_size)]
            new_col, col_score, col_merges = self._merge_row(col)
            self.score += col_score
            self.merges += col_merges

            for i in range(self.grid_size):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]
        return moved

    def _move_down(self) -> bool:
        moved = False
        for j in range(self.grid_size):
            col = [self.grid[i][j] for i in range(self.grid_size)][::-1]
            new_col, col_score, col_merges = self._merge_row(col)
            self.score += col_score
            self.merges += col_merges

            new_col = new_col[::-1]
            for i in range(self.grid_size):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]
        return moved

    def _merge_row(self, row: List[int]) -> Tuple[List[int], int, int]:
        non_zero = [x for x in row if x != 0]
        new_row = [0] * self.grid_size
        score_gained = 0
        merge_count = 0

        i = 0
        pos = 0
        while i < len(non_zero):
            if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                new_row[pos] = merged_value
                score_gained += merged_value
                merge_count += 1
                i += 2
            else:
                new_row[pos] = non_zero[i]
                i += 1
            pos += 1

        return new_row, score_gained, merge_count

    def _update_max_tile(self):
        for row in self.grid:
            for cell in row:
                if cell > self.max_tile:
                    self.max_tile = cell

    def _check_game_state(self):
        if self.max_tile >= self.target_score:
            self.won = True
            self.end_time = self._get_time()
        elif self.is_game_over():
            self.game_over = True
            self.end_time = self._get_time()

    def is_game_over(self) -> bool:
        if self.get_empty_cells():
            return False

        for i in range(self.grid_size):
            for j in range(self.grid_size - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False

        return True

    def get_grid(self) -> List[List[int]]:
        return copy.deepcopy(self.grid)

    def get_score(self) -> int:
        return self.score

    def get_stats(self) -> dict:
        return {
            'score': self.score,
            'moves': self.moves,
            'merges': self.merges,
            'max_tile': self.max_tile,
            'level': self.level,
            'difficulty': self.difficulty,
            'game_over': self.game_over,
            'won': self.won
        }

    def _get_time(self) -> float:
        import time
        return time.time()
