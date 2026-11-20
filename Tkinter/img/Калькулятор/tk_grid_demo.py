import tkinter as tk

root = tk.Tk()
root.title("Пример grid()")
root.geometry("350x250")

# Делаем 3 столбца и 3 строки одинаковыми по размеру
for c in range(3):
  root.columnconfigure(c, weight=1)
for r in range(3):
  root.rowconfigure(r, weight=1)

# 1. Объединение 3 столбцов (columnspan=3) и растягивание (sticky="nsew")
tk.Label(
    root, text='row=0, column=0, columnspan=3\nsticky="nsew"', bg="#89b4fa"
).grid(row=0, column=0, columnspan=3, sticky="nsew")

# 2. Объединение 2 строк вниз (rowspan=2)
tk.Label(
    root, text='row=1, col=0\nrowspan=2\nsticky="nsew"', bg="#a6e3a1"
).grid(row=1, column=0, rowspan=2, sticky="nsew")

# 3. Обычная ячейка, прижата только к верхнему правому углу (sticky="ne")
tk.Label(root, text='sticky="ne"', bg="#f38ba8").grid(
    row=1, column=1, sticky="ne"
)

# 4. Обычная ячейка по центру (без sticky)
tk.Label(root, text="Без sticky\n(по центру)", bg="#f9e2af").grid(
    row=1, column=2
)

# 5. Растянута только по горизонтали (sticky="ew") на 2 столбца
tk.Label(root, text='columnspan=2, sticky="ew"', bg="#cba6f7").grid(
    row=2, column=1, columnspan=2, sticky="ew"
)
''''''
root.mainloop()

