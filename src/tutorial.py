import pygame
from typing import List, Optional
from src.ui_components import Button, Panel, Label
from src.config import Config


class Tutorial:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.config = Config()

        self.title_font = font_manager.get_font('title', 48)
        self.button_font = font_manager.get_font('button', 28)
        self.label_font = font_manager.get_font('label', 22)

        self.elements = []
        self.current_page = 0
        self.pages = self._create_pages()

        self._create_elements()

        self.on_back = None

    def _create_pages(self) -> List[dict]:
        return [
            {
                'title': 'Welcome to 1024 Game!',
                'content': [
                    'Combine tiles with the same number',
                    'to create larger numbers.',
                    '',
                    'Use arrow keys or WASD to move tiles.',
                    '',
                    'Goal: Reach 1024 to win!'
                ]
            },
            {
                'title': 'How to Play',
                'content': [
                    'Press Arrow Keys or WASD to move tiles',
                    '',
                    'When two tiles with the same number',
                    'collide, they merge into one.',
                    '',
                    'Example: 2 + 2 = 4, 4 + 4 = 8, etc.'
                ]
            },
            {
                'title': 'Scoring',
                'content': [
                    'Each merge gives you points',
                    'equal to the new tile value.',
                    '',
                    'Larger merges = more points!',
                    '',
                    'Try to create 1024 for maximum score.'
                ]
            },
            {
                'title': 'Levels & Difficulty',
                'content': [
                    '20 levels with increasing difficulty',
                    '',
                    'Every 5 levels, difficulty increases',
                    '',
                    'Higher levels = higher targets',
                    '',
                    'Adaptive difficulty adjusts to your skill'
                ]
            },
            {
                'title': 'Tips & Tricks',
                'content': [
                    'Plan your moves ahead',
                    '',
                    'Keep high-value tiles in corners',
                    '',
                    'Build up from small numbers',
                    '',
                    'Don\'t fill the board too quickly'
                ]
            },
            {
                'title': 'Ready to Play!',
                'content': [
                    'Good luck and have fun!',
                    '',
                    'Complete all 20 levels',
                    '',
                    'Unlock achievements',
                    '',
                    'Beat your high score!'
                ]
            }
        ]

    def _create_elements(self):
        colors = self._get_theme_colors()

        self.back_button = Button(
            20, 20, 100, 40,
            "Back", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_back_click
        )

        self.prev_button = Button(
            100, self.screen_height - 80, 150, 50,
            "Previous", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_prev_click
        )

        self.next_button = Button(
            self.screen_width - 250, self.screen_height - 80, 150, 50,
            "Next", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_next_click
        )

        self.elements = [self.back_button, self.prev_button, self.next_button]

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'text': theme.get('text', (119, 110, 101))
        }

    def _on_back_click(self):
        if self.on_back:
            self.on_back()

    def _on_prev_click(self):
        if self.current_page > 0:
            self.current_page -= 1

    def _on_next_click(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1

    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._on_prev_click()
                return True
            elif event.key == pygame.K_RIGHT:
                self._on_next_click()
                return True

        return False

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        page = self.pages[self.current_page]

        title_surface = self.title_font.render(page['title'], True, colors['text'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(title_surface, title_rect)

        self._draw_content(surface, page['content'])

        for element in self.elements:
            element.draw(surface)

        self._draw_page_indicator(surface)

    def _draw_content(self, surface: pygame.Surface, content: List[str]):
        colors = self._get_theme_colors()

        start_y = 150
        line_spacing = 40

        for i, line in enumerate(content):
            y = start_y + i * line_spacing

            line_surface = self.label_font.render(line, True, colors['text'])
            line_rect = line_surface.get_rect(center=(self.screen_width // 2, y))
            surface.blit(line_surface, line_rect)

    def _draw_page_indicator(self, surface: pygame.Surface):
        colors = self._get_theme_colors()

        page_text = f"Page {self.current_page + 1} / {len(self.pages)}"
        page_surface = self.button_font.render(page_text, True, colors['text'])
        page_rect = page_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 55))
        surface.blit(page_surface, page_rect)

        dot_spacing = 15
        dots_start_x = self.screen_width // 2 - (len(self.pages) - 1) * dot_spacing // 2
        dots_y = self.screen_height - 30

        for i in range(len(self.pages)):
            x = dots_start_x + i * dot_spacing
            radius = 5 if i == self.current_page else 3
            color = colors['text'] if i == self.current_page else (150, 150, 150)
            pygame.draw.circle(surface, color, (x, dots_y), radius)
