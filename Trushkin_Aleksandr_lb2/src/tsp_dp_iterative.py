def tsp_dp_iterative():
    graph = []
    with open("matrix.txt", "r") as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        for i in range(1, n + 1):
            graph.append(list(map(int, lines[i].strip().split())))

    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0

    print("Итеративное заполнение таблицы ДП:")
    for mask in range(1, 1 << n):
        bin_mask = bin(mask)[2:].zfill(n)
        print(f"\nОбработка маски {bin_mask} (десятичное значение: {mask}):")
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            print(f"  Город {u} достижим, стоимость пути: {dp[mask][u]}")
            for v in range(n):
                if not (mask & (1 << v)):
                    if graph[u][v] != 0:
                        next_mask = mask | (1 << v)
                        next_mask_bin = bin(next_mask)[2:].zfill(n)
                        new_dist = dp[mask][u] + graph[u][v]
                        print(f"    Проверяем переход {u} -> {v} (ребро: {graph[u][v]})")
                        if new_dist < dp[next_mask][v]:
                            print(f"      Обновляем dp[маска={next_mask_bin}][город={v}]: {dp[next_mask][v]} -> {new_dist} через город {u}")
                            dp[next_mask][v] = new_dist
                            parent[next_mask][v] = u
                        else:
                            print(f"      Переход невыгоден (текущая стоимость {dp[next_mask][v]} <= {new_dist})")

    min_cost = INF
    last_node = -1
    full_mask = (1 << n) - 1

    print("\nПроверка возврата в стартовый город 0:")
    for u in range(1, n):
        if graph[u][0] != 0 and dp[full_mask][u] != INF:
            cost = dp[full_mask][u] + graph[u][0]
            print(f"  Путь через город {u} -> 0: стоимость {dp[full_mask][u]} + {graph[u][0]} = {cost}")
            if cost < min_cost:
                min_cost = cost
                last_node = u

    if min_cost == INF:
        print("\nno path")
        return

    print("\nВосстановление оптимального пути:")
    path = []
    curr_mask = full_mask
    curr_node = last_node
    while curr_node != -1:
        path.append(curr_node)
        print(f"  Добавляем город {curr_node} (маска {bin(curr_mask)[2:].zfill(n)})")
        prev_node = parent[curr_mask][curr_node]
        curr_mask = curr_mask ^ (1 << curr_node)
        curr_node = prev_node

    path.reverse()
    path.append(0)

    print("\nРезультат:")
    print(min_cost)
    print(" ".join(map(str, path)))

if __name__ == "__main__":
    tsp_dp_iterative()