import pytest
import sys
import os

# Add parent directory to path to import Day11
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day11 import parse_input, find_shortest_path, count_unique_paths, count_paths_through_nodes

class TestParseInput:
    """Test cases for the parse_input function"""
    
    def test_parse_input_small_file(self):
        """Test parsing the small input file."""
        graph = parse_input("inputs/day11input_small.txt")
        
        assert "aaa" in graph
        assert "you" in graph
        # Note: "out" is not a source node, so it won't be in the graph keys
        # but it can be reached as a destination
        
        assert graph["you"] == ["bbb", "ccc"]
        assert graph["bbb"] == ["ddd", "eee"]
        assert graph["ccc"] == ["ddd", "eee", "fff"]
        assert graph["eee"] == ["out"]
        assert graph["fff"] == ["out"]
        assert graph["ggg"] == ["out"]
    
    def test_parse_input_empty_line(self):
        """Test that empty lines are handled."""
        # Create a temporary file with empty lines
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("aaa: bbb ccc\n")
            f.write("\n")
            f.write("bbb: ddd\n")
            temp_path = f.name
        
        try:
            graph = parse_input(temp_path)
            assert "aaa" in graph
            assert "bbb" in graph
            assert graph["aaa"] == ["bbb", "ccc"]
        finally:
            os.unlink(temp_path)

class TestFindShortestPath:
    """Test cases for the find_shortest_path function"""
    
    def test_find_shortest_path_small_input(self):
        """Test shortest path on small input."""
        graph = parse_input("inputs/day11input_small.txt")
        result = find_shortest_path(graph, "you", "out")
        # Shortest path: you -> bbb -> eee -> out (3 edges)
        assert result == 3
    
    def test_find_shortest_path_start_equals_end(self):
        """Test when start equals end."""
        graph = {"aaa": ["bbb"], "bbb": ["ccc"]}
        result = find_shortest_path(graph, "aaa", "aaa")
        assert result == 0
    
    def test_find_shortest_path_no_path(self):
        """Test when no path exists."""
        graph = {"aaa": ["bbb"], "ccc": ["ddd"]}
        result = find_shortest_path(graph, "aaa", "ccc")
        assert result == -1
    
    def test_find_shortest_path_direct_edge(self):
        """Test when there's a direct edge."""
        graph = {"aaa": ["bbb"], "bbb": []}
        result = find_shortest_path(graph, "aaa", "bbb")
        assert result == 1
    
    def test_find_shortest_path_start_not_in_graph(self):
        """Test when start node is not in graph."""
        graph = {"aaa": ["bbb"]}
        result = find_shortest_path(graph, "xxx", "aaa")
        assert result == -1

class TestCountUniquePaths:
    """Test cases for the count_unique_paths function"""
    
    def test_count_unique_paths_small_input(self):
        """Test path counting on small input."""
        graph = parse_input("inputs/day11input_small.txt")
        count, paths = count_unique_paths(graph, "you", "out")
        assert count == 5
        assert len(paths) == 5
        # Verify all paths start with "you" and end with "out"
        for path in paths:
            assert path[0] == "you"
            assert path[-1] == "out"
    
    def test_count_unique_paths_start_equals_end(self):
        """Test when start equals end (should count as 1 path)."""
        graph = {"aaa": ["bbb"], "bbb": ["aaa"]}
        count, paths = count_unique_paths(graph, "aaa", "aaa")
        assert count == 1
        assert len(paths) == 1
        assert paths[0] == ["aaa"]
    
    def test_count_unique_paths_no_path(self):
        """Test when no path exists."""
        graph = {"aaa": ["bbb"], "ccc": ["ddd"]}
        count, paths = count_unique_paths(graph, "aaa", "ccc")
        assert count == 0
        assert len(paths) == 0
    
    def test_count_unique_paths_single_path(self):
        """Test with a single unique path."""
        graph = {"aaa": ["bbb"], "bbb": ["ccc"], "ccc": ["ddd"]}
        count, paths = count_unique_paths(graph, "aaa", "ddd")
        assert count == 1
        assert len(paths) == 1
        assert paths[0] == ["aaa", "bbb", "ccc", "ddd"]
    
    def test_count_unique_paths_multiple_paths(self):
        """Test with multiple paths."""
        graph = {
            "start": ["a", "b"],
            "a": ["end"],
            "b": ["end"]
        }
        count, paths = count_unique_paths(graph, "start", "end")
        assert count == 2
        assert len(paths) == 2
        # Verify paths
        path_nodes = [tuple(p) for p in paths]
        assert ("start", "a", "end") in path_nodes
        assert ("start", "b", "end") in path_nodes
    
    def test_count_unique_paths_start_not_in_graph(self):
        """Test when start node is not in graph."""
        graph = {"aaa": ["bbb"]}
        count, paths = count_unique_paths(graph, "xxx", "aaa")
        assert count == 0
        assert len(paths) == 0
    
    def test_count_unique_paths_avoids_cycles(self):
        """Test that cycles don't create infinite paths."""
        graph = {
            "start": ["a"],
            "a": ["b", "end"],
            "b": ["a"]
        }
        count, paths = count_unique_paths(graph, "start", "end")
        # Should find: start -> a -> end (only 1 path, cycle avoided)
        assert count == 1
        assert len(paths) == 1
        assert paths[0] == ["start", "a", "end"]

class TestCountPathsThroughNodes:
    """Test cases for the count_paths_through_nodes function"""
    
    def test_count_paths_through_nodes_example(self):
        """Test the provided example: svr to out through dac and fft."""
        graph = {
            "svr": ["aaa", "bbb"],
            "aaa": ["fft"],
            "fft": ["ccc"],
            "bbb": ["tty"],
            "tty": ["ccc"],
            "ccc": ["ddd", "eee"],
            "ddd": ["hub"],
            "hub": ["fff"],
            "eee": ["dac"],
            "dac": ["fff"],
            "fff": ["ggg", "hhh"],
            "ggg": ["out"],
            "hhh": ["out"]
        }
        result = count_paths_through_nodes(graph, "svr", "out", ["dac", "fft"])
        # Expected paths:
        # 1. svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> ggg -> out
        # 2. svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> hhh -> out
        assert result == 2
    
    def test_count_paths_through_nodes_no_key_nodes(self):
        """Test with empty key nodes list (should return all paths)."""
        graph = {
            "start": ["a", "b"],
            "a": ["end"],
            "b": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", [])
        assert result == 2
    
    def test_count_paths_through_nodes_single_key_node(self):
        """Test with a single key node."""
        graph = {
            "start": ["a", "b"],
            "a": ["key"],
            "b": ["key"],
            "key": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", ["key"])
        # Both paths go through key: start -> a -> key -> end, start -> b -> key -> end
        assert result == 2
    
    def test_count_paths_through_nodes_missing_key_node(self):
        """Test when path doesn't visit all key nodes."""
        graph = {
            "start": ["a"],
            "a": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", ["key"])
        # Path doesn't visit key node
        assert result == 0
    
    def test_count_paths_through_nodes_order_doesnt_matter(self):
        """Test that order of key nodes doesn't matter."""
        graph = {
            "start": ["a"],
            "a": ["key1"],
            "key1": ["key2"],
            "key2": ["end"]
        }
        result1 = count_paths_through_nodes(graph, "start", "end", ["key1", "key2"])
        result2 = count_paths_through_nodes(graph, "start", "end", ["key2", "key1"])
        # Order shouldn't matter
        assert result1 == 1
        assert result2 == 1
    
    def test_count_paths_through_nodes_start_is_key(self):
        """Test when start node is a key node."""
        graph = {
            "start": ["key"],
            "key": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", ["start", "key"])
        # Path: start -> key -> end (visits both start and key)
        assert result == 1
    
    def test_count_paths_through_nodes_end_is_key(self):
        """Test when end node is a key node."""
        graph = {
            "start": ["key"],
            "key": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", ["key", "end"])
        # Path: start -> key -> end (visits both key and end)
        assert result == 1
    
    def test_count_paths_through_nodes_no_path(self):
        """Test when no path exists."""
        graph = {
            "start": ["a"],
            "b": ["end"]
        }
        result = count_paths_through_nodes(graph, "start", "end", ["key"])
        assert result == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

