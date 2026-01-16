import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_manager import DataManager
from src.config import Config


class TestDataPersistence:
    def test_save_and_load_game(self):
        manager = DataManager()

        game_data = {
            'grid': [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            'score': 100,
            'level': 1,
            'moves': 10,
            'merges': 5,
            'max_tile': 64
        }

        manager.save_game(game_data)
        loaded_data = manager.load_game()

        assert loaded_data is not None
        assert loaded_data['score'] == 100
        assert loaded_data['level'] == 1
        assert loaded_data['moves'] == 10

    def test_save_overwrites_previous(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.save_game({'score': 200})

        loaded_data = manager.load_game()

        assert loaded_data['score'] == 200

    def test_delete_save_game(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.delete_save_game()

        assert manager.has_save_game() is False

    def test_stats_persistence(self):
        manager = DataManager()

        manager.update_stats({'score': 100, 'moves': 10})
        manager.update_stats({'score': 200, 'moves': 20})

        stats = manager.get_stats()

        assert stats['score'] == 300
        assert stats['moves'] == 30

    def test_achievement_persistence(self):
        manager = DataManager()

        manager.unlock_achievement('test_achievement')
        manager.unlock_achievement('another_achievement')

        achievements = manager.get_achievements()

        assert achievements['test_achievement'] is True
        assert achievements['another_achievement'] is True

    def test_high_score_persistence(self):
        manager = DataManager()

        manager.set_high_score(100)
        manager.set_high_score(200)
        manager.set_high_score(150)

        assert manager.get_high_score() == 200

    def test_play_time_persistence(self):
        manager = DataManager()

        manager.add_play_time(60.0)
        manager.add_play_time(30.0)
        manager.add_play_time(45.0)

        assert manager.get_total_play_time() == 135.0

    def test_game_history_persistence(self):
        manager = DataManager()

        manager.add_game_to_history({'score': 100, 'won': True})
        manager.add_game_to_history({'score': 200, 'won': False})
        manager.add_game_to_history({'score': 300, 'won': True})

        history = manager.get_game_history()

        assert len(history) == 3
        assert history[0]['score'] == 100
        assert history[1]['score'] == 200
        assert history[2]['score'] == 300

    def test_game_history_limit(self):
        manager = DataManager()

        for i in range(60):
            manager.add_game_to_history({'score': i, 'won': True})

        history = manager.get_game_history(limit=50)

        assert len(history) == 50

    def test_reset_stats(self):
        manager = DataManager()

        manager.update_stats({'score': 100, 'moves': 10})
        manager.reset_stats()

        stats = manager.get_stats()

        assert stats == {}

    def test_reset_achievements(self):
        manager = DataManager()

        manager.unlock_achievement('test_achievement')
        manager.reset_achievements()

        achievements = manager.get_achievements()

        assert achievements == {}

    def test_reset_all(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.update_stats({'score': 100})
        manager.unlock_achievement('test')

        manager.reset_all()

        assert manager.has_save_game() is False
        assert manager.get_stats() == {}
        assert manager.get_achievements() == {}

    def test_config_persistence(self):
        config = Config()

        config.set('display', 'width', value=1024)
        config.set('audio', 'volume', value=0.5)
        config.save()

        new_config = Config()
        new_config.load()

        assert new_config.get('display', 'width') == 1024
        assert new_config.get('audio', 'volume') == 0.5

    def test_theme_persistence(self):
        config = Config()

        config.set('theme', 'current_theme', value='dark')
        config.save()

        new_config = Config()
        new_config.load()

        assert new_config.get('theme', 'current_theme') == 'dark'

    def test_achievement_idempotent(self):
        manager = DataManager()

        result1 = manager.unlock_achievement('test')
        result2 = manager.unlock_achievement('test')

        assert result1 is True
        assert result2 is False

    def test_stats_accumulation(self):
        manager = DataManager()

        manager.update_stats({'score': 100, 'moves': 10, 'total_games': 1})
        manager.update_stats({'score': 200, 'moves': 20, 'total_games': 1})

        stats = manager.get_stats()

        assert stats['score'] == 300
        assert stats['moves'] == 30
        assert stats['total_games'] == 2

    def test_high_score_only_increases(self):
        manager = DataManager()

        manager.set_high_score(100)
        manager.set_high_score(50)

        assert manager.get_high_score() == 100

    def test_data_directory_creation(self):
        manager = DataManager()

        assert os.path.exists(manager.data_dir)

    def test_save_files_exist(self):
        manager = DataManager()

        manager.save_game({'score': 100})
        manager.update_stats({'score': 100})
        manager.unlock_achievement('test')

        assert os.path.exists(manager.save_file)
        assert os.path.exists(manager.stats_file)
        assert os.path.exists(manager.achievements_file)

    def test_corrupted_data_handling(self):
        manager = DataManager()

        with open(manager.save_file, 'w') as f:
            f.write('invalid json')

        manager.load_save_data()
        loaded_data = manager.load_game()

        assert loaded_data is None

    def test_empty_data_handling(self):
        manager = DataManager()

        if os.path.exists(manager.save_file):
            os.remove(manager.save_file)

        loaded_data = manager.load_game()

        assert loaded_data is None or loaded_data == {}

    def test_concurrent_access(self):
        manager = DataManager()

        for i in range(10):
            manager.save_game({'score': i})
            loaded = manager.load_game()
            assert loaded['score'] == i

    def test_large_data_handling(self):
        manager = DataManager()

        large_data = {'score': 100, 'grid': [[i * j for j in range(4)] for i in range(4)]}

        manager.save_game(large_data)
        loaded_data = manager.load_game()

        assert loaded_data['grid'] == large_data['grid']

    def test_special_characters_in_achievements(self):
        manager = DataManager()

        manager.unlock_achievement('achievement_with_underscores')
        manager.unlock_achievement('achievement-with-dashes')
        manager.unlock_achievement('achievement.with.dots')

        achievements = manager.get_achievements()

        assert achievements['achievement_with_underscores'] is True
        assert achievements['achievement-with-dashes'] is True
        assert achievements['achievement.with.dots'] is True

    def test_float_precision_in_stats(self):
        manager = DataManager()

        manager.add_play_time(0.1)
        manager.add_play_time(0.2)
        manager.add_play_time(0.3)

        total = manager.get_total_play_time()

        assert total == pytest.approx(0.6)
