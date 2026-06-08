# Motor de Telemetria

Sistema modular para processamento, análise estatística, validação e visualização gráfica de fluxos de telemetria baseados em médias móveis.

---

## Integrantes

Henrique Nunes Mororó — RM 574073

Bernardo de Paula Rodrigues — RM 572376

Arthur Moreira Costa — RM 571532

---

## Arquitetura do Projeto

O projeto é estruturado em módulos independentes com responsabilidades bem definidas:

* **`app.py` (Execução):** Ponto de entrada do sistema. Carrega as configurações, coordena o fluxo entre o processador de dados, a interface com o usuário e a geração de gráficos.
* **`motor.py` (Cálculo):** Contém a classe `MotorAnalise`. Mantém o histórico volátil dos sensores, calcula a média móvel das últimas 3 leituras e invoca dinamicamente as regras de validação via reflexão (`getattr`).
* **`regras.py` (Validação):** Contém a interface abstrata `RegraValidacao` e os algoritmos de análise:
  * `ValidacaoLimiteSimples`: Validação linear padrão (Normal, Alerta, Crítico).
  * `ValidacaoLimiteDuplo`: Validação bimodal para sensores que operam em faixas ótimas centrais e possuem limites em ambas as extremidades.
* **`processo.py` (Processamento):** Consome os logs brutos da telemetria, gerencia os contadores de mensagens de hardware e estrutura as séries temporais limpas para plotagem.
* **`interface.py` (Menu):** Controla a interface iterativa no terminal. Exibe as opções de sensores válidos disponíveis e trata de forma defensiva falhas de entrada do operador.
* **`graphic.py` (Plotagem):** Responsável por gerar os gráficos de linha temporais utilizando a biblioteca `matplotlib` com base nos dados processados do sensor selecionado.
* **`dados.py` (Logs):** Simula uma massa de dados de sensores em tempo real, contendo leituras normais e dados corrompidos para testes de estresse.

---

## Destaques Técnicos

* **Programação Defensiva:** Tratamento seletivo de exceções (`ValueError`, `KeyError`, `TypeError`, `AttributeError`). O sistema isola payloads corrompidos (strings inválidas, arrays incorretos ou sensores sem configuração) sem derrubar a aplicação.
* **Uso de Memória Otimizado:** Uso de `collections.deque(maxlen=3)` para garantir janelas fixas por sensor com complexidade de inserção $O(1)$ e descarte automático de leituras obsoletas.
* **Tipagem Estrita:** Uso de *Type Hints* verificados via `mypy`, garantindo que todas as assinaturas de métodos, retornos de salvaguarda e instâncias dinâmicas respeitem estritamente a arquitetura do sistema.
* **Integridade de Séries Temporais:** Filtração ativa de dados no pipeline de processamento que impede que registros marcados como `"Dado corrompido"` injetem valores nulos ou de *fallback* (como `0.0`) nos gráficos, evitando distorções nas linhas de tendência.
* **Interface Limpa:** Uso de códigos de escape ANSI padronizados de forma restrita para colorir apenas os cabeçalhos de seção e os status dinâmicos (`Normal`, `Alerta`, `CRÍTICO`), otimizando a legibilidade sem gerar poluição visual no terminal.
* **Testes de Fronteira:** Suite de testes automatizados via `unittest` que valida exaustivamente os limites de desigualdade estrita ($>$ e $<$) sob precisão de ponto flutuante.

---
