import pytest

from src.models import ContaSaldo
from src.repository import ContaSaldoRepositoryEmMemoria


def test_deve_adicionar_conta_ao_repositorio():
    """Deve adicionar uma conta nova ao repositório."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    conta = ContaSaldo(conta=123, saldo=100.0)

    repositorio.adicionar(conta)

    conta_salva = repositorio.buscar_por_conta(123)
    assert conta_salva == conta


def test_nao_deve_adicionar_conta_duplicada():
    """Deve lançar erro ao adicionar uma conta já existente."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    conta = ContaSaldo(conta=123, saldo=100.0)

    repositorio.adicionar(conta)

    with pytest.raises(ValueError, match="já existe no repositório"):
        repositorio.adicionar(conta)


def test_deve_buscar_conta_existente():
    """Deve retornar a conta quando ela existir no repositório."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    conta = ContaSaldo(conta=123, saldo=100.0)
    repositorio.adicionar(conta)

    resultado = repositorio.buscar_por_conta(123)

    assert resultado == conta


def test_deve_retornar_none_ao_buscar_conta_inexistente():
    """Deve retornar None ao buscar uma conta inexistente."""
    repositorio = ContaSaldoRepositoryEmMemoria()

    resultado = repositorio.buscar_por_conta(999)

    assert resultado is None


def test_deve_atualizar_saldo_de_conta_existente():
    """Deve atualizar o saldo de uma conta existente."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    conta = ContaSaldo(conta=123, saldo=100.0)
    repositorio.adicionar(conta)

    atualizado = repositorio.atualizar_saldo(ContaSaldo(conta=123, saldo=250.0))

    assert atualizado is True
    assert repositorio.buscar_por_conta(123).saldo == 250.0


def test_nao_deve_atualizar_saldo_de_conta_inexistente():
    """Deve retornar False ao tentar atualizar uma conta inexistente."""
    repositorio = ContaSaldoRepositoryEmMemoria()

    atualizado = repositorio.atualizar_saldo(ContaSaldo(conta=999, saldo=250.0))

    assert atualizado is False


def test_deve_retornar_lock_do_repositorio():
    """Deve retornar o objeto de lock usado no controle de concorrência."""
    repositorio = ContaSaldoRepositoryEmMemoria()

    lock = repositorio.obter_lock()

    assert lock is not None


def test_deve_listar_todas_as_contas():
    """Deve retornar todas as contas armazenadas no repositório."""
    repositorio = ContaSaldoRepositoryEmMemoria()
    conta_1 = ContaSaldo(conta=123, saldo=100.0)
    conta_2 = ContaSaldo(conta=456, saldo=200.0)

    repositorio.adicionar(conta_1)
    repositorio.adicionar(conta_2)

    contas = repositorio.listar_todas_contas()

    assert len(contas) == 2
    assert conta_1 in contas
    assert conta_2 in contas