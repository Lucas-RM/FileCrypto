import os
import random
import cypherMatriz
from convertASCII import number_ascii, string_ascii
from cryptoRSA import generator, lock, unlock


# A função "validatePrivateKey" valida a chave privada
def validatePrivateKey(decryptionKey, encryptionKey, phiKey):
    if ((decryptionKey * encryptionKey) % phiKey) == 1:
        return True
    else:
        return False


# A função "randomSeparatorCharacter" retorna caracteres aleatórios da tabela ASCII
def randomSeparatorCharacter(qtd):
    random_separator = ""
    for i in range(qtd):
        random_separator += chr(random.randrange(33, 48))

    return random_separator


# A função "randomNumber" retorna números aleatórios
def randomNumber(qtd):
    random_separator = ""
    for i in range(qtd):
        random_separator += str(random.randrange(33, 48))

    return random_separator


# A função "stretchKey" estica e codifica uma chave
def stretchKey(key, separatorKey):
    keyPlusSeparator_locked = str(lock(str(key), 41, 20413) + separatorKey)
    keyPlusSeparator_locked2x = str(lock(keyPlusSeparator_locked, 41, 20413))

    keyPlusSeparator_ascii = string_ascii(keyPlusSeparator_locked2x)
    stretched_key = keyPlusSeparator_ascii.encode("UTF-8").hex()

    return stretched_key


# A função "fileKeysAndDataSeparator" separa o conjunto de chaves dos dados do arquivo
def separatorOfKeysAndData(setOfKeysPlusData_ascii):
    keys_Separator_Data_ascii2x = number_ascii(setOfKeysPlusData_ascii)

    while True:
        keys_separator_data = str("10" + randomNumber(4) + "10")
        if keys_separator_data in keys_Separator_Data_ascii2x:
            break

    setOfKeysPlusSeparator_ascii = keys_Separator_Data_ascii2x.split(keys_separator_data)[0]
    fileData_ascii = keys_Separator_Data_ascii2x.split(keys_separator_data)[1]

    return setOfKeysPlusSeparator_ascii, fileData_ascii


# A função "captureKey" captura e retorna as chaves (pública, modular e phi)
def captureKey(keySetPlusSeparator):
    keySetPlusSeparator_unlocked = unlock(keySetPlusSeparator, 6873, 20413)

    while True:
        separator_key = randomSeparatorCharacter(2)
        if separator_key in keySetPlusSeparator_unlocked:
            break

    pKey_ascii = keySetPlusSeparator_unlocked.split(separator_key)[0]
    mKey_ascii = keySetPlusSeparator_unlocked.split(separator_key)[1]
    phiKey_ascii = keySetPlusSeparator_unlocked.split(separator_key)[2]

    p_key_unlocked = unlock(pKey_ascii, 6873, 20413)
    m_key_unlocked = unlock(mKey_ascii, 6873, 20413)
    phi_key_unlocked = unlock(phiKey_ascii, 6873, 20413)

    return p_key_unlocked, m_key_unlocked, phi_key_unlocked


def encryptStream(fIn, fOut, fileLength):
    # gerador de chave pública, modular, privada e phi
    publicKey, modularKey, privateKey, phiKey = generator()

    # separator de chave (aleatório)
    key_separator = randomSeparatorCharacter(2)

    # criptografia da chave pública, modular e phi
    publicKey_stretched = stretchKey(publicKey, key_separator)
    modularKey_stretched = stretchKey(modularKey, key_separator)
    phiKey_stretched = stretchKey(phiKey, key_separator)

    # escreve a chave pública, modular e phi no arquivo
    fOut.write(bytes(publicKey_stretched, "UTF-8"))
    fOut.write(bytes(modularKey_stretched, "UTF-8"))
    fOut.write(bytes(phiKey_stretched, "UTF-8"))

    # criptografia do separador (chaves e dados do arquivo)
    keyData_separator = str("10" + randomNumber(4) + "10")
    keyPlusSeparator_ascii = string_ascii(keyData_separator)
    keyData_separator_hex = keyPlusSeparator_ascii.encode("UTF-8").hex()
    fOut.write(bytes(keyData_separator_hex, "UTF-8"))

    try:
        # lê o arquivo para criptografar
        fdata = fIn.read()
    except ValueError:
        raise ValueError(f"\n>>> Não foi possível abrir o arquivo de entrada: {fIn.name}.\n"
                         "\n** O arquivo está corrompido; ou"
                         f"\n** O arquivo contém caracteres não ASCII.")

    if fileLength > 128:
        raise ValueError(f"\n>>> Arquivos que contém mais que 128 caracteres não podem ser criptografados."
                         f"\n>>> Seu arquivo contém {fileLength} caracteres.")
    elif fileLength <= 0:
        raise ValueError(f"\n>>> Arquivos que contém nenhum caractere não podem ser criptografados.")

    # criptografia CYPHER(Matriz)
    encryptedFileData_matrix = cypherMatriz.Cypher(fdata)

    # criptografia RSA
    lockedFileData = lock(encryptedFileData_matrix, publicKey, modularKey)

    # criptografia ASCII
    fileData_ascii = string_ascii(lockedFileData)

    # criptografia HEXADECIMAL
    fileData_hex = fileData_ascii.encode("UTF-8").hex()

    # passa os dados para bytes
    data_bytes = bytes(fileData_hex, "UTF-8")

    # escreve no arquivo os dados criptografados
    fOut.write(data_bytes)

    print(f"\nChave privada: {str(privateKey)}")
    print("Obs: Guarde a chave gerada acima para conseguir descriptografar o arquivo!")


def decryptStream(fIn, fOut, privateKey):
    try:
        # lê o arquivo para descriptografar
        fdata = fIn.read()

        # dados hexadecimal decodificados
        keysAndData_ascii = str(bytes.fromhex(fdata).decode("UTF-8"))

        # separador das chaves e dos dados do arquivo
        setOfKeysPlusSeparator_ascii, fData_ascii = separatorOfKeysAndData(keysAndData_ascii)

        # chave pública, modular, phi e dados do arquivo separados
        publicKey_decrypted, modularKey_decrypted, phiKey_decrypted = captureKey(setOfKeysPlusSeparator_ascii)

    except ValueError:
        raise ValueError("\n>>> Arquivo está corrompido")

    # valida a chave privada
    if not validatePrivateKey(int(privateKey), int(publicKey_decrypted), int(phiKey_decrypted)):
        raise ValueError("\n>>> Senha Errada (ou arquivo está corrompido).")

    # descriptografia RSA
    unlockedFileData = unlock(fData_ascii, int(privateKey), int(modularKey_decrypted))

    # descriptografia CYPHER(Matriz)
    decryptedFileData_matrix = cypherMatriz.Decypher(unlockedFileData)

    # passa os dados para bytes
    dataInBytes = bytes(decryptedFileData_matrix, "UTF-8")

    # escreve no arquivo os dados descriptografados
    fOut.write(dataInBytes)

def encrypt(inputFile):
    with open(inputFile, "r", encoding="UTF-8") as inFile:

        # pega o caminho do arquivo e concatena com o sufixo '.crypto'
        fileWithCRYPTO_path = inFile.name + ".crypto"

        with open(fileWithCRYPTO_path, "wb") as outFile:
            fileSize = os.stat(inputFile).st_size
            encryptStream(inFile, outFile, fileSize)

            print("\nCriptografando o arquivo...")
            return True


def decrypt(inputFile, privateKey):
    with open(inputFile, "r", encoding="UTF-8") as inFile:
        # pega o caminho do arquivo até o penúltimo sufixo (sem o '.crypto')
        fileNoCRIPTO_path = os.path.splitext(inputFile)[0]

        with open(fileNoCRIPTO_path, "wb") as outFile:
            decryptStream(inFile, outFile, privateKey)

            print("\nDescriptografando o arquivo...")
            return True
