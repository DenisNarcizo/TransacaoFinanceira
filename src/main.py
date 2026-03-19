import logging
from concurrent.futures import ThreadPoolExecutor

from src.models import ContaSaldo, Transacao
from src.repository import ContaSaldoRepositoryEmMemoria
from src.service import ServicoTransacao


# Configuração básica de log para exibir mensagens no console.
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)


def criar_repositorio_com_dados_iniciais() -> ContaSaldoRepositoryEmMemoria:
    """Cria o repositório e adiciona os saldos iniciais das contas."""
    repositorio = ContaSaldoRepositoryEmMemoria()

    contas_iniciais = [
        ContaSaldo(conta=938485762, saldo=180),
        ContaSaldo(conta=347586970, saldo=1200),
        ContaSaldo(conta=2147483649, saldo=0),
        ContaSaldo(conta=675869708, saldo=4900),
        ContaSaldo(conta=238596054, saldo=478),
        ContaSaldo(conta=573659065, saldo=787),
        ContaSaldo(conta=210385733, saldo=10),
        ContaSaldo(conta=674038564, saldo=400),
        ContaSaldo(conta=563856300, saldo=1200),
    ]

    for conta in contas_iniciais:
        repositorio.adicionar(conta)

    return repositorio


def criar_transacoes() -> list[Transacao]:
    """Monta a lista de transações que serão processadas."""
    return [
        Transacao(
            correlation_id=1,
            data_hora="09/09/2023 14:15:00",
            conta_origem=938485762,
            conta_destino=2147483649,
            valor=150,
        ),
        Transacao(
            correlation_id=2,
            data_hora="09/09/2023 14:15:05",
            conta_origem=2147483649,
            conta_destino=210385733,
            valor=149,
        ),
        Transacao(
            correlation_id=3,
            data_hora="09/09/2023 14:15:29",
            conta_origem=347586970,
            conta_destino=238596054,
            valor=1100,
        ),
        Transacao(
            correlation_id=4,
            data_hora="09/09/2023 14:17:00",
            conta_origem=675869708,
            conta_destino=210385733,
            valor=5300,
        ),
        Transacao(
            correlation_id=5,
            data_hora="09/09/2023 14:18:00",
            conta_origem=238596054,
            conta_destino=674038564,
            valor=1489,
        ),
        Transacao(
            correlation_id=6,
            data_hora="09/09/2023 14:18:20",
            conta_origem=573659065,
            conta_destino=563856300,
            valor=49,
        ),
        Transacao(
            correlation_id=7,
            data_hora="09/09/2023 14:19:00",
            conta_origem=938485762,
            conta_destino=2147483649,
            valor=44,
        ),
        Transacao(
            correlation_id=8,
            data_hora="09/09/2023 14:19:01",
            conta_origem=573659065,
            conta_destino=675869708,
            valor=150,
        ),
    ]


def main() -> None:
    """Executa o fluxo principal do processamento das transações."""
    repositorio = criar_repositorio_com_dados_iniciais()
    transacoes = criar_transacoes()
    servico = ServicoTransacao(repositorio)

    print("=" * 60)
    print("  PROCESSAMENTO DE TRANSAÇÕES FINANCEIRAS - INÍCIO  ")
    print("=" * 60)
    print()

    # Processa as transações em paralelo.
    with ThreadPoolExecutor() as executor:
        resultados = list(executor.map(servico.transferir, transacoes))

    # Exibe o resumo final do processamento.
    print()
    print("=" * 60)
    print("  RESUMO")
    print("=" * 60)

    efetivadas = sum(
        1 for resultado in resultados if resultado.status.value == "EFETIVADA"
    )
    canceladas = sum(
        1 for resultado in resultados if resultado.status.value == "CANCELADA"
    )

    print(f"  Transações efetivadas: {efetivadas}")
    print(f"  Transações canceladas: {canceladas}")
    print("=" * 60)


if __name__ == "__main__":
    main()