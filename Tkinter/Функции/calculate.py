import re

def calculate(expression: str) -> str:
    if not isinstance(expression, str) or not expression.strip():
        print("Ошибка: пустое выражение")
        return "err"

    # Приоритеты операторов (u- и u+ — унарные минус и плюс)
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'u-': 4, 'u+': 4}
    # Правоассоциативные операторы вычисляются справа налево
    right_assoc = {'^', 'u-', 'u+'}

    values = []  # Стек для операндов (чисел)
    ops = []     # Стек для операторов и скобок

    def apply_op():
        """Извлекает оператор из стека ops, применяет его к числам из values и кладет результат обратно."""
        if not ops:
            raise ValueError("отсутствует оператор")
        op = ops.pop()

        if op in ('u-', 'u+'):
            if not values:
                raise ValueError("недостаточно операндов для унарного оператора")
            val = values.pop()
            values.append(-val if op == 'u-' else val)
        else:
            if len(values) < 2:
                raise ValueError(f"недостаточно операндов для бинарного оператора '{op}'")
            b = values.pop()
            a = values.pop()
            if op == '+':
                values.append(a + b)
            elif op == '-':
                values.append(a - b)
            elif op == '*':
                values.append(a * b)
            elif op == '/':
                if b == 0:
                    raise ZeroDivisionError("деление на ноль")
                values.append(a / b)
            elif op == '^':
                if a == 0 and b < 0:
                    raise ZeroDivisionError("возведение нуля в отрицательную степень")
                if a < 0 and not float(b).is_integer():
                    raise ValueError("возведение отрицательного числа в дробную степень")
                values.append(a ** b)

    # 1. Токенизация и проверка на недопустимые символы
    token_pattern = re.compile(r'\s*(?:(\d+(?:\.\d+)?)|([\+\-\*\/\^\(\)]))')
    pos = 0
    tokens = []
    while pos < len(expression):
        match = token_pattern.match(expression, pos)
        if not match:
             rest = expression[pos:].strip()
             if not rest:
                 break
             print(f"Ошибка: недопустимый символ или формат числа возле '{rest}'")
             return "err"
        num, op = match.groups()
        tokens.append(num if num is not None else op)
        pos = match.end()

    # 2. Основной цикл двухстекового алгоритма Дейкстры
    expect_operand = True  # Флаг помогает отличить бинарный минус/плюс от унарного

    try:
        for token in tokens:
            # Если токен — число
            if token[0].isdigit():
                if not expect_operand:
                    raise ValueError(f"пропущен оператор перед числом '{token}'")
                values.append(float(token))
                expect_operand = False

            # Если токен — открывающая скобка
            elif token == '(':
                if not expect_operand:
                    raise ValueError("пропущен оператор перед '('")
                ops.append(token)
                expect_operand = True

            # Если токен — закрывающая скобка
            elif token == ')':
                if expect_operand:
                    raise ValueError("пустые скобки или пропущен операнд перед ')'")
                while ops and ops[-1] != '(':
                    apply_op()
                if not ops:
                    raise ValueError("несогласованные скобки: лишняя ')'")
                ops.pop()  # Удаляем открывающую скобку '('
                expect_operand = False

            # Если токен — оператор
            else:
                if expect_operand:
                    if token in ('+', '-'):
                        token = 'u' + token  # Преобразуем в унарный оператор
                    else:
                        raise ValueError(f"неожиданный бинарный оператор '{token}'")

                # Выталкиваем операторы с большим или равным приоритетом (с учетом ассоциативности)
                while ops and ops[-1] != '(':
                    top = ops[-1]
                    if (precedence[top] > precedence[token]) or \
                       (precedence[top] == precedence[token] and token not in right_assoc):
                        apply_op()
                    else:
                        break
                ops.append(token)
                expect_operand = True

        # Если после прохода по всем токенам выражение обрывается на операторе
        if expect_operand:
            raise ValueError("выражение не может заканчиваться оператором или '('")

        # 3. Вычисляем оставшиеся операции в стеке
        while ops:
            if ops[-1] == '(':
                raise ValueError("несогласованные скобки: не закрыта '('")
            apply_op()

        if len(values) != 1:
            raise ValueError("некорректная структура выражения")

        result = values[0]
        # Если результат целый (например 4.0), возвращаем без дробной части ("4")
        if result.is_integer():
            return str(int(result))
        return str(result)

    except ZeroDivisionError as e:
        print(f"Ошибка вычисления: {e}")
        return "err"
    except OverflowError:
        print("Ошибка вычисления: слишком большое число (переполнение)")
        return "err"
    except ValueError as e:
        print(f"Синтаксическая ошибка: {e}")
        return "err"
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return "err"

import tkinter as tk
#from calculate import calculate


class CalculatorApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Калькулятор")
    self.root.geometry("320x440")
    self.root.resizable(False, False)
    self.root.config(bg="#1e1e2e")

    # Настройка равномерного растягивания строк и столбцов сетки
    for i in range(6):
      self.root.rowconfigure(i, weight=1)
    for j in range(4):
      self.root.columnconfigure(j, weight=1)

    # Поле ввода (дисплей) в 0-й строке на все 4 столбца
    self.entry = tk.Entry(
        self.root,
        font=("Arial", 24, "bold"),
        justify="right",
        bg="#313244",
        fg="#cdd6f4",
        bd=0,
        insertbackground="#cdd6f4",
    )
    self.entry.grid(
        row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=15
    )

    # Описание кнопок: (текст, строка, столбец)
    buttons = [
        ("7", 1, 0),
        ("8", 1, 1),
        ("9", 1, 2),
        ("/", 1, 3),
        ("4", 2, 0),
        ("5", 2, 1),
        ("6", 2, 2),
        ("*", 2, 3),
        ("1", 3, 0),
        ("2", 3, 1),
        ("3", 3, 2),
        ("-", 3, 3),
        ("C", 4, 0),
        ("0", 4, 1),
        ("=", 4, 2),
        ("+", 4, 3),
        ("(", 5, 0),
        (")", 5, 1),
        ("^", 5, 2),
        (".", 5, 3),
    ]

    # Генерация кнопок по сетке
    for text, row, col in buttons:
      self.create_button(text, row, col)

  def create_button(self, text, row, col):
    """Создаёт и размещает кнопку с нужным цветом и обработчиком."""
    if text == "C":
      bg_color = "#f38ba8"
      fg_color = "#11111b"
      cmd = self.clear
    elif text == "=":
      bg_color = "#a6e3a1"
      fg_color = "#11111b"
      cmd = self.evaluate
    elif text in ("/", "*", "-", "+", "^", "(", ")"):
      bg_color = "#45475a"
      fg_color = "#89b4fa"
      cmd = lambda s=text: self.add_symbol(s)
    else:
      bg_color = "#313244"
      fg_color = "#cdd6f4"
      cmd = lambda s=text: self.add_symbol(s)

    btn = tk.Button(
        self.root,
        text=text,
        font=("Arial", 16, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground="#585b70",
        activeforeground="#ffffff",
        bd=0,
        command=cmd,
    )
    btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

  def add_symbol(self, symbol):
    """Добавляет нажатый символ в конец поля ввода."""
    self.entry.insert(tk.END, symbol)

  def clear(self):
    """Очищает поле ввода."""
    self.entry.delete(0, tk.END)

  def evaluate(self):
    """Вычисляет выражение с помощью функции из calculate.py."""
    expression = self.entry.get()
    result = calculate(expression)  #[cite: 3]
    self.clear()
    self.entry.insert(tk.END, result)


if __name__ == "__main__":
  root = tk.Tk()
  app = CalculatorApp(root)
  root.mainloop()