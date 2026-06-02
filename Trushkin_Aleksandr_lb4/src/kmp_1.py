def compute_pi(p):
    m = len(p)
    pi = [0] * m
    k = 0
    print(f"\nВычисление префикс-функции (pi) для шаблона '{p}':")
    for q in range(1, m):
        while k > 0 and p[q] != p[k]:
            k = pi[k-1]
        if p[q] == p[k]:
            k += 1
        pi[q] = k
    print(f"Массив pi: {pi}")
    return pi

def kmp_search(p, t):
    m, n = len(p), len(t)
    pi = compute_pi(p)
    res = []
    q = 0 
    
    print(f"\nПоиск вхождений '{p}' в тексте '{t}':")
    for i in range(n):
        while q > 0 and p[q] != t[i]:
            print(f"  Несовпадение: T[{i}]='{t[i]}' != P[{q}]='{p[q]}', откат q на {pi[q-1]}")
            q = pi[q-1]
        
        if p[q] == t[i]:
            print(f"  Совпадение: T[{i}]='{t[i]}' == P[{q}]='{p[q]}', новый q={q+1}")
            q += 1
        
        if q == m:
            start_index = i - m + 1
            print(f"Найдено вхождение на позиции {start_index}")
            res.append(str(start_index))
            q = pi[q-1]
            
    return res

p = input("Введите шаблон (P): ")
t = input("Введите текст (T): ")
matches = kmp_search(p, t)

print("\nРезультат:")
if not matches:
    print("-1")
else:
    print(",".join(matches))