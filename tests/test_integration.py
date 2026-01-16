import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game1024


class TestGameIntegration:
    def test_full_game_flow(self):
        game = Game1024()

        initial_score = game.score
        initial_moves = game.moves

        game.move('left')
        game.move('right')
        game.move('up')
        game.move('down')

        assert game.moves == initial_moves + 4
        assert game.score >= initial_score

    def test_multiple_merges(self):
        game = Game1024()
        game.grid = [
            [2, 2, 2, 2],
            [4, 4, 4, 4],
            [8, 8, 8, 8],
            [0, 0, 0, 0]
        ]

        game.move('left')

        assert game.grid[0][0] == 4
        assert game.grid[0][1] == 4
        assert game.grid[1][0] == 8
        assert game.grid[1][1] == 8
        assert game.grid[2][0] == 16
        assert game.grid[2][1] == 16

    def test_cascade_merges(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        assert game.grid[0][0] == 4
        assert game.grid[0][1] == 8
        assert game.grid[1][0] == 16
        assert game.grid[1][1] == 32

    def test_no_move_possible(self):
        game = Game1024()
        game.grid = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]

        result = game.move('left')

        assert result is False

    def test_score_accumulation(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        initial_score = game.score
        game.move('left')

        assert game.score > initial_score

    def test_max_tile_tracking(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        assert game.max_tile >= 32

    def test_game_state_tracking(self):
        game = Game1024()
        game.target_score = 64

        game.grid[0][0] = 64
        game._update_max_tile()
        game._check_game_state()

        assert game.won is True

    def test_grid_immutability(self):
        game = Game1024()
        original_grid = game.get_grid()

        original_grid[0][0] = 999

        assert game.grid[0][0] != 999

    def test_stats_comprehensive(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        stats = game.get_stats()

        assert 'score' in stats
        assert 'moves' in stats
        assert 'merges' in stats
        assert 'max_tile' in stats
        assert 'level' in stats
        assert 'difficulty' in stats
        assert 'game_over' in stats
        assert 'won' in stats

    def test_empty_board_fill(self):
        game = Game1024()
        game.grid = [[0] * 4 for _ in range(4)]

        for _ in range(10):
            game.add_random_tile()

        non_zero_count = sum(1 for row in game.grid for cell in row if cell != 0)

        assert non_zero_count == 10

    def test_corner_strategy(self):
        game = Game1024()
        game.grid = [
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [16, 0, 0, 0]
        ]

        game.move('left')

        assert game.grid[0][0] == 2
        assert game.grid[1][0] == 4
        assert game.grid[2][0] == 8
        assert game.grid[3][0] == 16

    def test_full_board_no_space(self):
        game = Game1024()
        game.grid = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]

        result = game.add_random_tile()

        assert result is False

    def test_merge_priority(self):
        game = Game1024()
        game.grid = [
            [2, 2, 2, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        assert game.grid[0][0] == 4
        assert game.grid[0][1] == 2

    def test_score_calculation(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        expected_score = 4 + 8 + 16 + 32
        assert game.score == expected_score

    def test_merges_count(self):
        game = Game1024()
        game.grid = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')

        assert game.merges == 4

    def test_random_tile_distribution(self):
        game = Game1024()
        game.grid = [[0] * 4 for _ in range(4)]

        twos = 0
        fours = 0

        for _ in range(100):
            game.grid = [[0] * 4 for _ in range(4)]
            game.add_random_tile()

            for row in game.grid:
                for cell in row:
                    if cell == 2:
                        twos += 1
                    elif cell == 4:
                        fours += 1

        total = twos + fours
        two_ratio = twos / total if total > 0 else 0

        assert 0.8 <= two_ratio <= 0.95

    def test_difficulty_impact(self):
        game_easy = Game1024(level=1, difficulty=0.5)
        game_hard = Game1024(level=10, difficulty=1.5)

        assert game_easy.difficulty == 0.5
        assert game_hard.difficulty == 1.5
        assert game_easy.level == 1
        assert game_hard.level == 10

    def test_reset_clears_state(self):
        game = Game1024()
        game.score = 1000
        game.moves = 50
        game.merges = 25
        game.max_tile = 512
        game.game_over = True

        game.reset()

        assert game.score == 0
        assert game.moves == 0
        assert game.merges == 0
        assert game.max_tile == 0
        assert not game.game_over

    def test_multiple_directions_same_result(self):
        game = Game1024()
        game.grid = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')
        grid_left = [row[:] for row in game.grid]

        game.reset()
        game.grid = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        game.move('right')
        grid_right = [row[:] for row in game.grid]

        assert grid_left[0][0] == grid_right[0][3]
