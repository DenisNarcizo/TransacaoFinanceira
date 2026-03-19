# 🚀 Desafio de Refatoração: Transação Financeira

Este projeto apresenta a refatoração de um sistema de transferências bancárias paralelas. O código original em C# foi migrado para **Python 3.14** com foco em **SOLID**, **Clean Code** e segurança de concorrência (*Thread Safety*).

## 🔍 Diagnóstico do Código Original (Legacy)

Na análise do código em C#, identifiquei e corrigi os seguintes pontos críticos:

### 1. Erros de Sintaxe e Compilação
* **Placeholders Inválidos:** Erros de digitação em strings como `{0 }` e chamadas a índices inexistentes como `{3}` no `Console.WriteLine`.
* **Nomenclatura:** Variáveis e classes fora dos padrões de nomenclatura da linguagem.

### 2. Falhas de Lógica e Performance
* **Busca Lenta:** O uso de `Find()` em listas ($O(n)$) foi substituído por busca em dicionários ($O(1)$).
* **Estado não Persistido:** As alterações de saldo não eram devidamente atualizadas no repositório.

### 3. Condição de Corrida (Race Condition) - **Crítico**
* O uso de paralelismo sem travas (*Locks*) permitia que duas transações alterassem o mesmo saldo simultaneamente, gerando inconsistências graves.

---

## 🛠️ Minha Solução em Python

* **Thread Safety (RLock):** Implementei `threading.RLock` para garantir a **atomicidade**. Enquanto uma transação altera uma conta, outras aguardam a liberação.
* **Repository Pattern:** Camada de dados isolada para facilitar futuras migrações para bancos de dados reais.
* **Integridade de Dados:** Validação via `dataclasses` para impedir valores negativos ou transações inválidas.

---

## 🧪 Qualidade e Testes

O projeto conta com **99% de cobertura de código**.

```text
$ python -m pytest --cov=src --cov-report=term-missing
============================= test session starts =============================
tests\test_main.py ...                                                   [ 12%]
tests\test_models.py ..........                                          [ 52%]
tests\test_repository.py ........                                         [ 84%]
tests\test_service.py ....                                               [100%]

---------- coverage: platform win32, python 3.14.3-final-0 -----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
TOTAL                 116      1    99%
============================== 25 passed in 0.16s =============================