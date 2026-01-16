import pygame
from typing import List, Optional
from src.ui_components import Button, Panel, Label
from src.config import Config
from src.data_manager import DataManager


class MainMenu:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.config = Config()
        self.data_manager = DataManager()

        self.title_font = font_manager.get_font('title', 60)
        self.button_font = font_manager.get_font('button', 32)

        self.elements = []
        self._create_elements()

        self.on_play = None
        self.on_levels = None
        self.on_settings = None
        self.on_achievements = None
        self.on_tutorial = None
        self.on_quit = None

    def _create_elements(self):
        center_x = self.screen_width // 2
        start_y = 200
        button_spacing = 70
        button_width = 250
        button_height = 50

        colors = self._get_theme_colors()

        self.play_button = Button(
            center_x - button_width // 2, start_y,
            button_width, button_height,
            "Play", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_play_click
        )

        self.levels_button = Button(
            center_x - button_width // 2, start_y + button_spacing,
            button_width, button_height,
            "Levels", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_levels_click
        )

        self.settings_button = Button(
            center_x - button_width // 2, start_y + button_spacing * 2,
            button_width, button_height,
            "Settings", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_settings_click
        )

        self.achievements_button = Button(
            center_x - button_width // 2, start_y + button_spacing * 3,
            button_width, button_height,
            "Achievements", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_achievements_click
        )

        self.tutorial_button = Button(
            center_x - button_width // 2, start_y + button_spacing * 4,
            button_width, button_height,
            "Tutorial", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_tutorial_click
        )

        self.quit_button = Button(
            center_x - button_width // 2, start_y + button_spacing * 5,
            button_width, button_height,
            "Quit", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_quit_click
        )

        self.elements = [
            self.play_button,
            self.levels_button,
            self.settings_button,
            self.achievements_button,
            self.tutorial_button,
            self.quit_button
        ]

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'text': theme.get('text', (119, 110, 101))
        }

    def _on_play_click(self):
        if self.on_play:
            self.on_play()

    def _on_levels_click(self):
        if self.on_levels:
            self.on_levels()

    def _on_settings_click(self):
        if self.on_settings:
            self.on_settings()

    def _on_achievements_click(self):
        if self.on_achievements:
            self.on_achievements()

    def _on_tutorial_click(self):
        if self.on_tutorial:
            self.on_tutorial()

    def _on_quit_click(self):
        if self.on_quit:
            self.on_quit()

    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        title_text = "1024 Game"
        title_surface = self.title_font.render(title_text, True, colors['text'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 100))
        surface.blit(title_surface, title_rect)

        stats = self.data_manager.get_stats()
        high_score = stats.get('high_score', 0)
        games_played = stats.get('total_games', 0)

        stats_text = f"High Score: {high_score} | Games: {games_played}"
        stats_surface = self.button_font.render(stats_text, True, colors['text'])
        stats_rect = stats_surface.get_rect(center=(self.screen_width // 2, 160))
        surface.blit(stats_surface, stats_rect)

        for element in self.elements:
            element.draw(surface)
