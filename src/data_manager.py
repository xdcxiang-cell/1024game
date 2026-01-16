import json
import os
from typing import Dict, Any, List, Optional
from src.config import Config


class DataManager:
    def __init__(self):
        self.config = Config()
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

        self.save_file = os.path.join(self.data_dir, 'save_data.json')
        self.stats_file = os.path.join(self.data_dir, 'stats.json')
        self.achievements_file = os.path.join(self.data_dir, 'achievements.json')

        self.save_data: Dict[str, Any] = {}
        self.stats_data: Dict[str, Any] = {}
        self.achievements_data: Dict[str, bool] = {}

        self.load_all()

    def load_all(self):
        self.load_save_data()
        self.load_stats_data()
        self.load_achievements()

    def load_save_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    self.save_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.save_data = {}

    def load_stats_data(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.stats_data = {}

    def load_achievements(self):
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r') as f:
                    self.achievements_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.achievements_data = {}

    def save_all(self):
        self.save_save_data()
        self.save_stats_data()
        self.save_achievements()

    def save_save_data(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.save_data, f, indent=2)
        except IOError:
            pass

    def save_stats_data(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats_data, f, indent=2)
        except IOError:
            pass

    def save_achievements(self):
        try:
            with open(self.achievements_file, 'w') as f:
                json.dump(self.achievements_data, f, indent=2)
        except IOError:
            pass

    def save_game(self, game_data: Dict[str, Any]):
        self.save_data = game_data
        self.save_save_data()

    def load_game(self) -> Optional[Dict[str, Any]]:
        return self.save_data if self.save_data else None

    def has_save_game(self) -> bool:
        return bool(self.save_data)

    def delete_save_game(self):
        self.save_data = {}
        self.save_save_data()

    def update_stats(self, stats: Dict[str, Any]):
        for key, value in stats.items():
            if key in self.stats_data:
                if isinstance(value, (int, float)):
                    self.stats_data[key] += value
                elif isinstance(value, list):
                    self.stats_data[key].extend(value)
            else:
                self.stats_data[key] = value

        if 'total_games' in self.stats_data:
            self.stats_data['average_score'] = (
                self.stats_data.get('total_score', 0) / self.stats_data['total_games']
            )

        self.save_stats_data()

    def get_stats(self) -> Dict[str, Any]:
        return self.stats_data.copy()

    def unlock_achievement(self, achievement_id: str) -> bool:
        if achievement_id not in self.achievements_data:
            self.achievements_data[achievement_id] = True
            self.save_achievements()
            return True
        return False

    def is_achievement_unlocked(self, achievement_id: str) -> bool:
        return self.achievements_data.get(achievement_id, False)

    def get_achievements(self) -> Dict[str, bool]:
        return self.achievements_data.copy()

    def reset_all(self):
        self.save_data = {}
        self.stats_data = {}
        self.achievements_data = {}
        self.save_all()

    def reset_stats(self):
        self.stats_data = {}
        self.save_stats_data()

    def reset_achievements(self):
        self.achievements_data = {}
        self.save_achievements()

    def get_high_score(self) -> int:
        return self.stats_data.get('high_score', 0)

    def set_high_score(self, score: int):
        if score > self.get_high_score():
            self.stats_data['high_score'] = score
            self.save_stats_data()

    def get_total_play_time(self) -> float:
        return self.stats_data.get('total_play_time', 0.0)

    def add_play_time(self, seconds: float):
        self.stats_data['total_play_time'] = self.get_total_play_time() + seconds
        self.save_stats_data()

    def get_game_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        history = self.stats_data.get('game_history', [])
        return history[-limit:]

    def add_game_to_history(self, game_data: Dict[str, Any]):
        if 'game_history' not in self.stats_data:
            self.stats_data['game_history'] = []

        self.stats_data['game_history'].append(game_data)

        max_history = 50
        if len(self.stats_data['game_history']) > max_history:
            self.stats_data['game_history'] = self.stats_data['game_history'][-max_history:]

        self.save_stats_data()
