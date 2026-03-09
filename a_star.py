"""
A* (A-Star) Algorithm Implementation
=====================================
The A* algorithm is a heuristic search algorithm used to find the shortest path 
between two nodes in a graph.
"""

import heapq
import json
from typing import Dict, List, Tuple, Optional


def astar(graph: Dict[str, List[Tuple[str, float]]], 
          start: str, 
          goal: str, 
          heuristic: Dict[str, float]) -> Optional[List[str]]:
    """
    Implements the A* search algorithm to find the shortest path.
    """
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from: Dict[str, str] = {}
    
    g_cost: Dict[str, float] = {node: float('inf') for node in graph}
    g_cost[start] = 0
    
    f_cost: Dict[str, float] = {node: float('inf') for node in graph}
    f_cost[start] = heuristic[start]
    
    closed_set: set = set()
    
    while open_list:
        current_f, current = heapq.heappop(open_list)
        
        if current in closed_set:
            continue
            
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        closed_set.add(current)
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in closed_set:
                continue
                
            temp_g = g_cost[current] + weight
            
            if temp_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g
                f_cost[neighbor] = temp_g + heuristic.get(neighbor, 0)
                
                heapq.heappush(open_list, (f_cost[neighbor], neighbor))
    
    return None


def get_path_cost(path: List[str], graph: Dict[str, List[Tuple[str, float]]]) -> float:
    """Calculate total cost of a path."""
    total_cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        for neighbor, weight in graph[current]:
            if neighbor == next_node:
                total_cost += weight
                break
    return total_cost


# ==================== EXAMPLE 1: Simple Graph ====================
print("=" * 50)
print("EXAMPLE 1: Simple Graph")
print("=" * 50)

graph1 = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('C', 2)],
    'C': [('D', 1)],
    'D': []
}

heuristic1 = {
    'A': 3,
    'B': 1,
    'C': 1,
    'D': 0
}

path1 = astar(graph1, 'A', 'D', heuristic1)

result1 = {
    "example": 1,
    "description": "Simple Graph",
    "graph": graph1,
    "heuristic": heuristic1,
    "start": "A",
    "goal": "D",
    "path": path1,
    "path_cost": get_path_cost(path1, graph1) if path1 else None
}

print(f"Path: {path1}")
print(f"Cost: {result1['path_cost']}")


# ==================== EXAMPLE 2: Grid-like Graph ====================
print("\n" + "=" * 50)
print("EXAMPLE 2: Grid-like Graph")
print("=" * 50)

graph2 = {
    'A': [('B', 1), ('D', 1)],
    'B': [('A', 1), ('C', 1), ('E', 1)],
    'C': [('B', 1), ('F', 1)],
    'D': [('A', 1), ('E', 1), ('G', 1)],
    'E': [('B', 1), ('D', 1), ('F', 1), ('H', 1)],
    'F': [('C', 1), ('E', 1), ('I', 1)],
    'G': [('D', 1), ('H', 1)],
    'H': [('E', 1), ('G', 1), ('I', 1)],
    'I': [('F', 1), ('H', 1)]
}

heuristic2 = {
    'A': 4, 'B': 3, 'C': 2,
    'D': 3, 'E': 2, 'F': 1,
    'G': 2, 'H': 1, 'I': 0
}

path2 = astar(graph2, 'A', 'I', heuristic2)

result2 = {
    "example": 2,
    "description": "Grid-like Graph (City Map)",
    "graph": graph2,
    "heuristic": heuristic2,
    "start": "A",
    "goal": "I",
    "path": path2,
    "path_cost": get_path_cost(path2, graph2) if path2 else None
}

print(f"Path: {path2}")
print(f"Cost: {result2['path_cost']}")


# ==================== OUTPUT TO JSON ====================
output = {
    "algorithm": "A* (A-Star)",
    "results": [result1, result2]
}

with open('a_star_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n" + "=" * 50)
print("Results saved to a_star_results.json")
print("=" * 50)

