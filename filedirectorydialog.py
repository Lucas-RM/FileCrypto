import os
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


# Configuração da tela de seleção de arquivo
def TkinterConfig(window, title):
    window.title(title)
    window.overrideredirect(True)
    window.geometry('0x0+0+0')
    window.transient()
    window.focus_force()
    window.withdraw()  # Isto torna oculto a janela principal
    window.attributes("-topmost", True)
    return window


# A função "SelectFile" seleciona arquivo
def SelectFile():
    root = TkinterConfig(Tk(), "Select File")

    # seleciona um arquivo
    selectedFile = askopenfilename(parent=root, title=root.title())

    if len(selectedFile) == 0:
        return False
    else:
        return selectedFile  # retorna o arquivo selecionado


# A função "SelectDirectory" seleciona pasta
def SelectDirectory():
    root = TkinterConfig(Tk(), "Select Directory")

    # seleciona um diretório
    selectedDirectory = askdirectory(parent=root, title=root.title())

    if len(selectedDirectory) == 0:
        return False
    else:
        return selectedDirectory  # retorna o diretório selecionado


# A função "createFile" cria um arquivo ".txt"
def createFile(directory):
    while True:
        data = input("\nConteúdo do arquivo (máximo de 128 caracteres)\n"
                     "Para finalizar essa operação digite 0 (zero)\n"
                     "Escreva aqui: ")

        if data == "0":
            return False
        elif len(data) == 0 or len(data) > 128 or not data:
            print("\n>>> Para a criação do arquivo é preciso ter no mínimo 1 caractere e no máximo 128 caracteres.")
        else:
            break

    if Exists(directory):
        file_path = directory + "/default.txt"
        contador = 0
        while True:
            if Exists(file_path):
                file_path = directory + f"/default{contador}.txt"
                contador += 1
            else:
                break

        with open(file_path, "wb") as fileOutput:
            fileOutput.write(bytes(data, "UTF-8"))

        return True
    else:
        print(f"\n>>> O Diretório '{os.path.basename(directory)}' pode ter sido Excluído (ou modificado).", end="")
        return False


# A função "ToBackupFile" faz backup de arquivos
def ToBackupFile(file):
    if Exists(file):
        with open(file, "rb") as backupFile:
            return backupFile.read()


"""
    A função "FileValidation" faz a validação do arquivo selecionado e 
    retorna o caminho do arquivo de encriptação ou decriptação.
"""
def FileValidation(option_input, chosenFile, fileName):
    if option_input == 1:
        if '.crypto' in chosenFile:
            print("\n>>> Arquivos '.crypto' não podem ser Criptografados!")
            return ""
        else:
            return chosenFile + ".crypto"

    elif option_input == 2:
        # pega o caminho do arquivo até o penúltimo sufixo (sem o '.crypto')
        file_suffix = Path(fileName).suffix

        if not file_suffix == '.crypto':
            print("\n>>> O arquivo '{}' não está Criptografado!".format(fileName))
            return ""
        else:
            return chosenFile.replace(".crypto", "")


"""
    A função "ReplaceExistingFileInput" verifica se o arquivo de encriptação ou 
    decriptação já existe, se existir pergunta se deseja substituí-lo.
"""
def ReplaceExistingFileInput(file, fileName):
    if Exists(file):
        print(f"\n>>> O arquivo '{fileName}' já Existe!\n")

        while True:
            replaceFile_input = int(input("\nDeseja Substituí-lo?\n>> [1] para Sim\n>> [0] para Não\nR: "))

            if replaceFile_input == 1:
                return 1
            elif replaceFile_input == 0:
                return 0
            else:
                print("\n>>> Valor Inválido!")
    else:
        return 3


# A função "Exists" verifica se um arquivo ou diretório já existe neste mesmo caminho
def Exists(path):
    path_exists = os.path.exists(path)
    return path_exists


# A função "FileName" retorna o nome do arquivo com sufixo
def FileName(file):
    fullName = file[file.rfind("/")+1:]
    return fullName
