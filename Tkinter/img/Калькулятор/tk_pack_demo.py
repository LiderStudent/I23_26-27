import tkinter as tk

root = tk.Tk()
root.title("Пример pack()")
root.geometry("350x280")

# 1. Прижата к верху, растянута по ширине (fill="x")
tk.Label(root, text='side="top", fill="x"', bg="#89b4fa", fg="#11111b").pack(
    side="top", fill="x", padx=10, pady=5, ipady=5
)

# 2. Прижата к низу (side="bottom")
tk.Label(root, text='side="bottom", fill="x"', bg="#f38ba8", fg="#11111b").pack(
    side="bottom", fill="x", padx=10, pady=5, ipady=5
)

# 3. Прижата влево, растянута по высоте (fill="y")
tk.Label(root, text='side="left"\nfill="y"', bg="#a6e3a1", fg="#11111b").pack(
    side="left", fill="y", padx=10, pady=5, ipadx=10
)

# 4. Забирает всё оставшееся место по центру (expand=True, fill="both")
tk.Label(
    root, text='expand=True\nfill="both"', bg="#f9e2af", fg="#11111b"
).pack(expand=True, fill="both", padx=10, pady=5)

root.mainloop()