#!/usr/bin/env python3
"""Renderer - Handles all drawing operations with 60FPS cap"""

import pygame
from typing import Tuple, List, Optional

from src.engine.constants import *


class Renderer:
    """Main rendering system for the game"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.delta_time = 0
        self.last_frame_time = 0
        
        # Font cache
        self.fonts = {}
        self._init_fonts()
        
        # Background
        self.background_color = pygame.Color(COLORS['background'])
        
        # Animation state
        self.animations = []

    def _init_fonts(self):
        """Initialize font cache"""
        try:
            self.fonts['large'] = pygame.font.Font(None, FONT_SIZES['large'])
            self.fonts['medium'] = pygame.font.Font(None, FONT_SIZES['medium'])
            self.fonts['normal'] = pygame.font.Font(None, FONT_SIZES['normal'])
            self.fonts['small'] = pygame.font.Font(None, FONT_SIZES['small'])
            self.fonts['tiny'] = pygame.font.Font(None, FONT_SIZES['tiny'])
            self.fonts['title'] = pygame.font.Font(None, FONT_SIZES['title'])
            self.fonts['heading'] = pygame.font.Font(None, FONT_SIZES['heading'])
        except Exception as e:
            print(f"Font initialization error: {e}")
            # Fallback to default font
            self.fonts['normal'] = pygame.font.Font(None, 24)

    def begin_frame(self):
        """Begin a new frame"""
        current_time = pygame.time.get_ticks()
        if self.last_frame_time > 0:
            self.delta_time = (current_time - self.last_frame_time) / 1000.0
        self.last_frame_time = current_time
        
        # Clear screen
        self.screen.fill(self.background_color)

    def end_frame(self):
        """End current frame and update display"""
        pygame.display.flip()
        self.clock.tick(FPS)
        self.fps = self.clock.get_fps()
        
        # Update animations
        self._update_animations()

    def _update_animations(self):
        """Update all active animations"""
        self.animations = [anim for anim in self.animations if not anim.update(self.delta_time)]

    def draw_grid(self, grid: List[List[int]], offset_x: int = GRID_OFFSET_X, 
                  offset_y: int = GRID_OFFSET_Y):
        """Draw the game grid"""
        # Draw grid background
        grid_bg_rect = pygame.Rect(
            offset_x - TILE_PADDING,
            offset_y - TILE_PADDING,
            TILE_SIZE * GRID_SIZE + TILE_PADDING * (GRID_SIZE + 1),
            TILE_SIZE * GRID_SIZE + TILE_PADDING * (GRID_SIZE + 1)
        )
        pygame.draw.rect(self.screen, pygame.Color(COLORS['grid']), grid_bg_rect)
        
        # Draw tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = grid[i][j]
                x = offset_x + j * (TILE_SIZE + TILE_PADDING)
                y = offset_y + i * (TILE_SIZE + TILE_PADDING)
                
                if value == 0:
                    self._draw_empty_tile(x, y)
                else:
                    self._draw_tile(value, x, y)

    def _draw_empty_tile(self, x: int, y: int):
        """Draw empty tile"""
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, pygame.Color(COLORS['empty']), rect)

    def _draw_tile(self, value: int, x: int, y: int):
        """Draw tile with value"""
        # Get tile color
        if value in TILE_VALUES:
            bg_color, text_color = TILE_VALUES[value]
        else:
            bg_color = COLORS['tile_super']
            text_color = COLORS['text_light']
        
        # Convert colors
        bg_color = pygame.Color(bg_color)
        if isinstance(text_color, str):
            text_color = pygame.Color(text_color)
        
        # Draw tile background
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=8)
        
        # Draw tile value
        self._draw_tile_text(value, x, y, text_color)

    def _draw_tile_text(self, value: int, x: int, y: int, color: pygame.Color):
        """Draw tile value text"""
        # Determine font size based on value
        if value >= 1000:
            font = self.fonts['medium']
        elif value >= 100:
            font = self.fonts['large']
        else:
            font = self.fonts['title']
        
        # Render text
        text = font.render(str(value), True, color)
        text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.screen.blit(text, text_rect)

    def draw_text(self, text: str, x: int, y: int, font_size: str = 'normal', 
                  color: str = 'text_dark', center: bool = True) -> pygame.Rect:
        """Draw text on screen"""
        font = self.fonts.get(font_size, self.fonts['normal'])
        color = pygame.Color(COLORS[color] if color in COLORS else color)
        
        text_surface = font.render(text, True, color)
        
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_button(self, text: str, x: int, y: int, width: int, height: int, 
                    state: str = 'normal') -> pygame.Rect:
        """Draw button with state"""
        rect = pygame.Rect(x, y, width, height)
        
        # Determine colors based on state
        if state == 'hover':
            bg_color = COLORS['button_hover']
        elif state == 'pressed':
            bg_color = COLORS['button_pressed']
        else:
            bg_color = COLORS['button']
        
        # Draw button
        pygame.draw.rect(self.screen, pygame.Color(bg_color), rect, border_radius=10)
        
        # Draw button text
        self.draw_text(text, x + width // 2, y + height // 2, 'medium', 'text_light')
        
        return rect

    def draw_panel(self, x: int, y: int, width: int, height: int, 
                   title: Optional[str] = None) -> pygame.Rect:
        """Draw panel with optional title"""
        # Panel background
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, pygame.Color(COLORS['empty']), rect, border_radius=15)
        
        # Panel border
        pygame.draw.rect(self.screen, pygame.Color(COLORS['grid']), rect, 3, border_radius=15)
        
        # Draw title
        if title:
            title_rect = self.draw_text(title, x + width // 2, y + 30, 'heading', 'text_dark')
        
        return rect

    def draw_progress_bar(self, x: int, y: int, width: int, height: int, 
                         progress: float, color: str = 'accent'):
        """Draw progress bar"""
        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, pygame.Color(COLORS['empty']), bg_rect, border_radius=5)
        
        # Progress fill
        progress = max(0, min(1, progress))
        fill_width = int(width * progress)
        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, pygame.Color(COLORS[color]), fill_rect, border_radius=5)

    def draw_fps_counter(self, x: int = 10, y: int = 10):
        """Draw FPS counter"""
        fps_text = f"FPS: {int(self.fps)}"
        self.draw_text(fps_text, x, y, 'small', 'text_dark', center=False)

    def draw_score(self, score: int, high_score: int, x: int, y: int):
        """Draw score display"""
        # Score panel
        panel_width = 200
        panel_height = 100
        panel_x = x - panel_width // 2
        
        self.draw_panel(panel_x, y, panel_width, panel_height, "SCORE")
        
        # Current score
        self.draw_text(str(score), x, y + 60, 'title', 'text_dark')
        
        # High score
        hs_text = f"BEST: {high_score}"
        self.draw_text(hs_text, x, y + 95, 'tiny', 'accent')

    def draw_level_info(self, level: int, moves: int, x: int, y: int):
        """Draw level information"""
        level_text = f"LEVEL {level}"
        moves_text = f"MOVES: {moves}"
        
        self.draw_text(level_text, x, y, 'subtitle', 'text_dark')
        self.draw_text(moves_text, x, y + 40, 'small', 'accent')

    def draw_game_over(self, score: int, level: int):
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(pygame.Color(COLORS['background']))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        self.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, 
                      'title', 'danger')
        
        # Final score
        self.draw_text(f"Final Score: {score}", SCREEN_WIDTH // 2, 
                      SCREEN_HEIGHT // 2, 'large', 'text_dark')
        
        # Level reached
        self.draw_text(f"Level Reached: {level}", SCREEN_WIDTH // 2, 
                      SCREEN_HEIGHT // 2 + 50, 'medium', 'accent')

    def draw_win_screen(self, score: int):
        """Draw win screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(pygame.Color(COLORS['background']))
        self.screen.blit(overlay, (0, 0))
        
        # Win text
        self.draw_text("YOU WIN!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, 
                      'title', 'success')
        
        # Score
        self.draw_text(f"Score: {score}", SCREEN_WIDTH // 2, 
                      SCREEN_HEIGHT // 2, 'large', 'text_dark')

    def set_background_color(self, color: str):
        """Set background color"""
        self.background_color = pygame.Color(COLORS.get(color, color))

    def get_delta_time(self) -> float:
        """Get time since last frame in seconds"""
        return self.delta_time

    def get_fps(self) -> float:
        """Get current FPS"""
        return self.fps
