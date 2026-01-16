import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game1024
from src.level_manager import LevelManager
from src.config import Config
from src.data_manager import DataManager


class TestGame1024:
    def test_initialization(self):
        game = Game1024()
        assert game.grid_size == 4
        assert game.score == 0
        assert game.level == 1
        assert game.difficulty == 1.0
        assert not game.game_over
        assert not game.won

    def test_reset(self):
        game = Game1024()
        game.score = 100
        game.moves = 10
        game.game_over = True

        game.reset()

        assert game.score == 0
        assert game.moves == 0
        assert not game.game_over

    def test_add_random_tile(self):
        game = Game1024()
        game.grid = [[0] * 4 for _ in range(4)]

        result = game.add_random_tile()

        assert result is True
        non_zero_count = sum(1 for row in game.grid for cell in row if cell != 0)
        assert non_zero_count == 1

    def test_get_empty_cells(self):
        game = Game1024()
        game.grid = [
            [2, 0, 0, 4],
            [0, 0, 2, 0],
            [0, 4, 0, 0],
            [0, 0, 0, 0]
        ]

        empty_cells = game.get_empty_cells()

        assert len(empty_cells) == 12
        assert (0, 1) in empty_cells
        assert (0, 2) in empty_cells
        assert (1, 0) in empty_cells

    def test_move_left(self):
        game = Game1024()
        game.grid = [
            [2, 2, 0, 0],
            [4, 0, 4, 0],
            [0, 0, 0, 0],
            [2, 0, 2, 0]
        ]

        result = game.move('left')

        assert result is True
        assert game.grid[0][0] == 4
        assert game.grid[1][0] == 8
        assert game.grid[3][0] == 4

    def test_move_right(self):
        game = Game1024()
        game.grid = [
            [0, 0, 2, 2],
            [0, 4, 0, 4],
            [0, 0, 0, 0],
            [0, 2, 0, 2]
        ]

        result = game.move('right')

        assert result is True
        assert game.grid[0][3] == 4
        assert game.grid[1][3] == 8
        assert game.grid[3][3] == 4

    def test_move_up(self):
        game = Game1024()
        game.grid = [
            [2, 0, 0, 4],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 4]
        ]

        result = game.move('up')

        assert result is True
        assert game.grid[0][0] == 4
        assert game.grid[0][3] == 8

    def test_move_down(self):
        game = Game1024()
        game.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 4],
            [2, 0, 0, 4]
        ]

        result = game.move('down')

        assert result is True
        assert game.grid[3][0] == 4
        assert game.grid[3][3] == 8

    def test_invalid_move(self):
        game = Game1024()
        original_grid = [row[:] for row in game.grid]

        result = game.move('invalid')

        assert result is False
        assert game.grid == original_grid

    def test_merge_row(self):
        game = Game1024()

        new_row, score, merges = game._merge_row([2, 2, 4, 4])

        assert new_row == [4, 8, 0, 0]
        assert score == 12
        assert merges == 2

    def test_merge_row_no_merges(self):
        game = Game1024()

        new_row, score, merges = game._merge_row([2, 4, 8, 16])

        assert new_row == [2, 4, 8, 16]
        assert score == 0
        assert merges == 0

    def test_is_game_over_empty_cells(self):
        game = Game1024()
        game.grid = [[0] * 4 for _ in range(4)]

        assert game.is_game_over() is False

    def test_is_game_over_possible_merges(self):
        game = Game1024()
        game.grid = [
            [2, 4, 8, 16],
            [4, 8, 16, 2],
            [8, 16, 2, 4],
            [16, 2, 4, 8]
        ]

        assert game.is_game_over() is True

    def test_is_game_over_no_moves(self):
        game = Game1024()
        game.grid = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]

        assert game.is_game_over() is True

    def test_win_condition(self):
        game = Game1024()
        game.target_score = 1024
        game.grid[0][0] = 1024
        game._update_max_tile()
        game._check_game_state()

        assert game.won is True

    def test_get_stats(self):
        game = Game1024()
        game.score = 100
        game.moves = 10
        game.merges = 5
        game.max_tile = 64

        stats = game.get_stats()

        assert stats['score'] == 100
        assert stats['moves'] == 10
        assert stats['merges'] == 5
        assert stats['max_tile'] == 64

    def test_get_grid(self):
        game = Game1024()
        game.grid[0][0] = 2

        grid = game.get_grid()

        assert grid[0][0] == 2
        grid[0][0] = 4

        assert game.grid[0][0] == 2


class TestLevelManager:
    def test_initialization(self):
        manager = LevelManager()

        assert manager.max_levels == 20
        assert manager.current_level == 1
        assert len(manager.level_difficulty) == 20

    def test_get_level_config(self):
        manager = LevelManager()

        config = manager.get_level_config(1)

        assert config['level'] == 1
        assert 'difficulty' in config
        assert 'target_score' in config

    def test_get_level_config_out_of_range(self):
        manager = LevelManager()

        config = manager.get_level_config(100)

        assert config['level'] == 20

    def test_set_level(self):
        manager = LevelManager()

        manager.set_level(5)

        assert manager.get_current_level() == 5

    def test_set_level_invalid(self):
        manager = LevelManager()
        original_level = manager.get_current_level()

        manager.set_level(100)

        assert manager.get_current_level() == original_level

    def test_next_level(self):
        manager = LevelManager()
        manager.set_level(1)

        result = manager.next_level()

        assert result is True
        assert manager.get_current_level() == 2

    def test_next_level_max(self):
        manager = LevelManager()
        manager.set_level(20)

        result = manager.next_level()

        assert result is False
        assert manager.get_current_level() == 20

    def test_update_player_stats(self):
        manager = LevelManager()

        manager.update_player_stats({
            'score': 100,
            'moves': 10,
            'won': True,
            'level': 1
        })

        assert manager.player_stats['total_games'] == 1
        assert manager.player_stats['total_wins'] == 1
        assert manager.player_stats['total_score'] == 100

    def test_calculate_adaptive_difficulty(self):
        manager = LevelManager()

        for _ in range(5):
            manager.update_player_stats({'score': 2000, 'won': True, 'moves': 20})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty > 1.0

    def test_get_unlocked_levels(self):
        manager = LevelManager()
        manager.player_stats['levels_completed'] = 3

        unlocked = manager.get_unlocked_levels()

        assert unlocked == 4

    def test_get_level_progress(self):
        manager = LevelManager()

        progress = manager.get_level_progress()

        assert len(progress) == 20
        assert progress[0]['level'] == 1
        assert progress[0]['unlocked'] is True

    def test_reset_progress(self):
        manager = LevelManager()
        manager.set_level(5)
        manager.player_stats['total_games'] = 10

        manager.reset_progress()

        assert manager.get_current_level() == 1
        assert manager.player_stats['total_games'] == 0


class TestConfig:
    def test_singleton(self):
        config1 = Config()
        config2 = Config()

        assert config1 is config2

    def test_get_default(self):
        config = Config()

        width = config.get('display', 'width')

        assert width == 800

    def test_get_nonexistent(self):
        config = Config()

        value = config.get('nonexistent', 'key', default='default')

        assert value == 'default'

    def test_set_value(self):
        config = Config()

        config.set('test', 'value', value=123)

        assert config.get('test', 'value') == 123


class TestDataManager:
    def test_initialization(self):
        manager = DataManager()

        assert manager.data_dir is not None
        assert manager.save_file is not None

    def test_save_and_load_game(self):
        manager = DataManager()

        game_data = {
            'grid': [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            'score': 100,
            'level': 1
        }

        manager.save_game(game_data)
        loaded_data = manager.load_game()

        assert loaded_data is not None
        assert loaded_data['score'] == 100

    def test_has_save_game(self):
        manager = DataManager()

        manager.save_game({'score': 100})

        assert manager.has_save_game() is True

    def test_delete_save_game(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.delete_save_game()

        assert manager.has_save_game() is False

    def test_update_stats(self):
        manager = DataManager()
        manager.reset_all()

        manager.update_stats({'score': 100, 'moves': 10})

        stats = manager.get_stats()

        assert stats['score'] == 100
        assert stats['moves'] == 10

    def test_unlock_achievement(self):
        manager = DataManager()

        result = manager.unlock_achievement('test_achievement')

        assert result is True
        assert manager.is_achievement_unlocked('test_achievement') is True

    def test_unlock_achievement_twice(self):
        manager = DataManager()

        manager.unlock_achievement('test_achievement')
        result = manager.unlock_achievement('test_achievement')

        assert result is False

    def test_high_score(self):
        manager = DataManager()

        manager.set_high_score(100)
        manager.set_high_score(200)

        assert manager.get_high_score() == 200

    def test_add_play_time(self):
        manager = DataManager()
        manager.reset_all()

        manager.add_play_time(60.0)
        manager.add_play_time(30.0)

        assert manager.get_total_play_time() == 90.0

    def test_add_game_to_history(self):
        manager = DataManager()

        manager.add_game_to_history({'score': 100, 'won': True})
        manager.add_game_to_history({'score': 200, 'won': False})

        history = manager.get_game_history()

        assert len(history) == 2
        assert history[0]['score'] == 100

    def test_reset_all(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.update_stats({'score': 100})
        manager.unlock_achievement('test')

        manager.reset_all()

        assert manager.has_save_game() is False
        assert manager.get_stats() == {}
        assert manager.get_achievements() == {}
