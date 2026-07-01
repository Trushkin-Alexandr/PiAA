def calc_L_alsh2(n, graph, visited, path):
    start = path[0]
    end = path[-1]
    
    min_out_end = float('inf')
    for v in range(n):
        if not visited[v] and graph[end][v] > 0:
            min_out_end = min(min_out_end, graph[end][v])
            
    min_in_start = float('inf')
    for v in range(n):
        if not visited[v] and graph[v][start] > 0:
            min_in_start = min(min_in_start, graph[v][start])
            
    unvisited_sum = 0
    for u in range(n):
        if not visited[u]:
            min_out_u = float('inf')
            for v in range(n):
                if (not visited[v] or v == start) and u != v and graph[u][v] > 0:
                    min_out_u = min(min_out_u, graph[u][v])
            
            min_in_u = float('inf')
            for v in range(n):
                if (not visited[v] or v == end) and u != v and graph[v][u] > 0:
                    min_in_u = min(min_in_u, graph[v][u])
                    
            if min_out_u == float('inf'): min_out_u = 0
            if min_in_u == float('inf'): min_in_u = 0
            unvisited_sum += min_out_u + min_in_u
            
    if min_out_end == float('inf'): min_out_end = 0
    if min_in_start == float('inf'): min_in_start = 0
    
    return (min_out_end + min_in_start + unvisited_sum) / 2

def alsh_2(n, graph):
    visited = [False] * n
    path = [0]
    visited[0] = True
    total_cost = 0
    curr = 0

    print("АЛШ-2 — алгоритм лучшего шага на основе полусуммы легчайших ребер:")

    for i in range(n - 1):
        next_city = -1
        best_f = float('inf')
        best_s = 0
        best_L = 0

        print(f"\nШаг {i + 1}")
        print(f"Текущий город в пути: {curr}")

        for v in range(n):
            if not visited[v] and graph[curr][v] > 0:
                s = graph[curr][v]
                
                visited[v] = True
                path.append(v)
                L = calc_L_alsh2(n, graph, visited, path)
                path.pop()
                visited[v] = False
                
                f = s + L
                print(f"  Проверка {curr} -> {v}: s + L = {s} + {L} = {f}")

                if f < best_f:
                    best_f, best_s, best_L = f, s, L
                    next_city = v

        print(f"  Выбран город: {next_city}")
        print(f"  Лучшее значение f: s + L = {best_s} + {best_L} = {best_f}")

        if next_city == -1:
            return "no path", None

        path.append(next_city)
        visited[next_city] = True
        total_cost += graph[curr][next_city]
        print(f"  Текущая стоимость накопленного пути: {total_cost}")
        curr = next_city

    if graph[curr][0] > 0:
        total_cost += graph[curr][0]
        path.append(0)
        print(f"\nВозврат в стартовый город 0 за {graph[curr][0]}")
        return total_cost, path

    return "no path", None

graph = []
with open("matrix.txt", "r") as f:
    lines = f.readlines()
    n = int(lines[0].strip())
    for i in range(1, n + 1):
        graph.append(list(map(int, lines[i].strip().split())))

cost, path = alsh_2(n, graph)

print("\nИтог:")
if cost == "no path":
    print("no path")
else:
    print(cost)
    print(" ".join(map(str, path)))