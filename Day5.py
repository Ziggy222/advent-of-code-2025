class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def contains(self, number):
        """Check if the number is within this range (inclusive)."""
        return self.min <= number <= self.max

    def size(self):
        # Returns the inclusive size of the range
        return self.max - self.min + 1

def parse_range(range_string):
    """Parse a range string in the format 'min-max' into a Range object.
    
    Args:
        range_string: A string in the format 'min-max' (e.g., '3-5')
    
    Returns:
        A Range object with the parsed min and max values.
    """
    parts = range_string.strip().split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid range format: {range_string}")
    return Range(int(parts[0]), int(parts[1]))

def read_ranges(file):
    """Read ranges from a file until a blank line is encountered.
    
    Args:
        file: An open file object
    
    Returns:
        A list of Range objects parsed from the file.
    """
    ranges = []
    for line in file:
        line = line.strip()
        # Stop reading when we hit a blank line
        if not line:
            break
        ranges.append(parse_range(line))
    return ranges

def read_numbers(file):
    """Read numbers from a file, one per line, until the end of the file.
    
    Args:
        file: An open file object (should be positioned after the blank line)
    
    Returns:
        A list of integers read from the file.
    """
    numbers = []
    for line in file:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        numbers.append(int(line))
    return numbers

def is_number_in_any_range(number, ranges):
    """Check if a number is contained in any of the given ranges.
    
    Args:
        number: The number to check
        ranges: A list of Range objects
    
    Returns:
        True if the number is in any range, False otherwise.
    """
    for range_obj in ranges:
        if range_obj.contains(number):
            return True
    return False

def count_unique_numbers_in_ranges(ranges):
    """Count the total number of unique numbers contained in any of the ranges.
    
    If a number is present in multiple ranges, it is only counted once.
    Uses interval merging for efficiency with large ranges.
    
    Args:
        ranges: A list of Range objects
    
    Returns:
        The count of unique numbers that are contained in any range.
    """
    if not ranges:
        return 0
    
    # Sort ranges by min value
    sorted_ranges = sorted(ranges, key=lambda r: r.min)
    
    # Merge overlapping or adjacent ranges
    merged = []
    current_min = sorted_ranges[0].min
    current_max = sorted_ranges[0].max
    
    for range_obj in sorted_ranges[1:]:
        # If this range overlaps or is adjacent to the current merged range
        if range_obj.min <= current_max + 1:
            # Extend the current merged range
            current_max = max(current_max, range_obj.max)
        else:
            # No overlap, save current merged range and start a new one
            merged.append((current_min, current_max))
            current_min = range_obj.min
            current_max = range_obj.max
    
    # Don't forget the last merged range
    merged.append((current_min, current_max))
    
    # Sum the sizes of all merged ranges
    total = 0
    for min_val, max_val in merged:
        total += (max_val - min_val + 1)
    
    return total

def main():
    with open("inputs/day5input.txt", "r") as file:
        ranges = read_ranges(file)
        numbers = read_numbers(file)
        # Get the count of numbers that are in any of the ranges
        count = sum(1 for number in numbers if is_number_in_any_range(number, ranges))
        print(f"The count of numbers that are in any of the ranges is: {count}")

        # Count the total number of unique numbers contained in any range
        unique_count = count_unique_numbers_in_ranges(ranges)
        print(f"The total number of unique numbers contained in any range is: {unique_count}")


if __name__ == "__main__":
    main()