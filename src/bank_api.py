from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Account:
    id: int
    owner: str
    balance: float = 0.0

    def __str__(self) -> str:
        return f"Conta {self.id} | Titular: {self.owner} | Saldo: EUR {self.balance:.2f}"


class Bank:
    def __init__(self) -> None:
        self._accounts: Dict[int, Account] = {}
        self._next_id: int = 1

    def create_account(self, owner: str, initial_balance: float = 0.0) -> Account:
        account = Account(id=self._next_id, owner=owner, balance=initial_balance)
        self._accounts[self._next_id] = account
        self._next_id += 1
        return account

    def get_account(self, account_id: int) -> Optional[Account]:
        return self._accounts.get(account_id)

    def deposit(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        account = self.get_account(account_id)
        if not account:
            raise ValueError("Conta não encontrada.")
        account.balance += amount
        return account.balance

    def withdraw(self, account_id: int, amount: float) -> float:
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        account = self.get_account(account_id)
        if not account:
            raise ValueError("Conta não encontrada.")
        if account.balance < amount:
            raise ValueError("Saldo insuficiente.")
        account.balance -= amount
        return account.balance

    def transfer(self, from_id: int, to_id: int, amount: float) -> None:
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        from_acc = self.get_account(from_id)
        to_acc = self.get_account(to_id)
        if not from_acc:
            raise ValueError("Conta de origem não encontrada.")
        if not to_acc:
            raise ValueError("Conta de destino não encontrada.")
        if from_acc.balance < amount:
            raise ValueError("Saldo insuficiente na conta de origem.")
        from_acc.balance -= amount
        to_acc.balance += amount

    def list_accounts(self) -> Dict[int, Account]:
        return self._accounts.copy()
