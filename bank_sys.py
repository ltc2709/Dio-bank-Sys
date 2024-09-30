class PessoaFisica:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Cliente(PessoaFisica):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito de R$ {self.valor:.2f}")
            return conta.saldo
        else:
            return "Valor de depósito inválido!"

class Saque(Transacao):
    def registrar(self, conta):
        if conta.saques_diarios >= conta.limite_saques_diarios:
            return "Limite diário de saques atingido."
        elif self.valor > conta.limite_saque:
            return f"O valor de saque máximo é de R$ {conta.limite_saque:.2f}."
        elif self.valor > conta.saldo:
            return "Saldo insuficiente para realizar o saque."
        else:
            conta.saldo -= self.valor
            conta.saques_diarios += 1
            conta.historico.adicionar_transacao(f"Saque de R$ {self.valor:.2f}")
            return conta.saldo

class Conta:
    def __init__(self, agencia, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

    def extrato(self):
        extrato_detalhes = "\nExtrato da Conta:\n"
        for transacao in self.historico.transacoes:
            extrato_detalhes += f"  - {transacao}\n"
        extrato_detalhes += f"Saldo atual: R$ {self.saldo:.2f}\n"
        return extrato_detalhes

class ContaCorrente(Conta):
    def __init__(self, agencia, numero, cliente, limite_saque=500.0, limite_saques_diarios=3):
        super().__init__(agencia, numero, cliente)
        self.limite_saque = limite_saque
        self.limite_saques_diarios = limite_saques_diarios
        self.saques_diarios = 0

# Managing Users and Accounts
clientes = []
contas = []

def criar_usuario(nome, data_nascimento, cpf, endereco):
    cpf = ''.join(filter(str.isdigit, cpf))  # Normalize CPF to digits only
    
    # Check if the CPF is already registered
    for cliente in clientes:
        if cliente.cpf == cpf:
            return "Erro: CPF já cadastrado."
    
    # Register new user
    cliente = Cliente(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    return f"Usuário {nome} cadastrado com sucesso!"

def criar_conta_corrente(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Ensure only digits for CPF search
    
    # Find the user with the given CPF
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    
    if cliente is None:
        return "Erro: Cliente não encontrado."

    # Generate new account number
    numero_conta = len(contas) + 1
    agencia = "0001"
    
    # Create new bank account
    conta = ContaCorrente(agencia, numero_conta, cliente)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    
    return f"Conta criada com sucesso! Agência: {agencia}, Conta: {numero_conta}"

def menu():
    print("\n--- Operações Bancárias ---")
    print("1. Criar Usuário")
    print("2. Criar Conta Corrente")
    print("3. Depósito")
    print("4. Saque")
    print("5. Extrato")
    print("6. Sair")

def main():
    while True:
        menu()
        escolha = input("Escolha a operação: ")

        if escolha == '1':
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
            cpf = input("CPF: ")
            endereco = input("Endereço (logradouro, nro - bairro - cidade): ")
            print(criar_usuario(nome, data_nascimento, cpf, endereco))

        elif escolha == '2':
            cpf = input("Digite o CPF do cliente: ")
            print(criar_conta_corrente(cpf))

        elif escolha == '3':
            cpf = input("Digite o CPF do cliente: ")
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Digite o valor para depositar: R$ "))
                saldo = conta.depositar(valor)
                print(f"Saldo: R$ {saldo:.2f}\n{conta.extrato()}")
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '4':
            cpf = input("Digite o CPF do cliente: ")
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                valor = float(input("Digite o valor para sacar: R$ "))
                saldo = conta.sacar(valor)
                if isinstance(saldo, str):  # Se for uma mensagem de erro
                 print(saldo)
                else:
                    print(f"Saldo: R$ {saldo:.2f}\n{conta.extrato()}")
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '5':
            cpf = input("Digite o CPF do cliente: ")
            conta = next((c for c in contas if c.cliente.cpf == cpf), None)
            if conta:
                print(conta.extrato())
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '6':
            print("Saindo do sistema bancário. Obrigado!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma operação válida.")

if __name__ == "__main__":
    main()
