import os, sys, time
import crypto
from os import remove, path
from filedirectorydialog import SelectFile, SelectDirectory, createFile, ToBackupFile, \
    FileValidation, ReplaceExistingFileInput, Exists, FileName


def PasswordValidation(key):
    if not bool(key): return False
    elif " " in key: return False
    return True


def CloseProgram():
    print("\nFechando o programa...")
    time.sleep(2)
    sys.exit()


def Run(options_input):
    encryptedFile = False
    readBackupFile = ''

    if int(options_input) == 1 or int(options_input) == 2:
        # select a file
        file = SelectFile()

        if not file:
            print("\n>>> Selecione um Arquivo!")
        else:
            fileName = FileName(file)

            filePath_modified = FileValidation(int(options_input), file, fileName)
            if filePath_modified == '':
                return False

            fileName_modified = FileName(filePath_modified)

            # substituir arquivo já existente
            replacedFile = ReplaceExistingFileInput(filePath_modified, fileName_modified)
            if replacedFile == 0:
                return False

            if int(options_input) == 1:
                try:
                    # criptografar
                    encryptedFile = crypto.encrypt(file)

                except ValueError as error:
                    print(error)

                    if Exists(filePath_modified):
                        remove(filePath_modified)

                finally:
                    if encryptedFile:
                        remove(file)
                        time.sleep(3)
                        print("Arquivo Criptografado")

                    return False

            else:
                # número máximo de tentativas de chave privada
                maxPrivateKeyAttempts = 3

                while maxPrivateKeyAttempts > 0:
                    print(f"\n[ Restam ({maxPrivateKeyAttempts}) Tentativa(s) ]")
                    privateKey = input("Digite a chave de decriptação (chave privada): ")

                    if replacedFile == 3:
                        # substituir arquivo já existente
                        replacedFile = ReplaceExistingFileInput(filePath_modified, fileName_modified)
                        if not replacedFile:
                            break

                    if PasswordValidation(privateKey):
                        if not Exists(file):
                            print(f"\n>>> O arquivo '{fileName}' pode ter sido Excluído (ou modificado)\n")
                            break

                        else:
                            try:
                                # fazendo backup do arquivo
                                readBackupFile = ToBackupFile(filePath_modified)

                                # descriptografar
                                decryptedFile = crypto.decrypt(file, privateKey)

                            except ValueError as error:
                                print(error)

                                if readBackupFile:
                                    with open(filePath_modified, "wb") as newFile:
                                        newFile.write(bytes(readBackupFile))
                                else:
                                    remove(filePath_modified)

                                maxPrivateKeyAttempts -= 1
                                continue

                            if decryptedFile:
                                remove(file)
                                time.sleep(3)
                                print("Arquivo Descriptografado")

                            break
                    else:
                        maxPrivateKeyAttempts -= 1
                        print("\n>>> Senha Inválida")
                else:
                    print("\n>>> Você atingiu o limite das tentativas de senha!")

    elif int(options_input) == 4:
        os.system('cls' if os.name == 'nt' else 'clear')

        return False
    else:
        directory = SelectDirectory()
        if not directory:
            print("\n>>> Selecione um Diretório!")
        else:
            print(f"\nPasta: {path.basename(directory)}")
            print(f"Caminho: {directory}")

            fileCreated = createFile(directory)

            if fileCreated:
                print("\n>>> Arquivo Criado Com Sucesso!")
            else:
                print("\n>>> A operação foi finalizada!")