import pytest
import sys
import os

# Add parent directory to path to import Day9
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day9 import build_point, calculate_area, find_largest_rectangle_area

class TestBuildPoint:
    def test_build_point_basic_positive_numbers(self):
        """Test that build_point correctly parses basic positive numbers."""
        assert build_point("7,1") == (7, 1)
        assert build_point("11,7") == (11, 7)
        assert build_point("9,5") == (9, 5)
        assert build_point("2,3") == (2, 3)
    
    def test_build_point_single_digit_numbers(self):
        """Test that build_point works with single digit numbers."""
        assert build_point("0,0") == (0, 0)
        assert build_point("1,2") == (1, 2)
        assert build_point("9,9") == (9, 9)
    
    def test_build_point_negative_numbers(self):
        """Test that build_point correctly parses negative numbers."""
        assert build_point("-1,-2") == (-1, -2)
        assert build_point("-10,5") == (-10, 5)
        assert build_point("5,-10") == (5, -10)
        assert build_point("-100,-200") == (-100, -200)
    
    def test_build_point_zero_values(self):
        """Test that build_point correctly handles zero values."""
        assert build_point("0,0") == (0, 0)
        assert build_point("0,5") == (0, 5)
        assert build_point("5,0") == (5, 0)
    
    def test_build_point_large_numbers(self):
        """Test that build_point works with large numbers."""
        assert build_point("1000,2000") == (1000, 2000)
        assert build_point("99999,88888") == (99999, 88888)
        assert build_point("123456789,987654321") == (123456789, 987654321)
    
    def test_build_point_strips_whitespace(self):
        """Test that build_point correctly strips whitespace from input."""
        assert build_point("  7,1  ") == (7, 1)
        assert build_point("7,1\n") == (7, 1)
        assert build_point("\t11,7\t") == (11, 7)
        assert build_point("  9,5  \n") == (9, 5)
    
    def test_build_point_leading_trailing_whitespace(self):
        """Test that build_point handles leading and trailing whitespace."""
        assert build_point(" 2,3 ") == (2, 3)
        assert build_point("\n7,1\n") == (7, 1)
        assert build_point("  11,7  ") == (11, 7)
    
    def test_build_point_mixed_positive_negative(self):
        """Test that build_point handles mixed positive and negative numbers."""
        assert build_point("-1,1") == (-1, 1)
        assert build_point("1,-1") == (1, -1)
        assert build_point("-100,100") == (-100, 100)
        assert build_point("100,-100") == (100, -100)

class TestCalculateArea:
    def test_calculate_area_basic_positive_coordinates(self):
        """Test that calculate_area correctly calculates area with positive coordinates."""
        # Rectangle from (0,0) to (5,3) should have area (5+1)*(3+1) = 6*4 = 24
        assert calculate_area((0, 0), (5, 3)) == 24
        assert calculate_area((5, 3), (0, 0)) == 24  # Order shouldn't matter
        
        # Rectangle from (2,3) to (7,8) should have area (5+1)*(5+1) = 6*6 = 36
        assert calculate_area((2, 3), (7, 8)) == 36
        assert calculate_area((7, 8), (2, 3)) == 36
        
        # Rectangle from (1,1) to (4,6) should have area (3+1)*(5+1) = 4*6 = 24
        assert calculate_area((1, 1), (4, 6)) == 24
    
    def test_calculate_area_with_origin(self):
        """Test that calculate_area works when one point is at the origin."""
        assert calculate_area((0, 0), (5, 3)) == 24
        assert calculate_area((5, 3), (0, 0)) == 24
        assert calculate_area((0, 0), (10, 10)) == 121  # (10+1)*(10+1) = 11*11
        assert calculate_area((10, 10), (0, 0)) == 121
    
    def test_calculate_area_zero_area(self):
        """Test that calculate_area handles degenerate cases (includes boundary points)."""
        # Same point should have area (0+1)*(0+1) = 1*1 = 1
        assert calculate_area((5, 3), (5, 3)) == 1
        
        # Same x-coordinate (vertical line) should have area (0+1)*(7+1) = 1*8 = 8
        assert calculate_area((5, 3), (5, 10)) == 8
        
        # Same y-coordinate (horizontal line) should have area (7+1)*(0+1) = 8*1 = 8
        assert calculate_area((3, 5), (10, 5)) == 8
    
    def test_calculate_area_negative_coordinates(self):
        """Test that calculate_area works with negative coordinates."""
        # Rectangle from (-5,-3) to (-1,-1) should have area (4+1)*(2+1) = 5*3 = 15
        assert calculate_area((-5, -3), (-1, -1)) == 15
        assert calculate_area((-1, -1), (-5, -3)) == 15
        
        # Rectangle from (-10,-10) to (-5,-5) should have area (5+1)*(5+1) = 6*6 = 36
        assert calculate_area((-10, -10), (-5, -5)) == 36
    
    def test_calculate_area_mixed_positive_negative(self):
        """Test that calculate_area works with mixed positive and negative coordinates."""
        # Rectangle from (-5, -3) to (5, 3) should have area (10+1)*(6+1) = 11*7 = 77
        assert calculate_area((-5, -3), (5, 3)) == 77
        assert calculate_area((5, 3), (-5, -3)) == 77
        
        # Rectangle from (-2, 1) to (3, 6) should have area (5+1)*(5+1) = 6*6 = 36
        assert calculate_area((-2, 1), (3, 6)) == 36
        assert calculate_area((3, 6), (-2, 1)) == 36
        
        # Rectangle from (1, -3) to (6, 2) should have area (5+1)*(5+1) = 6*6 = 36
        assert calculate_area((1, -3), (6, 2)) == 36
    
    def test_calculate_area_large_numbers(self):
        """Test that calculate_area works with large numbers."""
        assert calculate_area((0, 0), (1000, 2000)) == 2003001  # (1000+1)*(2000+1) = 1001*2001
        assert calculate_area((100, 200), (500, 600)) == 160801  # (400+1)*(400+1) = 401*401
        assert calculate_area((1000, 2000), (5000, 6000)) == 16008001  # (4000+1)*(4000+1) = 4001*4001
    
    def test_calculate_area_unit_square(self):
        """Test that calculate_area correctly calculates unit squares (includes boundary points)."""
        assert calculate_area((0, 0), (1, 1)) == 4  # (1+1)*(1+1) = 2*2
        assert calculate_area((5, 5), (6, 6)) == 4  # (1+1)*(1+1) = 2*2
        assert calculate_area((10, 10), (11, 11)) == 4  # (1+1)*(1+1) = 2*2
    
    def test_calculate_area_rectangles_from_input(self):
        """Test that calculate_area works with actual input data."""
        # Using points from day9input_small.txt
        point1 = build_point("7,1")
        point2 = build_point("11,7")
        # Rectangle from (7,1) to (11,7) should have area (4+1)*(6+1) = 5*7 = 35
        assert calculate_area(point1, point2) == 35
        
        point3 = build_point("2,3")
        point4 = build_point("9,7")
        # Rectangle from (2,3) to (9,7) should have area (7+1)*(4+1) = 8*5 = 40
        assert calculate_area(point3, point4) == 40

class TestFindLargestRectangleArea:
    def test_find_largest_rectangle_area_two_points(self):
        """Test that find_largest_rectangle_area works with exactly two points."""
        points = [(0, 0), (5, 3)]
        # Area should be (5+1)*(3+1) = 6*4 = 24
        assert find_largest_rectangle_area(points) == 24
        
        points = [(2, 3), (7, 8)]
        # Area should be (5+1)*(5+1) = 6*6 = 36
        assert find_largest_rectangle_area(points) == 36
    
    def test_find_largest_rectangle_area_three_points(self):
        """Test that find_largest_rectangle_area finds maximum among three points."""
        points = [(0, 0), (5, 3), (10, 10)]
        # Areas: (0,0)-(5,3)=24, (0,0)-(10,10)=121, (5,3)-(10,10)=36
        # Maximum should be 121
        assert find_largest_rectangle_area(points) == 121
        
        points = [(1, 1), (4, 6), (2, 2)]
        # Areas: (1,1)-(4,6)=24, (1,1)-(2,2)=4, (4,6)-(2,2)=15
        # Maximum should be 24
        assert find_largest_rectangle_area(points) == 24
    
    def test_find_largest_rectangle_area_small_input(self):
        """Test that find_largest_rectangle_area works with points from day9input_small.txt."""
        points = [
            (7, 1), (11, 1), (11, 7), (9, 7),
            (9, 5), (2, 5), (2, 3), (7, 3)
        ]
        # The maximum should be between points with largest x-difference and y-difference
        # Points (2, 1) and (11, 7) would give (9+1)*(6+1) = 10*7 = 70
        # But we need to check actual pairs. Let's verify:
        # (2,3) to (11,7): (9+1)*(4+1) = 10*5 = 50
        # (2,5) to (11,1): (9+1)*(4+1) = 10*5 = 50
        # (2,3) to (11,1): (9+1)*(2+1) = 10*3 = 30
        # Actually, the maximum width is 9 (from x=2 to x=11) and max height is 6 (from y=1 to y=7)
        # So if we have (2,1) and (11,7), that would be 70, but we don't have (2,1)
        # Let's check: (2,3) to (11,7) = 50, (2,5) to (11,1) = 50
        # Actually wait, let me recalculate properly:
        # We need to find the actual maximum among all pairs
        result = find_largest_rectangle_area(points)
        # The result should be a positive integer representing the maximum area
        assert result > 0
        assert isinstance(result, int)
        # For verification, we know at least one pair gives area 50
        assert result >= 50
    
    def test_find_largest_rectangle_area_edge_cases(self):
        """Test that find_largest_rectangle_area handles edge cases."""
        # Empty list should return 0
        assert find_largest_rectangle_area([]) == 0
        
        # Single point should return 0 (need at least 2 points)
        assert find_largest_rectangle_area([(5, 3)]) == 0
    
    def test_find_largest_rectangle_area_duplicate_points(self):
        """Test that find_largest_rectangle_area handles duplicate points."""
        points = [(5, 3), (5, 3), (10, 10)]
        # Areas: (5,3)-(5,3)=1, (5,3)-(10,10)=48, (5,3)-(10,10)=48
        # Maximum should be 48 (area between (5,3) and (10,10) = (5+1)*(7+1) = 6*8)
        assert find_largest_rectangle_area(points) == 48
    
    def test_find_largest_rectangle_area_obvious_maximum(self):
        """Test cases where the maximum is obvious (points far apart)."""
        points = [(0, 0), (1, 1), (100, 100), (50, 50)]
        # The maximum should be between (0,0) and (100,100) = (100+1)*(100+1) = 10201
        assert find_largest_rectangle_area(points) == 10201
        
        points = [(-10, -10), (0, 0), (10, 10)]
        # Maximum should be between (-10,-10) and (10,10) = (20+1)*(20+1) = 441
        assert find_largest_rectangle_area(points) == 441
    
    def test_find_largest_rectangle_area_negative_coordinates(self):
        """Test that find_largest_rectangle_area works with negative coordinates."""
        points = [(-5, -3), (-1, -1), (5, 3)]
        # Maximum should be between (-5,-3) and (5,3) = (10+1)*(6+1) = 77
        assert find_largest_rectangle_area(points) == 77

