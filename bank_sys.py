class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.depositos = []
        self.saques = []
        self.saques_diarios = 0
        self.limite_saque = 500.0
        self.limite_saques_diarios = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.depositos.append(valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito inválido!")

    def sacar(self, valor):
        if self.saques_diarios >= self.limite_saques_diarios:
            print("Limite diário de saques atingido.")
        elif valor > self.limite_saque:
            print(f"O valor de saque máximo é de R$ {self.limite_saque:.2f}.")
        elif valor > self.saldo:
            print("Saldo insuficiente para realizar o saque.")
        else:
            self.saldo -= valor
            self.saques.append(valor)
            self.saques_diarios += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    def extrato(self):
        print("\nExtrato da Conta:")
        print("Depósitos:")
        for deposito in self.depositos:
            print(f"  + R$ {deposito:.2f}")
        print("Saques:")
        for saque in self.saques:
            print(f"  - R$ {saque:.2f}")
        print(f"Saldo atual: R$ {self.saldo:.2f}\n")

def menu():
    print("\n--- Operações Bancárias ---")
    print("1. Depósito")
    print("2. Saque")
    print("3. Extrato")
    print("4. Sair")

def main():
    conta = ContaBancaria()

    while True:
        menu()
        escolha = input("Escolha a operação (1-Depósito, 2-Saque, 3-Extrato, 4-Sair): ")

        if escolha == '1':
            valor = float(input("Digite o valor para depositar: R$ "))
            conta.depositar(valor)

        elif escolha == '2':
            valor = float(input("Digite o valor para sacar: R$ "))
            conta.sacar(valor)

        elif escolha == '3':
            conta.extrato()

        elif escolha == '4':
            print("Saindo do sistema bancário. Obrigado!")
            break

        else:
            print("Opção inválida! Por favor, escolha uma operação válida.")

if __name__ == "__main__":
    main()
