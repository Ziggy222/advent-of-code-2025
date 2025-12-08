import pytest
import sys
import os
import math

# Add parent directory to path to import Day8
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day8 import Box, calculate_distance, connect_boxes, connect_boxes_by_shortest_distance, get_top_three_circuits_sizes, count_unique_circuits, get_top_circuit_products

class TestCalculateDistance:
    def test_calculate_distance_same_coordinates(self):
        """Test that distance is 0 when boxes have the same coordinates."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["0", "0", "0"])
        assert calculate_distance(box1, box2) == 0.0
        
        box3 = Box(["5", "5", "5"])
        box4 = Box(["5", "5", "5"])
        assert calculate_distance(box3, box4) == 0.0
    
    def test_calculate_distance_zero_and_positive_small(self):
        """Test distance calculation with zero and small positive numbers."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["3", "4", "0"])
        # Distance should be 5 (3-4-5 triangle)
        assert abs(calculate_distance(box1, box2) - 5.0) < 1e-10
        
        box3 = Box(["0", "0", "0"])
        box4 = Box(["1", "1", "1"])
        # Distance should be sqrt(1^2 + 1^2 + 1^2) = sqrt(3)
        assert abs(calculate_distance(box3, box4) - math.sqrt(3)) < 1e-10
    
    def test_calculate_distance_small_positive_numbers(self):
        """Test distance calculation with small positive numbers."""
        box1 = Box(["1", "2", "3"])
        box2 = Box(["4", "5", "6"])
        # Distance = sqrt((4-1)^2 + (5-2)^2 + (6-3)^2) = sqrt(9 + 9 + 9) = sqrt(27) = 3*sqrt(3)
        expected = 3 * math.sqrt(3)
        assert abs(calculate_distance(box1, box2) - expected) < 1e-10
        
        box3 = Box(["2", "3", "1"])
        box4 = Box(["5", "7", "4"])
        # Distance = sqrt((5-2)^2 + (7-3)^2 + (4-1)^2) = sqrt(9 + 16 + 9) = sqrt(34)
        expected = math.sqrt(34)
        assert abs(calculate_distance(box3, box4) - expected) < 1e-10
    
    def test_calculate_distance_large_numbers(self):
        """Test distance calculation with large positive numbers."""
        box1 = Box(["1000", "2000", "3000"])
        box2 = Box(["5000", "6000", "7000"])
        # Distance = sqrt((5000-1000)^2 + (6000-2000)^2 + (7000-3000)^2)
        # = sqrt(4000^2 + 4000^2 + 4000^2) = sqrt(48000000) = 4000*sqrt(3)
        expected = 4000 * math.sqrt(3)
        assert abs(calculate_distance(box1, box2) - expected) < 1e-10
        
        box3 = Box(["100000", "200000", "300000"])
        box4 = Box(["100001", "200000", "300000"])
        # Distance = sqrt((100001-100000)^2 + 0 + 0) = sqrt(1) = 1
        assert abs(calculate_distance(box3, box4) - 1.0) < 1e-10
    
    def test_calculate_distance_very_large_numbers(self):
        """Test distance calculation with very large positive numbers."""
        box1 = Box(["1000000", "2000000", "3000000"])
        box2 = Box(["5000000", "6000000", "7000000"])
        # Distance = sqrt((5000000-1000000)^2 + (6000000-2000000)^2 + (7000000-3000000)^2)
        # = sqrt(4000000^2 + 4000000^2 + 4000000^2) = 4000000*sqrt(3)
        expected = 4000000 * math.sqrt(3)
        assert abs(calculate_distance(box1, box2) - expected) < 1e-10
    
    def test_calculate_distance_one_coordinate_difference(self):
        """Test distance when only one coordinate differs."""
        box1 = Box(["5", "5", "5"])
        box2 = Box(["8", "5", "5"])
        # Distance = sqrt((8-5)^2 + 0 + 0) = 3
        assert abs(calculate_distance(box1, box2) - 3.0) < 1e-10
        
        box3 = Box(["10", "10", "10"])
        box4 = Box(["10", "15", "10"])
        # Distance = sqrt(0 + (15-10)^2 + 0) = 5
        assert abs(calculate_distance(box3, box4) - 5.0) < 1e-10
        
        box5 = Box(["20", "20", "20"])
        box6 = Box(["20", "20", "25"])
        # Distance = sqrt(0 + 0 + (25-20)^2) = 5
        assert abs(calculate_distance(box5, box6) - 5.0) < 1e-10
    
    def test_calculate_distance_two_coordinate_difference(self):
        """Test distance when two coordinates differ."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["3", "4", "0"])
        # Distance = sqrt(3^2 + 4^2 + 0) = sqrt(9 + 16) = 5
        assert abs(calculate_distance(box1, box2) - 5.0) < 1e-10
        
        box3 = Box(["1", "1", "1"])
        box4 = Box(["4", "5", "1"])
        # Distance = sqrt(3^2 + 4^2 + 0) = 5
        assert abs(calculate_distance(box3, box4) - 5.0) < 1e-10
    
    def test_calculate_distance_commutative(self):
        """Test that distance is the same regardless of box order."""
        box1 = Box(["10", "20", "30"])
        box2 = Box(["40", "50", "60"])
        
        distance1 = calculate_distance(box1, box2)
        distance2 = calculate_distance(box2, box1)
        
        assert abs(distance1 - distance2) < 1e-10
    
    def test_calculate_distance_mixed_small_and_zero(self):
        """Test distance with mixed zero and small positive values."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["0", "0", "10"])
        # Distance = sqrt(0 + 0 + 10^2) = 10
        assert abs(calculate_distance(box1, box2) - 10.0) < 1e-10
        
        box3 = Box(["0", "5", "0"])
        box4 = Box(["0", "0", "0"])
        # Distance = sqrt(0 + 5^2 + 0) = 5
        assert abs(calculate_distance(box3, box4) - 5.0) < 1e-10

class TestBoxConnect:
    def test_box_connect_basic(self):
        """Test that connecting two boxes puts both in each other's circuits."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        
        # Initially, each box is in its own circuit
        assert box1 in box1.circuit
        assert box2 in box2.circuit
        assert box1 not in box2.circuit
        assert box2 not in box1.circuit
        
        # Connect the boxes
        box1.connect(box2)
        
        # After connection, both boxes should be in each other's circuits
        assert box1 in box1.circuit
        assert box2 in box1.circuit
        assert box1 in box2.circuit
        assert box2 in box2.circuit
    
    def test_box_connect_multiple_boxes(self):
        """Test connecting multiple boxes in a chain."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        
        # Connect box1 to box2
        box1.connect(box2)
        
        # Connect box2 to box3
        box2.connect(box3)
        
        # All boxes should be in each other's circuits
        assert box1 in box1.circuit
        assert box2 in box1.circuit
        assert box3 in box1.circuit
        
        assert box1 in box2.circuit
        assert box2 in box2.circuit
        assert box3 in box2.circuit
        
        assert box1 in box3.circuit
        assert box2 in box3.circuit
        assert box3 in box3.circuit
    
    def test_box_connect_three_boxes_separate_connections(self):
        """Test connecting three boxes with separate initial connections."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        
        # Connect box1 to box2
        box1.connect(box2)
        
        # Connect box1 to box3 (box1 is already connected to box2)
        box1.connect(box3)
        
        # All boxes should be in each other's circuits
        assert box1 in box1.circuit
        assert box2 in box1.circuit
        assert box3 in box1.circuit
        
        assert box1 in box2.circuit
        assert box2 in box2.circuit
        assert box3 in box2.circuit
        
        assert box1 in box3.circuit
        assert box2 in box3.circuit
        assert box3 in box3.circuit
    
    def test_box_connect_circuit_preservation(self):
        """Test that connecting preserves all existing circuit members."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        
        # First connect box1 and box2
        box1.connect(box2)
        
        # Now connect box1 (which is in a circuit with box2) to box3
        box1.connect(box3)
        
        # box3's circuit should include box1 and box2 (since box1 was already connected to box2)
        assert box1 in box3.circuit
        assert box2 in box3.circuit
        assert box3 in box3.circuit
        
        # box2's circuit should include box1 and box3
        assert box1 in box2.circuit
        assert box2 in box2.circuit
        assert box3 in box2.circuit

class TestConnectBoxes:
    def test_connect_boxes_basic(self):
        """Test that connect_boxes connects two boxes."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        
        # Initially separate
        assert box1 not in box2.circuit
        assert box2 not in box1.circuit
        
        # Connect them
        connect_boxes(box1, box2)
        
        # Should now be connected
        assert box1 in box2.circuit
        assert box2 in box1.circuit
    
    def test_connect_boxes_already_connected(self):
        """Test that connect_boxes doesn't reconnect boxes already in the same circuit."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        
        # Connect them first time
        connect_boxes(box1, box2)
        
        # Get initial circuit lengths
        initial_length_box1 = len(box1.circuit)
        initial_length_box2 = len(box2.circuit)
        
        # Try to connect again
        connect_boxes(box1, box2)
        
        # Circuit lengths should not have changed (no reconnection)
        assert len(box1.circuit) == initial_length_box1
        assert len(box2.circuit) == initial_length_box2
        
        # They should still be connected
        assert box1 in box2.circuit
        assert box2 in box1.circuit
    
    def test_connect_boxes_indirectly_connected(self):
        """Test that connect_boxes doesn't reconnect boxes indirectly connected through other boxes."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        
        # Connect box1 to box2
        connect_boxes(box1, box2)
        
        # Connect box2 to box3 (now box1 and box3 are indirectly connected)
        connect_boxes(box2, box3)
        
        # Get circuit lengths before attempting to connect box1 and box3
        initial_length_box1 = len(box1.circuit)
        initial_length_box3 = len(box3.circuit)
        
        # Try to connect box1 and box3 (they're already in the same circuit)
        connect_boxes(box1, box3)
        
        # Circuit lengths should not have increased (no reconnection)
        assert len(box1.circuit) == initial_length_box1
        assert len(box3.circuit) == initial_length_box3
        
        # They should still all be in each other's circuits
        assert box1 in box1.circuit
        assert box2 in box1.circuit
        assert box3 in box1.circuit
    
    def test_connect_boxes_commutative(self):
        """Test that connect_boxes works the same regardless of box order."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        box4 = Box(["3", "3", "3"])
        
        # Connect box1->box2 and box3->box4
        connect_boxes(box1, box2)
        connect_boxes(box3, box4)
        
        # Now connect box1->box3
        connect_boxes(box1, box3)
        
        # All boxes should be in the same circuit
        assert box1 in box1.circuit
        assert box2 in box1.circuit
        assert box3 in box1.circuit
        assert box4 in box1.circuit
        
        # Try connecting box4->box2 (already connected)
        initial_length_box2 = len(box2.circuit)
        initial_length_box4 = len(box4.circuit)
        
        connect_boxes(box4, box2)
        
        # Should not reconnect
        assert len(box2.circuit) == initial_length_box2
        assert len(box4.circuit) == initial_length_box4
    
    def test_connect_boxes_multiple_calls_same_pair(self):
        """Test multiple calls to connect_boxes with the same pair."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        
        # First connection
        connect_boxes(box1, box2)
        length_after_first = len(box1.circuit)
        
        # Second connection attempt
        connect_boxes(box1, box2)
        assert len(box1.circuit) == length_after_first
        
        # Third connection attempt
        connect_boxes(box2, box1)  # Reverse order
        assert len(box1.circuit) == length_after_first
        
        # They should still be properly connected
        assert box1 in box2.circuit
        assert box2 in box1.circuit
    
    def test_connect_boxes_ensures_bidirectional_connection(self):
        """Test that connect_boxes ensures both boxes end up in each other's circuits."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        
        connect_boxes(box1, box2)
        
        # Verify bidirectional connection
        assert box1 in box1.circuit, "box1 should be in its own circuit"
        assert box2 in box1.circuit, "box2 should be in box1's circuit"
        assert box1 in box2.circuit, "box1 should be in box2's circuit"
        assert box2 in box2.circuit, "box2 should be in its own circuit"

class TestConnectBoxesByShortestDistance:
    def test_connect_boxes_by_shortest_distance_two_boxes(self):
        """Test connecting two boxes by shortest distance."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["3", "4", "0"])  # Distance = 5
        boxes = [box1, box2]
        
        # Initially separate
        assert box1.circuit != box2.circuit
        
        # Connect by shortest distance
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Should now be connected
        assert box1 in box2.circuit
        assert box2 in box1.circuit
    
    def test_connect_boxes_by_shortest_distance_three_boxes(self):
        """Test finding shortest distance among three boxes."""
        # box1 to box2: distance = sqrt(1^2 + 1^2 + 1^2) = sqrt(3) ≈ 1.73
        # box1 to box3: distance = sqrt(3^2 + 4^2 + 0^2) = 5
        # box2 to box3: distance = sqrt(2^2 + 3^2 + 1^2) = sqrt(14) ≈ 3.74
        # Shortest is box1 to box2
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["3", "4", "0"])
        boxes = [box1, box2, box3]
        
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # box1 and box2 should be connected (shortest distance)
        assert box1 in box2.circuit
        assert box2 in box1.circuit
        # box3 should still be separate
        assert box3 not in box1.circuit
        assert box3 not in box2.circuit
    
    def test_connect_boxes_by_shortest_distance_multiple_calls(self):
        """Test multiple calls - each call finds shortest connections from all pairs."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "0", "0"])  # Distance = 1 from box1
        box3 = Box(["2", "0", "0"])  # Distance = 2 from box1, distance = 1 from box2
        boxes = [box1, box2, box3]
        
        # First call: connects the 1 shortest connection (box1-box2, distance=1)
        connect_boxes_by_shortest_distance(boxes, 1)
        assert box1 in box2.circuit
        assert box2 in box1.circuit
        assert box3 not in box1.circuit  # box3 still separate
        assert box3 not in box2.circuit
        
        # Second call: finds 1 shortest again. Since box1-box2 is already connected,
        # it will try to connect it again (skip) but won't connect anything new.
        # To actually connect box2-box3, we need to request 2 connections total
        # (box1-box2 which is already connected, and box2-box3 which is new)
        connect_boxes_by_shortest_distance(boxes, 1)
        # After second call with 1 connection, box1-box2 is still shortest, so nothing new connects
        assert box3 not in box1.circuit
        assert box3 not in box2.circuit
        
        # To connect box2-box3, we need to request enough connections to include it
        # The 2 shortest are: box1-box2 (distance=1, already connected) and box2-box3 (distance=1)
        connect_boxes_by_shortest_distance(boxes, 2)
        assert box1 in box2.circuit
        assert box1 in box3.circuit
        assert box2 in box1.circuit
        assert box2 in box3.circuit
        assert box3 in box1.circuit
        assert box3 in box2.circuit
    
    def test_connect_boxes_by_shortest_distance_skips_already_connected(self):
        """Test that it skips boxes already in the same circuit but still counts them."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "0", "0"])  # Distance = 1 from box1
        box3 = Box(["5", "0", "0"])  # Distance = 5 from box1, distance = 4 from box2
        boxes = [box1, box2, box3]
        
        # Manually connect box1 and box2 first
        connect_boxes(box1, box2)
        
        # Now call connect_boxes_by_shortest_distance with 2 connections
        # The 2 shortest are: box1-box2 (distance=1, already connected) and box2-box3 (distance=4)
        # It will try to connect both, skip box1-box2, but connect box2-box3
        connect_boxes_by_shortest_distance(boxes, 2)
        
        # All boxes should be connected
        assert box1 in box2.circuit
        assert box2 in box1.circuit
        assert box3 in box1.circuit
        assert box3 in box2.circuit
        assert box1 in box3.circuit
        assert box2 in box3.circuit
    
    def test_connect_boxes_by_shortest_distance_four_boxes_progressive(self):
        """Test connecting four boxes - request all connections at once."""
        # Distances:
        # box1-box2: sqrt(1^2+0+0) = 1
        # box2-box3: sqrt(1^2+0+0) = 1
        # box3-box4: sqrt(1^2+0+0) = 1
        # box1-box3: sqrt(2^2+0+0) = 2
        # box1-box4: sqrt(3^2+0+0) = 3
        # box2-box4: sqrt(2^2+0+0) = 2
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "0", "0"])
        box3 = Box(["2", "0", "0"])
        box4 = Box(["3", "0", "0"])
        boxes = [box1, box2, box3, box4]
        
        # Connect 1 shortest: connects box1-box2 (distance = 1, first in sorted order)
        connect_boxes_by_shortest_distance(boxes, 1)
        assert box1 in box2.circuit
        assert len(box1.circuit) == 2
        
        # Connect 2 more shortest: The 2 shortest are box1-box2 (already connected) 
        # and box2-box3 (distance=1). This will connect box2-box3.
        connect_boxes_by_shortest_distance(boxes, 2)
        assert box3 in box1.circuit
        assert box3 in box2.circuit
        assert len(box1.circuit) == 3
        
        # Connect 3 more shortest: The 3 shortest are box1-box2 (already connected),
        # box2-box3 (already connected), and box3-box4 (distance=1). This will connect box3-box4.
        connect_boxes_by_shortest_distance(boxes, 3)
        assert box4 in box1.circuit
        assert box4 in box2.circuit
        assert box4 in box3.circuit
        assert len(box1.circuit) == 4
    
    def test_connect_boxes_by_shortest_distance_same_distance_ties(self):
        """Test behavior when multiple pairs have the same shortest distance."""
        # box1-box2: distance = sqrt(2)
        # box2-box3: distance = sqrt(2)
        # box1-box3: distance = 2
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "0"])  # Distance = sqrt(2) from box1
        box3 = Box(["2", "2", "0"])  # Distance = sqrt(2) from box2, 2*sqrt(2) from box1
        boxes = [box1, box2, box3]
        
        # Connect 1 shortest: will pick one of the sqrt(2) pairs
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Should connect one pair with distance sqrt(2)
        # The exact pair depends on iteration order, but two boxes should be connected
        connected_count = sum(1 for box in boxes if len(box.circuit) > 1)
        assert connected_count >= 2  # At least two boxes should be in a circuit together
    
    def test_connect_boxes_by_shortest_distance_zero_distance(self):
        """Test handling boxes with zero distance (same coordinates)."""
        box1 = Box(["5", "5", "5"])
        box2 = Box(["5", "5", "5"])  # Same coordinates, distance = 0
        box3 = Box(["10", "10", "10"])
        boxes = [box1, box2, box3]
        
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # box1 and box2 should be connected (distance = 0)
        assert box1 in box2.circuit
        assert box2 in box1.circuit
        assert box3 not in box1.circuit
    
    def test_connect_boxes_by_shortest_distance_all_already_connected(self):
        """Test behavior when all boxes are already in the same circuit."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        boxes = [box1, box2, box3]
        
        # Connect all boxes first
        connect_boxes(box1, box2)
        connect_boxes(box2, box3)
        
        # All should be in same circuit
        assert box1.circuit is box2.circuit is box3.circuit
        
        # Now try to connect by shortest distance
        # Should not raise an error, but nothing should change
        # (it will try to connect the shortest pair, but they're already connected)
        initial_circuit_length = len(box1.circuit)
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Circuit should remain the same
        assert len(box1.circuit) == initial_circuit_length
        assert box1.circuit is box2.circuit is box3.circuit
    
    def test_connect_boxes_by_shortest_distance_single_box(self):
        """Test behavior with a single box."""
        box1 = Box(["0", "0", "0"])
        boxes = [box1]
        
        # Should not raise an error
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Box should remain in its own circuit
        assert len(box1.circuit) == 1
        assert box1 in box1.circuit
    
    def test_connect_boxes_by_shortest_distance_empty_list(self):
        """Test behavior with an empty list."""
        boxes = []
        
        # Should not raise an error (no pairs to connect)
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Should still work with larger num_connections
        connect_boxes_by_shortest_distance(boxes, 10)
    
    def test_connect_boxes_by_shortest_distance_verifies_correct_connection(self):
        """Test that the function connects the correct boxes based on distance calculation."""
        # Create boxes with known distances
        # box1-box2: sqrt((1-0)^2 + (0-0)^2 + (0-0)^2) = 1
        # box1-box3: sqrt((3-0)^2 + (4-0)^2 + (0-0)^2) = 5
        # box2-box3: sqrt((3-1)^2 + (4-0)^2 + (0-0)^2) = sqrt(20) ≈ 4.47
        # Shortest is box1-box2
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "0", "0"])
        box3 = Box(["3", "4", "0"])
        boxes = [box1, box2, box3]
        
        connect_boxes_by_shortest_distance(boxes, 1)
        
        # Verify box1 and box2 are connected (shortest distance = 1)
        assert box1 in box2.circuit
        assert box2 in box1.circuit
        # Verify box3 is not connected yet
        assert box3 not in box1.circuit
        assert box3 not in box2.circuit
        
        # Verify the distance calculation was correct
        assert abs(calculate_distance(box1, box2) - 1.0) < 1e-10
        assert abs(calculate_distance(box1, box3) - 5.0) < 1e-10

class TestGetTopThreeCircuits:
    def test_get_top_three_circuits_all_separate(self):
        """Test with all boxes in separate circuits."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        boxes = [box1, box2, box3]
        
        result = get_top_three_circuits_sizes(boxes)
        # All circuits are size 1, should return [1, 1, 1]
        assert result == [1, 1, 1]
    
    def test_get_top_three_circuits_two_connected(self):
        """Test with some boxes connected."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        boxes = [box1, box2, box3]
        
        # Connect box1 and box2
        connect_boxes(box1, box2)
        
        result = get_top_three_circuits_sizes(boxes)
        # Should have circuit of size 2 and circuit of size 1
        assert result == [2, 1]
        assert len(result) == 2
    
    def test_get_top_three_circuits_no_duplicates(self):
        """Test that same circuit is not counted multiple times."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        boxes = [box1, box2, box3]
        
        # Connect all boxes
        connect_boxes(box1, box2)
        connect_boxes(box2, box3)
        
        result = get_top_three_circuits_sizes(boxes)
        # All boxes are in the same circuit, should return [3] only
        assert result == [3]
        assert len(result) == 1
    
    def test_get_top_three_circuits_three_different_sizes(self):
        """Test with three circuits of different sizes."""
        # Create 6 boxes
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        box4 = Box(["3", "3", "3"])
        box5 = Box(["4", "4", "4"])
        box6 = Box(["5", "5", "5"])
        boxes = [box1, box2, box3, box4, box5, box6]
        
        # Connect box1-box2 (size 2)
        connect_boxes(box1, box2)
        # Connect box3-box4-box5 (size 3)
        connect_boxes(box3, box4)
        connect_boxes(box4, box5)
        # box6 remains separate (size 1)
        
        result = get_top_three_circuits_sizes(boxes)
        # Should return [3, 2, 1]
        assert result == [3, 2, 1]
    
    def test_get_top_three_circuits_more_than_three(self):
        """Test with more than three circuits - should return top 3."""
        # Create 7 boxes
        boxes = [Box([str(i), str(i), str(i)]) for i in range(7)]
        
        # Create circuits of sizes: 3, 2, 1, 1
        connect_boxes(boxes[0], boxes[1])
        connect_boxes(boxes[1], boxes[2])
        connect_boxes(boxes[3], boxes[4])
        # boxes[5] and boxes[6] remain separate
        
        result = get_top_three_circuits_sizes(boxes)
        # Should return top 3: [3, 2, 1]
        assert result == [3, 2, 1]
        assert len(result) == 3
    
    def test_count_unique_circuits_small_input_scenario(self):
        """Test that we get 11 unique circuits with small input file and 10 connections."""
        boxes = []
        with open("inputs/day8input_small.txt", "r") as file:
            for line in file:
                numbers = line.strip().split(",")
                box = Box(numbers)
                boxes.append(box)
        
        # Initially, all boxes are separate (20 boxes = 20 circuits)
        assert count_unique_circuits(boxes) == 20
        
        # Make 10 connections (find 10 shortest, then connect them all)
        connect_boxes_by_shortest_distance(boxes, 10)
        
        # After 10 connections, should have 11 unique circuits
        # (20 boxes - 10 connections = 10 circuits merged, leaving 11 unique)
        unique_count = count_unique_circuits(boxes)
        assert unique_count == 11, f"Expected 11 unique circuits, got {unique_count}"
    
    def test_get_top_three_circuits_small_input_scenario(self):
        """Test with small input file scenario - 10 connections should yield [5, 4, 2]."""
        boxes = []
        with open("inputs/day8input_small.txt", "r") as file:
            for line in file:
                numbers = line.strip().split(",")
                box = Box(numbers)
                boxes.append(box)
        
        # Make 10 connections (find 10 shortest, then connect them all)
        connect_boxes_by_shortest_distance(boxes, 10)
        
        # First verify we have 11 unique circuits
        assert count_unique_circuits(boxes) == 11
        
        result = get_top_three_circuits_sizes(boxes)
        # Should return [5, 4, 2]
        assert result == [5, 4, 2]
    
    def test_get_top_three_circuits_empty_list(self):
        """Test with empty list."""
        boxes = []
        result = get_top_three_circuits_sizes(boxes)
        assert result == []
    
    def test_get_top_three_circuits_single_box(self):
        """Test with single box."""
        box1 = Box(["0", "0", "0"])
        boxes = [box1]
        
        result = get_top_three_circuits_sizes(boxes)
        assert result == [1]
    
    def test_get_top_three_circuits_two_boxes(self):
        """Test with two boxes."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        boxes = [box1, box2]
        
        result = get_top_three_circuits_sizes(boxes)
        # Two separate circuits
        assert result == [1, 1]
        
        # Connect them
        connect_boxes(box1, box2)
        result = get_top_three_circuits_sizes(boxes)
        # One circuit of size 2
        assert result == [2]
    
    def test_get_top_three_circuits_verifies_no_duplicates(self):
        """Test that boxes in the same circuit don't cause duplicates."""
        box1 = Box(["0", "0", "0"])
        box2 = Box(["1", "1", "1"])
        box3 = Box(["2", "2", "2"])
        boxes = [box1, box2, box3]
        
        # Connect all boxes
        connect_boxes(box1, box2)
        connect_boxes(box2, box3)
        
        # All boxes share the same circuit list object
        assert box1.circuit is box2.circuit
        assert box2.circuit is box3.circuit
        
        result = get_top_three_circuits_sizes(boxes)
        # Should only count the circuit once, returning [3]
        assert result == [3]
        assert len(result) == 1

