# pathfinding.py
import heapq

def astar_hex(graph, start, end):
    # Create the heap and add the start node
    heap = []
    heapq.heappush(heap, (0, start))
    
    # Create an empty dictionary to store the parent of each node
    parents = {}

    # Create a dictionary to store the cost of each node from the start node
    costs = {}

    # Create the dictionaries for storing the costs and parents of each node
    costs = {start: 0}
    parents = {start: None}
    current_cost = 0

    # While the heap is not empty
    while heap:
        # Pop the node with the lowest cost from the heap
        current_cost, current_node = heapq.heappop(heap)

        # If the current node is the end node, return the path
        if current_node == end:
            path = [current_node]
            while current_node in parents:
                current_node = parents[current_node]
                path.append(current_node)
            # remove the starting node from the path
            path = path[::-1][1:]
            graph.draw_path(path)
            return path
        
        # Loop through the neighbors of the current node
        for neighbor in graph.neighbors_hex(current_node):
            
            # Calculate the cost to move from the current node to the neighbor
            new_cost = costs[current_node] + graph.hex_cost(current_node, neighbor)

            # Estimate the cost to move from the neighbor to the end node
            neighbor_cube = graph.hex_to_cube(neighbor)
            end_cube = graph.hex_to_cube(end)
            heuristic_cost = graph.hex_cube_distance(neighbor_cube, end_cube)
            
            # If the neighbor has not been visited or the new cost is lower than the previous cost
            if neighbor not in costs or new_cost < costs[neighbor]:
                # Update the cost and parent dictionaries
                costs[neighbor] = new_cost
                parents[neighbor] = current_node
                
                # Generate cube coordinates for the neighbor and end node
                neighbor_cube = graph.hex_to_cube(neighbor)
                end_cube = graph.hex_to_cube(end)

                # Calculate the heuristic cost from the neighbor to the end node
                heuristic_cost = graph.hex_cube_distance(neighbor_cube, end_cube)
                
                # Add the neighbor to the heap with the total cost as the priority
                priority = new_cost + heuristic_cost
                heapq.heappush(heap, (priority, neighbor))
    
    # If the end node is not reachable, return an empty list
    return []
