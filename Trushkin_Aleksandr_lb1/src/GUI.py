import tkinter as tk
from tkinter import messagebox
import time

class TilingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация укладки квадратов (Вариант 4р)")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        self.running = False
        self.rectangles = {}
        self.colors = ["#ff4d4d", "#ff9e4d", "#ffea4d", "#4dff4d", "#4dffd2", "#4da6ff", "#9e4dff", "#ff4da6"]

        control_frame = tk.Frame(self.root, bg="#e0e0e0", width=250, bd=2, relief="groove")
        control_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(control_frame, text="Параметры поля", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=10)

        tk.Label(control_frame, text="Высота N:", bg="#e0e0e0").pack(anchor="w", padx=10)
        self.entry_n = tk.Entry(control_frame, width=15, font=("Arial", 11))
        self.entry_n.pack(padx=10, pady=5)
        self.entry_n.insert(0, "5")

        tk.Label(control_frame, text="Ширина M:", bg="#e0e0e0").pack(anchor="w", padx=10)
        self.entry_m = tk.Entry(control_frame, width=15, font=("Arial", 11))
        self.entry_m.pack(padx=10, pady=5)
        self.entry_m.insert(0, "6")

        tk.Label(control_frame, text="Скорость (задержка в сек):", bg="#e0e0e0").pack(anchor="w", padx=10, pady=5)
        self.delay_slider = tk.Scale(control_frame, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", bg="#e0e0e0")
        self.delay_slider.pack(fill="x", padx=10, pady=5)
        self.delay_slider.set(0.1)

        self.btn_start = tk.Button(control_frame, text="Запустить", command=self.start_visualization, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        self.btn_start.pack(fill="x", padx=10, pady=10)

        self.btn_stop = tk.Button(control_frame, text="Стоп", command=self.stop_visualization, bg="#f44336", fg="white", font=("Arial", 11, "bold"), state="disabled")
        self.btn_stop.pack(fill="x", padx=10, pady=5)

        tk.Label(control_frame, text="Статистика", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=20)
        
        self.lbl_record = tk.Label(control_frame, text="Текущий рекорд: -", bg="#e0e0e0", font=("Arial", 10))
        self.lbl_record.pack(anchor="w", padx=10)

        self.lbl_variants = tk.Label(control_frame, text="Найдено вариантов: -", bg="#e0e0e0", font=("Arial", 10))
        self.lbl_variants.pack(anchor="w", padx=10, pady=5)

        self.lbl_current = tk.Label(control_frame, text="Квадратов сейчас: -", bg="#e0e0e0", font=("Arial", 10))
        self.lbl_current.pack(anchor="w", padx=10)

        self.canvas_width = 600
        self.canvas_height = 660
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", bd=2, relief="sunken")
        self.canvas.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def draw_grid(self, n, m):
        self.canvas.delete("all")
        self.cell_size = min(self.canvas_width // m, self.canvas_height // n)
        self.offset_x = (self.canvas_width - self.cell_size * m) // 2
        self.offset_y = (self.canvas_height - self.cell_size * n) // 2

        for r in range(n):
            for c in range(m):
                x1 = self.offset_x + c * self.cell_size
                y1 = self.offset_y + r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#d0d0d0", fill="#fafafa")

    def draw_square(self, row, column, size, is_placing):
        if is_placing:
            x1 = self.offset_x + column * self.cell_size
            y1 = self.offset_y + row * self.cell_size
            x2 = x1 + size * self.cell_size
            y2 = y1 + size * self.cell_size
            color = self.colors[size % len(self.colors)]
            rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
            
            text_id = self.canvas.create_text(x1 + (size * self.cell_size)/2, y1 + (size * self.cell_size)/2, 
                                              text=f"{size}", font=("Arial", max(10, self.cell_size // 3), "bold"), fill="black")
            
            self.rectangles[(row, column)] = (rect_id, text_id)
        else:
            if (row, column) in self.rectangles:
                rect_id, text_id = self.rectangles.pop((row, column))
                self.canvas.delete(rect_id)
                self.canvas.delete(text_id)
        
        self.lbl_current.config(text=f"Квадратов сейчас: {len(self.rectangles)}")
        self.root.update()
        time.sleep(self.delay_slider.get())

    def is_safe(self, row, column, size, board, n, m):
        if row + size <= n and column + size <= m:
            for x in range(row, row + size):
                for y in range(column, column + size):
                    if board[x][y] == 1:
                        return False
            return True
        else:
            return False

    def add_square(self, row, column, size, val, board):
        for x in range(row, row + size):
            for y in range(column, column + size):
                board[x][y] = val

    def find_empty(self, n, m, board):
        for row in range(n):
            for column in range(m):
                if board[row][column] == 0:
                    return row, column
        return False

    def get_max_size(self, row, column, board, n, m):
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

    def backtrack(self, count, current_list, n, m, board, min_squares, count_variants, best_list):
        if not self.running:
            return

        if count >= min_squares[0]:
            return
        
        res = self.find_empty(n, m, board)
        
        if res is False:
            if count < min_squares[0]:
                min_squares[0] = count
                count_variants[0] = 1
                best_list[0] = list(current_list)
                self.lbl_record.config(text=f"Текущий рекорд: {count}")
                self.lbl_variants.config(text=f"Найдено вариантов: {count_variants[0]}")
            elif count == min_squares[0]:
                count_variants[0] += 1
                self.lbl_variants.config(text=f"Найдено вариантов: {count_variants[0]}")
            return 

        row, column = res
        max_fit = self.get_max_size(row, column, board, n, m)
        max_fit = min(max_fit, n - 1, m - 1)

        for size in range(max_fit, 0, -1):
            if not self.running:
                return
            if self.is_safe(row, column, size, board, n, m):
                self.add_square(row, column, size, 1, board)
                current_list.append((row, column, size))
                
                self.draw_square(row, column, size, True)

                self.backtrack(count + 1, current_list, n, m, board, min_squares, count_variants, best_list)

                current_list.pop()
                self.add_square(row, column, size, 0, board)
                self.draw_square(row, column, size, False)

    def start_visualization(self):
        try:
            n = int(self.entry_n.get())
            m = int(self.entry_m.get())
            if n < 2 or m < 2 or n > 25 or m > 25:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные целые числа N и M от 2 до 25.")
            return

        self.running = True
        self.rectangles.clear()
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.entry_n.config(state="disabled")
        self.entry_m.config(state="disabled")

        self.draw_grid(n, m)

        board = [[0] * m for _ in range(n)]
        min_squares = [n * m] 
        count_variants = [0]
        best_list = [[]]

        self.lbl_record.config(text="Текущий рекорд: -")
        self.lbl_variants.config(text="Найдено вариантов: -")

        self.backtrack(0, [], n, m, board, min_squares, count_variants, best_list)

        self.running = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.entry_n.config(state="normal")
        self.entry_m.config(state="normal")

        if min_squares[0] < n * m:
            messagebox.showinfo("Готово", f"Поиск завершен!\nМинимальное число квадратов: {min_squares[0]}\nВсего вариантов: {count_variants[0]}")
        else:
            messagebox.showinfo("Готово", "Поиск остановлен или решений не найдено.")

    def stop_visualization(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TilingVisualizer(root)
    root.mainloop()