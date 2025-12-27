import re

def validate_phone_number(number: str) -> bool:
    print("-Проверка номера-")
    
    # Убираем все пробелы, дефисы, скобки
    clean_number = re.sub(r"[ \-\(\)]", "", number)
    
    # Проверяем, что номер состоит только из цифр (и может начинаться с плюса)
    if not re.fullmatch(r"\+?\d+", clean_number):
        print("Ошибка: Номер содержит недопустимые символы.")
        return False
    
    # Убираем все нецифровые символы (если они есть)
    digits_only = re.sub(r"\D", "", clean_number)
    
    # Проверяем длину номера
    if len(digits_only) < 10:
        print("Ошибка: Номер слишком короткий. Номер должен содержать хотя бы 10 цифр.")
        return False
    elif len(digits_only) > 15:
        print("Ошибка: Номер слишком длинный. Номер не может содержать больше 15 цифр.")
        return False
    
    # Если все проверки прошли, номер валиден
    print("Проверка номера пройдена")
    return True



def get_question(text) -> bool:
    print(text)
    m = input("Напиши да или нет: ")
    return m.lower() == "да"


def out_basic_tutorial():
    print()