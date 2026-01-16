#!/usr/bin/env python3
"""1024 Game Launcher - Full-featured Pygame version with theme support"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
from src.engine.game_engine import GameEngine
from src.menus.ui_manager import UIManager, UIScreen
from src.utils.save_manager import SaveManager
from src.utils.theme_manager import ThemeManager
from src.utils.tutorial_manager import TutorialManager
from src.game.level_manager import LevelManager
from src.utils.achievement_manager import AchievementManager
from src.engine.constants import *


class GameLauncher:
    """Main game launcher integrating all systems"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("2048 Game - Pygame Edition")
        
        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Initialize managers
        self.save_manager = SaveManager()
        self.theme_manager = ThemeManager()
        self.tutorial_manager = TutorialManager()
        self.level_manager = LevelManager()
        self.achievement_manager = AchievementManager()
        
        # Initialize game engine and UI
        self.game_engine = GameEngine()
        self.ui_manager = UIManager(self.screen)
        
        # Connect managers
        self._connect_managers()
        
        # Load saved theme
        self._load_saved_theme()
        
        # Game state
        self.running = True

    def _connect_managers(self):
        """Connect all managers together"""
        # UI connections
        self.ui_manager.level_manager = self.level_manager
        self.ui_manager.achievement_manager = self.achievement_manager
        self.ui_manager.theme_manager = self.theme_manager
        self.ui_manager.tutorial_manager = self.tutorial_manager
        self.ui_manager.save_manager = self.save_manager
        
        # Set callbacks
        self.ui_manager.on_start_game = self._start_game
        self.ui_manager.on_restart_game = self._restart_game
        self.ui_manager.on_quit = self._quit_game

    def _load_saved_theme(self):
        """Load saved theme from settings"""
        try:
            settings = self.save_manager.load_settings()
            theme_name = settings.get('theme', 'default')
            self.theme_manager.apply_theme(theme_name)
        except Exception as e:
            print(f"Error loading theme: {e}")
            self.theme_manager.apply_theme('default')

    def _start_game(self, level: int):
        """Start a new game"""
        self.game_engine.reset_game(level)

    def _restart_game(self):
        """Restart current game"""
        current_level = self.game_engine.get_level()
        self.game_engine.reset_game(current_level)

    def _quit_game(self):
        """Quit the game"""
        self.running = False

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle keyboard input for game
            if self.ui_manager.current_screen == UIScreen.GAME:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.game_engine.move('up')
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.game_engine.move('down')
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.game_engine.move('left')
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.game_engine.move('right')
                    elif event.key == pygame.K_ESCAPE:
                        self.ui_manager._toggle_pause()
            
            # Handle keyboard for other screens
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go back to main menu
                    if self.ui_manager.current_screen == UIScreen.PAUSE:
                        self.ui_manager._toggle_pause()
                    elif self.ui_manager.current_screen != UIScreen.MAIN_MENU:
                        self.ui_manager._show_main_menu()
            
            # Handle UI events
            self.ui_manager.handle_event(event)

    def update(self):
        """Update game state"""
        if self.ui_manager.current_screen == UIScreen.GAME:
            # Game is active
            pass

    def render(self):
        """Render game and UI"""
        # Clear screen with theme background
        self.screen.fill(pygame.Color(self.theme_manager.get_current_colors()['background']))
        
        if self.ui_manager.current_screen == UIScreen.GAME:
            # Render game grid
            self._render_game()
        
        # Always render UI overlay
        self.ui_manager.render()
        
        pygame.display.flip()

    def _render_game(self):
        """Render the game grid"""
        grid = self.game_engine.get_grid()
        colors = self.theme_manager.get_current_colors()
        
        # Calculate grid position
        grid_x = (SCREEN_WIDTH - GRID_WIDTH) // 2
        grid_y = 100
        
        # Draw grid background
        grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
        grid_surface.fill(pygame.Color(colors['grid']))
        self.screen.blit(grid_surface, (grid_x, grid_y))
        
        # Draw cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell_value = grid[i][j]
                
                # Calculate cell position
                cell_x = grid_x + j * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
                cell_y = grid_y + i * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
                
                # Get cell color
                if cell_value == 0:
                    cell_color = colors['empty']
                else:
                    cell_color = colors.get(f'tile_{cell_value}', colors['tile_default'])
                
                # Draw cell
                cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, pygame.Color(cell_color), cell_rect, border_radius=8)
                
                # Draw number if not empty
                if cell_value != 0:
                    # Determine text color
                    text_color = colors['text_light'] if cell_value <= 4 else colors['text_dark']
                    
                    # Draw text
                    font_size = 36 if cell_value < 100 else 28 if cell_value < 1000 else 22
                    font = pygame.font.Font(None, font_size)
                    text_surface = font.render(str(cell_value), True, pygame.Color(text_color))
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(text_surface, text_rect)
        
        # Draw score
        score = self.game_engine.get_score()
        high_score = self.game_engine.get_high_score()
        level = self.game_engine.get_level()
        
        score_font = pygame.font.Font(None, 32)
        
        score_text = score_font.render(f"Score: {score}", True, pygame.Color(colors['text_dark']))
        self.screen.blit(score_text, (50, 30))
        
        high_score_text = score_font.render(f"High Score: {high_score}", True, pygame.Color(colors['text_dark']))
        self.screen.blit(high_score_text, (50, 65))
        
        level_text = score_font.render(f"Level: {level}", True, pygame.Color(colors['text_dark']))
        self.screen.blit(level_text, (50, 100))
        
        # Draw game over overlay
        if self.game_engine.is_game_over():
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(pygame.Color(colors['background']))
            self.screen.blit(overlay, (0, 0))
            
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, pygame.Color(colors['error']))
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
            
            final_score_font = pygame.font.Font(None, 48)
            final_score_text = final_score_font.render(f"Final Score: {score}", True, pygame.Color(colors['text_dark']))
            self.screen.blit(final_score_text, final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)))
            
            restart_text = score_font.render("Press R to restart or M for menu", True, pygame.Color(colors['text_dark']))
            self.screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)))

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    """Entry point"""
    try:
        launcher = GameLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
