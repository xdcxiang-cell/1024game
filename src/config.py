import os
import json
from typing import Dict, Any


class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_default_config()
        return cls._instance

    def _load_default_config(self):
        self._config = {
            'display': {
                'width': 800,
                'height': 600,
                'fps': 60,
                'fullscreen': False,
                'vsync': True
            },
            'audio': {
                'enabled': True,
                'volume': 0.7,
                'music_volume': 0.5,
                'sfx_volume': 0.8
            },
            'game': {
                'grid_size': 4,
                'target_score': 1024,
                'max_levels': 20,
                'difficulty_increase_interval': 5
            },
            'theme': {
                'current_theme': 'default',
                'themes': {
                    'default': {
                        'background': (187, 173, 160),
                        'grid': (205, 193, 180),
                        'empty_cell': (238, 228, 218),
                        'text': (119, 110, 101),
                        'tile_colors': {
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
                            2048: (237, 194, 46)
                        }
                    },
                    'dark': {
                        'background': (30, 30, 30),
                        'grid': (50, 50, 50),
                        'empty_cell': (70, 70, 70),
                        'text': (220, 220, 220),
                        'tile_colors': {
                            2: (80, 80, 80),
                            4: (100, 100, 100),
                            8: (150, 100, 50),
                            16: (180, 80, 40),
                            32: (200, 60, 30),
                            64: (220, 40, 20),
                            128: (200, 180, 60),
                            256: (220, 190, 50),
                            512: (240, 200, 40),
                            1024: (255, 210, 30),
                            2048: (255, 220, 20)
                        }
                    }
                }
            },
            'particles': {
                'enabled': True,
                'count': 20,
                'lifetime': 1.0
            },
            'achievements': {
                'first_win': False,
                'score_1000': False,
                'score_5000': False,
                'score_10000': False,
                'level_5': False,
                'level_10': False,
                'level_20': False,
                'perfect_game': False
            }
        }

    def get(self, *keys, default=None):
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys, value):
        config = self._config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value

    def save(self):
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_dir, exist_ok=True)
        config_path = os.path.join(data_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(self._config, f, indent=2)

    def load(self):
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        config_path = os.path.join(data_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                self._config.update(loaded_config)
