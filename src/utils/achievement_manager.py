#!/usr/bin/env python3
"""Achievement Manager - Tracks achievements and statistics"""

import json
import os
import time
from typing import Dict, Optional, List

from src.engine.constants import *


class AchievementManager:
    """Manages game achievements and statistics"""

    def __init__(self):
        self.achievements: Dict[str, Dict] = {}
        self.statistics: Dict[str, int] = {}
        self._init_achievements()
        self._init_statistics()
        self._load_data()

    def _init_achievements(self):
        """Initialize all achievements"""
        for ach_id in ACHIEVEMENTS.keys():
            self.achievements[ach_id] = {
                'unlocked': False,
                'unlocked_at': None,
                'progress': 0,
                'target': 1
            }

    def _init_statistics(self):
        """Initialize statistics"""
        for stat in STATISTICS:
            self.statistics[stat] = 0

    def unlock_achievement(self, achievement_id: str):
        """Unlock an achievement"""
        if achievement_id in self.achievements:
            ach = self.achievements[achievement_id]
            if not ach['unlocked']:
                ach['unlocked'] = True
                ach['unlocked_at'] = time.time()
                self.statistics['achievements_unlocked'] += 1
                self._save_data()
                return True
        return False

    def check_achievements(self, game_state: Dict):
        """Check and unlock achievements based on game state"""
        score = game_state.get('score', 0)
        moves = game_state.get('moves', 0)
        level = game_state.get('level', 1)
        max_tile = game_state.get('max_tile', 0)
        game_over = game_state.get('game_over', False)
        won = game_state.get('won', False)

        # Score-based achievements
        if score >= 1000:
            self.unlock_achievement('score_1000')
        if score >= 5000:
            self.unlock_achievement('score_5000')
        if score >= 10000:
            self.unlock_achievement('score_10000')
        if score >= 50000:
            self.unlock_achievement('score_50000')

        # Moves-based achievements
        if moves >= 100:
            self.unlock_achievement('moves_100')
        if moves >= 500:
            self.unlock_achievement('moves_500')
        if moves >= 1000:
            self.unlock_achievement('moves_1000')

        # Level-based achievements
        if level >= 5:
            self.unlock_achievement('level_5')
        if level >= 10:
            self.unlock_achievement('level_10')
        if level >= 15:
            self.unlock_achievement('level_15')
        if level >= 20:
            self.unlock_achievement('level_20')

        # Tile-based achievements
        if max_tile >= 128:
            self.unlock_achievement('first_128')
        if max_tile >= 256:
            self.unlock_achievement('first_256')
        if max_tile >= 512:
            self.unlock_achievement('first_512')
        if max_tile >= 1024:
            self.unlock_achievement('first_1024')
        if max_tile >= 2048:
            self.unlock_achievement('first_2048')

        # Game state achievements
        if game_state.get('games_played', 0) >= 1:
            self.unlock_achievement('first_game')
        
        if won and moves <= 50:
            self.unlock_achievement('perfect_game')

    def update_statistics(self, game_state: Dict):
        """Update game statistics"""
        # Update game count
        if game_state.get('game_over', False) or game_state.get('won', False):
            self.statistics['games_played'] += 1
            if game_state.get('won', False):
                self.statistics['games_won'] += 1
        
        # Update best score
        current_score = game_state.get('score', 0)
        if current_score > self.statistics['best_score']:
            self.statistics['best_score'] = current_score
        
        # Update total moves
        self.statistics['total_moves'] += game_state.get('moves', 0)
        
        # Update levels completed
        if game_state.get('level_complete', False):
            self.statistics['levels_completed'] += 1
        
        # Update max tile reached
        max_tile = game_state.get('max_tile', 0)
        if max_tile > self.statistics['max_tile_reached']:
            self.statistics['max_tile_reached'] = max_tile
        
        # Calculate average moves per game
        if self.statistics['games_played'] > 0:
            self.statistics['avg_moves_per_game'] = (
                self.statistics['total_moves'] // self.statistics['games_played']
            )
        
        self._save_data()

    def get_statistics(self) -> Dict:
        """Get all statistics"""
        return self.statistics.copy()

    def get_achievement(self, achievement_id: str) -> Optional[Dict]:
        """Get specific achievement"""
        return self.achievements.get(achievement_id)

    def get_all_achievements(self) -> Dict[str, Dict]:
        """Get all achievements"""
        return self.achievements.copy()

    def get_unlocked_count(self) -> int:
        """Get count of unlocked achievements"""
        return sum(1 for ach in self.achievements.values() if ach['unlocked'])

    def get_total_achievements(self) -> int:
        """Get total number of achievements"""
        return len(self.achievements)

    def get_statistics_display(self) -> List[str]:
        """Get formatted statistics for display"""
        stats = self.statistics
        lines = [
            f"Games Played: {stats['games_played']}",
            f"Games Won: {stats['games_won']}",
            f"Win Rate: {stats['games_won'] * 100 // max(stats['games_played'], 1)}%",
            f"Best Score: {stats['best_score']}",
            f"Total Moves: {stats['total_moves']}",
            f"Average Moves: {stats['avg_moves_per_game']}",
            f"Max Tile: {stats['max_tile_reached']}",
            f"Levels Completed: {stats['levels_completed']}",
            f"Achievements: {self.get_unlocked_count()}/{self.get_total_achievements()}"
        ]
        return lines

    def _save_data(self):
        """Save achievements and statistics to file"""
        try:
            os.makedirs(SAVES_PATH, exist_ok=True)
            data_file = os.path.join(SAVES_PATH, 'achievements.json')
            
            data = {
                'achievements': self.achievements,
                'statistics': self.statistics
            }
            
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save achievements: {e}")

    def _load_data(self):
        """Load achievements and statistics from file"""
        try:
            data_file = os.path.join(SAVES_PATH, 'achievements.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    
                # Merge loaded data
                if 'achievements' in data:
                    self.achievements.update(data['achievements'])
                if 'statistics' in data:
                    self.statistics.update(data['statistics'])
                    
        except Exception as e:
            print(f"Failed to load achievements: {e}")

    def reset_all(self):
        """Reset all achievements and statistics"""
        self._init_achievements()
        self._init_statistics()
        self._save_data()
