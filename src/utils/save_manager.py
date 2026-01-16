#!/usr/bin/env python3
"""Save Manager - Handles game data persistence"""

import json
import os
import pickle
from datetime import datetime
from typing import Dict, Optional


class SaveManager:
    """Manages game state saving and loading"""

    def __init__(self, save_dir: str = 'saves'):
        self.save_dir = save_dir
        self.save_files = {
            'game_state': 'game_state.json',
            'settings': 'settings.json',
            'progress': 'progress.json',
            'statistics': 'statistics.pkl'
        }
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure save directory exists"""
        os.makedirs(self.save_dir, exist_ok=True)

    def save_game_state(self, game_state: Dict):
        """Save current game state"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['game_state'])
            data = {
                'state': game_state,
                'timestamp': datetime.now().isoformat(),
                'version': '1.0'
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save game state: {e}")
            return False

    def load_game_state(self) -> Optional[Dict]:
        """Load saved game state"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['game_state'])
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data.get('state')
        except Exception as e:
            print(f"Failed to load game state: {e}")
            return None

    def save_settings(self, settings: Dict):
        """Save game settings"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['settings'])
            data = {
                'settings': settings,
                'timestamp': datetime.now().isoformat()
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False

    def load_settings(self) -> Optional[Dict]:
        """Load saved settings"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['settings'])
            if not os.path.exists(filepath):
                return self.get_default_settings()
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data.get('settings', self.get_default_settings())
        except Exception as e:
            print(f"Failed to load settings: {e}")
            return self.get_default_settings()

    def get_default_settings(self) -> Dict:
        """Get default settings"""
        return {
            'master_volume': 0.7,
            'sfx_volume': 0.8,
            'music_volume': 0.5,
            'fullscreen': False,
            'fps_limit': 60,
            'particle_effects': True,
            '3d_audio': True,
            'theme': 'default',
            'language': 'en',
            'show_fps': False,
            'auto_save': True,
            'difficulty': 'normal'
        }

    def save_progress(self, progress: Dict):
        """Save game progress"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['progress'])
            data = {
                'progress': progress,
                'timestamp': datetime.now().isoformat()
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save progress: {e}")
            return False

    def load_progress(self) -> Optional[Dict]:
        """Load game progress"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['progress'])
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data.get('progress')
        except Exception as e:
            print(f"Failed to load progress: {e}")
            return None

    def save_statistics(self, statistics: Dict):
        """Save statistics using pickle for complex objects"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['statistics'])
            data = {
                'statistics': statistics,
                'timestamp': datetime.now().isoformat()
            }
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Failed to save statistics: {e}")
            return False

    def load_statistics(self) -> Optional[Dict]:
        """Load statistics"""
        try:
            filepath = os.path.join(self.save_dir, self.save_files['statistics'])
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            return data.get('statistics')
        except Exception as e:
            print(f"Failed to load statistics: {e}")
            return None

    def delete_save(self, save_type: str):
        """Delete specific save file"""
        if save_type not in self.save_files:
            return False
        try:
            filepath = os.path.join(self.save_dir, self.save_files[save_type])
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception as e:
            print(f"Failed to delete save: {e}")
            return False

    def delete_all_saves(self):
        """Delete all save files"""
        for save_file in self.save_files.values():
            filepath = os.path.join(self.save_dir, save_file)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass

    def has_save(self, save_type: str) -> bool:
        """Check if save file exists"""
        if save_type not in self.save_files:
            return False
        filepath = os.path.join(self.save_dir, self.save_files[save_type])
        return os.path.exists(filepath)

    def get_save_info(self, save_type: str) -> Optional[Dict]:
        """Get information about save file"""
        if not self.has_save(save_type):
            return None
        filepath = os.path.join(self.save_dir, self.save_files[save_type])
        stat = os.stat(filepath)
        return {
            'exists': True,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
        }

    def backup_saves(self, backup_dir: str = 'backups'):
        """Create backup of all saves"""
        import shutil
        
        try:
            backup_path = os.path.join(self.save_dir, backup_dir)
            os.makedirs(backup_path, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'save_backup_{timestamp}'
            full_backup_path = os.path.join(backup_path, backup_name)
            
            # Copy save directory
            shutil.copytree(self.save_dir, full_backup_path, 
                           ignore=shutil.ignore_patterns(backup_dir))
            
            return full_backup_path
        except Exception as e:
            print(f"Failed to backup saves: {e}")
            return None

    def auto_save(self, game_state: Dict, settings: Dict, progress: Dict):
        """Auto-save all data"""
        results = {
            'game_state': self.save_game_state(game_state),
            'settings': self.save_settings(settings),
            'progress': self.save_progress(progress)
        }
        return all(results.values())
