import pytest
from src.main import criar_repositorio_com_dados_iniciais, criar_transacoes, main

def test_deve_criar_repositorio_com_dados_iniciais():
    """Deve criar o repositório com todas as contas iniciais e saldos corretos."""
    repositorio = criar_repositorio_com_dados_iniciais()
    contas = repositorio.listar_todas_contas()

    # Verifica quantidade de contas
    assert len(contas) == 9
    
    # Verifica contas específicas e saldos (amostragem)
    conta_1 = repositorio.buscar_por_conta(938485762)
    assert conta_1 is not None
    assert conta_1.saldo == 180

    conta_vazia = repositorio.buscar_por_conta(2147483649)
    assert conta_vazia.saldo == 0


def test_deve_criar_lista_de_transacoes():
    """Deve criar a lista inicial de transações com os IDs corretos."""
    transacoes = criar_transacoes()

    assert len(transacoes) == 8
    assert transacoes[0].correlation_id == 1
    assert transacoes[-1].correlation_id == 8
    assert transacoes[0].valor == 150


def test_execucao_completa_da_main(capsys):
    """
    Testa se a função main executa o fluxo end-to-end.
    O capsys captura as saídas de print para validação.
    """
    # Executa a função principal
    main()

    # Captura tudo que foi printado no console
    saida = capsys.readouterr().out

    # Validações de texto no console
    assert "PROCESSAMENTO DE TRANSAÇÕES FINANCEIRAS - INÍCIO" in saida
    assert "RESUMO" in saida
    assert "Transações efetivadas:" in saida
    assert "Transações canceladas:" in saida

    # Validação lógica baseada nos dados estáticos da main:
    # (Opcional) Você pode verificar se os números batem com a lógica do seu Service
    assert "Transações efetivadas: 6" in saida # Exemplo, ajuste conforme seu service
    assert "Transações canceladas: 2" in saida  # Exemplo, ajuste conforme seu service