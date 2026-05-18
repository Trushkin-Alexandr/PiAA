def add_square(row, column, size, val, board):
    for x in range(row, row + size):
        for y in range(column, column + size):
            board[x][y] = val

def find_empty(n, m, board):
    for row in range(n):
        for column in range(m):
            if board[row][column] == 0:
                return row, column
    return False

def get_max_size(row, column, board, n, m):
    size = 1
    while row + size < n and column + size < m:
        conflict = False
        for i in range(size + 1):
            if board[row + size][column + i] == 1 or board[row + i][column + size] == 1:
                conflict = True
                break
        if conflict:
            break
        size += 1
    return size

def backtrack(count, current_list, n, m, board, min_squares, count_variants, best_list):
    if count > min_squares[0]:
        return
    
    res = find_empty(n, m, board)
    
    if res is False:
        if count < min_squares[0]:
            print(f">>> [НОВЫЙ РЕКОРД] Найдена сборка из {count} квадратов!")
            min_squares[0] = count
            count_variants[0] = 1
            best_list[0] = list(current_list)
        elif count == min_squares[0]:
            if count_variants[0] < 5:
                print(f"--- [АЛЬТЕРНАТИВА] Найдена еще одна сборка из {count} квадратов.")
            count_variants[0] += 1
        return 

    row, column = res
    max_fit = get_max_size(row, column, board, n, m)
    
    max_fit = min(max_fit, n - 1, m - 1)

    for size in range(max_fit, 0, -1):
        add_square(row, column, size, 1, board)
        current_list.append((row, column, size))
        
        backtrack(count + 1, current_list, n, m, board, min_squares, count_variants, best_list)
        
        current_list.pop()
        add_square(row, column, size, 0, board)

print("Введите размеры поля N M:")
n, m = map(int, input().split())

board = [[0] * m for _ in range(n)]
min_squares = [n * m] 
count_variants = [0]
best_list = [[]]

print("\n--- Старт поиска ---")
backtrack(0, [], n, m, board, min_squares, count_variants, best_list)
print("--- Поиск завершен ---\n")

print("Итоговые результаты:")
print(f"Минимальное число квадратов: {min_squares[0]}")
for r, c, size in best_list[0]:
    print(f"{r + 1} {c + 1} {size}")

print(f"\nВсего найдено вариантов оптимального покрытия: {count_variants[0]}")