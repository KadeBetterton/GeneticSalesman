import math
import random

# List of cities with names and coordinates
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


def calculate_distance(city1, city2):
     #Euclidean distance
    x1, y1 = city1[1]
    x2, y2 = city2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def create_distance_matrix(cities):
    #Distance matrix for cities
    num_cities = len(cities)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i][j] = calculate_distance(cities[i], cities[j])
    return distance_matrix


def route_distance(route, distance_matrix):
    #Calculate the total distance of a given route based on the distance matrix
    total_distance = 0
    for i in range(len(route)):
        total_distance += distance_matrix[route[i]][route[(i + 1) % len(route)]]
    return total_distance


def initialize_population(num_routes, num_cities):
    #Generate an initial population of random routes
    routes = []
    for _ in range(num_routes):
        remaining_cities = random.sample(range(1, num_cities), num_cities - 1)  # Exclude City A
        route = [0] + remaining_cities + [0]  # Start and end at City A
        routes.append(route)
    return routes


def select_parents(population, fitnesses):
    #Select parents for crossover based on fitness using roulette wheel selection
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for route, fitness in zip(population, fitnesses):
        current += fitness
        if current > pick:
            return route


def crossover(parent1, parent2):
    #Perform crossover between two parent routes to create a child route
    start, end = sorted(random.sample(range(1, len(parent1) - 1), 2))
    child = [None] * len(parent1)
    child[0] = parent1[0]  # Start with City A
    child[-1] = parent1[-1]  # End with City A

    # Fill in the child with part of parent1
    child[start:end] = parent1[start:end]

    p2_index = 0
    # Fill in remaining cities from parent2
    for i in range(len(child)):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]

    return child


def mutate(route, mutation_rate):
    #Mutate a route by swapping two cities based on the mutation rate
    if random.random() < mutation_rate:
        i, j = random.sample(range(1, len(route) - 1), 2)  # Exclude City A
        route[i], route[j] = route[j], route[i]


def next_generation(population, distance_matrix, mutation_rate):
    #Generate the next generation of routes
    fitnesses = []

    # Calculate fitness for each route
    for route in population:
        distance = route_distance(route, distance_matrix)
        fitnesses.append(1 / distance if distance > 0 else float('inf'))

    new_population = []

    # Keep a portion of the best routes as elite
    elite_count = max(1, len(population) // 4)
    elite_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])[:elite_count]
    new_population.extend([population[i] for i in elite_indices])

    # Create new routes through selection, crossover, and mutation
    while len(new_population) < len(population):
        parent1 = select_parents(population, fitnesses)
        parent2 = select_parents(population, fitnesses)
        child = crossover(parent1, parent2)
        mutate(child, mutation_rate)
        new_population.append(child)

    return new_population


def genetic_algorithm(distance_matrix, num_generations, population_size, mutation_rate):
    #run
    num_cities = len(distance_matrix)
    population = initialize_population(population_size, num_cities)

    for generation in range(num_generations):
        population = next_generation(population, distance_matrix, mutation_rate)

    # Find the best route from the final population
    best_route = min(population, key=lambda r: route_distance(r, distance_matrix))
    return best_route


def two_opt(route, distance_matrix):
    #two-opt optimization
    best = route
    best_distance = route_distance(best, distance_matrix)
    improved = True

    while improved:
        improved = False
        # Check edges for potential improvement
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route) - 1):
                if j - i == 1: continue  # Skip adjacent nodes
                new_route = best[:]
                new_route[i:j] = reversed(best[i:j])  # Reverse the segment
                new_distance = route_distance(new_route, distance_matrix)
                if new_distance < best_distance:
                    best = new_route
                    best_distance = new_distance
                    improved = True

    return best


# Initialize variables for trial 
i = 0  # Check for lesser value
y = 0
current_best_route = float('inf')
current_best = None

# Create the distance matrix for the cities
distance_matrix = create_distance_matrix(cities)

# Run the algorithm multiple times to ensure finding the best route
while i < 20:
    best_route = genetic_algorithm(distance_matrix, num_generations=100, population_size=20, mutation_rate=0.2)
    best_route = two_opt(best_route, distance_matrix)

    current_route_distance = route_distance(best_route, distance_matrix)

    # Check if the current route is better than the previously best found
    if current_best_route > current_route_distance:
        current_best = best_route
        current_best_route = current_route_distance
        # Reset check since a better route was found
        i = 0
        print("Check reset")
    else:
        i += 1  # Begin check
        print("Check begin: checkTrial", i)

    # Output the best route for the current trial
    print("Best Route for trial:", y, [cities[i][0] for i in best_route])
    y += 1
    print("Current Trial Best Route Distance:", route_distance(best_route, distance_matrix))

# Final output after all trials
print("Final best after", y, "algorithm trials:", [cities[i][0] for i in current_best])
print("Final Trial Best Route Distance:", current_best_route)