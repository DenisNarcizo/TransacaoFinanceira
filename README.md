# 🚀 Desafio de Refatoração: Transação Financeira

Este projeto apresenta a refatoração de um sistema de transferências bancárias paralelas. O código original, escrito em C#, foi migrado para **Python 3.14** com foco em **SOLID**, **Clean Code** e segurança de concorrência (*Thread Safety*).

## 🔍 Diagnóstico do Código Original (Legacy)

Na análise do código em C#, identifiquei e corrigi os seguintes pontos críticos:

### 1. Erros de Sintaxe e Compilação
* **Placeholders Inválidos:** Erros de digitação em strings como `{0 }` (espaço indevido) e chamadas a índices inexistentes como `{3}` no `Console.WriteLine`.
* **Nomenclatura:** Variáveis (ex: `TRANSACOES`) e classes (ex: `executarTransacaoFinanceira`) fora dos padrões de nomenclatura da linguagem.
* **Inconsistência:** O sistema gerenciava dados em listas e dicionários de forma duplicada e sem sincronia.

### 2. Falhas de Lógica e Performance
* **Busca Lenta:** O uso de `Find()` em listas ($O(n)$) foi substituído por busca em dicionários ($O(1)$) no Repositório.
* **Estado não Persistido:** As alterações de saldo eram feitas em variáveis locais, mas nunca devolvidas para a "tabela" de saldos, fazendo com que o estado não fosse atualizado.

### 3. Condição de Corrida (Race Condition) - **Crítico**
* O uso de `Parallel.ForEach` sem travas (*Locks*) permitia que duas transações lessem o saldo de uma mesma conta ao mesmo tempo, gerando inconsistências graves nos saldos finais.

---

## 🛠️ Minha Solução em Python

A refatoração seguiu padrões de mercado para garantir que o código seja escalável e fácil de manter:

* **Repository Pattern:** Camada de dados isolada em `repository.py`, permitindo trocar a memória por um banco de dados real futuramente.
* **Thread Safety (RLock):** Implementei `threading.RLock` para garantir a **atomicidade**. Enquanto uma transação altera uma conta, outras aguardam a liberação.
* **Injeção de Dependência:** O `ServicoTransacao` recebe o repositório via construtor, facilitando o uso de Mocks.
* **Integridade de Dados:** Uso de `dataclasses` com validação no `__post_init__` para impedir valores negativos ou transações inválidas.

---

## 🧪 Qualidade e Testes

O projeto conta com **99% de cobertura de código**, validando desde os modelos até o fluxo principal. Abaixo, o resultado da última execução da suíte de testes:

```text
$ python -m pytest --cov=src --cov-report=term-missing
============================= test session starts =============================
collected 25 items

tests\test_main.py ...                                                   [ 12%]
tests\test_models.py ..........                                          [ 52%]
tests\test_repository.py ........                                         [ 84%]
tests\test_service.py ....                                               [100%]

---------- coverage: platform win32, python 3.14.3-final-0 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src\__init__.py         0      0   100%
src\main.py            35      1    97%   134
src\models.py          23      0   100%
src\repository.py      27      0   100%
src\service.py         31      0   100%
-------------------------------------------------
TOTAL                 116      1    99%
============================== 25 passed in 0.16s =============================