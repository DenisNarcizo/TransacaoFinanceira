"""Acesso aos dados usando o padrão Repository."""

import threading
from typing import Protocol

from src.models import ContaSaldo


class ContaSaldoRepositoryInterface(Protocol):
    """Define o contrato para acesso aos saldos das contas."""

    def buscar_por_conta(self, numero_conta: int) -> ContaSaldo | None:
        ...

    def atualizar_saldo(self, conta_saldo: ContaSaldo) -> bool:
        ...


class ContaSaldoRepositoryEmMemoria:
    """Repositório em memória para armazenamento dos saldos das contas."""

    def __init__(self) -> None:
        self._dados: dict[int, ContaSaldo] = {}
        self._lock = threading.RLock()

    def adicionar(self, conta_saldo: ContaSaldo) -> None:
        # Evita cadastro duplicado de conta.
        with self._lock:
            if conta_saldo.conta in self._dados:
                raise ValueError(
                    f"Conta {conta_saldo.conta} já existe no repositório."
                )

            self._dados[conta_saldo.conta] = conta_saldo

    def buscar_por_conta(self, numero_conta: int) -> ContaSaldo | None:
        with self._lock:
            return self._dados.get(numero_conta)

    def atualizar_saldo(self, conta_saldo: ContaSaldo) -> bool:
        with self._lock:
            if conta_saldo.conta not in self._dados:
                return False

            self._dados[conta_saldo.conta] = conta_saldo
            return True

    def obter_lock(self) -> threading.RLock:
        """Retorna o lock usado no controle de concorrência."""
        return self._lock

    def listar_todas_contas(self) -> list[ContaSaldo]:
        """Retorna todas as contas armazenadas no repositório."""
        with self._lock:
            return list(self._dados.values())