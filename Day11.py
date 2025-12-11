from collections import deque
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def parse_input(file_path: str) -> dict[str, list[str]]:
    """
    Parse input file to build a directed graph adjacency list.
    
    Args:
        file_path: Path to input file
        
    Returns:
        Dictionary mapping node names to lists of destination nodes
    """
    graph = {}
    
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            # Split on colon
            parts = line.split(":", 1)
            if len(parts) != 2:
                continue
                
            node = parts[0].strip()
            destinations_str = parts[1].strip()
            
            # Split destinations by whitespace
            destinations = destinations_str.split() if destinations_str else []
            
            graph[node] = destinations
    
    return graph

def find_shortest_path(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Find the shortest path length from start to end using BFS.
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node name
        end: Target node name
        
    Returns:
        Number of edges in shortest path, or -1 if no path exists
    """
    if start == end:
        return 0
    
    if start not in graph:
        return -1
    
    # BFS setup
    queue = deque([(start, 0)])  # (node, distance)
    visited = {start}
    
    while queue:
        current_node, distance = queue.popleft()
        
        # Check neighbors
        if current_node in graph:
            for neighbor in graph[current_node]:
                if neighbor == end:
                    return distance + 1
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
    
    # No path found
    return -1

def count_unique_paths(graph: dict[str, list[str]], start: str, end: str) -> tuple[int, list[list[str]]]:
    """
    Count all unique simple paths from start to end using DFS with backtracking.
    Also returns the actual paths found.
    
    Args:
        graph: Adjacency list representation of the graph
        start: Starting node name
        end: Target node name
        
    Returns:
        Tuple of (count, paths) where:
        - count: Total count of unique simple paths (no repeated nodes)
        - paths: List of all paths, where each path is a list of node names
    """
    all_paths = []
    
    def dfs(current: str, visited: set[str], current_path: list[str]) -> int:
        """
        Recursive DFS helper to count paths and collect them.
        
        Args:
            current: Current node
            visited: Set of nodes visited in current path
            current_path: List of nodes visited so far in current path
            
        Returns:
            Number of paths from current to end
        """
        # Add current node to path
        current_path.append(current)
        
        # Note: Cycle detection is handled by checking 'neighbor not in visited' 
        # before calling dfs recursively. This ensures we never visit a node twice in the same path.
        
        if current == end:
            # Found a complete path - store it
            path_copy = current_path.copy()
            all_paths.append(path_copy)
            logging.info(f"Found path #{len(all_paths)}: {' -> '.join(path_copy)}")
            current_path.pop()  # Remove current before returning
            return 1
        
        if current not in graph:
            current_path.pop()  # Remove current before returning
            return 0
        
        count = 0
        # Mark current node as visited for this path
        visited.add(current)
        
        # Explore all neighbors
        for neighbor in graph[current]:
            if neighbor not in visited:
                count += dfs(neighbor, visited, current_path)
        
        # Backtrack: remove current node from visited set and path
        visited.remove(current)
        current_path.pop()
        
        return count
    
    if start not in graph:
        return (0, [])
    
    visited = set()
    path = []
    count = dfs(start, visited, path)
    
    return (count, all_paths)

def count_paths_through_nodes(paths, key_nodes):
    count = 0
    for path in paths:
        if all(node in path for node in key_nodes):
            count += 1
    return count

def main():
    """
    Read input file, build graph, and find shortest path and total unique paths.
    """
    graph = parse_input("inputs/day11input.txt")
    
    shortest = find_shortest_path(graph, "you", "out")
    total_paths, paths = count_unique_paths(graph, "you", "out")
    
    print(shortest)
    print(total_paths)
    
    key_nodes = ["dac", "fft"]

    # Find paths from svr to out passing through dac and fft
    paths_through_keys = count_paths_through_nodes(paths, key_nodes)
    print(paths_through_keys)

if __name__ == "__main__":
    main()

