# -*- coding: utf-8 -*-
"""
1024 Game - Main Menu UI
Handles main menu, level selection, settings, and other UI screens
"""

import pygame
import json
import os
from typing import Callable
from .custom_menu import MainMenuScreen, LevelSelectScreen, SettingsScreen, AchievementScreen, TutorialScreen


class MenuConfig:
    def __init__(self, theme='default', font='arial', font_size=30, 
                 bg_color=(187, 173, 160), selected_color=(242, 177, 121),
                 text_color=(119, 110, 101), button_color=(205, 193, 180)):
        self.theme = theme
        self.font = font
        self.font_size = font_size
        self.bg_color = bg_color
        self.selected_color = selected_color
        self.text_color = text_color
        self.button_color = button_color


class MainMenu(MainMenuScreen):
    """Main menu screen - Uses custom menu implementation"""
    
    def __init__(self, screen, on_start_game, 
                 on_level_select, on_settings, 
                 on_achievements, on_tutorial):
        # Use the custom MainMenuScreen implementation
        def on_quit():
            pygame.quit()
            exit()
        
        super().__init__(
            screen,
            on_start=on_start_game,
            on_level_select=on_level_select,
            on_settings=on_settings,
            on_achievements=on_achievements,
            on_tutorial=on_tutorial,
            on_quit=on_quit
        )
    
    def render(self) -> None:
        """Render menu"""
        self.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.running


class LevelSelectMenu(LevelSelectScreen):
    """Level selection screen - Uses custom menu implementation"""
    
    def __init__(self, screen: pygame.Surface, on_level_selected, 
                 on_back, unlocked_levels: int = 1):
        # Use the custom LevelSelectScreen implementation
        super().__init__(
            screen,
            on_select=on_level_selected,
            on_back=on_back,
            unlocked_levels=unlocked_levels
        )
    
    def render(self) -> None:
        """Render menu"""
        self.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.running
    
    def set_unlocked_levels(self, count: int) -> None:
        """Set number of unlocked levels"""
        self.unlocked_levels = count
        self.widgets = []
        self._create_widgets()


class SettingsMenu(SettingsScreen):
    """Settings screen - Uses custom menu implementation"""
    
    def __init__(self, screen: pygame.Surface, on_save, on_back):
        # Load settings first
        settings_path = os.path.join(os.path.dirname(__file__), '../data/settings.json')
        default_settings = {
            'music_volume': 0.5,
            'sound_volume': 0.7,
            'fps_limit': 60,
            'particle_effects': True,
            '3d_sound': True,
            'theme': 'default',
            'show_tutorial': True,
            'auto_save': True
        }
        
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    loaded = json.load(f)
                    settings = {**default_settings, **loaded}
            except:
                settings = default_settings
        else:
            settings = default_settings
        
        # Use the custom SettingsScreen implementation
        def on_save_callback(settings_dict):
            # Save to file
            settings_path = os.path.join(os.path.dirname(__file__), '../data/settings.json')
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                json.dump(settings_dict, f, indent=4)
            self.on_save(settings_dict)
        
        super().__init__(
            screen,
            on_save=on_save_callback,
            on_back=on_back,
            initial_settings=settings
        )
    
    def render(self) -> None:
        """Render menu"""
        self.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.running


class AchievementMenu(AchievementScreen):
    """Achievements screen - Uses custom menu implementation"""
    
    def __init__(self, screen: pygame.Surface, on_back, achievements):
        # Use the custom AchievementScreen implementation
        super().__init__(
            screen,
            on_back=on_back,
            achievements=achievements
        )
    
    def render(self) -> None:
        """Render menu"""
        self.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.running
    
    def update_achievements(self, achievements) -> None:
        """Update achievements display"""
        self.achievements = achievements
        self._create_widgets()


class TutorialMenu(TutorialScreen):
    """Tutorial screen - Uses custom menu implementation"""
    
    def __init__(self, screen: pygame.Surface, on_back):
        # Use the custom TutorialScreen implementation
        super().__init__(
            screen,
            on_back=on_back
        )
    
    def render(self) -> None:
        """Render menu"""
        self.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.running


# Legacy method for backward compatibility
class TutorialMenuLegacy:
    """Legacy tutorial screen - kept for backward compatibility"""
    
    def __init__(self, screen: pygame.Surface, on_back: Callable):
        self.screen = screen
        self.on_back = on_back
        
        self.config = MenuConfig()
        self._create_menu()
        self.is_running = True
    
    def _create_menu(self) -> None:
        """Create tutorial menu"""
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.background_color = self.config.bg_color
        theme.title_background_color = self.config.selected_color
        theme.title_font_color = (255, 255, 255)
        theme.title_font_size = 42
        theme.title_font = pygame_menu.font.FONT_FRANCHISE
        theme.widget_font = pygame_menu.font.FONT_FRANCHISE
        theme.widget_font_size = 24
        theme.widget_font_color = self.config.text_color
        theme.widget_background_color = self.config.button_color
        theme.widget_border_color = self.config.selected_color
        theme.widget_border_width = 2
        theme.widget_padding = 12
        theme.widget_margin = (0, 8)
        
        self.menu = pygame_menu.Menu(
            title='How to Play',
            width=self.screen.get_width(),
            height=self.screen.get_height(),
            theme=theme,
            scrollarea=True,
            mouse_scroll=True
        )
        
        # Tutorial content
        self.menu.add.label('Welcome to 1024 Game!', font_size=36, font_color=(255, 255, 255))
        self.menu.add.vertical_margin(20)
        
        # Game rules
        self.menu.add.label('Game Rules', font_size=32, font_color=(242, 177, 121))
        self.menu.add.vertical_margin(10)
        
        rules = [
            '1. Use arrow keys or WASD to slide tiles',
            '2. When two tiles with the same number touch, they merge into one!',
            '3. Each merge adds to your score',
            '4. The goal is to reach the target number for each level',
            '5. The game ends when no more moves are possible'
        ]
        
        for rule in rules:
            self.menu.add.label(f'  • {rule}', font_size=24)
        
        self.menu.add.vertical_margin(20)
        
        # Controls
        self.menu.add.label('Controls', font_size=32, font_color=(242, 177, 121))
        self.menu.add.vertical_margin(10)
        
        controls = [
            'Arrow Keys / WASD - Move tiles',
            'R - Restart current level',
            'M - Return to main menu',
            'P - Pause game',
            'ESC - Quit game'
        ]
        
        for control in controls:
            self.menu.add.label(f'  {control}', font_size=24)
        
        self.menu.add.vertical_margin(20)
        
        # Tips
        self.menu.add.label('Tips', font_size=32, font_color=(242, 177, 121))
        self.menu.add.vertical_margin(10)
        
        tips = [
            '• Keep your largest tile in a corner',
            '• Try to maintain order in rows/columns',
            '• Plan ahead - think several moves in advance',
            '• Don\'t fixate on high scores - focus on strategy',
            '• Use the undo feature if you make a mistake'
        ]
        
        for tip in tips:
            self.menu.add.label(f'{tip}', font_size=24)
        
        self.menu.add.vertical_margin(30)
        self.menu.add.button('Back to Menu', self._on_back_click, font_size=26, background_color=(143, 240, 164))
    
    def _on_back_click(self) -> None:
        """Handle back button"""
        self.is_running = False
        self.on_back()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame event"""
        self.menu.update([event])
    
    def render(self) -> None:
        """Render menu"""
        self.menu.draw(self.screen)
    
    def is_menu_running(self) -> bool:
        return self.is_running
    
    def reset(self) -> None:
        """Reset menu state"""
        self.is_running = True