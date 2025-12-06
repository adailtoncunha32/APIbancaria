from bank_api import Bank


def show_menu() -> None:
    print("\n=== BANCO PYTHON ===")
    print("1 - Criar conta")
    print("2 - Listar contas")
    print("3 - Depositar")
    print("4 - Sacar")
    print("5 - Transferir")
    print("0 - Sair")


def input_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Por favor, informe um número inteiro.")


def input_float(prompt: str) -> float:
    while True:
        value = input(prompt).replace(",", ".").strip()
        try:
            amount = float(value)
            return amount
        except ValueError:
            print("Por favor, informe um valor numérico válido.")


def main() -> None:
    bank = Bank()
    print("Bem-vindo ao sistema bancário em Python! (simulação, sem dinheiro real)")

    while True:
        show_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("A sair do sistema. Obrigado por utilizar o Banco Python.")
            break

        elif opcao == "1":
            owner = input("Nome do titular da conta: ").strip()
            if not owner:
                print("Nome inválido.")
                continue
            initial = input_float("Depósito inicial (EUR, pode escrever 0): ")
            account = bank.create_account(owner, initial)
            print(f"Conta criada com sucesso: {account}")

        elif opcao == "2":
            contas = bank.list_accounts()
            if not contas:
                print("Nenhuma conta cadastrada.")
            else:
                print("\n--- Contas registadas ---")
                for acc in contas.values():
                    print(acc)

        elif opcao == "3":
            acc_id = input_int("ID da conta para depósito: ")
            amount = input_float("Valor do depósito (EUR): ")
            try:
                new_balance = bank.deposit(acc_id, amount)
                print(f"Depósito realizado. Novo saldo: EUR {new_balance:.2f}")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "4":
            acc_id = input_int("ID da conta para saque: ")
            amount = input_float("Valor do saque (EUR): ")
            try:
                new_balance = bank.withdraw(acc_id, amount)
                print(f"Saque realizado. Novo saldo: EUR {new_balance:.2f}")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "5":
            from_id = input_int("ID da conta de origem: ")
            to_id = input_int("ID da conta de destino: ")
            amount = input_float("Valor da transferência (EUR): ")
            try:
                bank.transfer(from_id, to_id, amount)
                print("Transferência realizada com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
