import pytest
import sys
import os

# Add parent directory to path to import Day5
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day5 import Range, parse_range, read_ranges, read_numbers, is_number_in_any_range, count_unique_numbers_in_ranges

class TestRange:
    def test_range_creation(self):
        """Test creating a Range object with min and max values."""
        r = Range(3, 5)
        assert r.min == 3
        assert r.max == 5
    
    def test_range_contains_within_range(self):
        """Test contains method with numbers within the range."""
        r = Range(3, 5)
        assert r.contains(3) == True
        assert r.contains(4) == True
        assert r.contains(5) == True
    
    def test_range_contains_below_range(self):
        """Test contains method with numbers below the range."""
        r = Range(3, 5)
        assert r.contains(2) == False
        assert r.contains(1) == False
        assert r.contains(0) == False
    
    def test_range_contains_above_range(self):
        """Test contains method with numbers above the range."""
        r = Range(3, 5)
        assert r.contains(6) == False
        assert r.contains(10) == False
    
    def test_range_contains_single_value_range(self):
        """Test contains method with a range that has min == max."""
        r = Range(5, 5)
        assert r.contains(5) == True
        assert r.contains(4) == False
        assert r.contains(6) == False
    
    def test_range_contains_large_numbers(self):
        """Test contains method with large numbers."""
        r = Range(100, 200)
        assert r.contains(150) == True
        assert r.contains(100) == True
        assert r.contains(200) == True
        assert r.contains(99) == False
        assert r.contains(201) == False
    
    def test_range_size_basic(self):
        """Test size method with basic ranges."""
        r = Range(3, 5)
        assert r.size() == 3  # 3, 4, 5
    
    def test_range_size_example_10_14(self):
        """Test size method with the example 10-14."""
        r = Range(10, 14)
        assert r.size() == 5  # 10, 11, 12, 13, 14
    
    def test_range_size_single_value(self):
        """Test size method with a single-value range."""
        r = Range(5, 5)
        assert r.size() == 1  # Just 5
    
    def test_range_size_large_range(self):
        """Test size method with a large range."""
        r = Range(100, 200)
        assert r.size() == 101  # 100 to 200 inclusive
    
    def test_range_size_small_range(self):
        """Test size method with a small range."""
        r = Range(1, 2)
        assert r.size() == 2  # 1, 2
    
    def test_range_size_zero_based(self):
        """Test size method with zero-based range."""
        r = Range(0, 10)
        assert r.size() == 11  # 0 to 10 inclusive
    
    def test_range_size_16_20(self):
        """Test size method with range 16-20."""
        r = Range(16, 20)
        assert r.size() == 5  # 16, 17, 18, 19, 20
    
    def test_range_size_12_18(self):
        """Test size method with range 12-18."""
        r = Range(12, 18)
        assert r.size() == 7  # 12, 13, 14, 15, 16, 17, 18

class TestParseRange:
    def test_parse_range_basic(self):
        """Test parsing a basic range string."""
        r = parse_range("3-5")
        assert r.min == 3
        assert r.max == 5
    
    def test_parse_range_with_whitespace(self):
        """Test parsing a range string with whitespace."""
        r = parse_range("  10-14  ")
        assert r.min == 10
        assert r.max == 14
    
    def test_parse_range_single_value(self):
        """Test parsing a range where min equals max."""
        r = parse_range("5-5")
        assert r.min == 5
        assert r.max == 5
    
    def test_parse_range_large_numbers(self):
        """Test parsing ranges with large numbers."""
        r = parse_range("273755558074677-273755558074677")
        assert r.min == 273755558074677
        assert r.max == 273755558074677
    
    def test_parse_range_invalid_format(self):
        """Test parsing an invalid range format raises an error."""
        with pytest.raises(ValueError):
            parse_range("3")
        with pytest.raises(ValueError):
            parse_range("3-5-7")
        with pytest.raises(ValueError):
            parse_range("invalid")

class TestReadRanges:
    def test_read_ranges_from_file(self):
        """Test reading ranges from a file until a blank line."""
        with open("inputs/day5input_small.txt", "r") as file:
            ranges = read_ranges(file)
            assert len(ranges) == 4
            assert ranges[0].min == 3
            assert ranges[0].max == 5
            assert ranges[1].min == 10
            assert ranges[1].max == 14
            assert ranges[2].min == 16
            assert ranges[2].max == 20
            assert ranges[3].min == 12
            assert ranges[3].max == 18
    
    def test_read_ranges_empty_file(self):
        """Test reading ranges from an empty file."""
        import io
        file = io.StringIO("\n")
        ranges = read_ranges(file)
        assert len(ranges) == 0
    
    def test_read_ranges_stops_at_blank_line(self):
        """Test that read_ranges stops reading at a blank line."""
        import io
        file = io.StringIO("3-5\n10-14\n\n16-20\n")
        ranges = read_ranges(file)
        assert len(ranges) == 2
        assert ranges[0].min == 3
        assert ranges[0].max == 5
        assert ranges[1].min == 10
        assert ranges[1].max == 14

class TestReadNumbers:
    def test_read_numbers_from_file(self):
        """Test reading numbers from a file after the blank line."""
        with open("inputs/day5input_small.txt", "r") as file:
            # Skip the ranges section
            read_ranges(file)
            # Now read the numbers
            numbers = read_numbers(file)
            assert len(numbers) == 6
            assert numbers == [1, 5, 8, 11, 17, 32]
    
    def test_read_numbers_empty_file(self):
        """Test reading numbers from an empty file."""
        import io
        file = io.StringIO("\n")
        numbers = read_numbers(file)
        assert len(numbers) == 0
    
    def test_read_numbers_with_blank_lines(self):
        """Test that read_numbers skips blank lines."""
        import io
        file = io.StringIO("1\n\n5\n\n8\n")
        numbers = read_numbers(file)
        assert numbers == [1, 5, 8]
    
    def test_read_numbers_large_numbers(self):
        """Test reading large numbers."""
        import io
        file = io.StringIO("273755558074677\n473129501945828\n")
        numbers = read_numbers(file)
        assert numbers == [273755558074677, 473129501945828]

class TestIsNumberInAnyRange:
    def test_number_in_range(self):
        """Test checking if a number is in any range when it is."""
        ranges = [Range(3, 5), Range(10, 14), Range(16, 20)]
        assert is_number_in_any_range(4, ranges) == True
        assert is_number_in_any_range(12, ranges) == True
        assert is_number_in_any_range(18, ranges) == True
    
    def test_number_not_in_range(self):
        """Test checking if a number is in any range when it is not."""
        ranges = [Range(3, 5), Range(10, 14), Range(16, 20)]
        assert is_number_in_any_range(1, ranges) == False
        assert is_number_in_any_range(8, ranges) == False
        assert is_number_in_any_range(32, ranges) == False
    
    def test_number_at_range_boundary(self):
        """Test checking numbers at range boundaries."""
        ranges = [Range(3, 5), Range(10, 14)]
        assert is_number_in_any_range(3, ranges) == True  # min boundary
        assert is_number_in_any_range(5, ranges) == True  # max boundary
        assert is_number_in_any_range(2, ranges) == False  # just below
        assert is_number_in_any_range(6, ranges) == False  # just above
    
    def test_number_in_overlapping_ranges(self):
        """Test checking numbers in overlapping ranges."""
        ranges = [Range(3, 5), Range(4, 6), Range(10, 14)]
        assert is_number_in_any_range(4, ranges) == True  # in first two ranges
        assert is_number_in_any_range(5, ranges) == True  # in first two ranges
    
    def test_empty_ranges_list(self):
        """Test checking a number against an empty list of ranges."""
        ranges = []
        assert is_number_in_any_range(5, ranges) == False
    
    def test_single_value_range(self):
        """Test checking numbers against single-value ranges."""
        ranges = [Range(5, 5), Range(10, 10)]
        assert is_number_in_any_range(5, ranges) == True
        assert is_number_in_any_range(10, ranges) == True
        assert is_number_in_any_range(7, ranges) == False
    
    def test_number_in_any_range_with_small_input(self):
        """Test checking numbers from the small input file against its ranges."""
        with open("inputs/day5input_small.txt", "r") as file:
            ranges = read_ranges(file)
            numbers = read_numbers(file)
        
        # From the small input:
        # Ranges: 3-5, 10-14, 16-20, 12-18
        # Numbers: 1, 5, 8, 11, 17, 32
        # Expected: 5 (in 3-5), 11 (in 10-14 or 12-18), 17 (in 16-20 or 12-18)
        assert is_number_in_any_range(1, ranges) == False
        assert is_number_in_any_range(5, ranges) == True
        assert is_number_in_any_range(8, ranges) == False
        assert is_number_in_any_range(11, ranges) == True
        assert is_number_in_any_range(17, ranges) == True
        assert is_number_in_any_range(32, ranges) == False

class TestCountUniqueNumbersInRanges:
    def test_count_unique_numbers_single_range(self):
        """Test counting unique numbers in a single range."""
        ranges = [Range(3, 5)]
        assert count_unique_numbers_in_ranges(ranges) == 3  # 3, 4, 5
    
    def test_count_unique_numbers_non_overlapping(self):
        """Test counting unique numbers in non-overlapping ranges."""
        ranges = [Range(3, 5), Range(10, 14)]
        assert count_unique_numbers_in_ranges(ranges) == 8  # 3,4,5 + 10,11,12,13,14
    
    def test_count_unique_numbers_overlapping(self):
        """Test counting unique numbers in overlapping ranges."""
        ranges = [Range(3, 5), Range(4, 7)]
        # Range 3-5: 3, 4, 5
        # Range 4-7: 4, 5, 6, 7
        # Unique: 3, 4, 5, 6, 7 = 5 numbers
        assert count_unique_numbers_in_ranges(ranges) == 5
    
    def test_count_unique_numbers_fully_overlapping(self):
        """Test counting unique numbers when one range is fully contained in another."""
        ranges = [Range(3, 10), Range(5, 7)]
        # Range 3-10: 3, 4, 5, 6, 7, 8, 9, 10
        # Range 5-7: 5, 6, 7 (all already in first range)
        # Unique: 3, 4, 5, 6, 7, 8, 9, 10 = 8 numbers
        assert count_unique_numbers_in_ranges(ranges) == 8
    
    def test_count_unique_numbers_adjacent(self):
        """Test counting unique numbers in adjacent ranges."""
        ranges = [Range(3, 5), Range(6, 8)]
        # Range 3-5: 3, 4, 5
        # Range 6-8: 6, 7, 8
        # Unique: 3, 4, 5, 6, 7, 8 = 6 numbers
        assert count_unique_numbers_in_ranges(ranges) == 6
    
    def test_count_unique_numbers_small_input(self):
        """Test counting unique numbers with the small input file ranges."""
        # Ranges: 3-5, 10-14, 16-20, 12-18
        # 3-5: 3, 4, 5
        # 10-14: 10, 11, 12, 13, 14
        # 16-20: 16, 17, 18, 19, 20
        # 12-18: 12, 13, 14, 15, 16, 17, 18 (overlaps with 10-14 and 16-20)
        # Unique: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 = 14 numbers
        ranges = [Range(3, 5), Range(10, 14), Range(16, 20), Range(12, 18)]
        assert count_unique_numbers_in_ranges(ranges) == 14
    
    def test_count_unique_numbers_single_value_ranges(self):
        """Test counting unique numbers with single-value ranges."""
        ranges = [Range(5, 5), Range(7, 7), Range(5, 5)]  # Duplicate 5
        # Unique: 5, 7 = 2 numbers
        assert count_unique_numbers_in_ranges(ranges) == 2
    
    def test_count_unique_numbers_empty_list(self):
        """Test counting unique numbers with an empty list of ranges."""
        ranges = []
        assert count_unique_numbers_in_ranges(ranges) == 0
    
    def test_count_unique_numbers_three_overlapping(self):
        """Test counting unique numbers with three overlapping ranges."""
        ranges = [Range(1, 5), Range(3, 7), Range(5, 9)]
        # Range 1-5: 1, 2, 3, 4, 5
        # Range 3-7: 3, 4, 5, 6, 7
        # Range 5-9: 5, 6, 7, 8, 9
        # Unique: 1, 2, 3, 4, 5, 6, 7, 8, 9 = 9 numbers
        assert count_unique_numbers_in_ranges(ranges) == 9

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

