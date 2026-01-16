# -*- coding: utf-8 -*-
"""
1024 Game - Core Game Logic
Contains the Game class with all game mechanics
"""

import random
from datetime import datetime

class Achievement:
    def __init__(self, id, name, description, unlocked=False, unlock_date=None, icon='', progress=0, max_progress=1):
        self.id = id
        self.name = name
        self.description = description
        self.unlocked = unlocked
        self.unlock_date = unlock_date
        self.icon = icon
        self.progress = progress
        self.max_progress = max_progress
    
    def unlock(self):
        self.unlocked = True
        self.unlock_date = datetime.now().isoformat()
    
    def update_progress(self, amount):
        self.progress = min(self.progress + amount, self.max_progress)
        if self.progress >= self.max_progress:
            self.unlock()

class GameProgress:
    def __init__(self, current_level=None, highest_level=None, total_score=None, total_moves=None, games_played=None, games_won=None, total_time_played=None, tiles_merged=None, max_tile_ever=None, achievements=None, last_played=None):
        self.current_level = current_level if current_level is not None else 1
        self.highest_level = highest_level if highest_level is not None else 1
        self.total_score = total_score if total_score is not None else 0
        self.total_moves = total_moves if total_moves is not None else 0
        self.games_played = games_played if games_played is not None else 0
        self.games_won = games_won if games_won is not None else 0
        self.total_time_played = total_time_played if total_time_played is not None else 0.0
        self.tiles_merged = tiles_merged if tiles_merged is not None else 0
        self.max_tile_ever = max_tile_ever if max_tile_ever is not None else 0
        self.achievements = achievements if achievements is not None else self._create_default_achievements()
        self.last_played = last_played
    
    def _create_default_achievements(self):
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
            Achievement('no_merge_fail', 'Merge Master', 'Merge 100 tiles in a row', False, None, '🔗', 0, 100)
        ]

class Settings:
    def __init__(self):
        self.theme = 'default'
        self.sound_enabled = True
        self.music_enabled = True
        self.volume = 0.7
        self.show_fps = False
        self.tutorial_completed = False

import os
import json


class GameState:
    def __init__(self, grid, score, high_score, moves, time_elapsed, level):
        self.grid = grid
        self.score = score
        self.high_score = high_score
        self.moves = moves
        self.time_elapsed = time_elapsed
        self.level = level


class Game:
    """Main game class containing all game logic"""

    GRID_SIZE = 4
    WIN_VALUE = 1024

    def __init__(self, level=1):
        """Initialize the game"""
        self.level = level
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.score = 0
        self.high_score = 0
        self.moves = 0
        self.time_elapsed = 0.0
        self.level_target = self._calculate_level_target(level)
        self.difficulty = self._calculate_difficulty(level)
        
        self.load_high_score()
        self.reset_game()

    def _calculate_level_target(self, level):
        """Calculate target value for the level"""
        # Levels 1-5: 128, 6-10: 256, 11-15: 512, 16-20: 1024
        tier = (level - 1) // 5
        return 128 * (2 ** tier)

    def _calculate_difficulty(self, level):
        """Calculate difficulty parameters for the level"""
        difficulty_tier = (level - 1) // 5
        return {
            'spawn_prob_4': 0.1 + difficulty_tier * 0.05,
            'max_tiles': 12 + difficulty_tier * 2,
            'time_limit': 600 - difficulty_tier * 60,
            'merge_bonus': 1.0 + difficulty_tier * 0.2
        }

    def reset_game(self, level=None):
        """Reset the game to initial state"""
        if level is not None:
            self.level = level
            self.level_target = self._calculate_level_target(level)
            self.difficulty = self._calculate_difficulty(level)
        
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.score = 0
        self.moves = 0
        self.time_elapsed = 0.0
        
        # Add initial tiles
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell"""
        empty_cells = self.get_empty_cells()
        
        # Check difficulty limits
        if len(empty_cells) > self.difficulty['max_tiles']:
            return False
        
        if not empty_cells:
            return False

        # Calculate spawn probability based on difficulty
        prob_4 = self.difficulty['spawn_prob_4']
        value = 2 if random.random() < (1 - prob_4) else 4
        row, col = random.choice(empty_cells)
        self.grid[row][col] = value
        return True

    def get_empty_cells(self):
        """Get list of empty cell coordinates"""
        empty_cells = []
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def move(self, direction):
        """Move tiles in the specified direction"""
        if direction not in ['up', 'down', 'left', 'right']:
            return False

        original_grid = [row[:] for row in self.grid]
        moved = False

        if direction == 'left':
            moved = self._move_left()
        elif direction == 'right':
            moved = self._move_right()
        elif direction == 'up':
            moved = self._move_up()
        elif direction == 'down':
            moved = self._move_down()

        if moved:
            self.moves += 1
            
            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score

        return moved

    def _move_left(self):
        """Move tiles to the left"""
        moved = False
        for i in range(self.GRID_SIZE):
            row = self.grid[i][:]
            new_row, row_score = self._merge_row(row)
            self.score += row_score * self.difficulty['merge_bonus']

            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row

        return moved

    def _move_right(self):
        """Move tiles to the right"""
        moved = False
        for i in range(self.GRID_SIZE):
            row = self.grid[i][::-1]
            new_row, row_score = self._merge_row(row)
            self.score += row_score * self.difficulty['merge_bonus']

            new_row = new_row[::-1]
            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row

        return moved

    def _move_up(self):
        """Move tiles up"""
        moved = False
        for j in range(self.GRID_SIZE):
            col = [self.grid[i][j] for i in range(self.GRID_SIZE)]
            new_col, col_score = self._merge_row(col)
            self.score += col_score * self.difficulty['merge_bonus']

            for i in range(self.GRID_SIZE):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]

        return moved

    def _move_down(self):
        """Move tiles down"""
        moved = False
        for j in range(self.GRID_SIZE):
            col = [self.grid[i][j] for i in range(self.GRID_SIZE)][::-1]
            new_col, col_score = self._merge_row(col)
            self.score += col_score * self.difficulty['merge_bonus']

            new_col = new_col[::-1]
            for i in range(self.GRID_SIZE):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]

        return moved

    def _merge_row(self, row):
        """Merge a row and return new row and score gained"""
        non_zero = [x for x in row if x != 0]
        new_row = [0] * self.GRID_SIZE
        score_gained = 0

        i = 0
        while i < len(non_zero) - 1:
            if non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                new_row[i // 2] = merged_value
                score_gained += merged_value
                i += 2
            else:
                new_row[i // 2] = non_zero[i]
                i += 1

        if i < len(non_zero):
            new_row[i // 2] = non_zero[i]

        return new_row, score_gained

    def is_game_over(self):
        """Check if the game is over (no more moves possible)"""
        if self.get_empty_cells():
            return False

        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if self.grid[j][i] == self.grid[j + 1][i]:
                    return False

        return True

    def is_level_complete(self):
        """Check if current level is complete"""
        for row in self.grid:
            if any(cell >= self.level_target for cell in row):
                return True
        return False

    def get_game_state(self):
        """Get current game state"""
        return GameState(
            grid=[row[:] for row in self.grid],
            score=self.score,
            high_score=self.high_score,
            moves=self.moves,
            time_elapsed=self.time_elapsed,
            level=self.level
        )

    def load_high_score(self):
        """Load high score from file"""
        try:
            data_dir = os.path.join(os.path.dirname(__file__), '../data')
            try:
                os.makedirs(data_dir)
            except OSError:
                if not os.path.isdir(data_dir):
                    raise
            high_score_file = os.path.join(data_dir, 'high_score.txt')

            if os.path.exists(high_score_file):
                with open(high_score_file, 'r') as f:
                    self.high_score = int(f.read().strip())
        except (ValueError, IOError):
            self.high_score = 0

    def save_high_score(self):
        """Save high score to file"""
        try:
            data_dir = os.path.join(os.path.dirname(__file__), '../data')
            os.makedirs(data_dir, exist_ok=True)
            high_score_file = os.path.join(data_dir, 'high_score.txt')

            with open(high_score_file, 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            pass

    def get_grid(self):
        """Get current grid state"""
        return [row[:] for row in self.grid]

    def get_score(self):
        """Get current score"""
        return self.score

    def get_high_score(self):
        """Get high score"""
        return self.high_score

    def update_time(self, delta_time):
        """Update elapsed time"""
        self.time_elapsed += delta_time

    def get_level_progress(self):
        """Get progress towards level target"""
        max_cell = max(max(row) for row in self.grid) if self.grid else 0
        return min(1.0, max_cell / self.level_target)

    def get_stats(self):
        """Get game statistics"""
        return {
            'level': self.level,
            'score': self.score,
            'moves': self.moves,
            'time_elapsed': self.time_elapsed,
            'max_tile': max(max(row) for row in self.grid) if self.grid else 0,
            'empty_cells': len(self.get_empty_cells()),
            'level_target': self.level_target
        }
