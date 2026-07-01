import random

n = int(input("Введите количество городов: "))
sym_input = input("Матрица симметричная (y/n): ").strip().lower()
symmetric = (sym_input == 'y')

matrix = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            if symmetric:
                if j > i:
                    val = random.randint(1, 50)
                    matrix[i][j] = val
                    matrix[j][i] = val
            else:
                matrix[i][j] = random.randint(1, 50)

with open("matrix.txt", "w") as f:
    f.write(str(n) + "\n")
    for row in matrix:
        f.write(" ".join(map(str, row)) + "\n")
