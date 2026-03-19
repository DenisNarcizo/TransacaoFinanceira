"""Modelos de dados da aplicação de transações financeiras."""

from dataclasses import dataclass
from enum import Enum


class StatusTransacao(Enum):
    """Status possível para uma transação."""

    CANCELADA = "CANCELADA"
    EFETIVADA = "EFETIVADA"


@dataclass
class ContaSaldo:
    """Representa uma conta com seu respectivo saldo."""

    conta: int
    saldo: float

    def __post_init__(self) -> None:
        # Garante que o número da conta seja válido.
        if self.conta <= 0:
            raise ValueError(
                f"Número da conta não pode ser negativo ou zero: {self.conta}"
            )

        # Garante que o saldo inicial não seja negativo.
        if self.saldo < 0:
            raise ValueError(f"Saldo não pode ser negativo: {self.saldo}")


@dataclass
class Transacao:
    """Representa uma transferência entre duas contas."""

    correlation_id: int
    data_hora: str
    conta_origem: int
    conta_destino: int
    valor: float

    def __post_init__(self) -> None:
        # O valor da transação deve ser maior que zero.
        if self.valor <= 0:
            raise ValueError(f"Valor da transação deve ser positivo: {self.valor}")

        # Evita transferências para a mesma conta.
        if self.conta_origem == self.conta_destino:
            raise ValueError("Conta de origem e destino não podem ser iguais.")


@dataclass
class ResultadoTransacao:
    """Armazena o resultado final do processamento de uma transação."""

    correlation_id: int
    status: StatusTransacao
    mensagem: str
    saldo_origem: float | None = None
    saldo_destino: float | None = None