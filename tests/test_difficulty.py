import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.level_manager import LevelManager


class TestLevelDifficulty:
    def test_difficulty_increases_with_tiers(self):
        manager = LevelManager()

        level_1_diff = manager.get_level_config(1)['difficulty']
        level_5_diff = manager.get_level_config(5)['difficulty']
        level_10_diff = manager.get_level_config(10)['difficulty']

        assert level_5_diff > level_1_diff
        assert level_10_diff > level_5_diff

    def test_target_score_increases(self):
        manager = LevelManager()

        level_1_target = manager.get_level_config(1)['target_score']
        level_10_target = manager.get_level_config(10)['target_score']
        level_20_target = manager.get_level_config(20)['target_score']

        assert level_10_target > level_1_target
        assert level_20_target > level_10_target

    def test_grid_obstacles_increase(self):
        manager = LevelManager()

        level_1_obstacles = manager.get_level_config(1)['grid_obstacles']
        level_10_obstacles = manager.get_level_config(10)['grid_obstacles']
        level_20_obstacles = manager.get_level_config(20)['grid_obstacles']

        assert level_1_obstacles == 0
        assert level_10_obstacles > level_1_obstacles
        assert level_20_obstacles <= 3

    def test_time_limit_appears_at_higher_levels(self):
        manager = LevelManager()

        level_5_time = manager.get_level_config(5)['time_limit']
        level_10_time = manager.get_level_config(10)['time_limit']
        level_11_time = manager.get_level_config(11)['time_limit']

        assert level_5_time is None
        assert level_10_time is None
        assert level_11_time is not None

    def test_tile_spawn_rate_decreases(self):
        manager = LevelManager()

        level_1_rate = manager.get_level_config(1)['tile_spawn_rate']
        level_10_rate = manager.get_level_config(10)['tile_spawn_rate']
        level_20_rate = manager.get_level_config(20)['tile_spawn_rate']

        assert level_10_rate < level_1_rate
        assert level_20_rate < level_10_rate

    def test_four_spawn_rate_increases(self):
        manager = LevelManager()

        level_1_rate = manager.get_level_config(1)['four_spawn_rate']
        level_10_rate = manager.get_level_config(10)['four_spawn_rate']
        level_20_rate = manager.get_level_config(20)['four_spawn_rate']

        assert level_10_rate > level_1_rate
        assert level_20_rate > level_10_rate


class TestAdaptiveDifficulty:
    def test_low_win_rate_decreases_difficulty(self):
        manager = LevelManager()

        for _ in range(5):
            manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty < 1.0

    def test_high_win_rate_increases_difficulty(self):
        manager = LevelManager()

        for _ in range(5):
            manager.update_player_stats({'score': 2000, 'won': True, 'moves': 20})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty > 1.0

    def test_high_score_increases_difficulty(self):
        manager = LevelManager()

        for _ in range(5):
            manager.update_player_stats({'score': 5000, 'won': True, 'moves': 30})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty > 1.0

    def test_low_score_decreases_difficulty(self):
        manager = LevelManager()

        for _ in range(5):
            manager.update_player_stats({'score': 200, 'won': False, 'moves': 5})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty < 1.0

    def test_adaptive_difficulty_clamped(self):
        manager = LevelManager()

        for _ in range(10):
            manager.update_player_stats({'score': 10000, 'won': True, 'moves': 5})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty <= 2.0

    def test_few_games_no_adjustment(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 1000, 'won': True, 'moves': 10})

        difficulty = manager.calculate_adaptive_difficulty()

        assert difficulty == 1.0

    def test_mixed_performance_moderate_difficulty(self):
        manager = LevelManager()

        for i in range(10):
            won = i % 2 == 0
            score = 1500 if won else 500
            manager.update_player_stats({'score': score, 'won': won, 'moves': 15})

        difficulty = manager.calculate_adaptive_difficulty()

        assert 0.8 <= difficulty <= 1.2


class TestLevelProgression:
    def test_unlocked_levels_based_on_completion(self):
        manager = LevelManager()
        manager.player_stats['levels_completed'] = 5

        unlocked = manager.get_unlocked_levels()

        assert unlocked == 6

    def test_max_unlocked_levels(self):
        manager = LevelManager()
        manager.player_stats['levels_completed'] = 25

        unlocked = manager.get_unlocked_levels()

        assert unlocked == 20

    def test_level_progress_structure(self):
        manager = LevelManager()

        progress = manager.get_level_progress()

        assert len(progress) == 20
        assert all('level' in p for p in progress)
        assert all('unlocked' in p for p in progress)
        assert all('completed' in p for p in progress)
        assert all('difficulty' in p for p in progress)
        assert all('target_score' in p for p in progress)

    def test_first_level_always_unlocked(self):
        manager = LevelManager()

        progress = manager.get_level_progress()

        assert progress[0]['unlocked'] is True

    def test_higher_levels_locked_initially(self):
        manager = LevelManager()

        progress = manager.get_level_progress()

        assert progress[19]['unlocked'] is False

    def test_completed_levels_marked(self):
        manager = LevelManager()
        manager.player_stats['levels_completed'] = 3

        progress = manager.get_level_progress()

        assert progress[0]['completed'] is True
        assert progress[1]['completed'] is True
        assert progress[2]['completed'] is True
        assert progress[3]['completed'] is False


class TestPlayerStats:
    def test_total_games_incremented(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})

        assert manager.player_stats['total_games'] == 1

    def test_total_wins_incremented(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': True, 'moves': 10})

        assert manager.player_stats['total_wins'] == 1

    def test_total_score_accumulated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})
        manager.update_player_stats({'score': 200, 'won': True, 'moves': 15})

        assert manager.player_stats['total_score'] == 300

    def test_average_score_calculated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})
        manager.update_player_stats({'score': 200, 'won': True, 'moves': 15})

        assert manager.player_stats['average_score'] == 150.0

    def test_win_rate_calculated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': True, 'moves': 10})
        manager.update_player_stats({'score': 200, 'won': False, 'moves': 15})
        manager.update_player_stats({'score': 300, 'won': True, 'moves': 20})

        assert manager.player_stats['win_rate'] == pytest.approx(0.6667, rel=0.01)

    def test_best_score_updated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})
        manager.update_player_stats({'score': 500, 'won': True, 'moves': 15})
        manager.update_player_stats({'score': 300, 'won': True, 'moves': 20})

        assert manager.player_stats['best_score'] == 500

    def test_levels_completed_updated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': True, 'level': 1, 'moves': 10})
        manager.update_player_stats({'score': 200, 'won': True, 'level': 2, 'moves': 15})
        manager.update_player_stats({'score': 300, 'won': True, 'level': 5, 'moves': 20})

        assert manager.player_stats['levels_completed'] == 5

    def test_average_moves_calculated(self):
        manager = LevelManager()

        manager.update_player_stats({'score': 100, 'won': False, 'moves': 10})
        manager.update_player_stats({'score': 200, 'won': True, 'moves': 20})
        manager.update_player_stats({'score': 300, 'won': True, 'moves': 30})

        assert manager.player_stats['average_moves'] == 20.0
