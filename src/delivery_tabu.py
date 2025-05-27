import math
import random
import numpy as np
import matplotlib.pyplot as plt
import os
import csv


TOTAL_POINTS = 10   
RANDOM_SEED = 42  


PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))   
DATA_FOLDER = os.path.join(PROJECT_DIRECTORY, "..", "data")       
COORDINATES_FILE = os.path.join(DATA_FOLDER, "coordinates.csv")
PENALTY_MATRIX_FILE = os.path.join(DATA_FOLDER, "penalty_matrix.csv")



# 1) Generiranje točaka i zapis u CSV (uvijek isti seed i uvijek prepisujemo)
random.seed(RANDOM_SEED)
locations = [
    (random.uniform(0, 100), random.uniform(0, 100))
    for _ in range(TOTAL_POINTS)
]
with open(COORDINATES_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    for coordinate_x, coordinate_y in locations:
        writer.writerow([f"{coordinate_x:.3f}", f"{coordinate_y:.3f}"])
print(f"Generirano i spremljeno {len(locations)} točaka u {COORDINATES_FILE}")

# 2) Matrica euklidskih udaljenosti - anai

num_locations = len(locations)
distance_matrix_values = np.zeros((num_locations, num_locations))
for i in range(num_locations):
    for j in range(num_locations):
        if i == j:
            continue
        dx = locations[i][0] - locations[j][0]
        dy = locations[i][1] - locations[j][1]
        distance_matrix_values[i, j] = math.hypot(dx, dy)

# 3) Matrica penalizacije rush-hour (7–9 i 16–18 simulirano) - anai
penalty_matrix_values = np.zeros((num_locations, num_locations))
random.seed(RANDOM_SEED) 
for i in range(num_locations):
    for j in range(i+1, num_locations):
        r = random.random()
        if r < 0.15:
            delay = 0.5 * distance_matrix_values[i, j]
        elif r < 0.30:
            delay = 0.2 * distance_matrix_values[i, j]
        else:
            delay = 0.0
        penalty_matrix_values[i, j] = penalty_matrix_values[j, i] = delay

# Spremanje penalty matrice
np.savetxt(PENALTY_MATRIX_FILE, penalty_matrix_values, fmt="%.3f", delimiter=",")
print(f"Penal matrica spremljena u {PENALTY_MATRIX_FILE}")

# 4) Funkcija za izračun ukupnog vremena rute (udaljenost + penal)
def calculate_route_cost(route):
    total = 0.0
    for k in range(len(route) - 1):
        i, j = route[k], route[k+1]
        total += distance_matrix_values[i, j] + penalty_matrix_values[i, j]
    # povratak na start
    total += distance_matrix_values[route[-1], route[0]] + penalty_matrix_values[route[-1], route[0]]
    return total

# 5) Tabu Search algoritam- anai
def optimize_route_tabu_search(start_location_index=0, tabu_size=5, max_iter=500):
    remaining_locations = list(range(num_locations))
    remaining_locations.remove(start_location_index)
    random.shuffle(remaining_locations)
    current_route_order = [start_location_index] + remaining_locations

    optimal_route = current_route_order[:]
    minimal_cost = calculate_route_cost(optimal_route)
    tabu_memory = [tuple(current_route_order)]

    for _ in range(max_iter):
        best_neighbor_route = None
        best_neighbor_route_cost = float('inf')

        # generiramo sve swap susjede (osim indexa 0)
        for i in range(1, num_locations):
            for j in range(i+1, num_locations):
                candidate_route = current_route_order[:]
                candidate_route[i], candidate_route[j] = candidate_route[j], candidate_route[i]
                c = calculate_route_cost(candidate_route)
                route_tuple = tuple(candidate_route)

                if route_tuple in tabu_memory:
                    # aspiration: ako je bolje od globalnog, dozvoli
                    if c < minimal_cost and c < best_neighbor_route_cost:
                        best_neighbor_route, best_neighbor_route_cost = candidate_route, c
                else:
                    if c < best_neighbor_route_cost:
                        best_neighbor_route, best_neighbor_route_cost = candidate_route, c

        if best_neighbor_route is None:
            break

        current_route_order = best_neighbor_route
        current_route_cost = best_neighbor_route_cost
        tabu_memory.append(tuple(current_route_order))
        if len(tabu_memory) > tabu_size:
            tabu_memory.pop(0)

        if current_route_cost < minimal_cost:
            optimal_route, minimal_cost = current_route_order[:], current_route_cost

    return optimal_route, minimal_cost

# 6) Pokretanje pretrage
random.seed(1)  # seed za inicijalni shuffle u optimize_route_tabu_search
optimal_route, minimal_time = optimize_route_tabu_search()
print("Optimalna ruta:", optimal_route + [optimal_route[0]])
print(f"Ukupno vrijeme dostave (s penalima): {minimal_time:.2f} jedinica\n")

# 7) Ispis redoslijeda, čvora, koordinata i vremena dolaska
cumulative_travel_time = 0.0
print(f"{'Order':>5} | {'Node':>4} | {'Coordinate':>15} | {'Arrival time':>12}")
print("-"*50)
for step_number, current_node in enumerate(optimal_route):
    coordinate_x, coordinate_y = locations[current_node]
    if step_number > 0:
        previous_node = optimal_route[step_number-1]
        leg_travel_time = distance_matrix_values[previous_node, current_node] + penalty_matrix_values[previous_node, current_node]
        cumulative_travel_time += leg_travel_time
    print(f"{step_number+1:5d} | {current_node:4d} | ({coordinate_x:6.2f}, {coordinate_y:6.2f}) | {cumulative_travel_time:12.2f}")

# 8) Vizualizacija rute s detaljnim labelama na grafu
figure, axis = plt.subplots(figsize=(9,9))

# 8.1 Linija rute
x_coordinates = [locations[i][0] for i in optimal_route + [optimal_route[0]]]
y_coordinates = [locations[i][1] for i in optimal_route + [optimal_route[0]]]
axis.plot(x_coordinates, y_coordinates, '-o', linewidth=1.5, markersize=6, markerfacecolor='lightblue')

# 8.2 Priprema kumulativnog vremena za anotacije
cumulative_travel_time = 0.0

# Prolazak kroz svaki korak rute inkl. povratka na start
complete_route_order = optimal_route + [optimal_route[0]]
for step_number, current_node_idx in enumerate(complete_route_order, start=1):
    coordinate_x, coordinate_y = locations[current_node_idx]
    if step_number > 1:
        previous_node = complete_route_order[step_number-2]
        leg = distance_matrix_values[previous_node, current_node_idx] + penalty_matrix_values[previous_node, current_node_idx]
        cumulative_travel_time += leg

    # Tekst koji će stajati pored točke
    annotation_label = (
        f"{step_number}. Node {current_node_idx}\n"
        f"({coordinate_x:.1f},{coordinate_y:.1f})\n"
        f"t={cumulative_travel_time:.1f}"
    )
    axis.annotate(annotation_label,
                  (coordinate_x, coordinate_y),
                  textcoords="offset points",
                  xytext=(5, -15),
                  fontsize=8,
                  bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5))

# 8.3 Isticanje Start i End markera
starting_location_index = optimal_route[0]
final_location_index = optimal_route[-1]
axis.plot(*locations[starting_location_index],
          marker='o', markersize=12, markerfacecolor='red', label='Start')
axis.plot(*locations[final_location_index],
          marker='o', markersize=12, markerfacecolor='green', label='End')

# 8.4 Legenda, naslovi i grid
axis.legend(loc='upper right')
axis.set_title("Tabu Search")
axis.set_xlabel("X koordinata")
axis.set_ylabel("Y koordinata")
axis.grid(True)

plt.tight_layout()
plt.show()