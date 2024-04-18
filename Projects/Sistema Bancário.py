menu = '''
Bem vindo ao Banco Do Brasil! O que deseja fazer?

    ----------Menu----------
    [1] - Depositar
    [2] - Sacar
    [3] - Verificar Extrato
    [4] - Sair
    ------------------------
'''

saldo = 0
limite_saque = 500
extrato = ""
numero_de_saques = 0
LIMITE_DE_SAQUES = 3

while True: 
    option = input(menu)

    if option == "1":
        valor_deposito = input("Digite o valor a ser depositado: ")
        while not valor_deposito.isnumeric:
            print("Digite um número!!")
        valor_deposito = float(valor_deposito)
        saldo += valor_deposito
        extrato += f"\nDepósito de R${valor_deposito}"

    elif option == "2":
        if numero_de_saques >= 3:
            print("Você não pode fazer mais saques! O limite de saques diários foi ultrapassado!")
        else: 
            valor_saque = input("Digite o valor a ser sacado: ")
            while not valor_saque.isnumeric:
                print("Digite um número!!")
            valor_saque = float(valor_saque)
            if valor_saque > 500: 
                print("Não é possível sacar um valor acima de R$500!!")
            else:
                saldo -= valor_saque
                numero_de_saques += 1
                print(f"Saques diários restantes: {3 - numero_de_saques}")
                extrato += f"\nSaque de R${valor_saque}"

    elif option == "3":
        print(f"Seu extrato: {extrato}")
    
    elif option == "4":
        break

    else:
        print("Essa não é uma opção válida!")
