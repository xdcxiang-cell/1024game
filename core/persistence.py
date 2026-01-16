# -*- coding: utf-8 -*-
"""
1024 Game - Data Persistence System
Handles saving and loading game progress, achievements, and settings
"""

import json
import os
from datetime import datetime


class Achievement:
    def __init__(self, id, name, description, unlocked, unlock_date, icon, progress, max_progress):
        self.id = id
        self.name = name
        self.description = description
        self.unlocked = unlocked
        self.unlock_date = unlock_date
        self.icon = icon
        self.progress = progress
        self.max_progress = max_progress


class GameProgress:
    def __init__(self, current_level, highest_level, total_score, total_moves, games_played, games_won, total_time_played, tiles_merged, max_tile_ever, achievements):
        self.current_level = current_level
        self.highest_level = highest_level
        self.total_score = total_score
        self.total_moves = total_moves
        self.games_played = games_played
        self.games_won = games_won
        self.total_time_played = total_time_played
        self.tiles_merged = tiles_merged
        self.max_tile_ever = max_tile_ever
        self.achievements = achievements


class Settings:
    def __init__(self, theme, music_volume, sound_volume, particle_enabled, fps_limit, language, enable_3d_sound, show_fps, tutorial_completed):
        self.theme = theme
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.particle_enabled = particle_enabled
        self.fps_limit = fps_limit
        self.language = language
        self.enable_3d_sound = enable_3d_sound
        self.show_fps = show_fps
        self.tutorial_completed = tutorial_completed


class PersistenceManager:
    """Manages all data persistence for the game"""

    SAVE_DIR = os.path.join(os.path.dirname(__file__), '../data')
    PROGRESS_FILE = os.path.join(SAVE_DIR, 'progress.json')
    SETTINGS_FILE = os.path.join(SAVE_DIR, 'settings.json')

    def __init__(self):
        try:
            os.makedirs(self.SAVE_DIR)
        except OSError:
            if not os.path.isdir(self.SAVE_DIR):
                raise
        self._ensure_defaults()

    def _ensure_defaults(self):
        """Ensure default files exist"""
        if not os.path.exists(self.PROGRESS_FILE):
            self.save_progress(self._create_default_progress())
        if not os.path.exists(self.SETTINGS_FILE):
            self.save_settings(self._create_default_settings())

    def _create_default_progress(self):
        """Create default game progress"""
        return GameProgress(
            current_level=1,
            highest_level=1,
            total_score=0,
            total_moves=0,
            games_played=0,
            games_won=0,
            total_time_played=0.0,
            tiles_merged=0,
            max_tile_ever=0,
            achievements=self._create_default_achievements()
        )

    def _create_default_achievements(self):
        """Create default achievements"""
        return [
            Achievement('first_game', 'First Game', 'Start your first game', False, None, '🎮', 0, 1),
            Achievement('first_win', 'First Victory', 'Complete level 1', False, None, '🏆', 0, 1),
            Achievement('score_1000', 'Score Hunter', 'Reach 1000 points', False, None, '🎯', 0, 1000),
            Achievement('score_10000', 'Score Master', 'Reach 10000 points', False, None, '🎯', 0, 10000),
            Achievement('level_5', 'Level Champion', 'Reach level 5', False, None, '⭐', 0, 5),
            Achievement('level_10', 'Level Master', 'Reach level 10', False, None, '⭐', 0, 10),
            Achievement('level_20', 'Ultimate Champion', 'Reach level 20', False, None, '👑', 0, 20),
            Achievement('tile_2048', '2048 Master', 'Create a 2048 tile', False, None, '💎', 0, 2048),
            Achievement('tile_4096', '4096 Master', 'Create a 4096 tile', False, None, '💎', 0, 4096),
            Achievement('fast_win', 'Speed Demon', 'Complete a level in under 60 seconds', False, None, '⚡', 0, 1),
            Achievement('perfect_game', 'Perfect Game', 'Complete a level without losing a move', False, None, '💯', 0, 1),
            Achievement('50_games', 'Game Addict', 'Play 50 games', False, None, '🎰', 0, 50),
            Achievement('1000_moves', 'Strategist', 'Make 1000 moves', False, None, '🧠', 0, 1000),
            Achievement('no_merge_fail', 'Merge Master', 'Merge 100 tiles in a row', False, None, '🔗', 0, 100),
        ]

    def _create_default_settings(self):
        """Create default settings"""
        return Settings(
            theme='default',
            music_volume=0.5,
            sound_volume=0.7,
            particle_enabled=True,
            fps_limit=60,
            language='zh',
            enable_3d_sound=True,
            show_fps=False,
            tutorial_completed=False
        )

    def save_progress(self, progress):
        """Save game progress to file"""
        try:
            data = {
                'current_level': progress.current_level,
                'highest_level': progress.highest_level,
                'total_score': progress.total_score,
                'total_moves': progress.total_moves,
                'games_played': progress.games_played,
                'games_won': progress.games_won,
                'total_time_played': progress.total_time_played,
                'tiles_merged': progress.tiles_merged,
                'max_tile_ever': progress.max_tile_ever,
                'achievements': [{
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'unlocked': ach.unlocked,
                    'unlock_date': ach.unlock_date,
                    'icon': ach.icon,
                    'progress': ach.progress,
                    'max_progress': ach.max_progress
                } for ach in progress.achievements]
            }
            with open(self.PROGRESS_FILE, 'wb') as f:
                data_str = json.dumps(data, ensure_ascii=False, indent=2)
                f.write(data_str.encode('utf-8'))
            return True
        except Exception as e:
            print("Error saving progress: %s" % e)
            return False

    def load_progress(self):
        """Load game progress from file"""
        try:
            with open(self.PROGRESS_FILE, 'rb') as f:
                data_str = f.read().decode('utf-8')
                data = json.loads(data_str)

            achievements = []
            for ach_data in data.get('achievements', []):
                ach = Achievement(
                    id=ach_data['id'],
                    name=ach_data['name'],
                    description=ach_data['description'],
                    unlocked=ach_data['unlocked'],
                    unlock_date=ach_data.get('unlock_date'),
                    icon=ach_data.get('icon', '🏆'),
                    progress=ach_data.get('progress', 0),
                    max_progress=ach_data.get('max_progress', 1)
                )
                achievements.append(ach)

            return GameProgress(
                current_level=data.get('current_level', 1),
                highest_level=data.get('highest_level', 1),
                total_score=data.get('total_score', 0),
                total_moves=data.get('total_moves', 0),
                games_played=data.get('games_played', 0),
                games_won=data.get('games_won', 0),
                total_time_played=data.get('total_time_played', 0.0),
                tiles_merged=data.get('tiles_merged', 0),
                max_tile_ever=data.get('max_tile_ever', 0),
                achievements=achievements
            )
        except Exception as e:
            print("Error loading progress: %s" % e)
            return self._create_default_progress()

    def save_settings(self, settings):
        """Save settings to file"""
        try:
            data = {
                'theme': settings.theme,
                'music_volume': settings.music_volume,
                'sound_volume': settings.sound_volume,
                'particle_enabled': settings.particle_enabled,
                'fps_limit': settings.fps_limit,
                'language': settings.language,
                'enable_3d_sound': settings.enable_3d_sound,
                'show_fps': settings.show_fps,
                'tutorial_completed': settings.tutorial_completed
            }
            with open(self.SETTINGS_FILE, 'wb') as f:
                data_str = json.dumps(data, ensure_ascii=False, indent=2)
                f.write(data_str.encode('utf-8'))
            return True
        except Exception as e:
            print("Error saving settings: %s" % e)
            return False

    def load_settings(self):
        """Load settings from file"""
        try:
            with open(self.SETTINGS_FILE, 'rb') as f:
                data_str = f.read().decode('utf-8')
                data = json.loads(data_str)

            return Settings(
                theme=data.get('theme', 'default'),
                music_volume=data.get('music_volume', 0.5),
                sound_volume=data.get('sound_volume', 0.7),
                particle_enabled=data.get('particle_enabled', True),
                fps_limit=data.get('fps_limit', 60),
                language=data.get('language', 'zh'),
                enable_3d_sound=data.get('enable_3d_sound', True),
                show_fps=data.get('show_fps', False),
                tutorial_completed=data.get('tutorial_completed', False)
            )
        except Exception as e:
            print("Error loading settings: %s" % e)
            return self._create_default_settings()

    def update_game_stats(self, game_stats):
        """Update game statistics after a game session"""
        progress = self.load_progress()
        if not progress:
            return False

        progress.games_played += 1
        progress.total_score += int(game_stats.get('score', 0))
        progress.total_moves += game_stats.get('moves', 0)
        progress.total_time_played += game_stats.get('time_elapsed', 0.0)

        if game_stats.get('won', False):
            progress.games_won += 1

        max_tile = game_stats.get('max_tile', 0)
        if max_tile > progress.max_tile_ever:
            progress.max_tile_ever = max_tile

        if game_stats.get('level', 1) > progress.highest_level:
            progress.highest_level = game_stats.get('level', 1)

        progress.tiles_merged += game_stats.get('tiles_merged', 0)

        return self.save_progress(progress)

    def unlock_achievement(self, achievement_id, progress=1.0):
        """Unlock an achievement or update its progress"""
        progress_data = self.load_progress()
        if not progress_data:
            return False

        for ach in progress_data.achievements:
            if ach.id == achievement_id:
                if not ach.unlocked:
                    ach.progress = min(progress, ach.max_progress)
                    if ach.progress >= ach.max_progress:
                        ach.unlocked = True
                        ach.unlock_date = datetime.now().isoformat()

                return self.save_progress(progress_data)

        return False

    def check_achievements(self, game_stats):
        """Check and unlock achievements based on game stats"""
        unlocked = []
        progress = self.load_progress()
        if not progress:
            return unlocked

        # Check achievements
        for ach in progress.achievements:
            if not ach.unlocked:
                if self._check_achievement_condition(ach, game_stats, progress):
                    if self.unlock_achievement(ach.id):
                        unlocked.append(ach.id)

        return unlocked

    def _check_achievement_condition(self, ach, game_stats, progress):
        """Check if achievement condition is met"""
        if ach.id == 'first_game':
            return progress.games_played >= 1
        elif ach.id == 'first_win':
            return game_stats.get('won', False) and game_stats.get('level', 0) >= 1
        elif ach.id == 'score_1000':
            return game_stats.get('score', 0) >= 1000
        elif ach.id == 'score_10000':
            return game_stats.get('score', 0) >= 10000
        elif ach.id == 'level_5':
            return game_stats.get('level', 0) >= 5
        elif ach.id == 'level_10':
            return game_stats.get('level', 0) >= 10
        elif ach.id == 'level_20':
            return game_stats.get('level', 0) >= 20
        elif ach.id == 'tile_2048':
            return game_stats.get('max_tile', 0) >= 2048
        elif ach.id == 'tile_4096':
            return game_stats.get('max_tile', 0) >= 4096
        elif ach.id == 'fast_win':
            return game_stats.get('won', False) and game_stats.get('time_elapsed', float('inf')) < 60
        elif ach.id == 'perfect_game':
            return game_stats.get('won', False) and game_stats.get('failed_moves', 0) == 0
        elif ach.id == '50_games':
            return progress.games_played >= 50
        elif ach.id == '1000_moves':
            return progress.total_moves >= 1000
        elif ach.id == 'no_merge_fail':
            return game_stats.get('consecutive_merges', 0) >= 100

        return False

    def reset_progress(self):
        """Reset all progress to defaults"""
        return self.save_progress(self._create_default_progress())

    def get_statistics(self):
        """Get comprehensive game statistics"""
        progress = self.load_progress()
        if not progress:
            return {}

        win_rate = (progress.games_won / progress.games_played * 100) if progress.games_played > 0 else 0
        avg_score = progress.total_score / progress.games_played if progress.games_played > 0 else 0
        avg_moves = progress.total_moves / progress.games_played if progress.games_played > 0 else 0

        unlocked_count = sum(1 for ach in progress.achievements if ach.unlocked)
        total_achievements = len(progress.achievements)
        achievement_percentage = (unlocked_count / total_achievements * 100) if total_achievements > 0 else 0

        return {
            'current_level': progress.current_level,
            'highest_level': progress.highest_level,
            'total_score': progress.total_score,
            'total_moves': progress.total_moves,
            'games_played': progress.games_played,
            'games_won': progress.games_won,
            'win_rate': win_rate,
            'avg_score_per_game': avg_score,
            'avg_moves_per_game': avg_moves,
            'total_time_played_hours': progress.total_time_played / 3600,
            'tiles_merged': progress.tiles_merged,
            'max_tile_ever': progress.max_tile_ever,
            'unlocked_achievements': unlocked_count,
            'total_achievements': total_achievements,
            'achievement_percentage': achievement_percentage
        }

    def export_data(self):
        """Export all game data for backup"""
        progress = self.load_progress()
        settings = self.load_settings()
        
        progress_data = {
            'current_level': progress.current_level,
            'highest_level': progress.highest_level,
            'total_score': progress.total_score,
            'total_moves': progress.total_moves,
            'games_played': progress.games_played,
            'games_won': progress.games_won,
            'total_time_played': progress.total_time_played,
            'tiles_merged': progress.tiles_merged,
            'max_tile_ever': progress.max_tile_ever,
            'achievements': [{
                'id': ach.id,
                'name': ach.name,
                'description': ach.description,
                'unlocked': ach.unlocked,
                'unlock_date': ach.unlock_date,
                'icon': ach.icon,
                'progress': ach.progress,
                'max_progress': ach.max_progress
            } for ach in progress.achievements]
        } if progress else {}
        
        settings_data = {
            'theme': settings.theme,
            'music_volume': settings.music_volume,
            'sound_volume': settings.sound_volume,
            'particle_enabled': settings.particle_enabled,
            'fps_limit': settings.fps_limit,
            'language': settings.language,
            'enable_3d_sound': settings.enable_3d_sound,
            'show_fps': settings.show_fps,
            'tutorial_completed': settings.tutorial_completed
        } if settings else {}
        
        return {
            'progress': progress_data,
            'settings': settings_data,
            'export_date': datetime.now().isoformat()
        }

    def import_data(self, data):
        """Import game data from backup"""
        try:
            if 'progress' in data:
                with open(self.PROGRESS_FILE, 'wb') as f:
                    data_str = json.dumps(progress_data, ensure_ascii=False, indent=2)
                    f.write(data_str.encode('utf-8'))
                    json.dump(data['progress'], f, ensure_ascii=False, indent=2)

            if 'settings' in data:
                with open(self.SETTINGS_FILE, 'wb') as f:
                    data_str = json.dumps(settings_data, ensure_ascii=False, indent=2)
                    f.write(data_str.encode('utf-8'))
                    json.dump(data['settings'], f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print("Error importing data: %s" % e)
            return False


# Global instance
persistence = PersistenceManager()
