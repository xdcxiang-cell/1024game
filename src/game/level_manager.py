#!/usr/bin/env python3
"""Level Manager - Manages 20 levels with intelligent difficulty adjustment"""

import json
import os
from typing import Dict, List, Optional

from src.engine.constants import *


class LevelConfig:
    """Configuration for a single level"""

    def __init__(self, level_num: int, difficulty: int):
        self.level_num = level_num
        self.difficulty = difficulty
        
        # Difficulty parameters
        self.spawn_prob_2 = 0.9  # Probability to spawn 2
        self.spawn_prob_4 = 0.1  # Probability to spawn 4
        self.max_initial_tiles = 2
        self.move_time_limit = None  # None for unlimited
        self.target_score = 0
        self.max_moves = None  # None for unlimited
        
        # Tile spawning rules
        self.allow_high_tiles = False
        self.min_tile_value = 2
        self.max_tile_value = 2048
        
        # Initialize based on difficulty
        self._init_from_difficulty()

    def _init_from_difficulty(self):
        """Initialize level parameters based on difficulty"""
        # Difficulty 1-4 (every 5 levels)
        if self.difficulty == 1:
            # Levels 1-5: Easy
            self.spawn_prob_2 = 0.95
            self.spawn_prob_4 = 0.05
            self.max_initial_tiles = 2
            self.target_score = 1000 * self.level_num
        elif self.difficulty == 2:
            # Levels 6-10: Medium
            self.spawn_prob_2 = 0.85
            self.spawn_prob_4 = 0.15
            self.max_initial_tiles = 2
            self.target_score = 2500 * self.level_num
            self.max_moves = 150
        elif self.difficulty == 3:
            # Levels 11-15: Hard
            self.spawn_prob_2 = 0.75
            self.spawn_prob_4 = 0.25
            self.max_initial_tiles = 2
            self.allow_high_tiles = True
            self.target_score = 5000 * self.level_num
            self.max_moves = 120
        elif self.difficulty == 4:
            # Levels 16-20: Expert
            self.spawn_prob_2 = 0.65
            self.spawn_prob_4 = 0.35
            self.max_initial_tiles = 3
            self.allow_high_tiles = True
            self.target_score = 10000 * self.level_num
            self.max_moves = 100
            
            # Add random 8 tiles
            self.spawn_prob_4 = 0.30
            self.spawn_prob_8 = 0.05

    def can_spawn_tile(self, value: int) -> bool:
        """Check if tile value can be spawned"""
        return self.min_tile_value <= value <= self.max_tile_value

    def get_spawn_weights(self) -> Dict[int, float]:
        """Get tile spawn probabilities"""
        weights = {2: self.spawn_prob_2, 4: self.spawn_prob_4}
        if hasattr(self, 'spawn_prob_8'):
            weights[8] = self.spawn_prob_8
        return weights

    def is_level_complete(self, score: int, moves: int) -> bool:
        """Check if level is complete"""
        return score >= self.target_score

    def is_level_failed(self, moves: int, game_over: bool) -> bool:
        """Check if level is failed"""
        if game_over:
            return True
        if self.max_moves and moves >= self.max_moves:
            return True
        return False


class LevelManager:
    """Manages all 20 levels with difficulty progression"""

    def __init__(self):
        self.current_level = 1
        self.unlocked_levels = 1
        self.level_progress: Dict[int, Dict] = {}
        self.level_configs: List[LevelConfig] = []
        
        # Initialize all 20 levels
        self._init_levels()
        self._load_progress()

    def _init_levels(self):
        """Initialize all 20 levels"""
        for level_num in range(1, MAX_LEVEL + 1):
            difficulty = (level_num - 1) // DIFFICULTY_THRESHOLD + 1
            config = LevelConfig(level_num, difficulty)
            self.level_configs.append(config)
            
            # Initialize progress
            self.level_progress[level_num] = {
                'completed': False,
                'best_score': 0,
                'best_moves': None,
                'stars': 0
            }

    def get_level_config(self, level_num: int) -> Optional[LevelConfig]:
        """Get configuration for a specific level"""
        if 1 <= level_num <= MAX_LEVEL:
            return self.level_configs[level_num - 1]
        return None

    def is_level_unlocked(self, level_num: int) -> bool:
        """Check if level is unlocked"""
        return level_num <= self.unlocked_levels

    def unlock_level(self, level_num: int):
        """Unlock a level"""
        if level_num > self.unlocked_levels:
            self.unlocked_levels = level_num
            self._save_progress()

    def complete_level(self, level_num: int, score: int, moves: int):
        """Mark level as completed and calculate stars"""
        if level_num < 1 or level_num > MAX_LEVEL:
            return
        
        config = self.get_level_config(level_num)
        if not config:
            return
        
        progress = self.level_progress[level_num]
        
        # Update best score
        if score > progress['best_score']:
            progress['best_score'] = score
        
        # Update best moves
        if progress['best_moves'] is None or moves < progress['best_moves']:
            progress['best_moves'] = moves
        
        # Calculate stars (1-3 based on performance)
        target = config.target_score
        if score >= target * 2:
            stars = 3
        elif score >= target * 1.5:
            stars = 2
        elif score >= target:
            stars = 1
        else:
            stars = 0
        
        if stars > progress['stars']:
            progress['stars'] = stars
        
        if not progress['completed']:
            progress['completed'] = True
            self.unlock_level(level_num + 1)
        
        self._save_progress()

    def get_difficulty_stats(self) -> Dict:
        """Get statistics about difficulty progression"""
        stats = {
            'current_difficulty': self.get_difficulty_level(self.current_level),
            'levels_by_difficulty': {
                1: list(range(1, 6)),
                2: list(range(6, 11)),
                3: list(range(11, 16)),
                4: list(range(16, 21))
            },
            'difficulty_description': self.get_difficulty_description()
        }
        return stats

    def get_difficulty_level(self, level_num: int) -> int:
        """Get difficulty level for a given level"""
        return (level_num - 1) // DIFFICULTY_THRESHOLD + 1

    def get_difficulty_description(self) -> Dict[int, str]:
        """Get descriptions for each difficulty level"""
        return {
            1: "Easy - 95% chance to spawn 2 tiles, no move limit",
            2: "Medium - 85% chance to spawn 2 tiles, 150 move limit",
            3: "Hard - 75% chance to spawn 2 tiles, 120 move limit, high tiles allowed",
            4: "Expert - 65% chance to spawn 2 tiles, 100 move limit, may spawn 8s"
        }

    def get_level_stats(self, level_num: int) -> Optional[Dict]:
        """Get statistics for a specific level"""
        if level_num not in self.level_progress:
            return None
        
        config = self.get_level_config(level_num)
        progress = self.level_progress[level_num]
        
        return {
            'level_num': level_num,
            'difficulty': config.difficulty,
            'completed': progress['completed'],
            'stars': progress['stars'],
            'best_score': progress['best_score'],
            'best_moves': progress['best_moves'],
            'target_score': config.target_score,
            'max_moves': config.max_moves
        }

    def get_overall_progress(self) -> Dict:
        """Get overall game progress"""
        completed = sum(1 for p in self.level_progress.values() if p['completed'])
        total_stars = sum(p['stars'] for p in self.level_progress.values())
        max_stars = MAX_LEVEL * 3
        
        return {
            'total_levels': MAX_LEVEL,
            'completed_levels': completed,
            'unlocked_levels': self.unlocked_levels,
            'total_stars': total_stars,
            'max_stars': max_stars,
            'progress_percent': (completed / MAX_LEVEL) * 100,
            'stars_percent': (total_stars / max_stars) * 100
        }

    def _load_progress(self):
        """Load level progress from file"""
        try:
            progress_file = os.path.join(SAVES_PATH, 'level_progress.json')
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    data = json.load(f)
                    
                # Update progress
                for level_num, progress in data.get('level_progress', {}).items():
                    level_num = int(level_num)
                    if level_num in self.level_progress:
                        self.level_progress[level_num].update(progress)
                
                # Update unlocked levels
                self.unlocked_levels = data.get('unlocked_levels', 1)
                
        except Exception as e:
            print(f"Failed to load progress: {e}")

    def _save_progress(self):
        """Save level progress to file"""
        try:
            os.makedirs(SAVES_PATH, exist_ok=True)
            progress_file = os.path.join(SAVES_PATH, 'level_progress.json')
            
            data = {
                'level_progress': self.level_progress,
                'unlocked_levels': self.unlocked_levels
            }
            
            with open(progress_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save progress: {e}")

    def reset_progress(self):
        """Reset all progress"""
        self.unlocked_levels = 1
        self.level_progress.clear()
        
        for level_num in range(1, MAX_LEVEL + 1):
            self.level_progress[level_num] = {
                'completed': False,
                'best_score': 0,
                'best_moves': None,
                'stars': 0
            }
        
        self._save_progress()

    def get_difficulty_for_game(self, level_num: int) -> Dict:
        """Get difficulty parameters for the game engine"""
        config = self.get_level_config(level_num)
        if not config:
            return {}
        
        return {
            'spawn_weights': config.get_spawn_weights(),
            'max_initial_tiles': config.max_initial_tiles,
            'max_moves': config.max_moves,
            'target_score': config.target_score,
            'allow_high_tiles': config.allow_high_tiles
        }
