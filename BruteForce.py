import itertools
import math

# List of cities with their coordinates
cities = [
    ("city A", (100, 300)),
    ("city B", (200, 130)),
    ("city C", (300, 500)),
    ("city D", (500, 390)),
    ("city E", (700, 300)),
    ("city F", (900, 600)),
    ("city G", (800, 950)),
    ("city H", (600, 560)),
    ("city I", (350, 550)),
    ("city J", (270, 350)),
]


# Function to calculate the Euclidean distance between two cities
def calculate_distance(city1, city2):
    x1, y1 = city1[1]
    x2, y2 = city2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to generate all possible paths starting and ending with city A
def find_all_paths(cities):
    # Exclude city A for permutations
    other_cities = [city for city in cities if city[0] != "city A"]
    paths = []

    # Generate all permutations of the other cities
    for perm in itertools.permutations(other_cities):
        # Create a path that starts and ends with city A
        full_path = [cities[0]] + list(perm) + [cities[0]]
        total_distance = 0

        # Calculate the distance of the current permutation path
        for i in range(len(full_path) - 1):
            total_distance += calculate_distance(full_path[i], full_path[i + 1])

        # Store the path and its total distance
        paths.append((full_path, total_distance))

    # Sort paths by total distance
    paths.sort(key=lambda x: x[1])
    return paths


# Main execution
if __name__ == "__main__":
    all_paths = find_all_paths(cities)

    # Display the top ten sorted paths and their distances
    for path, distance in all_paths[:10]:
        path_names = ' -> '.join(city[0] for city in path)
        print(f"Path: {path_names} | Total Distance: {distance:.2f}")