# Motor de Telemetria

Sistema modular para processamento, análise estatística e validação de fluxos de telemetria baseados em médias móveis.

---

## Integrantes

Henrique Nunes Mororó — RM 574073

Bernardo de Paula Rodrigues — RM 572376

Arthur Moreira Costa — RM 571532


## Arquitetura do Projeto

O projeto é dividido em quatro módulos principais:

* **`app.py` (Execução):** Ponto de entrada do sistema. Carrega o arquivo `config.json`, processa os logs brutos e exibe os resultados formatados e coloridos no terminal.
* **`motor.py` (Cálculo):** Contém a classe `MotorAnalise`. Mantém o histórico dos sensores, calcula a média móvel das últimas 3 leituras e invoca as regras de validação via reflexão (`getattr`).
* **`regras.py` (Validação):** Contém a interface abstrata `RegraValidacao` e os algoritmos de análise:
  * `ValidacaoLimiteSimples`: Validação linear padrão (Normal, Alerta, Crítico).
  * `ValidacaoLimiteDuplo`: Validação bimodal para sensores que operam em faixas ótimas centrais e possuem limites em ambas as extremidades.
* **`dados.py` (Logs):** Simula uma massa de dados de sensores em tempo real, contendo leituras normais e dados corrompidos para testes de estresse.

---

## Destaques Técnicos

* **Programação Defensiva:** Tratamento seletivo de exceções (`ValueError`, `KeyError`, `TypeError`, `AttributeError`). O sistema isola payloads corrompidos (strings inválidas, arrays incorretos ou sensores sem configuração) sem derrubar a aplicação.
* **Uso de Memória Otimizado:** Uso de `collections.deque(maxlen=3)` para garantir janelas fixas por sensor com complexidade de inserção $O(1)$ e descarte automático de leituras obsoletas.
* **Tipagem Estrita:** Uso de *Type Hints* verificados via `mypy`, garantindo que as instâncias dinâmicas respeitem estritamente a interface abstrata do sistema.
* **Testes de Fronteira:** Suite de testes automatizados via `unittest` que valida exaustivamente os limites de desigualdade estrita ($>$ e $<$) sob precisão de ponto flutuante.

---
