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