"""
1024 Game - Game Logic Tests
Comprehensive tests for the core game mechanics
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game_logic import Game


class TestGameLogic(unittest.TestCase):
    """Test cases for the Game class"""

    def test_initialization(self):
        """Test game initialization"""
        game = Game(level=1)
        self.assertEqual(game.level, 1)
        self.assertEqual(game.score, 0)
        self.assertEqual(game.moves, 0)
        self.assertEqual(len(game.grid), 4)
        self.assertEqual(len(game.grid[0]), 4)

    def test_level_difficulty_calculation(self):
        """Test difficulty calculation for different levels"""
        game = Game(level=1)
        self.assertEqual(game.difficulty['spawn_prob_4'], 0.1)
        self.assertEqual(game.difficulty['max_tiles'], 12)
        self.assertEqual(game.difficulty['time_limit'], 600)

        game = Game(level=5)
        self.assertEqual(game.difficulty['spawn_prob_4'], 0.1)

        game = Game(level=6)
        self.assertEqual(game.difficulty['spawn_prob_4'], 0.15)
        self.assertEqual(game.difficulty['max_tiles'], 14)
        self.assertEqual(game.difficulty['time_limit'], 540)

        game = Game(level=20)
        self.assertEqual(game.difficulty['spawn_prob_4'], 0.25)
        self.assertEqual(game.difficulty['max_tiles'], 20)
        self.assertEqual(game.difficulty['time_limit'], 360)

    def test_level_target_calculation(self):
        """Test level target calculation"""
        game = Game(level=1)
        self.assertEqual(game.level_target, 1024)

        game = Game(level=5)
        self.assertEqual(game.level_target, 1024)

        game = Game(level=6)
        self.assertEqual(game.level_target, 2048)

        game = Game(level=10)
        self.assertEqual(game.level_target, 2048)

        game = Game(level=11)
        self.assertEqual(game.level_target, 4096)

        game = Game(level=20)
        self.assertEqual(game.level_target, 4096)

    def test_add_random_tile(self):
        """Test adding random tiles"""
        game = Game(level=1)
        game.grid = [[0] * 4 for _ in range(4)]

        result = game.add_random_tile()
        self.assertTrue(result)
        non_zero = sum(1 for row in game.grid for cell in row if cell != 0)
        self.assertEqual(non_zero, 1)

    def test_add_random_tile_full_grid(self):
        """Test adding tile when grid is full"""
        game = Game(level=1)
        game.grid = [[2] * 4 for _ in range(4)]

        result = game.add_random_tile()
        self.assertFalse(result)

    def test_get_empty_cells(self):
        """Test getting empty cells"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 0, 8],
            [0, 0, 16, 0],
            [32, 0, 0, 64],
            [0, 128, 0, 256]
        ]

        empty = game.get_empty_cells()
        self.assertEqual(len(empty), 7)
        self.assertIn((0, 2), empty)
        self.assertIn((1, 0), empty)

    def test_move_left_basic(self):
        """Test basic left move"""
        game = Game(level=1)
        game.grid = [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 8, 0],
            [0, 0, 0, 16]
        ]

        moved = game.move('left')
        self.assertTrue(moved)
        self.assertEqual(game.grid[0][0], 2)
        self.assertEqual(game.grid[1][0], 4)
        self.assertEqual(game.grid[2][0], 8)
        self.assertEqual(game.grid[3][0], 16)

    def test_move_left_merge(self):
        """Test merging tiles on left move"""
        game = Game(level=1)
        game.grid = [
            [2, 2, 0, 0],
            [4, 4, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')
        self.assertEqual(game.grid[0][0], 4)
        self.assertEqual(game.grid[1][0], 8)
        self.assertEqual(game.grid[1][1], 8)

    def test_move_right_basic(self):
        """Test basic right move"""
        game = Game(level=1)
        game.grid = [
            [2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 8, 0],
            [0, 0, 0, 16]
        ]

        moved = game.move('right')
        self.assertTrue(moved)
        self.assertEqual(game.grid[0][3], 2)
        self.assertEqual(game.grid[1][3], 4)
        self.assertEqual(game.grid[2][3], 8)
        self.assertEqual(game.grid[3][3], 16)

    def test_move_up_basic(self):
        """Test basic up move"""
        game = Game(level=1)
        game.grid = [
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [16, 0, 0, 0]
        ]

        moved = game.move('up')
        self.assertTrue(moved)
        self.assertEqual(game.grid[0][0], 2)
        self.assertEqual(game.grid[0][1], 4)
        self.assertEqual(game.grid[0][2], 8)
        self.assertEqual(game.grid[0][3], 16)

    def test_move_down_basic(self):
        """Test basic down move"""
        game = Game(level=1)
        game.grid = [
            [2, 0, 0, 0],
            [4, 0, 0, 0],
            [8, 0, 0, 0],
            [16, 0, 0, 0]
        ]

        moved = game.move('down')
        self.assertTrue(moved)
        self.assertEqual(game.grid[3][0], 2)
        self.assertEqual(game.grid[3][1], 4)
        self.assertEqual(game.grid[3][2], 8)
        self.assertEqual(game.grid[3][3], 16)

    def test_move_no_change(self):
        """Test move that doesn't change anything"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        moved = game.move('left')
        self.assertFalse(moved)
        self.assertEqual(game.score, 0)

    def test_merge_row(self):
        """Test row merging logic"""
        game = Game(level=1)

        row = [2, 2, 4, 4]
        new_row, score = game._merge_row(row)
        self.assertEqual(new_row, [4, 8, 0, 0])
        self.assertEqual(score, 12)

        row = [2, 0, 2, 0]
        new_row, score = game._merge_row(row)
        self.assertEqual(new_row, [4, 0, 0, 0])
        self.assertEqual(score, 4)

        row = [2, 4, 2, 4]
        new_row, score = game._merge_row(row)
        self.assertEqual(new_row, [2, 4, 2, 4])
        self.assertEqual(score, 0)

        row = [0, 0, 0, 0]
        new_row, score = game._merge_row(row)
        self.assertEqual(new_row, [0, 0, 0, 0])
        self.assertEqual(score, 0)

    def test_is_game_over_true(self):
        """Test game over detection"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 2, 4, 8]
        ]

        self.assertTrue(game.is_game_over())

    def test_is_game_over_false_empty(self):
        """Test game over when there are empty cells"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 2, 4, 0]
        ]

        self.assertFalse(game.is_game_over())

    def test_is_game_over_false_can_merge(self):
        """Test game over when merges are possible"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 2, 4, 2]
        ]

        self.assertFalse(game.is_game_over())

    def test_is_level_complete_true(self):
        """Test level completion detection"""
        game = Game(level=1)
        game.level_target = 1024
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 2, 4, 8]
        ]

        self.assertTrue(game.is_level_complete())

    def test_is_level_complete_false(self):
        """Test level not complete"""
        game = Game(level=1)
        game.level_target = 1024
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.assertFalse(game.is_level_complete())

    def test_reset_game(self):
        """Test game reset"""
        game = Game(level=1)
        game.score = 1000
        game.moves = 50
        game.time_elapsed = 100.0

        game.reset_game()

        self.assertEqual(game.score, 0)
        self.assertEqual(game.moves, 0)
        self.assertEqual(game.time_elapsed, 0.0)
        non_zero = sum(1 for row in game.grid for cell in row if cell != 0)
        self.assertEqual(non_zero, 2)

    def test_get_stats(self):
        """Test getting game stats"""
        game = Game(level=1)
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 0],
            [0, 0, 0, 0]
        ]
        game.score = 1000
        game.moves = 50
        game.time_elapsed = 120.0

        stats = game.get_stats()
        self.assertEqual(stats['level'], 1)
        self.assertEqual(stats['score'], 1000)
        self.assertEqual(stats['moves'], 50)
        self.assertEqual(stats['time_elapsed'], 120.0)
        self.assertEqual(stats['max_tile'], 1024)
        self.assertEqual(stats['empty_cells'], 6)

    def test_get_level_progress(self):
        """Test level progress calculation"""
        game = Game(level=1)
        game.level_target = 1024
        game.grid = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        progress = game.get_level_progress()
        self.assertEqual(progress, 0.5)

        game.grid = [
            [2048, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        progress = game.get_level_progress()
        self.assertEqual(progress, 1.0)

    def test_difficulty_merge_bonus(self):
        """Test difficulty merge bonus"""
        game = Game(level=6)
        game.grid = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        game.move('left')
        self.assertEqual(game.score, 4 * 1.2)


class TestGameDifficultyScaling(unittest.TestCase):
    """Test cases for difficulty scaling"""

    def test_spawn_probability_scaling(self):
        """Test spawn probability increases with difficulty"""
        for level in range(1, 21):
            game = Game(level=level)
            tier = (level - 1) // 5
            expected = 0.1 + tier * 0.05
            self.assertEqual(game.difficulty['spawn_prob_4'], expected)

    def test_max_tiles_scaling(self):
        """Test max tiles limit increases with difficulty"""
        for level in range(1, 21):
            game = Game(level=level)
            tier = (level - 1) // 5
            expected = 12 + tier * 2
            self.assertEqual(game.difficulty['max_tiles'], expected)

    def test_time_limit_scaling(self):
        """Test time limit decreases with difficulty"""
        for level in range(1, 21):
            game = Game(level=level)
            tier = (level - 1) // 5
            expected = 600 - tier * 60
            self.assertEqual(game.difficulty['time_limit'], expected)

    def test_merge_bonus_scaling(self):
        """Test merge bonus increases with difficulty"""
        for level in range(1, 21):
            game = Game(level=level)
            tier = (level - 1) // 5
            expected = 1.0 + tier * 0.2
            self.assertEqual(game.difficulty['merge_bonus'], expected)


if __name__ == '__main__':
    unittest.main()
