import math
def calculate_distance(city1, city2):
 x1, y1 = city1
 x2, y2 = city2
 return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
def nearest_neighbor_tsp(cities):
 num_cities = len(cities)
 visited = [False] * num_cities
 path = [0] # Start with the first city as the initial path
 visited[0] = True
 for _ in range(num_cities - 1):
     current_city = path[-1]
     nearest_city = None
     min_distance = float('inf')
     # Find the nearest unvisited city
     for i in range(num_cities):
         if not visited[i]:
             distance = calculate_distance(cities[current_city], cities[i])
             if distance < min_distance:
                 min_distance = distance
                 nearest_city = i
     # Mark the nearest city as visited and add it to the path
     visited[nearest_city] = True
     path.append(nearest_city)
 # Add the first city to complete the cycle
 path.append(0)
 return path
def main():
 num_cities = int(input("Enter the number of cities: "))
 cities = []
 for i in range(num_cities):
     x = float(input(f"Enter x-coordinate of city {i+1}: "))
     y = float(input(f"Enter y-coordinate of city {i+1}: "))
     cities.append((x, y))
 tsp_path = nearest_neighbor_tsp(cities)
 print("\nOptimal TSP path:")
 for city in tsp_path:
     print(city)
     
if __name__ == '__main__':
 main()