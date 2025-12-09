def main():
    # Order of Actions
    # 1. Read the input file
    # 2. Build a list of points (2D)
    # 3. Iterate the points, finding the largest rectangle that can be formed
    # 4. Print the area of the largest rectangle
    points = []
    with open("inputs/day9input.txt", "r") as file:
        for line in file:
            points.append(build_point(line))
    
    largest_area = find_largest_rectangle_area(points)
    print(largest_area)

# Taking in a line in format x,y\n and returning a tuple of (x, y)
def build_point(line):
    line = line.strip()
    x, y = line.split(",")
    return (int(x), int(y))

# Calculates the area of a rectangle between two points
#  Treating the two points as opposite corners of the rectangle and 
#  including the boundary points in the calculation.
def calculate_area(point1, point2):
    return (abs(point1[0] - point2[0]) + 1) * (abs(point1[1] - point2[1]) + 1)

# Finds the largest rectangle area that can be formed from any two points
#  Takes a list of points and returns the maximum area found
def find_largest_rectangle_area(points):
    if len(points) < 2:
        return 0
    
    max_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            area = calculate_area(points[i], points[j])
            if area > max_area:
                max_area = area
    
    return max_area

if __name__ == "__main__":
    main()