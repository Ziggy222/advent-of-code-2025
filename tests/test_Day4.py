import pytest
import sys
import os

# Add parent directory to path to import Day2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day4 import build_grid, count_surrounding_objects, get_total_count_below_limit

class TestGridBuild:
   def test_grid_build(self):
      "Build a grid from input file"
      with open("inputs/day4input_small.txt", "r") as file:
         grid = build_grid(file)
         assert grid == [['.','.','@','@','.','@','@','@','@','.'],
                         ['@','@','@','.','@','.','@','.','@','@'],
                         ['@','@','@','@','@','.','@','.','@','@'],
                         ['@','.','@','@','@','@','.','.','@','.'],
                         ['@','@','.','@','@','@','@','.','@','@'],
                         ['.','@','@','@','@','@','@','@','.','@'],
                         ['.','@','.','@','.','@','.','@','@','@'],
                         ['@','.','@','@','@','.','@','@','@','@'],
                         ['.','@','@','@','@','@','@','@','@','.'],
                         ['@','.','@','.','@','@','@','.','@','.']]

class TestCountSurroundingObjects:
   def test_count_surrounding_objects(self):
        "Count the surrounding objects for a given position in the grid"
        with open("inputs/day4input_small.txt", "r") as file:
            grid = build_grid(file)
            assert count_surrounding_objects(grid, 0, 0) == 2
            assert count_surrounding_objects(grid, 0, 1) == 3
            assert count_surrounding_objects(grid, 0, 2) == 4
            assert count_surrounding_objects(grid, 4, 4) == 8
            assert count_surrounding_objects(grid, 9, 9) == 2
            assert count_surrounding_objects(grid, 9, 8) == 4
            assert count_surrounding_objects(grid, 9, 7) == 4
            assert count_surrounding_objects(grid, 9, 6) == 4
            assert count_surrounding_objects(grid, 9, 5) == 4
            assert count_surrounding_objects(grid, 9, 4) == 3
            assert count_surrounding_objects(grid, 9, 3) == 5
            assert count_surrounding_objects(grid, 9, 2) == 4
            assert count_surrounding_objects(grid, 9, 1) == 4
            assert count_surrounding_objects(grid, 9, 0) == 3

class TestGetTotalCountBelowLimit:
    def test_get_total_count_below_limit(self):
        "Test get_total_count_below_limit with different limits"
        with open("inputs/day4input_small.txt", "r") as file:
            grid = build_grid(file)
            # Limit 3: objects with 3 or fewer surrounding objects
            assert get_total_count_below_limit(grid, 3) == 13
            # Limit 2: objects with 2 or fewer surrounding objects
            assert get_total_count_below_limit(grid, 2) == 4
            # Limit 4: objects with 4 or fewer surrounding objects
            assert get_total_count_below_limit(grid, 4) == 30
            # Limit 5: objects with 5 or fewer surrounding objects
            assert get_total_count_below_limit(grid, 5) == 41
            # Limit 0: objects with 0 surrounding objects
            assert get_total_count_below_limit(grid, 0) == 0
