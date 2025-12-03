import pytest
import sys
import os

# Add parent directory to path to import Day2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day3 import part_one, find_battery_output

class TestPartOne:
    # Test the part_one function in this class

    # We expect part_one to return the largest two-digit number that we can possibly
    #  build using digits from the given row, using digits that are not adjacent.
    # But we cannot re-order the digits.
    
    def test_987654321111111_should_be_98(self):
        """The largest two-digit number in 987654321111111 is 98"""
        assert part_one("987654321111111") == 98

    def test_811111111111119_should_be_89(self):
        """The largest two-digit number in 811111111111119 is 89"""
        assert part_one("811111111111119") == 89
    
    def test_234234234234278_should_be_78(self):
        """The largest two-digit number in 234234234234278 is 78"""
        assert part_one("234234234234278") == 78
    
    def test_818181911112111_should_be_92(self):
        """The largest two-digit number in 818181911112111 is 92"""
        assert part_one("818181911112111") == 92

    def test_1119911111_should_be_99(self):
        """The largest two-digit number in 1119911111 is 99"""
        assert part_one("1119911111") == 99
    
    def test_11911911_should_be_99(self):
        """The largest two-digit number in 11911911 is 99"""
        assert part_one("11911911") == 99

class TestFindBatteryOutput:
    # Test the find_battery_output function in this class
    
    def test_987654321111111_should_be_987654321111(self):
        """In 987654321111111, the largest joltage can be found by turning on 
        everything except some 1s at the end to produce 987654321111."""
        assert find_battery_output("987654321111111", 12) == 987654321111
    
    def test_811111111111119_should_be_811111111119(self):
        """In the digit sequence 811111111111119, the largest joltage can be 
        found by turning on everything except some 1s, producing 811111111119."""
        assert find_battery_output("811111111111119", 12) == 811111111119
    
    def test_234234234234278_should_be_434234234278(self):
        """In 234234234234278, the largest joltage can be found by turning on 
        everything except a 2 battery, a 3 battery, and another 2 battery near 
        the start to produce 434234234278."""
        assert find_battery_output("234234234234278", 12) == 434234234278
    
    def test_818181911112111_should_be_888911112111(self):
        """In 818181911112111, the joltage 888911112111 is produced by turning 
        on everything except some 1s near the front."""
        assert find_battery_output("818181911112111", 12) == 888911112111
    
    def test_single_digit_finds_largest(self):
        """With 1 digit, should find the largest single digit in the line."""
        assert find_battery_output("123456789", 1) == 9
        assert find_battery_output("987654321", 1) == 9
        assert find_battery_output("555123", 1) == 5
    
    def test_two_digits_matches_part_one(self):
        """With 2 digits, should match part_one behavior."""
        assert find_battery_output("987654321111111", 2) == 98
        assert find_battery_output("811111111111119", 2) == 89
        assert find_battery_output("234234234234278", 2) == 78
        assert find_battery_output("818181911112111", 2) == 92
    
    def test_three_digits(self):
        """Test finding the largest three-digit number."""
        assert find_battery_output("987654321111111", 3) == 987
        assert find_battery_output("123456789", 3) == 789
        assert find_battery_output("234234234234278", 3) == 478
    
    def test_five_digits(self):
        """Test finding the largest five-digit number."""
        assert find_battery_output("987654321111111", 5) == 98765
        assert find_battery_output("123456789", 5) == 56789
        assert find_battery_output("234234234234278", 5) == 44478
    
    def test_all_digits(self):
        """Test when num_digits equals the length of the line."""
        assert find_battery_output("12345", 5) == 12345
        assert find_battery_output("987654321", 9) == 987654321
    
    def test_short_line(self):
        """Test with a shorter line."""
        assert find_battery_output("1234", 2) == 34
        assert find_battery_output("5678", 3) == 678

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
