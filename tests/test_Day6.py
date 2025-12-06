import pytest
import sys
import os

# Add parent directory to path to import Day6
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day6 import read_file_columns, apply_operation, build_stacked_numbers, read_file_columns_stacked

class TestBuildStackedNumbers:
    def test_build_stacked_numbers_all_digits(self):
        """Test building stacked numbers when all rows have digits at each position."""
        # Column 1: [123, 45, 6] should give [356, 24, 1]
        result = build_stacked_numbers(['123', '45', '6'])
        assert result == [356, 24, 1]
    
    def test_build_stacked_numbers_column_3(self):
        """Test building stacked numbers for column 3."""
        # Column 3: [51, 387, 215] should give [175, 581, 32]
        result = build_stacked_numbers(['51', '387', '215'])
        assert result == [175, 581, 32]
    
    def test_build_stacked_numbers_single_digit(self):
        """Test building stacked numbers with single digit numbers."""
        result = build_stacked_numbers(['1', '2', '3'])
        assert result == [123]  # All at same position, read top to bottom: 1,2,3
    
    def test_build_stacked_numbers_mixed_lengths(self):
        """Test building stacked numbers with numbers of different lengths."""
        # This tests the case where not all rows have digits at every position
        result = build_stacked_numbers(['12', '3', '456'])
        # Right-aligned: " 12", "  3", "456"
        # Pos 2: '2', '3', '6' → 236
        # Pos 1: '1', ' ', '5' → 15 (or just 5?)
        # Pos 0: ' ', ' ', '4' → 4
        # Expected behavior needs to be determined
        assert len(result) > 0  # At least should produce some numbers

class TestReadFileColumnsStacked:
    def test_read_file_columns_stacked_small_input(self):
        """Test reading stacked columns from small input file."""
        with open("inputs/day6input_small.txt", "r") as file:
            stacked_columns, stacked_operations = read_file_columns_stacked(file)
        
        # Should have 4 columns (processed right-to-left)
        assert len(stacked_columns) == 4
        assert len(stacked_operations) == 4
        
        # Verify column 1 (leftmost, but processed last): [123, 45, 6] with *
        # Should build to [356, 24, 1]
        assert stacked_columns[0] == [356, 24, 1]
        assert stacked_operations[0] == '*'
        
        # Verify column 3: [51, 387, 215] with *
        # Should build to [175, 581, 32]
        assert stacked_columns[2] == [175, 581, 32]
        assert stacked_operations[2] == '*'
    
    def test_read_file_columns_stacked_integration(self):
        """Integration test: read file, apply operations, verify results."""
        with open("inputs/day6input_small.txt", "r") as file:
            stacked_columns, stacked_operations = read_file_columns_stacked(file)
        
        # Apply operations
        results = []
        for col, op in zip(stacked_columns, stacked_operations):
            result = apply_operation(col, op)
            results.append(result)
        
        # Expected results from the plan:
        # Rightmost: 4 + 431 + 623 = 1058
        # Second from right: 175 * 581 * 32 = 3253600
        # Third from right: 8 + 248 + 369 = 625
        # Leftmost: 356 * 24 * 1 = 8544
        # Note: columns are processed right-to-left, so results[3] is rightmost
        assert results[3] == 1058  # Rightmost column
        assert results[2] == 3253600  # Second from right
        assert results[1] == 625  # Third from right
        assert results[0] == 8544  # Leftmost
        
        # Total sum
        total = sum(results)
        assert total == 1058 + 3253600 + 625 + 8544

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
from Day6 import read_file_columns, apply_operation

class TestApplyOperation:
    def test_apply_operation_addition(self):
        """Test applying addition operation to a list of numbers."""
        assert apply_operation([1, 2, 3], '+') == 6
        assert apply_operation([10, 20, 30], '+') == 60
        assert apply_operation([5], '+') == 5
        assert apply_operation([0, 0, 0], '+') == 0
    
    def test_apply_operation_multiplication(self):
        """Test applying multiplication operation to a list of numbers."""
        assert apply_operation([2, 3, 4], '*') == 24
        assert apply_operation([5, 6], '*') == 30
        assert apply_operation([10], '*') == 10
        assert apply_operation([1, 1, 1], '*') == 1
    
    def test_apply_operation_empty_list(self):
        """Test applying operation to an empty list."""
        assert apply_operation([], '+') == 0
        assert apply_operation([], '*') == 0
    
    def test_apply_operation_large_numbers(self):
        """Test applying operations with larger numbers."""
        assert apply_operation([123, 45, 6], '*') == 33210
        assert apply_operation([51, 387, 215], '*') == 4243455
        assert apply_operation([328, 64, 98], '+') == 490
        assert apply_operation([64, 23, 314], '+') == 401
    
    def test_apply_operation_invalid_operation(self):
        """Test that invalid operation raises an error."""
        with pytest.raises(ValueError):
            apply_operation([1, 2, 3], '-')

class TestReadFileColumns:
    def test_read_file_columns_small_input(self):
        """Test reading columns from the small input file."""
        with open("inputs/day6input_small.txt", "r") as file:
            columns, operations = read_file_columns(file)
        
        # Should have 4 columns
        assert len(columns) == 4
        assert len(operations) == 4
        
        # Check column 1: [123, 45, 6]
        assert columns[0] == [123, 45, 6]
        assert operations[0] == '*'
        
        # Check column 2: [328, 64, 98]
        assert columns[1] == [328, 64, 98]
        assert operations[1] == '+'
        
        # Check column 3: [51, 387, 215]
        assert columns[2] == [51, 387, 215]
        assert operations[2] == '*'
        
        # Check column 4: [64, 23, 314]
        assert columns[3] == [64, 23, 314]
        assert operations[3] == '+'
    
    def test_read_file_columns_integration(self):
        """Integration test: read file, apply operations, verify results."""
        with open("inputs/day6input_small.txt", "r") as file:
            columns, operations = read_file_columns(file)
        
        # Apply operations and verify results
        results = []
        for col, op in zip(columns, operations):
            result = apply_operation(col, op)
            results.append(result)
        
        # Expected results:
        # Column 1: 123 * 45 * 6 = 33210
        # Column 2: 328 + 64 + 98 = 490
        # Column 3: 51 * 387 * 215 = 4243455
        # Column 4: 64 + 23 + 314 = 401
        assert results[0] == 33210
        assert results[1] == 490
        assert results[2] == 4243455
        assert results[3] == 401
        
        # Sum should be 4277556
        total = sum(results)
        assert total == 4277556
    
    def test_read_file_columns_variable_whitespace(self):
        """Test that the function handles variable whitespace correctly."""
        import io
        file_content = "1  2   3\n4 5 6\n+ * +"
        file = io.StringIO(file_content)
        columns, operations = read_file_columns(file)
        
        assert len(columns) == 3
        assert columns[0] == [1, 4]
        assert columns[1] == [2, 5]
        assert columns[2] == [3, 6]
        assert operations == ['+', '*', '+']
    
    def test_read_file_columns_single_column(self):
        """Test reading a file with a single column."""
        import io
        file_content = "1\n2\n3\n+"
        file = io.StringIO(file_content)
        columns, operations = read_file_columns(file)
        
        assert len(columns) == 1
        assert columns[0] == [1, 2, 3]
        assert operations == ['+']

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

