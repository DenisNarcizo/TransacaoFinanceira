"""Serviço de processamento de transações financeiras."""

import logging

from src.models import ContaSaldo, ResultadoTransacao, StatusTransacao, Transacao
from src.repository import ContaSaldoRepositoryEmMemoria

logger = logging.getLogger(__name__)


class ServicoTransacao:
    """Processa transferências entre contas usando o repositório informado."""

    def __init__(self, repositorio: ContaSaldoRepositoryEmMemoria) -> None:
        self.repositorio = repositorio

    def transferir(self, transacao: Transacao) -> ResultadoTransacao:
        """Executa a transferência entre contas com controle de consistência."""
        lock = self.repositorio.obter_lock()

        with lock:
            conta_origem = self.repositorio.buscar_por_conta(transacao.conta_origem)

            if conta_origem is None:
                mensagem = (
                    f"Transação número {transacao.correlation_id} foi cancelada: "
                    f"conta de origem {transacao.conta_origem} não encontrada."
                )

                logger.warning(mensagem)
                return ResultadoTransacao(
                    correlation_id=transacao.correlation_id,
                    status=StatusTransacao.CANCELADA,
                    mensagem=mensagem,
                )

            conta_destino = self.repositorio.buscar_por_conta(transacao.conta_destino)

            if conta_destino is None:
                mensagem = (
                    f"Transação número {transacao.correlation_id} foi cancelada: "
                    f"conta de destino {transacao.conta_destino} não encontrada."
                )

                logger.warning(mensagem)
                return ResultadoTransacao(
                    correlation_id=transacao.correlation_id,
                    status=StatusTransacao.CANCELADA,
                    mensagem=mensagem,
                )

            # Verifica se a conta de origem possui saldo suficiente.
            if conta_origem.saldo < transacao.valor:
                mensagem = (
                    f"Transação número {transacao.correlation_id} foi cancelada: "
                    f"saldo insuficiente na conta de origem {transacao.conta_origem}."
                )

                logger.warning(mensagem)
                return ResultadoTransacao(
                    correlation_id=transacao.correlation_id,
                    status=StatusTransacao.CANCELADA,
                    mensagem=mensagem,
                )

            novo_saldo_origem = conta_origem.saldo - transacao.valor
            novo_saldo_destino = conta_destino.saldo + transacao.valor

            # Atualiza os saldos das duas contas dentro da mesma região crítica.
            self.repositorio.atualizar_saldo(
                ContaSaldo(conta=conta_origem.conta, saldo=novo_saldo_origem)
            )
            self.repositorio.atualizar_saldo(
                ContaSaldo(conta=conta_destino.conta, saldo=novo_saldo_destino)
            )

            mensagem = (
                f"Transação número {transacao.correlation_id} foi efetivada: "
                f"valor {transacao.valor} transferido de {transacao.conta_origem} "
                f"para {transacao.conta_destino}. "
                f"Saldos atualizados - origem: {novo_saldo_origem}, "
                f"destino: {novo_saldo_destino}."
            )

            logger.info(mensagem)
            return ResultadoTransacao(
                correlation_id=transacao.correlation_id,
                status=StatusTransacao.EFETIVADA,
                mensagem=mensagem,
                saldo_origem=novo_saldo_origem,
                saldo_destino=novo_saldo_destino,
            )