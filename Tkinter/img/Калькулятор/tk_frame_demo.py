import tkinter as tk

root = tk.Tk()
root.title("Пример работы с Frame")
root.geometry("360x260")
root.config(bg="#1e1e2e")

# 1. Верхний фрейм с выпуклой рамкой (relief="ridge")
top_frame = tk.Frame(
    root,
    bg="#313244",
    bd=3,
    relief="ridge",
    padx=10,
    pady=10,
)
top_frame.pack(fill="x", padx=15, pady=10)

# Внутри top_frame используем pack(side="left")
tk.Label(top_frame, text="Верхний Frame (pack):", bg="#313244", fg="white").pack(
    side="left"
)
tk.Button(top_frame, text="Кнопка 1", bg="#89b4fa").pack(side="right", padx=5)
tk.Button(top_frame, text="Кнопка 2", bg="#a6e3a1").pack(side="right")

# 2. Нижний фрейм с цветной плоской обводкой (highlightthickness)
bottom_frame = tk.Frame(
    root,
    bg="#181825",
    highlightbackground="#f9e2af",
    highlightthickness=2,
    padx=10,
    pady=10,
)
bottom_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

# Настраиваем сетку внутри bottom_frame
for c in range(2):
    bottom_frame.columnconfigure(c, weight=1)
for r in range(2):
    bottom_frame.rowconfigure(r, weight=1)

# Внутри bottom_frame используем grid()
tk.Button(bottom_frame, text="Ячейка (0, 0)", bg="#cba6f7").grid(
    row=0, column=0, sticky="nsew", padx=5, pady=5
)
tk.Button(bottom_frame, text="Ячейка (0, 1)", bg="#f38ba8").grid(
    row=0, column=1, sticky="nsew", padx=5, pady=5
)
tk.Button(bottom_frame, text="Ячейка (1, 0) + colspan=2", bg="#fab387").grid(
    row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
)

root.mainloop()

