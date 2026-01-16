import math
from typing import List, Dict, Any


class LevelManager:
    def __init__(self):
        self.max_levels = 20
        self.current_level = 1
        self.difficulty_increase_interval = 5
        self.player_stats = {
            'total_games': 0,
            'total_wins': 0,
            'total_score': 0,
            'average_score': 0,
            'win_rate': 0,
            'average_moves': 0,
            'best_score': 0,
            'levels_completed': 0
        }
        self.level_difficulty = self._generate_level_difficulties()

    def _generate_level_difficulties(self) -> List[Dict[str, Any]]:
        difficulties = []
        base_difficulty = 1.0

        for level in range(1, self.max_levels + 1):
            tier = (level - 1) // self.difficulty_increase_interval
            tier_progress = (level - 1) % self.difficulty_increase_interval

            difficulty_multiplier = 1.0 + (tier * 0.3)
            level_difficulty = base_difficulty * difficulty_multiplier

            tier_bonus = 0.1
            level_difficulty += tier_bonus * (tier_progress / self.difficulty_increase_interval)

            target_score = 1024 * (1 + tier * 0.5)

            grid_obstacles = min(tier, 3)
            time_limit = None
            if tier >= 2:
                time_limit = 300 - (tier * 30)

            difficulties.append({
                'level': level,
                'difficulty': round(level_difficulty, 2),
                'target_score': int(target_score),
                'grid_obstacles': grid_obstacles,
                'time_limit': time_limit,
                'tile_spawn_rate': max(0.7, 0.9 - tier * 0.05),
                'four_spawn_rate': max(0.05, 0.1 + tier * 0.02)
            })

        return difficulties

    def get_level_config(self, level: int) -> Dict[str, Any]:
        if 1 <= level <= self.max_levels:
            return self.level_difficulty[level - 1]
        return self.level_difficulty[-1]

    def get_current_level(self) -> int:
        return self.current_level

    def set_level(self, level: int):
        if 1 <= level <= self.max_levels:
            self.current_level = level

    def next_level(self) -> bool:
        if self.current_level < self.max_levels:
            self.current_level += 1
            return True
        return False

    def update_player_stats(self, game_result: Dict[str, Any]):
        self.player_stats['total_games'] += 1
        self.player_stats['total_score'] += game_result.get('score', 0)

        if game_result.get('won', False):
            self.player_stats['total_wins'] += 1
            if game_result.get('level', 0) > self.player_stats['levels_completed']:
                self.player_stats['levels_completed'] = game_result.get('level', 0)

        if game_result.get('score', 0) > self.player_stats['best_score']:
            self.player_stats['best_score'] = game_result.get('score', 0)

        self.player_stats['average_score'] = (
            self.player_stats['total_score'] / self.player_stats['total_games']
        )

        self.player_stats['win_rate'] = (
            self.player_stats['total_wins'] / self.player_stats['total_games']
        )

        total_moves = self.player_stats.get('total_moves', 0) + game_result.get('moves', 0)
        self.player_stats['total_moves'] = total_moves
        self.player_stats['average_moves'] = total_moves / self.player_stats['total_games']

    def calculate_adaptive_difficulty(self) -> float:
        if self.player_stats['total_games'] < 3:
            return 1.0

        win_rate = self.player_stats['win_rate']
        avg_score = self.player_stats['average_score']
        base_difficulty = self.level_difficulty[self.current_level - 1]['difficulty']

        performance_factor = 0.0
        if win_rate > 0.7:
            performance_factor = 0.2
        elif win_rate > 0.5:
            performance_factor = 0.1
        elif win_rate < 0.3:
            performance_factor = -0.1

        score_factor = 0.0
        if avg_score > 2000:
            score_factor = 0.15
        elif avg_score > 1000:
            score_factor = 0.1
        elif avg_score < 500:
            score_factor = -0.1

        adaptive_difficulty = base_difficulty + performance_factor + score_factor
        return max(0.5, min(2.0, adaptive_difficulty))

    def get_unlocked_levels(self) -> int:
        return min(self.player_stats['levels_completed'] + 1, self.max_levels)

    def get_level_progress(self) -> List[Dict[str, Any]]:
        progress = []
        for level in range(1, self.max_levels + 1):
            config = self.get_level_config(level)
            unlocked = level <= self.get_unlocked_levels()
            completed = level <= self.player_stats['levels_completed']

            progress.append({
                'level': level,
                'unlocked': unlocked,
                'completed': completed,
                'difficulty': config['difficulty'],
                'target_score': config['target_score']
            })

        return progress

    def reset_progress(self):
        self.current_level = 1
        self.player_stats = {
            'total_games': 0,
            'total_wins': 0,
            'total_score': 0,
            'average_score': 0,
            'win_rate': 0,
            'average_moves': 0,
            'best_score': 0,
            'levels_completed': 0
        }
