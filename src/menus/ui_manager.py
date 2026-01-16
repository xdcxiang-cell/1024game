#!/usr/bin/env python3
"""UI Manager - Manages all UI screens and menus"""

import pygame
from enum import Enum
from typing import Optional, Callable, Tuple, List

from src.engine.constants import *
from src.engine.renderer import Renderer


class UIScreen(Enum):
    """Available UI screens"""
    MAIN_MENU = "main_menu"
    LEVEL_SELECT = "level_select"
    SETTINGS = "settings"
    ACHIEVEMENTS = "achievements"
    TUTORIAL = "tutorial"
    TUTORIAL_CONTENT = "tutorial_content"
    GAME = "game"
    STATISTICS = "statistics"
    PAUSE = "pause"
    THEME_SELECT = "theme_select"
    THEME_EDIT = "theme_edit"


class Button:
    """Interactive button component"""

    def __init__(self, text: str, x: int, y: int, width: int, height: int,
                callback: Optional[Callable] = None, args: Tuple = ()):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.args = args
        self.hovered = False
        self.pressed = False
        
    def is_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if button is clicked"""
        if self.x <= mouse_pos[0] <= self.x + self.width:
            if self.y <= mouse_pos[1] <= self.y + self.height:
                return True
        return False
        
    def on_click(self):
        """Handle button click"""
        if self.callback:
            self.callback(*self.args)

    def draw(self, renderer: Renderer):
        """Draw button"""
        state = 'normal'
        if self.pressed:
            state = 'pressed'
        elif self.hovered:
            state = 'hover'
        
        renderer.draw_button(self.text, self.x, self.y, self.width, self.height, state)


class UIManager:
    """Manages all UI elements and screens"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.renderer = Renderer(screen)
        self.current_screen = UIScreen.MAIN_MENU
        self.buttons: List[Button] = []
        self.level_select_buttons: List[Button] = []
        
        # Menu state
        self.menu_visible = True
        self.transitioning = False
        
        # Theme and tutorial management
        self.theme_manager = None
        self.tutorial_manager = None
        self.save_manager = None
        self.current_tutorial_id = None
        self.current_chapter_index = 0
        self.current_theme_id = None
        
        # Initialize buttons for each screen
        self._init_buttons()
        
        # Load main menu buttons
        self.set_screen(UIScreen.MAIN_MENU)

    def _init_buttons(self):
        """Initialize all buttons for different screens"""
        # Main menu buttons
        button_width = 250
        button_height = 60
        button_y = SCREEN_HEIGHT // 2 - 100
        
        self.main_menu_buttons = [
            Button("Play", SCREEN_WIDTH // 2 - button_width // 2, button_y,
                  button_width, button_height, self._start_game),
            Button("Level Select", SCREEN_WIDTH // 2 - button_width // 2, button_y + 80,
                  button_width, button_height, self._show_level_select),
            Button("Settings", SCREEN_WIDTH // 2 - button_width // 2, button_y + 160,
                  button_width, button_height, self._show_settings),
            Button("Theme Customizer", SCREEN_WIDTH // 2 - button_width // 2, button_y + 240,
                  button_width, button_height, self._show_theme_select),
            Button("Tutorial", SCREEN_WIDTH // 2 - button_width // 2, button_y + 320,
                  button_width, button_height, self._show_tutorial_select),
            Button("Achievements", SCREEN_WIDTH // 2 - button_width // 2, button_y + 400,
                  button_width, button_height, self._show_achievements),
            Button("Quit", SCREEN_WIDTH // 2 - button_width // 2, button_y + 480,
                  button_width, button_height, self._quit_game)
        ]
        
        # Settings buttons
        button_y = SCREEN_HEIGHT // 2 - 50
        self.settings_buttons = [
            Button("Reset Progress", SCREEN_WIDTH // 2 - button_width // 2, button_y,
                  button_width, button_height, self._reset_progress),
            Button("Back to Menu", SCREEN_WIDTH // 2 - button_width // 2, button_y + 300,
                  button_width, button_height, self._show_main_menu)
        ]
        
        # Game screen buttons
        self.game_buttons = [
            Button("Pause", SCREEN_WIDTH - 120, 30, 100, 40, self._toggle_pause),
            Button("Restart", SCREEN_WIDTH - 120, 80, 100, 40, self._restart_game),
            Button("Menu", SCREEN_WIDTH - 120, 130, 100, 40, self._show_main_menu)
        ]
        
        # Level select buttons
        self.level_select_buttons = self._create_level_buttons()

    def _create_level_buttons(self) -> List[Button]:
        """Create buttons for level select screen"""
        buttons = []
        button_size = 70
        padding = 20
        start_x = SCREEN_WIDTH // 2 - (4 * button_size + 3 * padding) // 2
        start_y = 180
        
        for level in range(1, MAX_LEVEL + 1):
            row = (level - 1) // 4
            col = (level - 1) % 4
            x = start_x + col * (button_size + padding)
            y = start_y + row * (button_size + padding)
            
            button = Button(str(level), x, y, button_size, button_size,
                           self._select_level, (level,))
            buttons.append(button)
        
        return buttons

    # Navigation callbacks
    def _start_game(self):
        self.set_screen(UIScreen.GAME)
        if self.on_start_game:
            self.on_start_game(1)

    def _show_level_select(self):
        self.set_screen(UIScreen.LEVEL_SELECT)

    def _show_settings(self):
        self.set_screen(UIScreen.SETTINGS)

    def _show_achievements(self):
        self.set_screen(UIScreen.ACHIEVEMENTS)

    def _show_tutorial(self):
        self.set_screen(UIScreen.TUTORIAL)

    def _show_tutorial_select(self):
        self.set_screen(UIScreen.TUTORIAL)

    def _show_theme_select(self):
        self.set_screen(UIScreen.THEME_SELECT)

    def _show_main_menu(self):
        self.set_screen(UIScreen.MAIN_MENU)

    def _quit_game(self):
        if self.on_quit:
            self.on_quit()

    def _select_level(self, level: int):
        if self.level_manager and self.level_manager.is_level_unlocked(level):
            self.set_screen(UIScreen.GAME)
            if self.on_start_game:
                self.on_start_game(level)

    def _toggle_pause(self):
        if self.current_screen == UIScreen.GAME:
            self.set_screen(UIScreen.PAUSE)
        elif self.current_screen == UIScreen.PAUSE:
            self.set_screen(UIScreen.GAME)

    def _restart_game(self):
        if self.on_restart_game:
            self.on_restart_game()

    def _reset_progress(self):
        if self.level_manager:
            self.level_manager.reset_progress()

    # Screen management
    def set_screen(self, screen: UIScreen):
        """Set current screen"""
        self.current_screen = screen
        self.buttons = []
        
        # Load buttons for current screen
        if screen == UIScreen.MAIN_MENU:
            self.buttons = self.main_menu_buttons
        elif screen == UIScreen.LEVEL_SELECT:
            self.buttons = self.level_select_buttons
        elif screen == UIScreen.SETTINGS:
            self.buttons = self.settings_buttons
        elif screen == UIScreen.GAME:
            self.buttons = self.game_buttons

    # Input handling
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self._handle_click(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_move(event.pos)
        
        return False

    def _handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle mouse click"""
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.on_click()
                return True
        return False

    def _handle_mouse_move(self, mouse_pos: Tuple[int, int]):
        """Handle mouse movement"""
        for button in self.buttons:
            button.hovered = (button.x <= mouse_pos[0] <= button.x + button.width and
                           button.y <= mouse_pos[1] <= button.y + button.height)

    # Rendering
    def render(self):
        """Render current UI screen"""
        self.renderer.begin_frame()
        
        if self.current_screen == UIScreen.MAIN_MENU:
            self._render_main_menu()
        elif self.current_screen == UIScreen.LEVEL_SELECT:
            self._render_level_select()
        elif self.current_screen == UIScreen.SETTINGS:
            self._render_settings()
        elif self.current_screen == UIScreen.ACHIEVEMENTS:
            self._render_achievements()
        elif self.current_screen == UIScreen.TUTORIAL:
            self._render_tutorial()
        elif self.current_screen == UIScreen.GAME:
            self._render_game_overlay()
        elif self.current_screen == UIScreen.PAUSE:
            self._render_pause_screen()
        
        self.renderer.end_frame()

    def _render_main_menu(self):
        """Render main menu"""
        # Title
        self.renderer.draw_text("2048", SCREEN_WIDTH // 2, 120, 'title', 'text_dark')
        self.renderer.draw_text("PYGAME EDITION", SCREEN_WIDTH // 2, 200, 'subtitle', 'accent')
        
        # Buttons
        for button in self.buttons:
            button.draw(self.renderer)
        
        # Footer
        self.renderer.draw_text("Use Arrow Keys or WASD to move", SCREEN_WIDTH // 2,
                               SCREEN_HEIGHT - 60, 'small', 'text_light')

    def _render_level_select(self):
        """Render level select screen"""
        self.renderer.draw_text("Select Level", SCREEN_WIDTH // 2, 80, 'heading', 'text_dark')
        
        # Level buttons
        for i, button in enumerate(self.level_select_buttons):
            level = i + 1
            
            if self.level_manager:
                if self.level_manager.is_level_unlocked(level):
                    progress = self.level_manager.level_progress.get(level, {})
                    stars = progress.get('stars', 0)
                    
                    # Draw button
                    button.draw(self.renderer)
                    
                    # Draw stars
                    if stars > 0:
                        star_y = button.y + button.height + 5
                        for star in range(stars):
                            star_x = button.x + button.width // 2 - 15 + star * 15
                            self.renderer.draw_text('★', star_x, star_y, 'small', 'warning', False)
                else:
                    # Locked level - gray out
                    self.renderer.draw_text("?", button.x + button.width // 2,
                                           button.y + button.height // 2, 'medium', 'empty')
            else:
                button.draw(self.renderer)
        
        # Back button
        back_button = Button("Back", 50, SCREEN_HEIGHT - 70, 120, 45, self._show_main_menu)
        back_button.draw(self.renderer)

    def _render_settings(self):
        """Render settings screen"""
        self.renderer.draw_text("Settings", SCREEN_WIDTH // 2, 80, 'heading', 'text_dark')
        
        # Settings options
        option_y = SCREEN_HEIGHT // 2 - 100
        
        self.renderer.draw_text("Volume Control:", SCREEN_WIDTH // 2, option_y, 
                               'medium', 'text_dark')
        self.renderer.draw_text("- Master Volume: 70%", SCREEN_WIDTH // 2, option_y + 50,
                               'small', 'text_dark')
        self.renderer.draw_text("- SFX Volume: 80%", SCREEN_WIDTH // 2, option_y + 80,
                               'small', 'text_dark')
        self.renderer.draw_text("- Music Volume: 50%", SCREEN_WIDTH // 2, option_y + 110,
                               'small', 'text_dark')
        
        self.renderer.draw_text("Graphics:", SCREEN_WIDTH // 2, option_y + 180, 
                               'medium', 'text_dark')
        self.renderer.draw_text("- FPS: 60", SCREEN_WIDTH // 2, option_y + 230, 'small', 'text_dark')
        self.renderer.draw_text("- Particle Effects: Enabled", SCREEN_WIDTH // 2, 
                               option_y + 260, 'small', 'text_dark')
        self.renderer.draw_text("- 3D Audio: Enabled", SCREEN_WIDTH // 2, option_y + 290,
                               'small', 'text_dark')
        
        for button in self.buttons:
            button.draw(self.renderer)

    def _render_achievements(self):
        """Render achievements screen"""
        self.renderer.draw_text("Achievements", SCREEN_WIDTH // 2, 80, 'heading', 'text_dark')
        
        y_offset = 180
        if self.achievement_manager:
            achievements = self.achievement_manager.get_all_achievements()
            
            for i, (ach_id, info) in enumerate(ACHIEVEMENTS.items()):
                unlocked = achievements.get(ach_id, {}).get('unlocked', False)
                color = 'success' if unlocked else 'empty'
                
                self.renderer.draw_text(info, SCREEN_WIDTH // 2, y_offset + i * 45,
                                       'medium', color)
        
        back_button = Button("Back", 50, SCREEN_HEIGHT - 70, 120, 45, self._show_main_menu)
        back_button.draw(self.renderer)

    def _render_tutorial(self):
        """Render tutorial selection screen"""
        self.renderer.draw_text("Tutorial Selection", SCREEN_WIDTH // 2, 80, 'heading', 'text_dark')
        
        if self.tutorial_manager:
            tutorials = self.tutorial_manager.get_all_tutorials()
            
            button_width = 300
            button_height = 70
            start_y = 200
            spacing = 90
            
            for i, tutorial in enumerate(tutorials):
                y_pos = start_y + i * spacing
                
                # Draw tutorial button
                button_x = SCREEN_WIDTH // 2 - button_width // 2
                button = Button(f"{tutorial['title']}", button_x, y_pos,
                              button_width, button_height,
                              self._start_tutorial, (tutorial['id'],))
                button.draw(self.renderer)
                
                # Draw tutorial info
                completed = self.tutorial_manager.is_tutorial_completed(tutorial['id'])
                percentage = self.tutorial_manager.get_completion_percentage(tutorial['id'])
                
                status_text = f"{percentage}% Complete" if not completed else "✓ Completed"
                color = 'success' if completed else 'text_dark'
                self.renderer.draw_text(status_text, SCREEN_WIDTH // 2,
                                       y_pos + button_height + 10, 'small', color)
                
                self.renderer.draw_text(f"Difficulty: {tutorial['difficulty']} | {tutorial['estimated_time']}",
                                       SCREEN_WIDTH // 2, y_pos + button_height + 35,
                                       'tiny', 'accent')
        
        back_button = Button("Back", 50, SCREEN_HEIGHT - 70, 120, 45, self._show_main_menu)
        back_button.draw(self.renderer)

    def _start_tutorial(self, tutorial_id: str):
        """Start a specific tutorial"""
        self.current_tutorial_id = tutorial_id
        self.current_chapter_index = 0
        self.set_screen(UIScreen.TUTORIAL_CONTENT)

    def _render_tutorial_content(self):
        """Render tutorial content with chapters"""
        if not self.tutorial_manager or not self.current_tutorial_id:
            self._show_main_menu()
            return
        
        tutorial = self.tutorial_manager.get_tutorial(self.current_tutorial_id)
        chapters = tutorial.get('chapters', [])
        
        if self.current_chapter_index >= len(chapters):
            self._show_tutorial_select()
            return
        
        chapter = chapters[self.current_chapter_index]
        
        # Tutorial header
        self.renderer.draw_text(f"{tutorial['title']}", SCREEN_WIDTH // 2, 50, 'subtitle', 'accent')
        self.renderer.draw_text(f"Chapter {self.current_chapter_index + 1}/{len(chapters)}",
                               SCREEN_WIDTH // 2, 85, 'small', 'text_light')
        
        # Chapter title
        self.renderer.draw_text(chapter['title'], SCREEN_WIDTH // 2, 130, 'heading', 'text_dark')
        
        # Chapter content
        y_offset = 220
        content_lines = chapter['content']
        for line in content_lines:
            if line:  # Skip empty lines
                self.renderer.draw_text(line, SCREEN_WIDTH // 2, y_offset,
                                       'small', 'text_dark')
                y_offset += 35
        
        # Chapter tip
        if chapter.get('tip'):
            y_offset += 20
            tip_box_y = y_offset - 10
            tip_box_height = 60
            
            # Draw tip box
            self.renderer.draw_text("💡 Tip:", SCREEN_WIDTH // 2 - 300, tip_box_y + 20,
                                   'small', 'warning')
            self.renderer.draw_text(chapter['tip'], SCREEN_WIDTH // 2, tip_box_y + 40,
                                   'small', 'text_dark')
        
        # Navigation buttons
        nav_y = SCREEN_HEIGHT - 100
        
        # Previous button
        prev_x = SCREEN_WIDTH // 2 - 180
        prev_button = Button("◀ Previous", prev_x, nav_y, 160, 50, self._prev_chapter)
        if self.current_chapter_index > 0:
            prev_button.draw(self.renderer)
        
        # Mark as completed button
        mark_button = Button("✓ Mark Completed", SCREEN_WIDTH // 2 - 120, nav_y, 240, 50,
                           self._mark_chapter_complete)
        mark_button.draw(self.renderer)
        
        # Next button
        next_x = SCREEN_WIDTH // 2 + 180
        next_button = Button("Next ▶", next_x - 160, nav_y, 160, 50, self._next_chapter)
        if self.current_chapter_index < len(chapters) - 1:
            next_button.draw(self.renderer)
        elif self.current_chapter_index == len(chapters) - 1:
            finish_button = Button("Finish Tutorial", next_x - 160, nav_y, 200, 50,
                                  self._finish_tutorial)
            finish_button.draw(self.renderer)
        
        # Back button
        back_button = Button("Back", 50, 50, 120, 45, self._show_tutorial_select)
        back_button.draw(self.renderer)

    def _prev_chapter(self):
        """Go to previous chapter"""
        if self.current_chapter_index > 0:
            self.current_chapter_index -= 1

    def _next_chapter(self):
        """Go to next chapter"""
        if self.tutorial_manager and self.current_tutorial_id:
            chapters = self.tutorial_manager.get_tutorial_chapters(self.current_tutorial_id)
            if self.current_chapter_index < len(chapters) - 1:
                self.current_chapter_index += 1

    def _mark_chapter_complete(self):
        """Mark current chapter as completed"""
        if self.tutorial_manager and self.current_tutorial_id:
            tutorial = self.tutorial_manager.get_tutorial(self.current_tutorial_id)
            if tutorial:
                chapters = tutorial.get('chapters', [])
                if self.current_chapter_index < len(chapters):
                    chapter = chapters[self.current_chapter_index]
                    self.tutorial_manager.mark_chapter_completed(self.current_tutorial_id,
                                                                 chapter['id'])

    def _finish_tutorial(self):
        """Finish current tutorial"""
        if self.tutorial_manager and self.current_tutorial_id:
            self.tutorial_manager.mark_tutorial_completed(self.current_tutorial_id)
        self._show_tutorial_select()

    def _render_theme_select(self):
        """Render theme selection screen"""
        self.renderer.draw_text("Theme Customizer", SCREEN_WIDTH // 2, 80, 'heading', 'text_dark')
        
        if self.theme_manager:
            theme_names = self.theme_manager.get_theme_names()
            
            # Create theme buttons in grid
            button_width = 200
            button_height = 100
            padding = 30
            cols = 4
            start_x = SCREEN_WIDTH // 2 - (cols * button_width + (cols - 1) * padding) // 2
            start_y = 180
            
            for i, theme_name in enumerate(theme_names):
                row = i // cols
                col = i % cols
                x = start_x + col * (button_width + padding)
                y = start_y + row * (button_height + padding)
                
                # Create theme preview button
                theme = self.theme_manager.get_theme(theme_name)
                button = Button(f"{theme['name']}", x, y, button_width, button_height,
                              self._apply_theme, (theme_name,))
                button.draw(self.renderer)
                
                # Draw theme preview swatch
                preview_colors = self.theme_manager.get_preview_colors(theme_name)
                swatch_y = y + button_height + 10
                swatch_size = 30
                
                # Background swatch
                bg_swatch = pygame.Surface((swatch_size, swatch_size))
                bg_swatch.fill(pygame.Color(preview_colors['background']))
                self.screen.blit(bg_swatch, (x + 20, swatch_y))
                
                # Grid swatch
                grid_swatch = pygame.Surface((swatch_size, swatch_size))
                grid_swatch.fill(pygame.Color(preview_colors['grid']))
                self.screen.blit(grid_swatch, (x + 65, swatch_y))
                
                # Accent swatch
                accent_swatch = pygame.Surface((swatch_size, swatch_size))
                accent_swatch.fill(pygame.Color(preview_colors['accent']))
                self.screen.blit(accent_swatch, (x + 110, swatch_y))
                
                # Text color swatch
                text_swatch = pygame.Surface((swatch_size, swatch_size))
                text_swatch.fill(pygame.Color(preview_colors['text']))
                self.screen.blit(text_swatch, (x + 155, swatch_y))
        
        back_button = Button("Back", 50, SCREEN_HEIGHT - 70, 120, 45, self._show_main_menu)
        back_button.draw(self.renderer)

    def _apply_theme(self, theme_name: str):
        """Apply a theme"""
        if self.theme_manager:
            self.theme_manager.apply_theme(theme_name)
            
            # Save theme to settings
            if self.save_manager:
                settings = self.save_manager.load_settings()
                settings['theme'] = theme_name
                self.save_manager.save_settings(settings)

    def _render_game_overlay(self):
        """Render game overlay buttons"""
        for button in self.buttons:
            button.draw(self.renderer)

    def _render_pause_screen(self):
        """Render pause overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(pygame.Color(COLORS['background']))
        self.screen.blit(overlay, (0, 0))
        
        self.renderer.draw_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                               'title', 'text_dark')
        
        resume_button = Button("Resume", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20,
                              200, 50, self._toggle_pause)
        menu_button = Button("Main Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90,
                            200, 50, self._show_main_menu)
        
        resume_button.draw(self.renderer)
        menu_button.draw(self.renderer)

    # Property setters
    @property
    def level_manager(self):
        return getattr(self, '_level_manager', None)

    @level_manager.setter
    def level_manager(self, value):
        self._level_manager = value

    @property
    def achievement_manager(self):
        return getattr(self, '_achievement_manager', None)

    @achievement_manager.setter
    def achievement_manager(self, value):
        self._achievement_manager = value

    @property
    def tutorial_manager(self):
        return getattr(self, '_tutorial_manager', None)

    @tutorial_manager.setter
    def tutorial_manager(self, value):
        self._tutorial_manager = value

    @property
    def theme_manager(self):
        return getattr(self, '_theme_manager', None)

    @theme_manager.setter
    def theme_manager(self, value):
        self._theme_manager = value

    @property
    def save_manager(self):
        return getattr(self, '_save_manager', None)

    @save_manager.setter
    def save_manager(self, value):
        self._save_manager = value

    @property
    def on_start_game(self):
        return getattr(self, '_on_start_game', None)

    @on_start_game.setter
    def on_start_game(self, callback):
        self._on_start_game = callback

    @property
    def on_restart_game(self):
        return getattr(self, '_on_restart_game', None)

    @on_restart_game.setter
    def on_restart_game(self, callback):
        self._on_restart_game = callback

    @property
    def on_quit(self):
        return getattr(self, '_on_quit', None)

    @on_quit.setter
    def on_quit(self, callback):
        self._on_quit = callback

    @property
    def current_tutorial_id(self):
        return getattr(self, '_current_tutorial_id', None)

    @current_tutorial_id.setter
    def current_tutorial_id(self, value):
        self._current_tutorial_id = value

    @property
    def current_chapter_index(self):
        return getattr(self, '_current_chapter_index', 0)

    @current_chapter_index.setter
    def current_chapter_index(self, value):
        self._current_chapter_index = value

    def get_renderer(self) -> Renderer:
        """Get the renderer instance"""
        return self.renderer
