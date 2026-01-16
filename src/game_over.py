import pygame
from typing import Dict, Any
from src.ui_components import Button, Panel, Label
from src.data_manager import DataManager
from src.config import Config


class GameOver:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.data_manager = DataManager()
        self.config = Config()

        self.title_font = font_manager.get_font('title', 60)
        self.button_font = font_manager.get_font('button', 32)
        self.label_font = font_manager.get_font('label', 24)

        self.elements = []
        self.game_stats = {}

        self._create_elements()

        self.on_restart = None
        self.on_menu = None
        self.on_next_level = None

    def _create_elements(self):
        colors = self._get_theme_colors()

        self.restart_button = Button(
            self.screen_width // 2 - 250, 450, 150, 50,
            "Restart", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_restart_click
        )

        self.menu_button = Button(
            self.screen_width // 2 + 100, 450, 150, 50,
            "Menu", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_menu_click
        )

        self.next_level_button = Button(
            self.screen_width // 2 - 75, 450, 150, 50,
            "Next Level", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_next_level_click
        )

        self.elements = [self.restart_button, self.menu_button, self.next_level_button]

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'text': theme.get('text', (119, 110, 101)),
            'win_color': (100, 200, 100),
            'lose_color': (200, 100, 100)
        }

    def set_game_stats(self, stats: Dict[str, Any]):
        self.game_stats = stats

        won = stats.get('won', False)
        level = stats.get('level', 1)

        if won and level < 20:
            self.restart_button.rect.x = self.screen_width // 2 - 280
            self.menu_button.rect.x = self.screen_width // 2 + 130
            self.next_level_button.set_enabled(True)
        else:
            self.restart_button.rect.x = self.screen_width // 2 - 125
            self.menu_button.rect.x = self.screen_width // 2 + 125
            self.next_level_button.set_enabled(False)

    def _on_restart_click(self):
        if self.on_restart:
            self.on_restart()

    def _on_menu_click(self):
        if self.on_menu:
            self.on_menu()

    def _on_next_level_click(self):
        if self.on_next_level:
            self.on_next_level()

    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        won = self.game_stats.get('won', False)
        title_text = "Victory!" if won else "Game Over"
        title_color = colors['win_color'] if won else colors['lose_color']

        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title_surface, title_rect)

        self._draw_stats(surface)

        for element in self.elements:
            element.draw(surface)

    def _draw_stats(self, surface: pygame.Surface):
        colors = self._get_theme_colors()

        stats = [
            ("Level", self.game_stats.get('level', 1)),
            ("Score", self.game_stats.get('score', 0)),
            ("Moves", self.game_stats.get('moves', 0)),
            ("Merges", self.game_stats.get('merges', 0)),
            ("Max Tile", self.game_stats.get('max_tile', 0)),
            ("Difficulty", f"{self.game_stats.get('difficulty', 1.0):.2f}")
        ]

        start_y = 150
        spacing = 50

        for i, (label, value) in enumerate(stats):
            y = start_y + i * spacing

            label_surface = self.label_font.render(f"{label}:", True, colors['text'])
            surface.blit(label_surface, (200, y))

            value_text = str(value)
            value_surface = self.label_font.render(value_text, True, colors['text'])
            value_rect = value_surface.get_rect(right=self.screen_width - 200, centery=y)
            surface.blit(value_surface, value_rect)

            pygame.draw.line(surface, colors['text'], (200, y + 30), (self.screen_width - 200, y + 30), 1)

        high_score = self.data_manager.get_high_score()
        current_score = self.game_stats.get('score', 0)

        if current_score > high_score:
            self.data_manager.set_high_score(current_score)

            new_high_text = "New High Score!"
            new_high_surface = self.button_font.render(new_high_text, True, (255, 215, 0))
            new_high_rect = new_high_surface.get_rect(center=(self.screen_width // 2, 400))
            surface.blit(new_high_surface, new_high_rect)
