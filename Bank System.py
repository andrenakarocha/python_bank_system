from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, nome, data_nascimento, cpf):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
       return cls(numero, cliente) 

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = saldo < valor

        if excedeu_saldo:
            print("\nOperação falhou! Saldo insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        
        else:
            print("\nOperação falhou! O valor é inválido!")
        
        return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            
        else:
            print("\nOperação falhou! O valor é inválido!")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saques):
        self.limite = limite
        self.limite_saques = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excedeu o limite!")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

    def __str__(self):
        return f"""
                Agência:\t{self.agencia}
                Número Conta:\t{self.numero}
                Titular:\n{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

menu = '''
Welcome to Awesome Bank! What would you like to do?

    ------Transactions------
    [1] - Deposit
    [2] - Withdraw
    [3] - Check Extract
    [4] - Leave
    ------------------------

    ----------User----------
    [5] - Create User
    [6] - Create Account
    [7] - List Accounts
    ------------------------
'''

def main():
    clientes = []
    contas = []
    
    while True: 
        opcao = input(menu)

        if opcao == "1":
            pass

        elif opcao == "2":
            pass

        elif opcao == "3":
            pass
        
        elif opcao == "4":
            break

        elif opcao == "5":
            pass

        elif opcao == "6":
            pass

        elif opcao == "7":
            pass

        else:
            print("Essa não é uma opção válida!")