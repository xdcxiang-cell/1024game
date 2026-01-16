"""
1024 Game - Persistence Tests
Comprehensive tests for the data persistence system
"""

import unittest
import os
import sys
import json
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.persistence import PersistenceManager, Achievement, GameProgress, Settings


class TestPersistence(unittest.TestCase):
    """Test cases for the PersistenceManager class"""

    def setUp(self):
        """Set up temporary files for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.progress_file = os.path.join(self.temp_dir, 'progress.json')
        self.settings_file = os.path.join(self.temp_dir, 'settings.json')

        self.original_save_dir = PersistenceManager.SAVE_DIR
        PersistenceManager.SAVE_DIR = self.temp_dir
        PersistenceManager.PROGRESS_FILE = self.progress_file
        PersistenceManager.SETTINGS_FILE = self.settings_file

        self.persistence = PersistenceManager()

    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir)
        PersistenceManager.SAVE_DIR = self.original_save_dir
        PersistenceManager.PROGRESS_FILE = os.path.join(self.original_save_dir, 'progress.json')
        PersistenceManager.SETTINGS_FILE = os.path.join(self.original_save_dir, 'settings.json')

    def test_default_creation(self):
        """Test default files are created"""
        self.assertTrue(os.path.exists(self.progress_file))
        self.assertTrue(os.path.exists(self.settings_file))

    def test_save_and_load_progress(self):
        """Test saving and loading progress"""
        progress = GameProgress(
            current_level=5,
            highest_level=10,
            total_score=10000,
            total_moves=500,
            games_played=10,
            games_won=5,
            total_time_played=3600.0,
            tiles_merged=200,
            max_tile_ever=2048,
            achievements=[]
        )

        result = self.persistence.save_progress(progress)
        self.assertTrue(result)

        loaded = self.persistence.load_progress()
        self.assertEqual(loaded.current_level, 5)
        self.assertEqual(loaded.highest_level, 10)
        self.assertEqual(loaded.total_score, 10000)

    def test_save_and_load_settings(self):
        """Test saving and loading settings"""
        settings = Settings(
            theme='dark',
            music_volume=0.8,
            sound_volume=0.9,
            particle_enabled=True,
            fps_limit=120,
            language='en',
            enable_3d_sound=True,
            show_fps=True,
            tutorial_completed=True
        )

        result = self.persistence.save_settings(settings)
        self.assertTrue(result)

        loaded = self.persistence.load_settings()
        self.assertEqual(loaded.theme, 'dark')
        self.assertEqual(loaded.music_volume, 0.8)
        self.assertEqual(loaded.fps_limit, 120)

    def test_update_game_stats(self):
        """Test updating game statistics"""
        game_stats = {
            'score': 1000,
            'moves': 50,
            'time_elapsed': 120.0,
            'won': True,
            'level': 3,
            'max_tile': 512,
            'tiles_merged': 25
        }

        result = self.persistence.update_game_stats(game_stats)
        self.assertTrue(result)

        progress = self.persistence.load_progress()
        self.assertEqual(progress.games_played, 1)
        self.assertEqual(progress.total_score, 1000)
        self.assertEqual(progress.games_won, 1)
        self.assertEqual(progress.tiles_merged, 25)

    def test_unlock_achievement(self):
        """Test unlocking an achievement"""
        result = self.persistence.unlock_achievement('first_game')
        self.assertTrue(result)

        progress = self.persistence.load_progress()
        for ach in progress.achievements:
            if ach.id == 'first_game':
                self.assertTrue(ach.unlocked)
                self.assertIsNotNone(ach.unlock_date)
                break
        else:
            self.fail('Achievement not found')

    def test_unlock_achievement_with_progress(self):
        """Test achievement progress update"""
        result = self.persistence.unlock_achievement('score_1000', 500)
        self.assertTrue(result)

        progress = self.persistence.load_progress()
        for ach in progress.achievements:
            if ach.id == 'score_1000':
                self.assertFalse(ach.unlocked)
                self.assertEqual(ach.progress, 500)
                break
        else:
            self.fail('Achievement not found')

    def test_check_achievements(self):
        """Test achievement checking"""
        game_stats = {
            'score': 1000,
            'moves': 50,
            'time_elapsed': 120.0,
            'won': True,
            'level': 3,
            'max_tile': 512,
            'tiles_merged': 25
        }

        unlocked = self.persistence.check_achievements(game_stats)
        self.assertIn('first_win', unlocked)
        self.assertIn('score_1000', unlocked)

    def test_reset_progress(self):
        """Test progress reset"""
        progress = GameProgress(
            current_level=5,
            highest_level=10,
            total_score=10000,
            total_moves=500,
            games_played=10,
            games_won=5,
            total_time_played=3600.0,
            tiles_merged=200,
            max_tile_ever=2048,
            achievements=[]
        )

        self.persistence.save_progress(progress)

        result = self.persistence.reset_progress()
        self.assertTrue(result)

        loaded = self.persistence.load_progress()
        self.assertEqual(loaded.current_level, 1)
        self.assertEqual(loaded.total_score, 0)

    def test_get_statistics(self):
        """Test getting comprehensive statistics"""
        progress = GameProgress(
            current_level=5,
            highest_level=10,
            total_score=10000,
            total_moves=500,
            games_played=10,
            games_won=5,
            total_time_played=3600.0,
            tiles_merged=200,
            max_tile_ever=2048,
            achievements=[
                Achievement('first_game', 'First', '', True, '', '', 1.0, 1.0),
                Achievement('first_win', 'Win', '', False, '', '', 0.0, 1.0),
                Achievement('score_1000', 'Score', '', True, '', '', 1.0, 1.0)
            ]
        )

        self.persistence.save_progress(progress)
        stats = self.persistence.get_statistics()

        self.assertEqual(stats['current_level'], 5)
        self.assertEqual(stats['highest_level'], 10)
        self.assertEqual(stats['win_rate'], 50.0)
        self.assertEqual(stats['avg_score_per_game'], 1000.0)
        self.assertEqual(stats['unlocked_achievements'], 2)

    def test_export_and_import_data(self):
        """Test exporting and importing data"""
        progress = GameProgress(
            current_level=5,
            highest_level=10,
            total_score=10000,
            total_moves=500,
            games_played=10,
            games_won=5,
            total_time_played=3600.0,
            tiles_merged=200,
            max_tile_ever=2048,
            achievements=[]
        )

        settings = Settings(
            theme='dark',
            music_volume=0.8,
            sound_volume=0.9,
            particle_enabled=True,
            fps_limit=120,
            language='en',
            enable_3d_sound=True,
            show_fps=True,
            tutorial_completed=True
        )

        self.persistence.save_progress(progress)
        self.persistence.save_settings(settings)

        exported = self.persistence.export_data()
        self.assertIn('progress', exported)
        self.assertIn('settings', exported)
        self.assertIn('export_date', exported)

        progress2 = GameProgress(
            current_level=1,
            highest_level=1,
            total_score=0,
            total_moves=0,
            games_played=0,
            games_won=0,
            total_time_played=0.0,
            tiles_merged=0,
            max_tile_ever=0,
            achievements=[]
        )

        self.persistence.save_progress(progress2)

        result = self.persistence.import_data(exported)
        self.assertTrue(result)

        loaded = self.persistence.load_progress()
        self.assertEqual(loaded.current_level, 5)

    def test_default_achievements_created(self):
        """Test default achievements are created"""
        progress = self.persistence.load_progress()
        self.assertGreater(len(progress.achievements), 0)

        ach_ids = [ach.id for ach in progress.achievements]
        self.assertIn('first_game', ach_ids)
        self.assertIn('first_win', ach_ids)
        self.assertIn('tile_2048', ach_ids)
        self.assertIn('level_20', ach_ids)

    def test_achievement_unlock_condition(self):
        """Test achievement unlocking conditions"""
        # Test first_game achievement
        game_stats = {'won': False}
        self.persistence.update_game_stats(game_stats)

        unlocked = self.persistence.check_achievements(game_stats)
        self.assertIn('first_game', unlocked)

        # Test first_win achievement
        game_stats = {'won': True, 'level': 1, 'score': 100}
        self.persistence.update_game_stats(game_stats)

        unlocked = self.persistence.check_achievements(game_stats)
        self.assertIn('first_win', unlocked)

    def test_invalid_file_handling(self):
        """Test handling of corrupted files"""
        with open(self.progress_file, 'w') as f:
            f.write('invalid json')

        loaded = self.persistence.load_progress()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.current_level, 1)

    def test_settings_defaults(self):
        """Test default settings"""
        settings = self.persistence.load_settings()
        self.assertEqual(settings.theme, 'default')
        self.assertEqual(settings.music_volume, 0.5)
        self.assertEqual(settings.particle_enabled, True)
        self.assertEqual(settings.fps_limit, 60)

    def test_achievement_progress_tracking(self):
        """Test achievement progress tracking"""
        # Test progress update without unlock
        result = self.persistence.unlock_achievement('score_1000', 500)
        self.assertTrue(result)

        progress = self.persistence.load_progress()
        for ach in progress.achievements:
            if ach.id == 'score_1000':
                self.assertFalse(ach.unlocked)
                self.assertEqual(ach.progress, 500)
                break
        else:
            self.fail('Achievement not found')

        # Test progress update with unlock
        result = self.persistence.unlock_achievement('score_1000', 1000)
        self.assertTrue(result)

        progress = self.persistence.load_progress()
        for ach in progress.achievements:
            if ach.id == 'score_1000':
                self.assertTrue(ach.unlocked)
                break


if __name__ == '__main__':
    unittest.main()
