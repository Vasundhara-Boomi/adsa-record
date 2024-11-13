import math

def tsp_nearest_neighbor(nodes):
    visited = set()
    current_node = nodes[0]
    visited.add(current_node)
    path = [current_node]

    while len(visited) < len(nodes):
        next_node = None
        min_distance = float('inf')

        for node in nodes:
            if node not in visited:
                distance = math.dist(current_node, node)
                if distance < min_distance:
                    min_distance = distance
                    next_node = node

        current_node = next_node
        visited.add(current_node)
        path.append(current_node)

    return path


# Get the number of nodes from the user
num_nodes = int(input("Enter the number of nodes: "))

# Prompt the user for the coordinates of each node
nodes = []
for i in range(num_nodes):
    x = float(input(f"Enter the x-coordinate for node {i+1}: "))
    y = float(input(f"Enter the y-coordinate for node {i+1}: "))
    nodes.append((x, y))

# Compute the TSP path using the nearest neighbor algorithm
path = tsp_nearest_neighbor(nodes)
print("TSP path:", path)
