class ContaBancaria:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0.0
        self.depositos = []
        self.saques = []
        self.saques_diarios = 0
        self.limite_saque = 500.0
        self.limite_saques_diarios = 3

    def depositar(self, valor, /):  # Positional-only
        if valor > 0:
            self.saldo += valor
            self.depositos.append(valor)
            return self.saldo, self.extrato()
        else:
            return "Valor de depósito inválido!"

    def sacar(self, *, valor):  # Keyword-only
        if self.saques_diarios >= self.limite_saques_diarios:
            return "Limite diário de saques atingido."
        elif valor > self.limite_saque:
            return f"O valor de saque máximo é de R$ {self.limite_saque:.2f}."
        elif valor > self.saldo:
            return "Saldo insuficiente para realizar o saque."
        else:
            self.saldo -= valor
            self.saques.append(valor)
            self.saques_diarios += 1
            return self.saldo, self.extrato()

    def extrato(self, saldo, /, *, extrato=True):  # Positional and keyword-only
        extrato_detalhes = "\nExtrato da Conta:\n"
        extrato_detalhes += "Depósitos:\n"
        for deposito in self.depositos:
            extrato_detalhes += f"  + R$ {deposito:.2f}\n"
        extrato_detalhes += "Saques:\n"
        for saque in self.saques:
            extrato_detalhes += f"  - R$ {saque:.2f}\n"
        extrato_detalhes += f"Saldo atual: R$ {saldo:.2f}\n"
        return extrato_detalhes if extrato else ""

# Managing Users and Accounts
usuarios = []
contas = []

def criar_usuario(nome, data_nascimento, cpf, endereco):
    # Storing only numbers from CPF
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Check if the CPF is already registered
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return "Erro: CPF já cadastrado."
    
    # Register new user
    usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(usuario)
    return f"Usuário {nome} cadastrado com sucesso!"

def criar_conta_corrente(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Ensure only digits for CPF search
    
    # Find the user with the given CPF
    usuario = next((user for user in usuarios if user['cpf'] == cpf), None)
    
    if usuario is None:
        return "Erro: Usuário não encontrado."

    # Generate new account number
    numero_conta = len(contas) + 1
    agencia = "0001"
    
    # Create new bank account
    conta = ContaBancaria(agencia, numero_conta, usuario)
    contas.append(conta)
    
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
            cpf = input("Digite o CPF do usuário: ")
            print(criar_conta_corrente(cpf))

        elif escolha == '3':
            cpf = input("Digite o CPF do usuário: ")
            conta = next((c for c in contas if c.usuario['cpf'] == cpf), None)
            if conta:
                valor = float(input("Digite o valor para depositar: R$ "))
                saldo, extrato = conta.depositar(valor)
                print(f"Saldo: R$ {saldo:.2f}\n{extrato}")
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '4':
            cpf = input("Digite o CPF do usuário: ")
            conta = next((c for c in contas if c.usuario['cpf'] == cpf), None)
            if conta:
                valor = float(input("Digite o valor para sacar: R$ "))
                saldo, extrato = conta.sacar(valor=valor)
                print(f"Saldo: R$ {saldo:.2f}\n{extrato}")
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '5':
            cpf = input("Digite o CPF do usuário: ")
            conta = next((c for c in contas if c.usuario['cpf'] == cpf), None)
            if conta:
                saldo = conta.saldo
                print(conta.extrato(saldo, extrato=True))
            else:
                print("Erro: Conta não encontrada.")

        elif escolha == '6':
            print("Saindo do sistema bancário. Obrigado!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma operação válida.")

if __name__ == "__main__":
    main()
