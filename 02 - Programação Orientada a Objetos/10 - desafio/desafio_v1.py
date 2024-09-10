from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe Cliente representa um cliente genérico de um banco.
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # Armazena as contas associadas ao cliente

    def realizar_transacao(self, conta, transacao):
        """Método para realizar uma transação em uma conta específica."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Método para adicionar uma nova conta ao cliente."""
        self.contas.append(conta)

# Classe PessoaFisica herda de Cliente e adiciona informações específicas de uma pessoa física.
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)  # Inicializa a classe base Cliente
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe Conta representa uma conta bancária genérica.
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"  # Agência padrão para todas as contas
        self._cliente = cliente
        self._historico = Historico()  # Histórico de transações da conta

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de classe para criar uma nova conta."""
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
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# Classe ContaCorrente herda de Conta e adiciona características específicas para contas correntes.
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite  # Limite de crédito da conta corrente
        self.limite_saques = limite_saques  # Limite de saques diários

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        """Método para exibir informações da conta corrente."""
        return f"""\ 
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe Historico armazena o histórico de transações de uma conta.
class Historico:
    def __init__(self):
        self._transacoes = []  # Lista para armazenar transações

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  # Corrigido formato da data
            }
        )

# Classe Transacao é uma classe abstrata para transações bancárias.
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Classe Saque representa uma transação de saque.
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

# Classe Deposito representa uma transação de depósito.
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