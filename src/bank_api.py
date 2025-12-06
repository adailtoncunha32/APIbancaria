from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional


@dataclass
class Account:
    id: int
    owner: str
    balance: float = 0.0

    def __str__(self) -> str:
        return f"Conta {self.id} | Titular: {self.owner} | Saldo: EUR {self.balance:.2f}"

    @staticmethod
    def from_dict(data: dict) -> "Account":
        return Account(
            id=int(data["id"]),
            owner=str(data["owner"]),
            balance=float(data["balance"]),
        )


class Bank:
    def __init__(self, storage_path: str = "bank_data.json") -> None:
        self._storage_file = Path(storage_path)
        self._accounts: Dict[int, Account] = {}
        self._next_id: int = 1
        self._load()

    # ---------- Persistência em JSON ----------

    def _load(self) -> None:
        """Carrega contas do ficheiro JSON, se existir."""
        if not self._storage_file.exists():
            return
        try:
            data = json.loads(self._storage_file.read_text(encoding="utf-8"))
            accounts_raw = data.get("accounts", [])
            self._accounts = {
                int(acc_data["id"]): Account.from_dict(acc_data)
                for acc_data in accounts_raw
            }
            self._next_id = int(data.get("next_id", len(self._accounts) + 1))
        except Exception as exc:
            print(f"[AVISO] Não foi possível carregar dados do ficheiro: {exc}")

    def _save(self) -> None:
        """Guarda as contas no ficheiro JSON."""
        data = {
            "next_id": self._next_id,
            "accounts": [asdict(acc) for acc in self._accounts.values()],
        }
        self._storage_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ---------- Operações bancárias ----------

    def create_account(self, owner: str, initial_balance: float = 0.0) -> Account:
        account = Account(id=self._next_id, owner=owner, balance=initial_balance)
        self._accounts[self._next_id] = account
        self._next_id += 1
        self._save()
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
        self._save()
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
        self._save()
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
        self._save()

    def list_accounts(self) -> Dict[int, Account]:
        return self._accounts.copy()
