import os

def base64_encode_manual(string: str) -> bytes:
    alphabet_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    string = string.encode('utf-8')
    data = ''
    for i in range(0, len(string), 3):
        piece = string[i:i+3]
        # Добавляем недостающие нулевые биты
        if len(piece) < 3:
            piece += b'\x00' * (3 - len(piece))
        binary = ''
        # Переводим в двоичную запись (8 бит на 1 разряд)
        for c in piece:
            binary += format(c, '08b')
        numbers = []
        # Перевод из двоичного формата в десятичный по 6 бит на символ
        for j in range(0, len(binary), 6):
            if int(binary[j:j+6], 2) == 0:
                continue
            else:
                numbers.append(int(binary[j:j+6], 2))
        # Берём символы из алфавита base64
        for num in range(len(numbers)):
            data += alphabet_base64[numbers[num]]
    # Проверка на наличие символов заполнения
    ending = (4 - len(data) % 4) % 4
    data += '=' * ending
    return data.encode('utf-8')


def base64_decode_manual(data: str) -> bytes:
    alphabet_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    ending = data.count("=")
    data = data.replace("=", "")

    # Переводим в двоичную запись по 6 бит
    binary = ""
    for c in data:
        num = alphabet_base64.index(c)
        binary += format(num, "06b")

    # Удаляем нулевые биты
    if ending == 1:
        binary = binary[:-2]
    elif ending == 2:
        binary = binary[:-4]

    result = b""
    for i in range(0, len(binary), 8):
        block = binary[i:i+8]
        # Преобразуем число в байтовую строку
        byte = int(block, 2).to_bytes(1, byteorder="big")
        result += byte

    return result


def getToEncode():
    data = input('Введите путь к файлу, или просто строку, или число, который хотите закодировать: ')
    try:
        if data.endswith('.zip') or data.endswith('.7z') or data.endswith('.rar') and os.path.exists(data):
            return zipEncoding(data)
        with open(data, 'rb') as f:
            result = f.read()
        return result
    except OSError:
        return data


def zipEncoding(data: str):
    with open(data, 'rb') as file_in, open(f'{data}.b64', 'wb') as file_out:
        first = file_in.read()
        file_out.write(base64_encode_manual(first.decode('ascii')))
    return [f'{first}', f'{data}.b64']


def main_manual():
    data = getToEncode()
    print(f'Исходные данные: {data}')
    print('Произвожу кодировку!')
    if isinstance(data, list):
        print(f'Архив закодирован под названием: {data}')
        with open(data[1], 'rb') as f:
            result = f.read()
        with open(data[1], 'rb') as f:
            result = f.read()
            print(f'Исходные данные: {result}')
            print(f'Закодированный результат: {result}')
        return
    elif isinstance(data, str):
        result = base64_encode_manual(data)
        print('Строка закодирования')
        print(f'Закодированный результат: {result}')
        return
    elif isinstance(data, bytes):
        encoded = base64_encode_manual(data.decode('ascii'))
        print(f'Результат: {encoded}')
        decoded = base64_decode_manual(encoded.decode('ascii'))
        print('Произвожу декодировку!')
        print(f'Результат: {decoded}')
    else:
        print('Произошла ошибка в связи с исходными данными!')



