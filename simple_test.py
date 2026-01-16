# -*- coding: utf-8 -*-
import sys
import os
import unittest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test cases that don't require pygame
from core.game_logic import Game
from core.game_logic import GameProgress, Achievement
from core.persistence import PersistenceManager

def test_game_logic():
    """Test core game logic"""
    print("=" * 50)
    print("Testing Game Logic")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    # Test 1: Game initialization
    print("\n1. Testing game initialization...")
    try:
        game = Game(level=1)
        assert game.level == 1
        assert game.grid is not None
        print("   [PASS] Game initialized successfully")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 2b: Debug difficulty calculation
    print("\n2b: Debug difficulty calculation...")
    try:
        game = Game(level=1)
        diff = game._calculate_difficulty(level=1)
        print("   Level 1 diff: %s" % str(diff))
        game2 = Game(level=5)
        diff2 = game2._calculate_difficulty(level=5)
        print("   Level 5 diff: %s" % str(diff2))
        game3 = Game(level=6)
        diff3 = game3._calculate_difficulty(level=6)
        print("   Level 6 diff: %s" % str(diff3))
    except Exception as e:
        print("   [FAIL] Debug failed: %s" % str(e))
    
    # Test 2: Difficulty calculation
    print("\n2. Testing difficulty calculation...")
    try:
        game = Game(level=1)
        diff = game._calculate_difficulty(level=1)
        assert diff['spawn_prob_4'] == 0.1
        assert diff['max_tiles'] == 12
        
        game2 = Game(level=5)
        diff2 = game2._calculate_difficulty(level=5)
        assert diff2['spawn_prob_4'] == 0.1
        assert diff2['max_tiles'] == 12
        
        game3 = Game(level=6)
        diff3 = game3._calculate_difficulty(level=6)
        assert abs(diff3['spawn_prob_4'] - 0.15) < 0.001
        assert diff3['max_tiles'] == 14
        
        print("   [PASS] Difficulty calculation works correctly")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 3: Move operations
    print("\n3. Testing move operations...")
    try:
        game = Game(level=1)
        game.grid = [
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        moved = game.move('left')
        assert moved == False  # No merge
        
        game.grid = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        moved = game.move('left')
        assert moved == True
        assert game.grid[0][0] == 4
        print("   [PASS] Move operations work correctly")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 4: Game over detection
    print("\n4. Testing game over detection...")
    try:
        game = Game(level=1)
        game.grid = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        
        # Check if game detects no moves
        is_over = game.is_game_over()
        assert is_over == True
        print("   [PASS] Game over detection works correctly")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 5: Level target
    print("\n5. Testing level target...")
    try:
        game = Game(level=1)
        target = game.level_target
        assert target == 128
        
        game2 = Game(level=5)
        target2 = game2.level_target
        assert target2 == 128
        
        game3 = Game(level=10)
        target3 = game3.level_target
        assert target3 == 256
        
        print("   [PASS] Level targets are correct")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    return passed, failed

def test_persistence():
    """Test persistence system"""
    print("\n" + "=" * 50)
    print("Testing Persistence")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    # Test 1: Create persistence manager
    print("\n1. Testing persistence manager...")
    try:
        persistence = PersistenceManager()
        assert persistence is not None
        print("   [PASS] Persistence manager created successfully")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 2: Achievement checking
    print("\n2. Testing achievement checking...")
    try:
        persistence = PersistenceManager()
        
        # Test First Game achievement
        stats = {'level': 1, 'score': 0, 'moves': 0, 'time': 0}
        unlocked = persistence.check_achievements(stats)
        # Check if any achievement was unlocked
        assert isinstance(unlocked, list)
        print("   [PASS] Achievement checking works correctly")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    # Test 3: Data classes
    print("\n3. Testing data classes...")
    try:
        progress = GameProgress(
            current_level=1,
            highest_level=1,
            total_score=0,
            total_moves=0,
            games_played=0,
            games_won=0,
            total_time_played=0.0,
            tiles_merged=0,
            max_tile_ever=0,
            achievements=[]
        )
        
        achievement = Achievement(
            id='test',
            name='Test',
            description='Test achievement',
            unlocked=True,
            unlock_date=None,
            icon='',
            progress=100,
            max_progress=100
        )
        
        assert progress.current_level == 1
        assert achievement.unlocked == True
        print("   [PASS] Data classes work correctly")
        passed += 1
    except Exception as e:
        print("   [FAIL] Failed: %s" % str(e))
        failed += 1
    
    return passed, failed

def main():
    print("1024 Game - Test Suite")
    print("=" * 60)
    print("Running core component tests...\n")
    
    # Run tests
    game_passed, game_failed = test_game_logic()
    persistence_passed, persistence_failed = test_persistence()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_passed = game_passed + persistence_passed
    total_failed = game_failed + persistence_failed
    total = total_passed + total_failed
    
    print("\nTotal tests: %d" % total)
    print("Passed: %d" % total_passed)
    print("Failed: %d" % total_failed)
    print("\n" + "=" * 60)
    
    if total_failed == 0:
        print("[RESULT] All tests passed!")
        return 0
    else:
        print("[RESULT] Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
