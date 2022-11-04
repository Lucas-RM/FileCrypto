import math, re


# Está função converte um texto de números em caracteres ascii
def string_ascii(asciiNumber):
    text_ascii = ""
    listNumbers = re.split("(\S{2})", asciiNumber)

    for ch in listNumbers:
        if ch.isnumeric():
            num = int(ch)
            if num < 32:
                if num < 16:
                    num += 16
                    num *= 2
                else:
                    num *= 4
            else:
                num **= 2

            text_ascii += str(chr(num))
    return text_ascii


# Está função converte uma string em números da tabela ascii
def number_ascii(asciiLetter):
    numbers_ascii = ""

    for ch in asciiLetter:
        num = int(ord(str(ch)))
        num2 = num / 4

        if (num2 >= 16) and (num2 <= 124):
            num /= 4
        elif num2 <= 16:
            num = int((num / 2)) - 16
        else:
            num = int(math.sqrt(num))

        if (num >= 0) and (num < 10):
            numbers_ascii += '0' + str(num)
        else:
            numbers_ascii += str(int(num))

    return numbers_ascii
