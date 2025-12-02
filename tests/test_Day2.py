import pytest
import sys
import os

# Add parent directory to path to import Day2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day2 import is_valid_basic, is_valid_complete


class TestIsValidBasic:
    """Test cases for the is_valid_basic function"""
    
    def test_11_should_be_false(self):
        """ID 11 should be invalid (False)"""
        assert is_valid_basic(11) == False
    
    def test_20_should_be_true(self):
        """ID 20 should be valid (True)"""
        assert is_valid_basic(20) == True
    
    def test_101_should_be_true(self):
        """ID 101 should be valid (True)"""
        assert is_valid_basic(101) == True
    
    def test_1010_should_be_false(self):
        """ID 1010 should be invalid (False)"""
        assert is_valid_basic(1010) == False
    
    def test_1698522_should_be_true(self):
        """ID 1698522 should be valid (True)"""
        assert is_valid_basic(1698522) == True
    
    def test_38593859_should_be_false(self):
        """ID 38593859 should be invalid (False)"""
        assert is_valid_basic(38593859) == False

class TestIsValidComplete:
    """Test cases for the is_valid_complete function"""
    
    def test_11_should_be_false(self):
        """ID 11 should be invalid (False)"""
        assert is_valid_complete(11) == False
    
    def test_20_should_be_true(self):
        """ID 20 should be valid (True)"""
        assert is_valid_complete(20) == True
    
    def test_101_should_be_true(self):
        """ID 101 should be valid (True)"""
        assert is_valid_complete(101) == True
    
    def test_1010_should_be_false(self):
        """ID 1010 should be invalid (False)"""
        assert is_valid_complete(1010) == False
    
    def test_1698522_should_be_true(self):
        """ID 1698522 should be valid (True)"""
        assert is_valid_complete(1698522) == True
    
    def test_38593859_should_be_false(self):
        """ID 38593859 should be invalid (False)"""
        assert is_valid_complete(38593859) == False

    def test_121212_should_be_false(self):
        """ID 121212 should be invalid (False)"""
        assert is_valid_complete(121212) == False
    
    def test_121314_should_be_true(self):
        """ID 121314 should be valid (True)"""
        assert is_valid_complete(121314) == True

    def test_2121212121_should_be_false(self):
        """ID 2121212121 should be invalid (False)"""
        assert is_valid_complete(2121212121) == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

