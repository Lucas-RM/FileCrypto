import numpy as np

# Variáveis Globais

# matriz de codificação
encodingMatrix = np.array([[3, 1], [2, 1]])

# matriz de decodificação
decodingMatrix = np.linalg.inv(encodingMatrix)

def Cypher(text):
    # variáveis
    cTextList_ascii = []
    cTextList_numbers = []
    encryptedList = []

    for ch in text:
        cTextList_ascii.append(str(ord(ch)))

    for ch in str(cTextList_ascii):
        cTextList_numbers.append(ord(ch))

    cTextList_length = len(cTextList_numbers)

    if cTextList_length % 2:
        cTextList_numbers.append(cTextList_numbers[-1])

    cTextMatrix = np.reshape(cTextList_numbers, (2, int(len(cTextList_numbers) / 2)))
    cTextMatrix2x = np.dot(encodingMatrix, cTextMatrix)
    cTextList2x = np.ravel(cTextMatrix2x)

    encryptedList.append(f"{str(cTextList2x[-1])}/")

    for item in cTextList2x:
        encryptedList.append(f"@{str(item)}")

    if cTextList_length % 2:
        return "".join(encryptedList[:-1])
    else:
        return "".join(encryptedList)


def Decypher(text):
    # variáveis
    keyNumber = ""
    cTextList2x = []
    dText_ascii = ""
    dText_ascii2x = ""
    dTextList = []

    if '/' in text:
        keyNumber = text.split('/')[0]
        text = text.split('/')[1]

    for cCharacter in text.split("@"):
        if cCharacter.isdigit():
            cTextList2x.append(int(cCharacter))

    cTextList2x_length = len(cTextList2x)

    if cTextList2x_length % 2:
        cTextList2x.append(int(keyNumber))

    cTextMatrix2x = np.reshape(cTextList2x, (2, int(len(cTextList2x) / 2)))
    dTextMatriz = np.rint(np.dot(decodingMatrix, cTextMatrix2x)).astype(int)
    dTextMatriz_list = np.ravel(dTextMatriz)

    if cTextList2x_length % 2:
        dTextMatriz_list = dTextMatriz_list[:-1]

    for ch in dTextMatriz_list:
        dText_ascii += str(ch) + ","

    for ch in dText_ascii.split(","):
        if ch.isdigit():
            dText_ascii2x += str(chr(int(ch)))

    for ch in dText_ascii2x.split("'"):
        if ch.isdigit():
            dTextList.append(chr(int(ch)))

    return "".join(dTextList)
