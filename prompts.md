# Histórico de Prompts - Motor de Telemetria

Este arquivo documenta a sequência de interações e consultas técnicas utilizadas para o design, arquitetura e refatoração do motor de análise de telemetria.

---

## Iteração 1: Estrutura de Dados para Média Móvel
**Usuário:** Necesito de uma estrutura em Python que armazene leituras de sensores para calcular uma média móvel, mas que mantenha apenas as últimas 3 leituras na memória de forma automática, descartando a mais antiga. Qual a melhor abordagem sem ter que manipular listas manualmente?

**Consultor:** A melhor abordagem é utilizar o `collections.deque` definindo o argumento `maxlen=3`. O `deque` (double-ended queue) é implementado como uma lista duplamente encadeada otimizada. Quando o limite de `maxlen` é atingido, o próprio interpretador descarta o elemento mais antigo na extremidade oposta em complexidade temporal de O(1) ao inserir um novo dado, garantindo uma janela deslizante eficiente para o cálculo da média.

### Justificativa da Adaptação da Equipe
A equipe adotou a recomendação de utilizar o `collections.deque` em vez de listas convencionais. A justificativa técnica para essa escolha baseia-se na otimização de memória e desempenho, já que o deque opera com complexidade constantee de O(1) e as listas operam com complexidade O(n).

---

## Iteração 2: Desacoplamento de Regras com Classes Abstratas
**Usuário:** Tenho regras de validação diferentes (alguns sensores têm limite simples, outros têm limite duplo como faixas de alerta superiores e inferiores). Como posso arquitetar isso de forma que o motor de análise não precise de um monte de condicionais `if/else` toda vez que surgir uma regra nova?

**Consultor:** Você pode aplicar o padrão de projeto *Strategy* combinado com Programação Orientada a Interfaces. Utilize o módulo nativo `abc` para criar uma classe abstrata pai que defina o método obrigatório de validação contratual. As regras específicas (ex: `ValidacaoLimiteSimples`, `ValidacaoLimiteDuplo`) herdarão dessa interface. No `MotorAnalise`, em vez de condicionais, você lê o nome da classe diretamente do arquivo de configuração JSON e faz a instanciação dinâmica em tempo de execução usando reflexão com a função `getattr(modulo, nome_classe)()`.

```python
from abc import ABC, abstractmethod
from typing import Dict

class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, valor: float, regras: Dict[str, float]) -> str:
        pass
```

### Justificativa da Adaptação da Equipe
Para evitar o acoplamento rígido e a proliferação de estruturas condicionais (`if/else`) no core do sistema, a equipe implementou o padrão de projeto *Strategy* por meio do módulo nativo `abc` (`Abstract Base Classes`). Definimos a interface `RegraValidacao` e estendemos os comportamentos específicos em classes isoladas. A principal adaptação da equipe foi integrar essa estrutura à leitura dinâmica do JSON de configuração via reflexão com `getattr()`, tornando o `MotorAnalise` expansível a novas regras sem necessidade de alteração no código fonte existente.

---

## Iteração 3: Programação Defensiva e Falhas de Telemetria
**Usuário:** Os dados que vêm dos sensores externos podem vir corrompidos, com strings em vez de números, chaves faltando ou até mesmo payloads mal formados (como listas onde deveriam ser dicionários). Como garantir que o loop principal e o motor continuem rodando sem travar a aplicação quando isso acontecer?

**Consultor:** Aplique o princípio da programação defensiva isolando os pontos críticos com capturas granulares de exceções. No loop de ingestão e dentro do método `adicionar_leitura`, envolva o processamento em blocos `try-except` que capturem especificamente `ValueError` (conversão falha de string para float), `KeyError` (ausência de chaves no dicionário do sensor) e `TypeError` (estrutura de dados errada, como uma lista). Em caso de exceção, defina um comportamento de *fallback*: retorne a média como `0.0` e defina o status explicitamente como `"Dado corrompido"`, permitindo que o sistema continue processando os logs subsequentes.

### Justificativa da Adaptação da Equipe
A telemetria real apresenta instabilidade no recebimento de payloads. A equipe adaptou a estrutura do motor para operar sob o princípio da programação defensiva. Implementamos capturas explícitas e granulares para `ValueError`, `KeyError` e `TypeError`. A decisão técnica de design foi definir um comportamento de *fallback* seguro: ao detectar um dado inválido, o sistema neutraliza a falha aplicando valor `0.0` e definindo o status como `"Dado corrompido"`, garantindo a resiliência e a continuidade do fluxo de processamento de logs do sistema.

---

## Iteração 4: Introdução ao MyPy e Análise Estática de Tipos
**Usuário:** Você mencionou o mypy. O que é exatamente o mypy?

**Consultor:** O MyPy é um verificador estático de tipos para Python. Como Python é uma linguagem de tipagem dinâmica, erros de tipo (como passar uma string para uma função que realiza cálculos matemáticos) só aparecem em tempo de execução. O MyPy atua antes da execução do código (tempo de compilação/análise estática), varrendo os arquivos e garantindo que os contratos definidos via *type hinting* (módulo `typing`) estejam sendo cumpridos.

Na prática, se você definir que o método recebe um `float` e tentar passar um dicionário por engano em outra parte do sistema, o MyPy rejeita o build. Nos cenários de testes unitários defensivos — onde você precisa injetar intencionalmente um tipo inválido (ex: passar uma string para testar o tratamento de exceção do motor) —, utiliza-se o comentário `# type: ignore` na linha correspondente. Isso instrui o MyPy a ignorar aquela violação estática específica, permitindo que o teste avalie o comportamento dinâmico do interpretador.

### Justificativa da Adaptação da Equipe
A equipe adotou o uso de anotações de tipo (*type hinting*) e integrou o `mypy` como validador estático na esteira de desenvolvimento. A justificativa para essa inclusão é mitigar falhas de atribuição de tipos comuns em linguagens de tipagem dinâmica antes da fase de runtime. 

---

## Iteração 5: Arquitetura de Testes Automatizados e Tipagem
**Usuário:** Como posso estruturar uma suite de testes unitários usando `unittest` para garantir que as fronteiras matemáticas das regras estão certas e que o comportamento defensivo contra dados corrompidos realmente funciona?

**Consultor:** Utilize o framework `unittest` nativo estruturando duas classes de teste distintas para separar as responsabilidades:
1. `TestRegrasValidacao`: Focada na exatidão matemática das fronteiras de limiar (testando valores exatos nos limites de alerta e crítico).
2. `TestMotorAnaliseDefensivo`: Focada em injetar dados intencionalmente incorretos (como strings e sensores inexistentes) para validar se o motor responde com `"Dado corrompido"` e `0.0` sem levantar exceções não tratadas.

Para a tipagem estática, utilize o módulo `typing` (`Dict`, `Tuple`, `Any`, `List`) em todas as assinaturas de métodos e variáveis para permitir a checagem rigorosa via `mypy`. Nos testes onde dados inválidos precisam ser injetados de propósito, utilize o comentário `# type: ignore` para silenciar o validador estático apenas naquele ponto específico.

### Justificativa da Adaptação da Equipe
A equipe implementou uma suite de testes utilizando o framework nativo `unittest`, segmentando as validações em duas classes com responsabilidades distintas: `TestRegrasValidacao` (para garantir a exatidão matemática nas fronteiras de transição de status) e `TestMotorAnaliseDefensivo` (para validar a resiliência contra dados corrompidos). 

---

## Iteração 6: Visualização de Gráficos
**Usuário:** Como posso mostrar os gráficos dos sensores usando `matplotlib` e criar um menu no terminal para o usuário escolher o sensor?

**Consultor:** Separe a lógica em módulos: o processador organiza os dados em um dicionário com os eixos X e Y, o módulo de gráficos (`graphic.py`) renderiza as linhas, e a interface (`interface.py`) gerencia o menu de escolha. Para o gráfico não ficar distorcido, filtre os logs para ignorar os registros com status `"Dado corrompido"`. 

### Justificativa da Adaptação da Equipe
A equipe desenvolveu os módulos `graphic.py` e `interface.py`. A decisão técnica foi isolar a geração de gráficos da lógica do motor. Filtramos a estrutura de dados para impedir que valores corrompidos fossem plotados, garantindo a fidelidade do gráfico.
