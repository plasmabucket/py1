# Пример кода с расставленными аннотациями типов
# Код взят из решения к эаключительному заданию курса py0

# Поиск подстроки в строке
def find_substring(string: str, substring: str) -> bool:
    s_len: int = len(string)
    sub_len: int = len(substring)

    match_ind: int = 0  # Счётчик совпадений/индекс подстроки
    i: int = 0
    while i <= s_len - sub_len:
        # Если совпадает вся подстрока, то она найдена
        if match_ind == sub_len:
            return True
        # Считаем совпадения
        if string[i + match_ind] == substring[match_ind]:
            match_ind += 1
        # Если совпадения нет -- сбрасываем счётчик,
        # поиск начинем со следующего символа строки
        else:
            match_ind = 0
            i += 1
    # Ничего не найдено
    return False


# Примеры использования
print(find_substring("12345", "234"))  # True
print(find_substring("12345", "235"))  # False
print(find_substring("12345", ""))     # True
