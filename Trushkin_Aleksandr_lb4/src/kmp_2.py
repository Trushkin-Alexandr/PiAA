def get_pi(p):
    m = len(p)
    pi = [0] * m
    k = 0
    print(f"\nВычисляем префикс-функцию для шаблона '{p}'")
    for i in range(1, m):
        while k > 0 and p[i] != p[k]:
            k = pi[k-1]
        if p[i] == p[k]:
            k += 1
        pi[i] = k
    print(f"pi-массив = {pi}")
    return pi

def cyclic_shift(a, b):
    n, m = len(a), len(b)
    if n != m:
        print("-1")
        return
    if n == 0:
        print("0")
        return

    pi = get_pi(b)
    print(f"\nНачинаем поиск в тексте длиной {n} символов")
    q = 0 
    
    for i in range(2 * n):
        char_a = a[i % n]
        print(f"Шаг {i}: Символ текста A[{i % n}] = '{char_a}', сопоставляем с B[{q}] = '{b[q]}'")
        
        while q > 0 and char_a != b[q]:
            q = pi[q-1]
            print(f"   Символы не совпали, откат по префикс функции: q = {q}")
        
        if char_a == b[q]:
            q += 1
            print(f"   Символы совпали идем вперед по префикс-функции: q = {q}")
        
        if q == m:
            start_index = i - m + 1
            print(f"   Найдено вхождение, Индекс начала: {start_index}")
            print(start_index)
            return

    print("-1")

str_a = input("Введите строку A: ").strip()
str_b = input("Введите строку B: ").strip()
cyclic_shift(str_a, str_b)