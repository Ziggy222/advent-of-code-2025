import math

class Box:
    def __init__(self, numbers):
        self.x = int(numbers[0])
        self.y = int(numbers[1])
        self.z = int(numbers[2])
        self.id = f"{self.x},{self.y},{self.z}"
        self.circuit = [self] # The circuit that the box is part of

    def connect(self, other_box):
        # Connect two boxes, merging both circuits to include all
        #  existing members of both circuits
        # Collect all unique boxes from both circuits
        merged_circuit = []
        seen = set()
        for box in self.circuit:
            if box not in seen:
                merged_circuit.append(box)
                seen.add(box)
        for box in other_box.circuit:
            if box not in seen:
                merged_circuit.append(box)
                seen.add(box)
        
        # Update all boxes in the merged circuit to point to the same list
        for box in merged_circuit:
            box.circuit = merged_circuit
    
    def __str__(self):
        return f"Box({self.id})"



def main():
    # Our list of all junction boxes
    boxes = []
    # The number of connections we want to make
    num_connections = 1000
    with open("inputs/day8input.txt", "r") as file:
        for line in file:
            # Each line is comma-delimited numbers, use numbers
            #  to build a Box object
            numbers = line.split(",")
            box = Box(numbers)
            boxes.append(box)
        # We process the number of connections we want to make
        connect_boxes_by_shortest_distance(boxes, num_connections)

        # Get the three largest circuits by number of boxes
        top_three_circuit_sizes = get_top_three_circuits_sizes(boxes)
        print(f"Top three circuit sizes: {top_three_circuit_sizes}")
        print(f"Top three circuit products: {get_top_circuit_products(top_three_circuit_sizes)}")

def get_top_circuit_products(top_three_circuit_sizes):
    # Get the product of the three largest circuits by number of boxes
    return top_three_circuit_sizes[0] * top_three_circuit_sizes[1] * top_three_circuit_sizes[2]

def count_unique_circuits(boxes):
    # Count the number of unique circuits
    # Since boxes in the same circuit share the same list object,
    # we can use the circuit list's identity to track unique circuits
    seen_circuit_ids = set()
    
    for box in boxes:
        circuit_id = id(box.circuit)
        seen_circuit_ids.add(circuit_id)
    
    return len(seen_circuit_ids)

def get_top_three_circuits_sizes(boxes):
    # Run through the boxes to find the three largest circuits by number
    #  of boxes. Do not return the same circuit multiple times.
    # Since boxes in the same circuit share the same list object,
    #  we can use the circuit list's identity to track unique circuits
    seen_circuit_ids = set()
    circuit_sizes = []
    
    for box in boxes:
        # Use id() to get unique identity of the circuit list
        circuit_id = id(box.circuit)
        if circuit_id not in seen_circuit_ids:
            seen_circuit_ids.add(circuit_id)
            circuit_sizes.append(len(box.circuit))
    
    # Sort in descending order and return top 3
    circuit_sizes.sort(reverse=True)
    return circuit_sizes[:3]

def connect_boxes_by_shortest_distance(boxes, num_connections):
    # Find the num_connections shortest connections overall (regardless of circuit)
    # Then connect them all. If boxes are already in the same circuit, skip but still count.
    connections = []
    
    # Find all pairs and their distances
    for i, box1 in enumerate(boxes):
        for j, box2 in enumerate(boxes):
            if i < j:  # Only consider each pair once
                distance = calculate_distance(box1, box2)
                connections.append((distance, box1, box2))
    
    # Sort by distance and take the first num_connections
    connections.sort(key=lambda x: x[0])
    connections = connections[:num_connections]
    
    # Connect each pair (will skip if already connected)
    for distance, box1, box2 in connections:
        connect_boxes(box1, box2)

def connect_boxes(box1, box2):
    # Confirm that the boxes are not already connected
    if box1.circuit is box2.circuit:  # Use 'is' for identity comparison
        return
    # Connect the boxes
    box1.connect(box2)

def calculate_distance(box1, box2):
    # Calculate the distance between two boxes
    return math.sqrt(
        ((box2.x - box1.x)**2) + 
        ((box2.y - box1.y)**2) + 
        ((box2.z - box1.z)**2))

if __name__ == "__main__":
    main()