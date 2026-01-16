import pygame
from typing import Tuple, Optional
from src.game import Game1024
from src.level_manager import LevelManager
from src.particle_system import ParticleSystem
from src.audio_engine import AudioEngine
from src.config import Config
from src.ui_components import Button, Label, Panel


class GameScreen:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.config = Config()

        self.title_font = font_manager.get_font('title', 48)
        self.button_font = font_manager.get_font('button', 28)
        self.label_font = font_manager.get_font('label', 24)

        self.game = None
        self.level_manager = LevelManager()
        self.particle_system = ParticleSystem()
        self.audio_engine = AudioEngine()

        self.grid_size = 4
        self.cell_size = 80
        self.grid_padding = 10
        self.grid_start_x = (screen_width - (self.grid_size * self.cell_size + (self.grid_size - 1) * self.grid_padding)) // 2
        self.grid_start_y = 200

        self.elements = []
        self._create_elements()

        self.on_pause = None
        self.on_game_over = None
        self.on_win = None

    def _create_elements(self):
        colors = self._get_theme_colors()

        self.pause_button = Button(
            20, 20, 100, 40,
            "Pause", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_pause_click
        )

        self.elements = [self.pause_button]

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'grid': theme.get('grid', (205, 193, 180)),
            'empty_cell': theme.get('empty_cell', (238, 228, 218)),
            'text': theme.get('text', (119, 110, 101)),
            'tile_colors': theme.get('tile_colors', {}),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121)
        }

    def start_game(self, level: int):
        level_config = self.level_manager.get_level_config(level)
        adaptive_difficulty = self.level_manager.calculate_adaptive_difficulty()

        self.game = Game1024(level=level, difficulty=adaptive_difficulty)
        self.game.target_score = level_config['target_score']
        self.game.start_time = pygame.time.get_ticks()

    def _on_pause_click(self):
        if self.on_pause:
            self.on_pause()

    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True

        if not self.game or self.game.game_over or self.game.won:
            return False

        if event.type == pygame.KEYDOWN:
            direction = None
            if event.key in [pygame.K_UP, pygame.K_w]:
                direction = 'up'
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                direction = 'down'
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                direction = 'left'
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                direction = 'right'

            if direction:
                if self.game.move(direction):
                    self._on_move(direction)
                return True

        return False

    def _on_move(self, direction: str):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        self.audio_engine.play_move(center_x, center_y)

        if self.game.game_over:
            self.particle_system.emit_game_over(center_x, center_y)
            self.audio_engine.play_game_over(center_x, center_y)
            if self.on_game_over:
                self.on_game_over(self.game.get_stats())
        elif self.game.won:
            self.particle_system.emit_win(center_x, center_y)
            self.audio_engine.play_win(center_x, center_y)
            if self.on_win:
                self.on_win(self.game.get_stats())

    def update(self, dt: float):
        self.particle_system.update(dt)

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        if self.game:
            self._draw_header(surface, colors)
            self._draw_grid(surface, colors)
            self._draw_footer(surface, colors)

        self.particle_system.draw(surface)

        for element in self.elements:
            element.draw(surface)

    def _draw_header(self, surface: pygame.Surface, colors: dict):
        level_text = f"Level {self.game.level}"
        level_surface = self.title_font.render(level_text, True, colors['text'])
        level_rect = level_surface.get_rect(center=(self.screen_width // 2, 60))
        surface.blit(level_surface, level_rect)

        score_text = f"Score: {self.game.score}"
        score_surface = self.button_font.render(score_text, True, colors['text'])
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, 120))
        surface.blit(score_surface, score_rect)

        target_text = f"Target: {self.game.target_score}"
        target_surface = self.label_font.render(target_text, True, colors['text'])
        target_rect = target_surface.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(target_surface, target_rect)

    def _draw_grid(self, surface: pygame.Surface, colors: dict):
        grid_width = self.grid_size * self.cell_size + (self.grid_size - 1) * self.grid_padding
        grid_height = grid_width

        grid_rect = pygame.Rect(
            self.grid_start_x - self.grid_padding,
            self.grid_start_y - self.grid_padding,
            grid_width + 2 * self.grid_padding,
            grid_height + 2 * self.grid_padding
        )

        pygame.draw.rect(surface, colors['grid'], grid_rect, border_radius=10)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x = self.grid_start_x + col * (self.cell_size + self.grid_padding)
                y = self.grid_start_y + row * (self.cell_size + self.grid_padding)

                cell_value = self.game.grid[row][col]

                if cell_value == 0:
                    pygame.draw.rect(surface, colors['empty_cell'],
                                   (x, y, self.cell_size, self.cell_size), border_radius=5)
                else:
                    tile_color = colors['tile_colors'].get(cell_value, (255, 255, 255))
                    pygame.draw.rect(surface, tile_color,
                                   (x, y, self.cell_size, self.cell_size), border_radius=5)

                    font_size = max(16, 40 - len(str(cell_value)) * 2)
                    tile_font = self.font_manager.get_font('label', font_size)

                    text_color = (119, 110, 101) if cell_value <= 4 else (255, 255, 255)
                    text_surface = tile_font.render(str(cell_value), True, text_color)
                    text_rect = text_surface.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    surface.blit(text_surface, text_rect)

    def _draw_footer(self, surface: pygame.Surface, colors: dict):
        moves_text = f"Moves: {self.game.moves}"
        moves_surface = self.label_font.render(moves_text, True, colors['text'])
        surface.blit(moves_surface, (50, self.screen_height - 40))

        max_tile_text = f"Max Tile: {self.game.max_tile}"
        max_tile_surface = self.label_font.render(max_tile_text, True, colors['text'])
        max_tile_rect = max_tile_surface.get_rect(right=self.screen_width - 50, bottom=self.screen_height - 20)
        surface.blit(max_tile_surface, max_tile_rect)

    def get_game_stats(self):
        if self.game:
            return self.game.get_stats()
        return {}
