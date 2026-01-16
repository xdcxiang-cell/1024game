# -*- coding: utf-8 -*-
"""
1024 Game - Game Screen UI
Handles the main game interface with grid display, score, stats, etc.
"""

import pygame
import math
import sys
from typing import Dict, List, Tuple, Optional, Callable
sys.path.insert(0, sys.path[0])

from core.game_logic import Game
from core.particle_system import ParticleSystem


class Theme:
    def __init__(self, name, bg_color, grid_color, cell_color, 
                 text_colors, tile_colors, accent_color, progress_color):
        self.name = name
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.cell_color = cell_color
        self.text_colors = text_colors
        self.tile_colors = tile_colors
        self.accent_color = accent_color
        self.progress_color = progress_color


class GameScreen:
    """Main game interface"""
    
    THEMES = {
        'default': Theme(
            name='Default',
            bg_color=(187, 173, 160),
            grid_color=(187, 173, 160),
            cell_color=(205, 193, 180),
            text_colors={
                2: (119, 110, 101),
                4: (119, 110, 101),
                8: (255, 245, 238),
                16: (255, 245, 238),
                32: (255, 245, 238),
                64: (255, 245, 238),
                128: (255, 245, 238),
                256: (255, 245, 238),
                512: (255, 245, 238),
                1024: (255, 245, 238),
                2048: (255, 245, 238),
            },
            tile_colors={
                2: (238, 228, 218),
                4: (237, 224, 200),
                8: (242, 177, 121),
                16: (245, 149, 99),
                32: (246, 124, 95),
                64: (246, 94, 59),
                128: (237, 207, 114),
                256: (237, 204, 97),
                512: (237, 200, 80),
                1024: (237, 197, 63),
                2048: (237, 194, 46),
            },
            accent_color=(242, 177, 121),
            progress_color=(143, 240, 160)
        ),
        'dark': Theme(
            name='Dark',
            bg_color=(50, 50, 50),
            grid_color=(60, 60, 60),
            cell_color=(70, 70, 70),
            text_colors={
                2: (200, 200, 200),
                4: (200, 200, 200),
                8: (255, 255, 255),
                16: (255, 255, 255),
                32: (255, 255, 255),
                64: (255, 255, 255),
                128: (255, 255, 255),
                256: (255, 255, 255),
                512: (255, 255, 255),
                1024: (255, 255, 255),
                2048: (255, 255, 255),
            },
            tile_colors={
                2: (80, 80, 80),
                4: (100, 100, 100),
                8: (150, 100, 50),
                16: (180, 80, 50),
                32: (200, 60, 50),
                64: (220, 40, 40),
                128: (180, 140, 60),
                256: (200, 160, 80),
                512: (220, 180, 100),
                1024: (240, 200, 80),
                2048: (255, 220, 60),
            },
            accent_color=(150, 100, 50),
            progress_color=(100, 200, 100)
        ),
        'ocean': Theme(
            name='Ocean',
            bg_color=(135, 206, 235),
            grid_color=(100, 149, 237),
            cell_color=(135, 206, 250),
            text_colors={
                2: (255, 255, 255),
                4: (255, 255, 255),
                8: (255, 255, 255),
                16: (255, 255, 255),
                32: (255, 255, 255),
                64: (255, 255, 255),
                128: (255, 255, 255),
                256: (255, 255, 255),
                512: (255, 255, 255),
                1024: (255, 255, 255),
                2048: (255, 255, 255),
            },
            tile_colors={
                2: (240, 248, 255),
                4: (176, 224, 230),
                8: (100, 149, 237),
                16: (30, 144, 255),
                32: (0, 191, 255),
                64: (0, 128, 128),
                128: (64, 224, 208),
                256: (72, 209, 204),
                512: (175, 238, 238),
                1024: (95, 158, 160),
                2048: (70, 130, 180),
            },
            accent_color=(30, 144, 255),
            progress_color=(100, 200, 100)
        ),
        'sunset': Theme(
            name='Sunset',
            bg_color=(255, 127, 80),
            grid_color=(255, 140, 0),
            cell_color=(255, 165, 0),
            text_colors={
                2: (255, 255, 255),
                4: (255, 255, 255),
                8: (255, 255, 255),
                16: (255, 255, 255),
                32: (255, 255, 255),
                64: (255, 255, 255),
                128: (255, 255, 255),
                256: (255, 255, 255),
                512: (255, 255, 255),
                1024: (255, 255, 255),
                2048: (255, 255, 255),
            },
            tile_colors={
                2: (255, 228, 225),
                4: (255, 192, 203),
                8: (255, 105, 180),
                16: (255, 69, 0),
                32: (255, 0, 0),
                64: (178, 34, 34),
                128: (218, 165, 32),
                256: (255, 215, 0),
                512: (255, 255, 0),
                1024: (255, 255, 200),
                2048: (255, 255, 255),
            },
            accent_color=(255, 105, 180),
            progress_color=(100, 200, 100)
        )
    }
    
    def __init__(self, screen: pygame.Surface, game: Game, 
                 on_back_to_menu: Callable, on_level_complete: Callable,
                 settings: Optional[Dict] = None):
        self.screen = screen
        self.game = game
        self.on_back_to_menu = on_back_to_menu
        self.on_level_complete = on_level_complete
        
        self.settings = settings or {}
        self.theme = self.THEMES.get(settings.get('theme', 'default'), self.THEMES['default'])
        
        self.particle_system = ParticleSystem()
        self.particle_enabled = self.settings.get('particle_effects', True)
        
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.grid_size = 4
        self.cell_size = 100
        self.cell_padding = 10
        self.grid_offset_x = (self.screen.get_width() - (self.cell_size * self.grid_size + self.cell_padding * (self.grid_size - 1))) // 2
        self.grid_offset_y = 150
        
        self.is_paused = False
        self.is_game_over = False
        self.is_level_complete = False
        
        self.animation_timer = 0
        self.merging_cells = []
        self.new_cells = []
        
        self.stats = {
            'total_moves': 0,
            'total_score': 0,
            'best_tile': 0
        }
    
    def set_game(self, game: Game) -> None:
        """Set current game instance"""
        self.game = game
    
    def set_theme(self, theme_name: str) -> None:
        """Set current theme"""
        self.theme = self.THEMES.get(theme_name, self.THEMES['default'])
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle pygame event"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
            elif event.key == pygame.K_r:
                self.game.reset_game()
                self.is_game_over = False
                self.is_level_complete = False
                self.particle_system.clear()
            elif event.key == pygame.K_m:
                self.on_back_to_menu()
            elif event.key == pygame.K_p:
                self.is_paused = not self.is_paused
            elif not self.is_paused and not self.is_game_over and not self.is_level_complete:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    return 'up'
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    return 'down'
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    return 'left'
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    return 'right'
        return None
    
    def move(self, direction: str) -> None:
        """Handle move in given direction"""
        if self.game.move(direction):
            self.stats['total_moves'] += 1
            self.game.add_random_tile()
            
            # Create particle effects
            if self.particle_enabled:
                self.particle_system.create_move_effect(
                    self.screen.get_width() // 2,
                    self.screen.get_height() // 2
                )
            
            # Check game state
            if self.game.is_game_over():
                self.is_game_over = True
            elif self.game.is_level_complete():
                self.is_level_complete = True
                self.on_level_complete(self.game.level)
            
            # Update stats
            self.stats['total_score'] = self.game.score
            self.stats['best_tile'] = max(self.stats['best_tile'], max(max(row) for row in self.game.grid))
    
    def update(self, delta_time: float) -> None:
        """Update game screen"""
        self.game.update_time(delta_time)
        self.particle_system.update(delta_time)
        self.animation_timer += delta_time
    
    def render(self) -> None:
        """Render game screen"""
        # Draw background
        self.screen.fill(self.theme.bg_color)
        
        # Draw header
        self._draw_header()
        
        # Draw grid
        self._draw_grid()
        
        # Draw particles
        if self.particle_enabled:
            self.particle_system.render(self.screen)
        
        # Draw pause overlay
        if self.is_paused:
            self._draw_pause_overlay()
        
        # Draw game over overlay
        if self.is_game_over:
            self._draw_game_over_overlay()
        
        # Draw level complete overlay
        if self.is_level_complete:
            self._draw_level_complete_overlay()
    
    def _draw_header(self) -> None:
        """Draw header with score, level info, etc."""
        # Game title
        title = self.font_large.render('1024 Game', True, (255, 255, 255))
        title_shadow = self.font_large.render('1024 Game', True, (100, 100, 100))
        self.screen.blit(title_shadow, (22, 12))
        self.screen.blit(title, (20, 10))
        
        # Level info
        level_text = f'Level {self.game.level}'
        level_surf = self.font_medium.render(level_text, True, (255, 255, 255))
        level_shadow = self.font_medium.render(level_text, True, (100, 100, 100))
        self.screen.blit(level_shadow, (self.screen.get_width() - level_surf.get_width() - 22, 12))
        self.screen.blit(level_surf, (self.screen.get_width() - level_surf.get_width() - 20, 10))
        
        # Score panel
        score_rect = pygame.Rect(20, 80, 180, 60)
        pygame.draw.rect(self.screen, self.theme.cell_color, score_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme.accent_color, score_rect, 2, border_radius=8)
        
        score_label = self.font_small.render('Score', True, (255, 255, 255))
        score_text = self.font_medium.render(str(int(self.game.score)), True, (255, 255, 255))
        self.screen.blit(score_label, (score_rect.x + 10, score_rect.y + 5))
        self.screen.blit(score_text, (score_rect.x + 10, score_rect.y + 25))
        
        # High score panel
        high_rect = pygame.Rect(220, 80, 180, 60)
        pygame.draw.rect(self.screen, self.theme.cell_color, high_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme.accent_color, high_rect, 2, border_radius=8)
        
        high_label = self.font_small.render('High Score', True, (255, 255, 255))
        high_text = self.font_medium.render(str(int(self.game.high_score)), True, (255, 255, 255))
        self.screen.blit(high_label, (high_rect.x + 10, high_rect.y + 5))
        self.screen.blit(high_text, (high_rect.x + 10, high_rect.y + 25))
        
        # Level progress bar
        progress_rect = pygame.Rect(self.screen.get_width() - 300, 80, 280, 60)
        pygame.draw.rect(self.screen, self.theme.cell_color, progress_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme.accent_color, progress_rect, 2, border_radius=8)
        
        progress = self.game.get_level_progress()
        progress_fill_rect = pygame.Rect(progress_rect.x + 5, progress_rect.y + 5, 
                                        (progress_rect.width - 10) * progress, progress_rect.height - 10)
        pygame.draw.rect(self.screen, self.theme.progress_color, progress_fill_rect, border_radius=5)
        
        target_text = f'Target: {self.game.level_target}'
        target_surf = self.font_tiny.render(target_text, True, (255, 255, 255))
        self.screen.blit(target_surf, (progress_rect.x + 10, progress_rect.y + 5))
        
        progress_text = f'{int(progress * 100)}%'
        progress_surf = self.font_small.render(progress_text, True, (255, 255, 255))
        self.screen.blit(progress_surf, (progress_rect.x + progress_rect.width - progress_surf.get_width() - 10, 
                                        progress_rect.y + 15))
        
        # Stats panel
        stats_rect = pygame.Rect(20, 550, 200, 80)
        pygame.draw.rect(self.screen, self.theme.cell_color, stats_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme.accent_color, stats_rect, 2, border_radius=8)
        
        moves_text = f'Moves: {self.game.moves}'
        moves_surf = self.font_tiny.render(moves_text, True, (255, 255, 255))
        self.screen.blit(moves_surf, (stats_rect.x + 10, stats_rect.y + 10))
        
        time_text = f'Time: {int(self.game.time_elapsed)}s'
        time_surf = self.font_tiny.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surf, (stats_rect.x + 10, stats_rect.y + 35))
        
        best_text = f'Best: {self.stats["best_tile"]}'
        best_surf = self.font_tiny.render(best_text, True, (255, 255, 255))
        self.screen.blit(best_surf, (stats_rect.x + 10, stats_rect.y + 60))
    
    def _draw_grid(self) -> None:
        """Draw game grid"""
        grid = self.game.get_grid()
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = self.grid_offset_x + col * (self.cell_size + self.cell_padding)
                y = self.grid_offset_y + row * (self.cell_size + self.cell_padding)
                
                # Draw cell background
                pygame.draw.rect(self.screen, self.theme.cell_color, 
                               (x, y, self.cell_size, self.cell_size), border_radius=8)
                
                # Draw tile
                value = grid[row][col]
                if value != 0:
                    self._draw_tile(x, y, value)
    
    def _draw_tile(self, x: int, y: int, value: int) -> None:
        """Draw a single tile"""
        # Get tile color
        color = self.theme.tile_colors.get(value, (128, 128, 128))
        text_color = self.theme.text_colors.get(value, (255, 255, 255))
        
        # Draw tile background
        pygame.draw.rect(self.screen, color, 
                       (x, y, self.cell_size, self.cell_size), border_radius=8)
        
        # Add glow effect for high value tiles
        if value >= 128:
            glow_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, 50), 
                           (0, 0, self.cell_size, self.cell_size), border_radius=8)
            self.screen.blit(glow_surface, (x - 2, y - 2))
        
        # Draw tile value
        if value < 100:
            font = self.font_medium
        elif value < 1000:
            font = self.font_small
        else:
            font = self.font_tiny
            
        text = str(value)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
        self.screen.blit(text_surface, text_rect)
        
        # Add animation for new tiles
        if (x, y) in self.new_cells:
            alpha = int(255 * (self.animation_timer / 0.3))
            overlay = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, alpha))
            self.screen.blit(overlay, (x, y))
    
    def _draw_pause_overlay(self) -> None:
        """Draw pause overlay"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        text = 'Paused'
        text_surface = self.font_large.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(text_surface, text_rect)
        
        subtext = 'Press P to resume'
        subtext_surface = self.font_small.render(subtext, True, (200, 200, 200))
        subtext_rect = subtext_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        self.screen.blit(subtext_surface, subtext_rect)
    
    def _draw_game_over_overlay(self) -> None:
        """Draw game over overlay"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        text = 'Game Over!'
        text_surface = self.font_large.render(text, True, (255, 100, 100))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(text_surface, text_rect)
        
        score_text = f'Final Score: {int(self.game.score)}'
        score_surface = self.font_medium.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        self.screen.blit(score_surface, score_rect)
        
        moves_text = f'Total Moves: {self.game.moves}'
        moves_surface = self.font_small.render(moves_text, True, (200, 200, 200))
        moves_rect = moves_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10))
        self.screen.blit(moves_surface, moves_rect)
        
        best_text = f'Best Tile: {self.stats["best_tile"]}'
        best_surface = self.font_small.render(best_text, True, (200, 200, 200))
        best_rect = best_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(best_surface, best_rect)
        
        restart_text = 'Press R to restart'
        restart_surface = self.font_small.render(restart_text, True, (100, 200, 100))
        restart_rect = restart_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 110))
        self.screen.blit(restart_surface, restart_rect)
        
        menu_text = 'Press M to return to menu'
        menu_surface = self.font_small.render(menu_text, True, (200, 200, 200))
        menu_rect = menu_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 150))
        self.screen.blit(menu_surface, menu_rect)
    
    def _draw_level_complete_overlay(self) -> None:
        """Draw level complete overlay"""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        text = 'Level Complete!'
        text_surface = self.font_large.render(text, True, (100, 255, 100))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(text_surface, text_rect)
        
        score_text = f'Score: {int(self.game.score)}'
        score_surface = self.font_medium.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        self.screen.blit(score_surface, score_rect)
        
        moves_text = f'Moves: {self.game.moves}'
        moves_surface = self.font_small.render(moves_text, True, (200, 200, 200))
        moves_rect = moves_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 10))
        self.screen.blit(moves_surface, moves_rect)
        
        time_text = f'Time: {int(self.game.time_elapsed)}s'
        time_surface = self.font_small.render(time_text, True, (200, 200, 200))
        time_rect = time_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(time_surface, time_rect)
        
        next_text = 'Continue to next level...'
        next_surface = self.font_small.render(next_text, True, (100, 200, 100))
        next_rect = next_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 110))
        self.screen.blit(next_surface, next_rect)
    
    def get_stats(self) -> Dict:
        """Get game statistics"""
        return {
            **self.stats,
            **self.game.get_stats()
        }

    def add_merge_effect(self, row: int, col: int, value: int) -> None:
        """Add merge effect at position"""
        if self.particle_enabled:
            x = self.grid_offset_x + col * (self.cell_size + self.cell_padding) + self.cell_size // 2
            y = self.grid_offset_y + row * (self.cell_size + self.cell_padding) + self.cell_size // 2
            self.particle_system.create_merge_effect(x, y, value)