import pytest

from src.models import ContaSaldo, ResultadoTransacao, StatusTransacao, Transacao


def test_deve_criar_conta_saldo_valida():
    """Deve criar uma conta com saldo válido."""
    conta = ContaSaldo(conta=123, saldo=100.0)

    assert conta.conta == 123
    assert conta.saldo == 100.0


def test_nao_deve_criar_conta_com_numero_zero():
    """Deve lançar erro ao criar conta com número zero."""
    with pytest.raises(ValueError, match="não pode ser negativo ou zero"):
        ContaSaldo(conta=0, saldo=100.0)


def test_nao_deve_criar_conta_com_numero_negativo():
    """Deve lançar erro ao criar conta com número negativo."""
    with pytest.raises(ValueError, match="não pode ser negativo ou zero"):
        ContaSaldo(conta=-1, saldo=100.0)


def test_nao_deve_criar_conta_com_saldo_negativo():
    """Deve lançar erro ao criar conta com saldo negativo."""
    with pytest.raises(ValueError, match="Saldo não pode ser negativo"):
        ContaSaldo(conta=123, saldo=-10.0)


def test_deve_criar_transacao_valida():
    """Deve criar uma transação válida."""
    transacao = Transacao(
        correlation_id=1,
        data_hora="18/03/2026 14:30:00",
        conta_origem=123,
        conta_destino=456,
        valor=50.0,
    )

    assert transacao.correlation_id == 1
    assert transacao.conta_origem == 123
    assert transacao.conta_destino == 456
    assert transacao.valor == 50.0


def test_nao_deve_criar_transacao_com_valor_zero():
    """Deve lançar erro ao criar transação com valor zero."""
    with pytest.raises(ValueError, match="deve ser positivo"):
        Transacao(
            correlation_id=1,
            data_hora="18/03/2026 14:30:00",
            conta_origem=123,
            conta_destino=456,
            valor=0,
        )


def test_nao_deve_criar_transacao_com_valor_negativo():
    """Deve lançar erro ao criar transação com valor negativo."""
    with pytest.raises(ValueError, match="deve ser positivo"):
        Transacao(
            correlation_id=1,
            data_hora="18/03/2026 14:30:00",
            conta_origem=123,
            conta_destino=456,
            valor=-1,
        )


def test_nao_deve_criar_transacao_com_mesma_conta():
    """Deve lançar erro quando origem e destino forem iguais."""
    with pytest.raises(ValueError, match="não podem ser iguais"):
        Transacao(
            correlation_id=1,
            data_hora="18/03/2026 14:30:00",
            conta_origem=123,
            conta_destino=123,
            valor=10,
        )


def test_deve_criar_resultado_transacao_com_saldos():
    """Deve criar o resultado da transação com os saldos informados."""
    resultado = ResultadoTransacao(
        correlation_id=1,
        status=StatusTransacao.EFETIVADA,
        mensagem="Sucesso",
        saldo_origem=50.0,
        saldo_destino=150.0,
    )

    assert resultado.correlation_id == 1
    assert resultado.status == StatusTransacao.EFETIVADA
    assert resultado.mensagem == "Sucesso"
    assert resultado.saldo_origem == 50.0
    assert resultado.saldo_destino == 150.0


def test_deve_criar_resultado_transacao_sem_saldos():
    """Deve criar o resultado da transação sem os saldos opcionais."""
    resultado = ResultadoTransacao(
        correlation_id=2,
        status=StatusTransacao.CANCELADA,
        mensagem="Falha",
    )

    assert resultado.saldo_origem is None
    assert resultado.saldo_destino is None