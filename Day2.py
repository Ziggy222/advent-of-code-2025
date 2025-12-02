def main():
    invalid_ids = []
    with open("inputs/day2input.txt", "r") as file:
        for line in file:
            # split the line into N ranges, separated by commas
            ranges = line.split(",")
            for group in ranges:
                # split the range into a start and end, separated by a hyphen
                start, end = group.split("-")
                # convert the start and end to integers
                start = int(start)
                end = int(end)
                # Check for validity of each id in the range
                for id in range(start, end + 1):
                    # Check if the id is valid
                    if not is_valid_complete(id):
                        # If the id is not valid, add it to the list of invalid ids
                        invalid_ids.append(id)
    # Print the sum of invalid ids
    print(sum(invalid_ids))

def is_valid_basic(id):
    # Check if the id is valid
    # ID is invalid if it contains only some sequence of digits repeated twice.
    # Convert the id to a string
    id_str = str(id)
    # First, we can return as valid any id that contains an odd number of digits
    if len(id_str) % 2 == 1:
        return True
    # Next, we can check if the id consists of two equal sequences of digits
    # If it does, the id is invalid (return False)
    # We do this by checking if the first half of the id is equal to the second half
    if id_str[:len(id_str)//2] == id_str[len(id_str)//2:]:
        return False
    return True

def is_valid_complete(id):
    # Check if the id is valid
    # ID is invalid if it contains only some sequence of digits repeated at least twice.
    # Convert the id to a string
    id_str = str(id)
    
    # Check all possible pattern lengths (from 1 to half the string length)
    # A pattern must repeat at least twice, so max pattern length is len(id_str) // 2
    for pattern_len in range(1, len(id_str) // 2 + 1):
        # Extract the pattern (first pattern_len characters)
        pattern = id_str[:pattern_len]
        
        # Check if the entire string can be formed by repeating this pattern
        # The string length must be divisible by the pattern length
        if len(id_str) % pattern_len != 0:
            continue
        
        # Check if repeating the pattern forms the entire string
        repetitions = len(id_str) // pattern_len
        # Pattern must repeat at least twice to be invalid
        if repetitions >= 2 and pattern * repetitions == id_str:
            # Found a repeating pattern, so the id is invalid
            return False
    
    # No repeating pattern found, so the id is valid
    return True

if __name__ == "__main__":
    main()