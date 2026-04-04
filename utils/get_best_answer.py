import itertools
import math


def solve_brute_force_small(data):
    """
    Résout les instances de petite taille par recherche exhaustive (Brute Force).
    Garantit l'optimum absolu pour les instances 1, 2 et 3.
    """
    nodes = data["nodes"]
    clients = [n for n in nodes.keys() if n != 0]
    num_vehicles = data["m_vehicles"]
    capacity = data["capacity"]

    best_dist = float("inf")
    best_routes = []

    def get_dist(n1, n2):
        p1, p2 = nodes[n1], nodes[n2]
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # 1. On génère toutes les permutations possibles des clients
    for p in itertools.permutations(clients):
        # 2. On teste toutes les manières de diviser cette permutation en 'm' camions
        # Pour les petites instances, on peut simplement itérer sur les tailles de segments
        for breaks in itertools.combinations(range(1, len(p)), num_vehicles - 1):
            temp_routes = []
            last = 0
            valid_cap = True

            # Découpage de la permutation selon les 'breaks'
            for b in breaks + (len(p),):
                segment = list(p[last:b])
                if len(segment) > capacity or len(segment) == 0:
                    valid_cap = False
                    break
                temp_routes.append([0] + segment + [0])
                last = b

            if not valid_cap:
                continue

            # 3. Calcul de la distance totale pour cette configuration
            current_total_dist = 0
            for r in temp_routes:
                current_total_dist += sum(
                    get_dist(r[i], r[i + 1]) for i in range(len(r) - 1)
                )

            # 4. Mise à jour de la meilleure solution
            if current_total_dist < best_dist:
                best_dist = current_total_dist
                best_routes = temp_routes

    return round(best_dist, 2), best_routes


def solve_savings_heuristic(data):
    nodes = data["nodes"]
    depot = nodes[0]
    clients = [n for n in nodes.keys() if n != 0]
    capacity = data["capacity"]
    max_vehicles = data["m_vehicles"]

    def get_dist(n1, n2):
        p1, p2 = nodes[n1], nodes[n2]
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # 1. Calculer les économies (savings) pour chaque paire de clients
    # S(i, j) = d(0, i) + d(0, j) - d(i, j)
    savings = []
    for i in range(len(clients)):
        for j in range(i + 1, len(clients)):
            c1, c2 = clients[i], clients[j]
            s = get_dist(0, c1) + get_dist(0, c2) - get_dist(c1, c2)
            savings.append((s, c1, c2))

    # Trier par économie décroissante
    savings.sort(key=lambda x: x[0], reverse=True)

    # 2. Initialiser chaque client dans sa propre route
    routes = {c: [0, c, 0] for c in clients}

    # 3. Fusionner les routes selon les économies
    for s, i, j in savings:
        r_i = None
        r_j = None
        for r_id, route in routes.items():
            if i in route:
                r_i = route
            if j in route:
                r_j = route

        if r_i != r_j:
            # Vérifier si i et j sont aux extrémités (proches du dépôt)
            if r_i[-2] == i and r_j[1] == j:
                new_route = r_i[:-1] + r_j[1:]
                # Vérifier la capacité (ici chaque client compte pour 1 unité)
                if len(new_route) - 2 <= capacity:
                    # Remplacer les anciennes routes par la nouvelle
                    for node in new_route:
                        if node != 0:
                            routes[node] = new_route
            elif r_i[1] == i and r_j[-2] == j:
                new_route = r_j[:-1] + r_i[1:]
                if len(new_route) - 2 <= capacity:
                    for node in new_route:
                        if node != 0:
                            routes[node] = new_route

    # Extraire les routes uniques
    unique_routes = []
    seen = []
    for r in routes.values():
        if r not in seen:
            unique_routes.append(r)
            seen.append(r)

    # Calculer la distance totale
    total_dist = 0
    for r in unique_routes:
        total_dist += sum(get_dist(r[k], r[k + 1]) for k in range(len(r) - 1))

    return round(total_dist, 2), unique_routes


from utils.CVRPDataLoader import CVRPDataLoader

loader = CVRPDataLoader()
for i in range(1, 4):  # On limite aux 3 premières
    instance = loader.get_instance(i)
    dist, routes = solve_brute_force_small(instance)
    print(f"Instance {i} OPTIMUM: {dist} | Routes: {routes}")

instance4 = loader.get_instance(4)
dist4, routes4 = solve_savings_heuristic(instance4)
print(f"Instance 4 HEURISTIC: {dist4} | Routes: {routes4}")
