def print_dp(dp, s1, s2):
    header = "        " + " ".join(f"{char:>3}" for char in s2)
    print(header)
    for i in range(len(dp)):
        char_a = s1[i-1] if i > 0 else "#"
        row = []
        for j in range(len(dp[0])):
            val = dp[i][j]
            display = " ∞ " if val >= 9999 else f"{val:3}"
            row.append(display)
        print(f"{char_a} | " + " ".join(row))
    print()

def levenstein_8a(str_1, str_2, forbidden):
    n, m = len(str_1), len(str_2)
    INF = 9999
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        if (j - 1) in forbidden:
            print(f"(!) Вставка на индексе {j-1} запрещена, прерываем первую строку.")
            break
        dp[0][j] = j

    print("\nМатрица после инициализации границ:")
    print_dp(dp, str_1, str_2)

    print("Построчное заполнение:")
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            
            delete = dp[i-1][j] + 1
            
            if (j - 1) in forbidden:
                insert = INF
            else:
                insert = dp[i][j-1] + 1
            
            if str_1[i-1] == str_2[j-1]:
                replace = dp[i-1][j-1]
            else:
                if (j - 1) in forbidden and (str_2[j-1] == 'K' or str_2[j-1] == 'k'):
                    replace = INF
                else:
                    replace = dp[i-1][j-1] + 1
            
            dp[i][j] = min(delete, insert, replace)
        
        print(f"Шаг {i} (символ A: '{str_1[i-1]}'):")
        print_dp(dp[:i+1], str_1[:i], str_2)

    return dp[n][m]

string_a = input("Строка A: ").strip()
string_b = input("Строка B: ").strip()
forbidden_indices = list(map(int, input("Индексы запрета: ").split()))

result = levenstein_8a(string_a, string_b, forbidden_indices)

if result >= 9999:
    print("Результат: Невозможно")
else:
    print(f"Итоговое расстояние: {result}")