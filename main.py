"""
1024 Game - Main Entry Point
Starts the game with the GameLoop
"""

# -*- coding: utf-8 -*-
"""
1024 Game - Main Entry Point
Starts the game with the GameLoop
"""

import sys
import os

# Ensure core module is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

try:
    from core.game_loop import GameLoop
except ImportError as e:
    print("Error importing GameLoop: %s" % e)
    sys.exit(1)


def main():
    """Main function to start the game"""
    try:
        game_loop = GameLoop()
        game_loop.run()
    except KeyboardInterrupt:
        print("\nGame exited by user")
    except Exception as e:
        print("\nError running game: %s" % e)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
