#!/usr/bin/env python3
"""Game Engine - Handles core game logic with multi-threaded rendering"""

import threading
import queue
import time
import pygame
from typing import Optional, Tuple, List, Dict

from src.engine.constants import *


class GameEngine:
    """Main game engine managing game state and rendering"""

    def __init__(self):
        self.running = False
        self.paused = False
        self.game_over = False
        self.won = False
        self.current_level = 1
        
        # Performance tracking
        self.fps = 0
        self.frame_count = 0
        self.last_fps_update = 0
        
        # Render queue for multi-threading
        self.render_queue = queue.Queue(maxsize=100)
        self.render_thread: Optional[threading.Thread] = None
        
        # Game state
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.high_score = 0
        self.moves = 0
        
        # Difficulty settings
        self.difficulty = 1
        self.difficulty_modifier = 1.0
        
        # Initialize
        self._load_high_score()

    def start(self):
        """Start the game engine"""
        self.running = True
        self.render_thread = threading.Thread(target=self._render_loop, daemon=True)
        self.render_thread.start()

    def stop(self):
        """Stop the game engine"""
        self.running = False
        if self.render_thread:
            self.render_thread.join(timeout=1.0)

    def _render_loop(self):
        """Background rendering loop (multi-threaded)"""
        frame_start = time.time()
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            delta_time = current_time - frame_start
            frame_start = current_time
            
            # FPS cap
            sleep_time = max(0, FRAME_TIME - delta_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            
            # Update FPS counter
            self._update_fps(current_time)
            
            # Process render queue
            try:
                render_task = self.render_queue.get(timeout=0.016)
                render_task()
            except queue.Empty:
                pass

    def _update_fps(self, current_time: float):
        """Update FPS counter"""
        self.frame_count += 1
        if current_time - self.last_fps_update >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_update = current_time

    def enqueue_render(self, render_func):
        """Queue a render task"""
        try:
            self.render_queue.put(render_func, block=False)
        except queue.Full:
            pass

    def reset_game(self, level: int = 1):
        """Reset the game to initial state"""
        self.current_level = level
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.won = False
        
        # Update difficulty based on level
        self._update_difficulty(level)
        
        # Add initial tiles
        self.add_random_tile()
        self.add_random_tile()

    def _update_difficulty(self, level: int):
        """Update difficulty based on level (every 5 levels)"""
        self.difficulty = (level - 1) // DIFFICULTY_THRESHOLD + 1
        self.difficulty_modifier = 1.0 + (self.difficulty - 1) * 0.25
        
        # Adjust difficulty parameters
        # Higher difficulty = more 4s, lower chance of spawning, etc.

    def add_random_tile(self) -> bool:
        """Add a random tile to an empty cell"""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        
        # Difficulty affects tile spawning probability
        if self.difficulty <= 2:
            value = 2 if random.random() < 0.9 else 4
        elif self.difficulty <= 3:
            value = 2 if random.random() < 0.8 else 4
        else:
            value = 2 if random.random() < 0.7 else 4
        
        row, col = random.choice(empty_cells)
        self.grid[row][col] = value
        return True

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get list of empty cell coordinates"""
        empty_cells = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def move(self, direction: str) -> bool:
        """Move tiles in the specified direction"""
        if self.game_over or self.paused:
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
            self.add_random_tile()
            self._check_game_state()
            
            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
        
        return moved

    def _move_left(self) -> bool:
        """Move tiles to the left"""
        moved = False
        for i in range(GRID_SIZE):
            row = self.grid[i][:]
            new_row, row_score = self._merge_row(row)
            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row
            self.score += row_score
        return moved

    def _move_right(self) -> bool:
        """Move tiles to the right"""
        moved = False
        for i in range(GRID_SIZE):
            row = self.grid[i][::-1]
            new_row, row_score = self._merge_row(row)
            new_row = new_row[::-1]
            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row
            self.score += row_score
        return moved

    def _move_up(self) -> bool:
        """Move tiles up"""
        moved = False
        for j in range(GRID_SIZE):
            col = [self.grid[i][j] for i in range(GRID_SIZE)]
            new_col, col_score = self._merge_row(col)
            for i in range(GRID_SIZE):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]
            self.score += col_score
        return moved

    def _move_down(self) -> bool:
        """Move tiles down"""
        moved = False
        for j in range(GRID_SIZE):
            col = [self.grid[i][j] for i in range(GRID_SIZE)][::-1]
            new_col, col_score = self._merge_row(col)
            new_col = new_col[::-1]
            for i in range(GRID_SIZE):
                if new_col[i] != self.grid[i][j]:
                    moved = True
                self.grid[i][j] = new_col[i]
            self.score += col_score
        return moved

    def _merge_row(self, row: List[int]) -> Tuple[List[int], int]:
        """Merge a row and return new row and score"""
        non_zero = [x for x in row if x != 0]
        new_row = [0] * GRID_SIZE
        score = 0
        
        i = 0
        while i < len(non_zero) - 1:
            if non_zero[i] == non_zero[i + 1]:
                merged = non_zero[i] * 2
                new_row[i // 2] = merged
                score += merged
                i += 2
            else:
                new_row[i // 2] = non_zero[i]
                i += 1
        
        if i < len(non_zero):
            new_row[i // 2] = non_zero[i]
        
        return new_row, score

    def _check_game_state(self):
        """Check if game is over or won"""
        # Check win condition
        for row in self.grid:
            if WIN_TILE in row:
                self.won = True
                return
        
        # Check game over
        if not self.get_empty_cells() and not self._can_move():
            self.game_over = True

    def _can_move(self) -> bool:
        """Check if any moves are possible"""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                current = self.grid[i][j]
                if j < GRID_SIZE - 1 and self.grid[i][j + 1] == current:
                    return True
                if i < GRID_SIZE - 1 and self.grid[i + 1][j] == current:
                    return True
        return False

    def next_level(self):
        """Advance to next level"""
        if self.current_level < MAX_LEVEL:
            self.current_level += 1
            self.reset_game(self.current_level)
            return True
        return False

    def _load_high_score(self):
        """Load high score from file"""
        try:
            import os
            high_score_file = os.path.join(SAVES_PATH, 'high_score.txt')
            if os.path.exists(high_score_file):
                with open(high_score_file, 'r') as f:
                    self.high_score = int(f.read().strip())
        except Exception:
            self.high_score = 0

    def _save_high_score(self):
        """Save high score to file"""
        try:
            import os
            os.makedirs(SAVES_PATH, exist_ok=True)
            high_score_file = os.path.join(SAVES_PATH, 'high_score.txt')
            with open(high_score_file, 'w') as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    # Getters
    def get_grid(self) -> List[List[int]]:
        return [row[:] for row in self.grid]
    
    def get_score(self) -> int:
        return self.score
    
    def get_high_score(self) -> int:
        return self.high_score
    
    def get_moves(self) -> int:
        return self.moves
    
    def get_level(self) -> int:
        return self.current_level
    
    def get_difficulty(self) -> int:
        return self.difficulty
    
    def is_game_over(self) -> bool:
        return self.game_over
    
    def is_won(self) -> bool:
        return self.won
    
    def toggle_pause(self):
        self.paused = not self.paused
