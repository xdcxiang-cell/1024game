# 1024 Game - Pygame Edition

A modern graphical version of the 1024 number sliding game built with Python 3 and Pygame, featuring 20 levels, adaptive difficulty, particle effects, and 3D audio simulation.

## 🎮 Game Features

### Core Gameplay
- 4x4 game grid with smooth tile merging mechanics
- 20 unique levels with increasing difficulty
- Adaptive difficulty algorithm that adjusts to player performance
- Multi-threaded rendering at 60 FPS for smooth gameplay
- Particle effects for merges, spawns, wins, and game over events
- 3D sound simulation for immersive audio experience

### User Interface
- Main menu with game options
- Level selection screen with progress tracking
- Settings interface for customization
- Achievement system with 12 unique achievements
- Game over screen with comprehensive statistics
- Interactive tutorial for new players
- Theme customization with multiple color schemes

### Data Persistence
- Automatic game state saving
- High score tracking
- Achievement progress
- Game history (last 50 games)
- Total play time tracking
- Customizable settings persistence

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Pygame 2.5.0 or higher

### Installation
1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
```bash
python src/main.py
```

## 🎯 Controls

### Game Controls
- **Arrow Keys / WASD**: Move tiles
- **ESC**: Pause game / Return to menu
- **P**: Pause game

### Menu Navigation
- **Mouse Click**: Select options and navigate menus
- **ESC**: Return to previous screen

## 📁 Project Structure

```
1024game/
├── src/
│   ├── main.py              # Main entry point and game loop
│   ├── config.py            # Configuration management
│   ├── game.py              # Core game logic
│   ├── level_manager.py     # Level system and difficulty
│   ├── render_engine.py     # Multi-threaded rendering
│   ├── particle_system.py   # Particle effects
│   ├── audio_engine.py      # 3D sound simulation
│   ├── data_manager.py      # Data persistence
│   ├── font_manager.py     # Font management
│   ├── ui_components.py    # UI elements (buttons, panels, etc.)
│   ├── main_menu.py         # Main menu interface
│   ├── level_select.py      # Level selection screen
│   ├── settings.py          # Settings interface
│   ├── achievements.py      # Achievement system
│   ├── game_screen.py       # Main game screen
│   ├── game_over.py         # Game over statistics
│   └── tutorial.py          # Tutorial system
├── tests/
│   ├── test_game.py         # Game logic tests
│   ├── test_systems.py      # System tests (particles, audio)
│   ├── test_ui.py           # UI component tests
│   ├── test_difficulty.py   # Difficulty algorithm tests
│   ├── test_integration.py  # Integration tests
│   └── test_persistence.py  # Data persistence tests
├── data/                    # Saved game data
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🔧 Features

### Game Mechanics
- ✅ 20 levels with progressive difficulty
- ✅ Adaptive difficulty algorithm based on player performance
- ✅ Smart tile spawning with probability adjustments
- ✅ Grid obstacles at higher levels
- ✅ Time limits for advanced levels
- ✅ Score tracking and high scores
- ✅ Move counter and merge statistics
- ✅ Max tile tracking

### Visual Effects
- ✅ Smooth 60 FPS rendering
- ✅ Multi-threaded rendering engine
- ✅ Particle effects for game events
- ✅ Tile merge animations
- ✅ Spawn animations
- ✅ Win celebration effects
- ✅ Game over effects
- ✅ Multiple theme options

### Audio System
- ✅ 3D sound simulation
- ✅ Position-based audio
- ✅ Volume control
- ✅ Sound effects for all game events
- ✅ UI sound effects
- ✅ Master and SFX volume controls

### User Interface
- ✅ Main menu
- ✅ Level selection with progress tracking
- ✅ Settings customization
- ✅ Achievement system
- ✅ Game statistics
- ✅ Tutorial system
- ✅ Theme customization
- ✅ Responsive UI elements

### Data Management
- ✅ Automatic game state saving
- ✅ High score persistence
- ✅ Achievement progress tracking
- ✅ Game history (last 50 games)
- ✅ Total play time tracking
- ✅ Settings persistence

## 🎯 Level System

### Difficulty Progression
- **Levels 1-5**: Basic gameplay, target score 1024
- **Levels 6-10**: Increased difficulty, target score 2048
- **Levels 11-15**: Advanced obstacles, target score 4096
- **Levels 16-20**: Expert challenges, target score 8192

### Adaptive Difficulty
The game analyzes your performance and adjusts difficulty:
- High win rate increases difficulty
- Low win rate decreases difficulty
- High scores increase difficulty
- Low scores decrease difficulty

### Level Features
- Grid obstacles (levels 6+)
- Time limits (levels 11+)
- Adjusted spawn rates
- Higher 4-tile spawn probability

## 🏆 Achievements

- **First Win**: Win your first game
- **Score 1000**: Reach 1000 points
- **Score 5000**: Reach 5000 points
- **Score 10000**: Reach 10000 points
- **Tile 1024**: Create a 1024 tile
- **Tile 2048**: Create a 2048 tile
- **Tile 4096**: Create a 4096 tile
- **Level 5**: Complete level 5
- **Level 10**: Complete level 10
- **Level 20**: Complete level 20
- **Perfect Game**: Win with no mistakes
- **Speed Demon**: Win quickly

## 🛠️ Development

### Running Tests
Run all tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_game.py
```

Run with coverage:
```bash
pytest --cov=src tests/
```

### Code Quality
- Follows PEP 8 style guidelines
- Comprehensive error handling
- Modular design for maintainability
- Type hints for better code clarity

### Testing Coverage
- Unit tests for game logic
- System tests for rendering and audio
- UI component tests
- Integration tests for complete game flow
- Persistence tests for data management

## 🎨 Themes

The game includes multiple color themes:
- **Classic**: Traditional 1024 color scheme
- **Dark**: Dark mode for low-light environments
- **Light**: Bright, clean interface
- **Retro**: Vintage arcade style
- **Neon**: Modern neon aesthetic

## 🔊 Audio

### Sound Effects
- Tile merge sounds
- Tile spawn sounds
- Move sounds
- Win celebration sounds
- Game over sounds
- UI interaction sounds

### 3D Audio
- Position-based audio simulation
- Stereo panning based on screen position
- Distance-based volume attenuation
- Listener position tracking

## 📊 Statistics

The game tracks comprehensive statistics:
- Total games played
- Total wins and losses
- Win rate
- Total score
- Average score
- Best score
- Total play time
- Average moves per game
- Max tile achieved
- Levels completed

## 🐛 Troubleshooting

**Game won't start?**
- Ensure Python 3.8+ is installed
- Check that Pygame is installed: `pip install pygame`
- Verify all dependencies: `pip install -r requirements.txt`

**Audio not working?**
- Check system audio settings
- Verify audio is enabled in game settings
- Check volume levels in settings

**Performance issues?**
- Reduce particle effects in settings
- Lower resolution in settings
- Close other applications

**Data not saving?**
- Ensure write permissions in the data directory
- Check available disk space
- Verify data directory exists

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify.

## 🎮 Game Screenshots

### Main Menu
```
┌─────────────────────────────────────┐
│           1024 Game                 │
│                                     │
│         [  Play Game  ]             │
│         [  Select Level ]           │
│         [   Settings   ]            │
│         [ Achievements ]            │
│         [   Tutorial   ]            │
│         [    Quit      ]            │
│                                     │
└─────────────────────────────────────┘
```

### Game Screen
```
┌─────────────────────────────────────┐
│  Level: 1    Score: 120    Moves: 5 │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │  2  │ │     │ │     │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │  4  │ │     │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │     │ │  8  │ │     │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │     │ │     │ │     │ │ 16  │     │
│  └─────┘ └─────┘ └─────┘ └─────┘     │
│                                     │
│  Target: 1024   High Score: 156     │
└─────────────────────────────────────┘
```

### Game Over
```
┌─────────────────────────────────────┐
│           Game Over                 │
│                                     │
│  Level: 1                           │
│  Score: 120                         │
│  Moves: 5                           │
│  Merges: 3                          │
│  Max Tile: 16                       │
│  Difficulty: 1.00                   │
│                                     │
│         [  Restart   ]              │
│         [  Main Menu ]              │
│                                     │
└─────────────────────────────────────┘
```

---

Happy gaming! 🎉
