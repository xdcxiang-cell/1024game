import pygame
import sys
from enum import Enum

from src.config import Config
from src.render_engine import RenderEngine
from src.font_manager import FontManager
from src.data_manager import DataManager
from src.level_manager import LevelManager

from src.main_menu import MainMenu
from src.level_select import LevelSelect
from src.settings import Settings
from src.achievements import Achievements
from src.game_screen import GameScreen
from src.game_over import GameOver
from src.tutorial import Tutorial


class GameState(Enum):
    MENU = "menu"
    LEVEL_SELECT = "level_select"
    SETTINGS = "settings"
    ACHIEVEMENTS = "achievements"
    GAME = "game"
    GAME_OVER = "game_over"
    TUTORIAL = "tutorial"


class GameApp:
    def __init__(self):
        print("Loading config...")
        self.config = Config()
        self.config.load()

        self.width = self.config.get('display', 'width', default=800)
        self.height = self.config.get('display', 'height', default=600)
        self.fps = self.config.get('display', 'fps', default=60)

        print(f"Initializing render engine ({self.width}x{self.height} @ {self.fps} FPS)...")
        self.render_engine = RenderEngine(self.width, self.height, self.fps)
        self.render_engine.initialize()

        print("Initializing font manager...")
        self.font_manager = FontManager()
        print("Initializing data manager...")
        self.data_manager = DataManager()
        print("Initializing level manager...")
        self.level_manager = LevelManager()

        self.current_state = GameState.MENU
        self.screens = {}
        print("Creating screens...")
        self._create_screens()

        self.running = True
        self.clock = pygame.time.Clock()
        print("GameApp initialization complete")

    def _create_screens(self):
        print("Creating MainMenu...")
        self.screens[GameState.MENU] = MainMenu(self.width, self.height, self.font_manager)
        print("Creating LevelSelect...")
        self.screens[GameState.LEVEL_SELECT] = LevelSelect(self.width, self.height, self.font_manager)
        print("Creating Settings...")
        self.screens[GameState.SETTINGS] = Settings(self.width, self.height, self.font_manager)
        print("Creating Achievements...")
        self.screens[GameState.ACHIEVEMENTS] = Achievements(self.width, self.height, self.font_manager)
        print("Creating GameScreen...")
        self.screens[GameState.GAME] = GameScreen(self.width, self.height, self.font_manager)
        print("Creating GameOver...")
        self.screens[GameState.GAME_OVER] = GameOver(self.width, self.height, self.font_manager)
        print("Creating Tutorial...")
        self.screens[GameState.TUTORIAL] = Tutorial(self.width, self.height, self.font_manager)

        print("Setting up callbacks...")
        self._setup_callbacks()
        print("Screens created successfully")

    def _setup_callbacks(self):
        menu = self.screens[GameState.MENU]
        menu.on_play = lambda: self._start_quick_game()
        menu.on_levels = lambda: self._change_state(GameState.LEVEL_SELECT)
        menu.on_settings = lambda: self._change_state(GameState.SETTINGS)
        menu.on_achievements = lambda: self._change_state(GameState.ACHIEVEMENTS)
        menu.on_tutorial = lambda: self._change_state(GameState.TUTORIAL)
        menu.on_quit = self._quit

        level_select = self.screens[GameState.LEVEL_SELECT]
        level_select.on_level_selected = self._start_level_game
        level_select.on_back = lambda: self._change_state(GameState.MENU)

        settings = self.screens[GameState.SETTINGS]
        settings.on_back = lambda: self._change_state(GameState.MENU)

        achievements = self.screens[GameState.ACHIEVEMENTS]
        achievements.on_back = lambda: self._change_state(GameState.MENU)

        game_screen = self.screens[GameState.GAME]
        game_screen.on_pause = lambda: self._change_state(GameState.MENU)
        game_screen.on_game_over = self._handle_game_over
        game_screen.on_win = self._handle_game_win

        game_over = self.screens[GameState.GAME_OVER]
        game_over.on_restart = self._restart_game
        game_over.on_menu = lambda: self._change_state(GameState.MENU)
        game_over.on_next_level = self._next_level

        tutorial = self.screens[GameState.TUTORIAL]
        tutorial.on_back = lambda: self._change_state(GameState.MENU)

    def _start_quick_game(self):
        current_level = self.level_manager.get_current_level()
        self._start_level_game(current_level)

    def _start_level_game(self, level: int):
        self.level_manager.set_level(level)
        self.screens[GameState.GAME].start_game(level)
        self._change_state(GameState.GAME)

    def _restart_game(self):
        current_level = self.level_manager.get_current_level()
        self.screens[GameState.GAME].start_game(current_level)
        self._change_state(GameState.GAME)

    def _next_level(self):
        if self.level_manager.next_level():
            self.screens[GameState.GAME].start_game(self.level_manager.get_current_level())
            self._change_state(GameState.GAME)
        else:
            self._change_state(GameState.MENU)

    def _handle_game_over(self, stats: dict):
        self._save_game_stats(stats, won=False)
        self.screens[GameState.GAME_OVER].set_game_stats(stats)
        self._change_state(GameState.GAME_OVER)

    def _handle_game_win(self, stats: dict):
        self._save_game_stats(stats, won=True)
        self.screens[GameState.GAME_OVER].set_game_stats(stats)
        self._change_state(GameState.GAME_OVER)

    def _save_game_stats(self, stats: dict, won: bool):
        self.data_manager.update_stats(stats)
        self.data_manager.add_game_to_history(stats)

        if won:
            self.data_manager.unlock_achievement('first_win')

        self.screens[GameState.ACHIEVEMENTS].check_achievements(stats)

    def _change_state(self, new_state: GameState):
        self.current_state = new_state

        if new_state == GameState.LEVEL_SELECT:
            self.screens[GameState.LEVEL_SELECT].refresh()

    def _quit(self):
        self.running = False

    def run(self):
        self.render_engine.start()

        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self._handle_events()
            self._update(dt)
            self._render()

        self.render_engine.stop()
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            else:
                current_screen = self.screens.get(self.current_state)
                if current_screen:
                    current_screen.handle_event(event)

    def _update(self, dt: float):
        current_screen = self.screens.get(self.current_state)
        if current_screen and hasattr(current_screen, 'update'):
            current_screen.update(dt)

    def _render(self):
        surface = self.render_engine.get_surface()
        current_screen = self.screens.get(self.current_state)

        if current_screen:
            current_screen.draw(surface)

        self.render_engine.flip()
        self.render_engine.tick()


def main():
    try:
        print("Initializing game...")
        app = GameApp()
        print("Game initialized, starting...")
        app.run()
        print("Game ended normally")
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
