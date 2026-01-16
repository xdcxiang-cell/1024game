import pygame
from typing import List, Optional, Dict, Any
from src.ui_components import Button, Panel, Label
from src.data_manager import DataManager
from src.config import Config


class Achievement:
    def __init__(self, achievement_id: str, name: str, description: str,
                 icon: str = "🏆", condition: Optional[callable] = None):
        self.id = achievement_id
        self.name = name
        self.description = description
        self.icon = icon
        self.condition = condition


class Achievements:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.data_manager = DataManager()
        self.config = Config()

        self.title_font = font_manager.get_font('title', 48)
        self.button_font = font_manager.get_font('button', 24)
        self.label_font = font_manager.get_font('label', 20)

        self.elements = []
        self.achievements = self._create_achievements()
        self.scroll_offset = 0
        self.max_scroll = 0

        self._create_elements()

        self.on_back = None

    def _create_achievements(self) -> List[Achievement]:
        return [
            Achievement("first_win", "First Victory", "Win your first game", "🎉"),
            Achievement("score_1000", "Scorer", "Score 1000 points in one game", "🎯"),
            Achievement("score_5000", "High Scorer", "Score 5000 points in one game", "🏅"),
            Achievement("score_10000", "Master Scorer", "Score 10000 points in one game", "🥇"),
            Achievement("level_5", "Advancer", "Complete level 5", "📈"),
            Achievement("level_10", "Expert", "Complete level 10", "⭐"),
            Achievement("level_20", "Champion", "Complete all 20 levels", "👑"),
            Achievement("perfect_game", "Perfectionist", "Win without any wrong moves", "💎"),
            Achievement("speed_demon", "Speed Demon", "Win a game in under 2 minutes", "⚡"),
            Achievement("marathon", "Marathon", "Play 100 games", "🏃"),
            Achievement("veteran", "Veteran", "Play 500 games", "🎖️"),
            Achievement("collector", "Collector", "Unlock all achievements", "🏆")
        ]

    def _create_elements(self):
        colors = self._get_theme_colors()

        self.back_button = Button(
            20, 20, 100, 40,
            "Back", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_back_click
        )

        self.elements = [self.back_button]
        self._calculate_scroll()

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'text': theme.get('text', (119, 110, 101)),
            'achievement_unlocked': (100, 200, 100),
            'achievement_locked': (100, 100, 100)
        }

    def _calculate_scroll(self):
        achievement_height = 80
        achievement_spacing = 20
        total_height = len(self.achievements) * (achievement_height + achievement_spacing)
        self.max_scroll = max(0, total_height - (self.screen_height - 150))

    def _on_back_click(self):
        if self.on_back:
            self.on_back()

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return True

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 20
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            return True

        return False

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        title_text = "Achievements"
        title_surface = self.title_font.render(title_text, True, colors['text'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 60))
        surface.blit(title_surface, title_rect)

        for element in self.elements:
            element.draw(surface)

        self._draw_achievements(surface)

    def _draw_achievements(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        achievement_height = 80
        achievement_spacing = 20
        start_y = 130 - self.scroll_offset

        unlocked_count = 0

        for i, achievement in enumerate(self.achievements):
            y = start_y + i * (achievement_height + achievement_spacing)

            if y + achievement_height < 0 or y > self.screen_height:
                continue

            unlocked = self.data_manager.is_achievement_unlocked(achievement.id)
            if unlocked:
                unlocked_count += 1

            bg_color = colors['achievement_unlocked'] if unlocked else colors['achievement_locked']
            panel_rect = pygame.Rect(100, y, self.screen_width - 200, achievement_height)

            pygame.draw.rect(surface, bg_color, panel_rect, border_radius=10)
            pygame.draw.rect(surface, (50, 50, 50), panel_rect, 2, border_radius=10)

            icon_text = achievement.icon
            icon_surface = self.title_font.render(icon_text, True, colors['text'])
            surface.blit(icon_surface, (120, y + 20))

            name_surface = self.button_font.render(achievement.name, True, colors['text'])
            surface.blit(name_surface, (180, y + 15))

            desc_surface = self.label_font.render(achievement.description, True, colors['text'])
            surface.blit(desc_surface, (180, y + 45))

            status_text = "✓" if unlocked else "🔒"
            status_surface = self.button_font.render(status_text, True, colors['text'])
            surface.blit(status_surface, (self.screen_width - 150, y + 25))

        total_text = f"Unlocked: {unlocked_count}/{len(self.achievements)}"
        total_surface = self.button_font.render(total_text, True, colors['text'])
        total_rect = total_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 40))
        surface.blit(total_surface, total_rect)

    def check_achievements(self, game_stats: Dict[str, Any]):
        stats = self.data_manager.get_stats()

        if game_stats.get('won', False):
            self.data_manager.unlock_achievement('first_win')

        if game_stats.get('score', 0) >= 1000:
            self.data_manager.unlock_achievement('score_1000')

        if game_stats.get('score', 0) >= 5000:
            self.data_manager.unlock_achievement('score_5000')

        if game_stats.get('score', 0) >= 10000:
            self.data_manager.unlock_achievement('score_10000')

        if game_stats.get('level', 0) >= 5:
            self.data_manager.unlock_achievement('level_5')

        if game_stats.get('level', 0) >= 10:
            self.data_manager.unlock_achievement('level_10')

        if game_stats.get('level', 0) >= 20:
            self.data_manager.unlock_achievement('level_20')

        if stats.get('total_games', 0) >= 100:
            self.data_manager.unlock_achievement('marathon')

        if stats.get('total_games', 0) >= 500:
            self.data_manager.unlock_achievement('veteran')

        total_unlocked = sum(1 for a in self.achievements
                            if self.data_manager.is_achievement_unlocked(a.id))

        if total_unlocked == len(self.achievements):
            self.data_manager.unlock_achievement('collector')
