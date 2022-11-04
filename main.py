from program import Run, CloseProgram


while True:
    options_input = input(
        "\nEscolha: "
        "\n1- Criptografar "
        "\n2- Descriptografar "
        "\n3- Criar Arquivo (.txt) "
        "\n4- Limpar a Tela "
        "\n5- Sair\nR: ")


    if (not options_input.isnumeric()) or (int(options_input) > 5) or (int(options_input) < 1):
        print("\n>>> Valor Inválido")
        continue
    elif int(options_input) == 5:
        CloseProgram()
    else:
        Run(options_input)
