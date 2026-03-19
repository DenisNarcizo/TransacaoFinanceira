from src.models import ContaSaldo, StatusTransacao, Transacao
from src.repository import ContaSaldoRepositoryEmMemoria
from src.service import ServicoTransacao


def criar_repositorio_base() -> ContaSaldoRepositoryEmMemoria:
    """Cria um repositório com contas base para os testes do serviço."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    repositorio.adicionar(ContaSaldo(conta=1, saldo=100.0))
    repositorio.adicionar(ContaSaldo(conta=2, saldo=50.0))
    return repositorio


def test_deve_efetivar_transferencia_quando_houver_saldo():
    """Deve efetivar a transação quando origem e destino existirem e houver saldo."""
    repositorio = criar_repositorio_base()
    servico = ServicoTransacao(repositorio)

    transacao = Transacao(
        correlation_id=1,
        data_hora="18/03/2026 14:30:00",
        conta_origem=1,
        conta_destino=2,
        valor=30.0,
    )

    resultado = servico.transferir(transacao)

    assert resultado.status == StatusTransacao.EFETIVADA
    assert resultado.saldo_origem == 70.0
    assert resultado.saldo_destino == 80.0
    assert repositorio.buscar_por_conta(1).saldo == 70.0
    assert repositorio.buscar_por_conta(2).saldo == 80.0


def test_deve_cancelar_transferencia_quando_conta_origem_nao_existir():
    """Deve cancelar a transação quando a conta de origem não existir."""
    repositorio = criar_repositorio_base()
    servico = ServicoTransacao(repositorio)

    transacao = Transacao(
        correlation_id=2,
        data_hora="18/03/2026 14:30:00",
        conta_origem=999,
        conta_destino=2,
        valor=10.0,
    )

    resultado = servico.transferir(transacao)

    assert resultado.status == StatusTransacao.CANCELADA
    assert "origem" in resultado.mensagem.lower()
    assert resultado.saldo_origem is None
    assert resultado.saldo_destino is None


def test_deve_cancelar_transferencia_quando_conta_destino_nao_existir():
    """Deve cancelar a transação quando a conta de destino não existir."""
    repositorio = criar_repositorio_base()
    servico = ServicoTransacao(repositorio)

    transacao = Transacao(
        correlation_id=3,
        data_hora="18/03/2026 14:30:00",
        conta_origem=1,
        conta_destino=999,
        valor=10.0,
    )

    resultado = servico.transferir(transacao)

    assert resultado.status == StatusTransacao.CANCELADA
    assert "destino" in resultado.mensagem.lower()
    assert resultado.saldo_origem is None
    assert resultado.saldo_destino is None


def test_deve_cancelar_transferencia_quando_saldo_for_insuficiente():
    """Deve cancelar a transação quando a conta de origem não tiver saldo suficiente."""
    repositorio = criar_repositorio_base()
    servico = ServicoTransacao(repositorio)

    transacao = Transacao(
        correlation_id=4,
        data_hora="18/03/2026 14:30:00",
        conta_origem=2,
        conta_destino=1,
        valor=999.0,
    )

    resultado = servico.transferir(transacao)

    assert resultado.status == StatusTransacao.CANCELADA
    assert "saldo insuficiente" in resultado.mensagem.lower()
    assert repositorio.buscar_por_conta(1).saldo == 100.0
    assert repositorio.buscar_por_conta(2).saldo == 50.0